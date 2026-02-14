from __future__ import annotations

import os
import uuid
from typing import Any, Optional, Tuple

from flask import Flask, jsonify, render_template, request

try:
    # Package-style imports (recommended): `python -m smarttrip.app`
    from smarttrip.ai_recommender import (
        MODEL_VERSION,
        build_features_from_context,
        pairwise_update,
        rank_places,
        seed_weights,
    )
    from smarttrip.algorithm import demo_places
    from smarttrip.chat_parser import parse_message
    from smarttrip.services.osm_service import geocode_city, get_places, get_places_city
    from smarttrip.storage import (
        connect as connect_db,
        ensure_seed_global_weights,
        get_recommendation,
        load_global_weights,
        load_user_weights,
        log_event,
        log_recommendation,
        upsert_global_weights,
        upsert_user_weights,
    )
except ImportError:  # pragma: no cover
    # Script-style fallback: `python smarttrip/app.py`
    from ai_recommender import (  # type: ignore
        MODEL_VERSION,
        build_features_from_context,
        pairwise_update,
        rank_places,
        seed_weights,
    )
    from algorithm import demo_places  # type: ignore
    from chat_parser import parse_message  # type: ignore
    from services.osm_service import geocode_city, get_places, get_places_city  # type: ignore
    from storage import (  # type: ignore
        connect as connect_db,
        ensure_seed_global_weights,
        get_recommendation,
        load_global_weights,
        load_user_weights,
        log_event,
        log_recommendation,
        upsert_global_weights,
        upsert_user_weights,
    )


DEFAULT_ORIGIN: Tuple[float, float] = (35.6892, 51.3890)
_MAX_ABS_WEIGHT = 6.0


def _safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _budget_from_price_tier(price_tier: Any) -> str:
    tier = _safe_int(price_tier, 2)
    return {1: "low", 2: "medium", 3: "high"}.get(tier, "medium")


def _normalize_lang(value: Any) -> str:
    s = str(value or "").strip().lower()
    if s.startswith("fa") or s in {"farsi", "persian", "فارسی"}:
        return "fa"
    return "en"


def _clip_weights(weights: dict) -> dict:
    clipped = {}
    for k, v in (weights or {}).items():
        try:
            fv = float(v)
        except (TypeError, ValueError):
            continue
        clipped[str(k)] = max(-_MAX_ABS_WEIGHT, min(_MAX_ABS_WEIGHT, fv))
    return clipped


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.setdefault("SMARTTRIP_DB_PATH", os.path.join(app.instance_path, "smarttrip.sqlite"))
    app.config["JSON_SORT_KEYS"] = False

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/recommend")
    def recommend():
        payload = request.get_json(silent=True) or {}

        lang = _normalize_lang(payload.get("lang"))

        session_id_raw = payload.get("session_id")
        session_id = session_id_raw.strip() if isinstance(session_id_raw, str) else None

        user_activity = payload.get("activity", "nature")
        user_group_type = payload.get("group_type", "friends")
        user_budget = payload.get("budget", "medium")
        people_count = payload.get("people_count", 2)
        has_car = payload.get("has_car", False)

        city_raw = payload.get("city")
        city = city_raw.strip() if isinstance(city_raw, str) else ""
        search_mode = str(payload.get("search_mode") or ("city" if city else "radius")).strip().lower()
        if search_mode != "city":
            city = ""

        city_info = geocode_city(city, timeout_s=4.0) if city else None

        lat = _safe_float(payload.get("lat"))
        lon = _safe_float(payload.get("lon"))
        if lat is not None and lon is not None:
            origin = (lat, lon)
            origin_source = "user"
        elif city_info:
            city_lat = _safe_float(city_info.get("lat"))
            city_lon = _safe_float(city_info.get("lon"))
            if city_lat is not None and city_lon is not None:
                origin = (city_lat, city_lon)
                origin_source = "city"
            else:
                origin = DEFAULT_ORIGIN
                origin_source = "demo"
        else:
            origin = DEFAULT_ORIGIN
            origin_source = "demo"

        default_radius = 7000 if bool(has_car) else 4500
        radius_m = int(payload.get("radius_m", default_radius))
        radius_m = max(1000, min(15000, radius_m))

        if city and city_info:
            places = get_places_city(city, activity=user_activity, timeout_s=12.0, limit=200)
            search_mode_out = "city"
            if not places:
                city_lat = _safe_float(city_info.get("lat")) if isinstance(city_info, dict) else None
                city_lon = _safe_float(city_info.get("lon")) if isinstance(city_info, dict) else None
                if city_lat is not None and city_lon is not None:
                    # City-area queries can be slow/unavailable; fall back to a large-radius
                    # search around the city center before using demo data.
                    fallback_radius_m = 15000
                    places = get_places(
                        city_lat,
                        city_lon,
                        radius=fallback_radius_m,
                        activity=user_activity,
                        timeout_s=8.0,
                        limit=80,
                    )
        else:
            places = get_places(
                origin[0],
                origin[1],
                radius=radius_m,
                activity=user_activity,
                timeout_s=8.0,
                limit=80,
            )
            search_mode_out = "radius"
            city = ""

        data_source = "osm" if places else "demo"
        if not places:
            places = demo_places(origin[0], origin[1])

        db_path = str(app.config["SMARTTRIP_DB_PATH"])
        conn = connect_db(db_path)
        try:
            ensure_seed_global_weights(conn, seed_weights())
            weights_global = load_global_weights(conn)
            weights_user = load_user_weights(conn, session_id) if session_id else {}
            weights = dict(weights_global)
            for f, w in weights_user.items():
                weights[f] = float(weights.get(f, 0.0)) + float(w)

            context = {
                "lang": lang,
                "user_activity": user_activity,
                "user_group_type": user_group_type,
                "user_budget": user_budget,
                "people_count": people_count,
                "has_car": has_car,
                "origin": [origin[0], origin[1]],
                "radius_m": radius_m,
                "search_mode": search_mode_out,
                "city": city or None,
            }

            recommendations = rank_places(places, context=context, weights=weights, limit=5)
            if data_source == "osm" and len(recommendations) < 5:
                # OSM may return too few candidates for a small radius.
                # Keep all OSM picks, and top-up with demo candidates.
                demo_candidates = demo_places(origin[0], origin[1])
                demo_ranked = rank_places(demo_candidates, context=context, weights=weights, limit=5)
                needed = max(0, 5 - len(recommendations))
                if needed:
                    recommendations = list(recommendations) + list(demo_ranked[:needed])
                    data_source = "osm+demo"

            for i, p in enumerate(recommendations, start=1):
                p["rank"] = i
                p["budget"] = _budget_from_price_tier(p.get("price_tier"))

                best_for = p.get("best_for") or []
                best_for_set = {str(x).strip().lower() for x in best_for}
                if str(user_group_type).strip().lower() in best_for_set:
                    p["group"] = user_group_type
                elif best_for:
                    p["group"] = str(best_for[0])
                else:
                    p["group"] = user_group_type

                rating = _safe_float(p.get("rating"))
                if rating is not None:
                    p["rating"] = rating

                pop_raw = _safe_float(p.get("popularity_score"))
                if pop_raw is None:
                    pop_raw = (rating / 5.0) * 100 if rating is not None else 50.0
                p["popularity_score"] = int(max(0, min(100, round(pop_raw))))

                plat = _safe_float(p.get("lat"))
                plon = _safe_float(p.get("lon"))
                if plat is not None and plon is not None:
                    p["lat"] = plat
                    p["lon"] = plon

            request_id = uuid.uuid4().hex
            log_recommendation(
                conn,
                request_id=request_id,
                session_id=session_id,
                context=context,
                search_mode=search_mode_out,
                city=city or None,
                recommendations=recommendations,
            )
            log_event(
                conn,
                session_id=session_id,
                request_id=request_id,
                action="recommend",
                payload={"data_source": data_source, "model_version": MODEL_VERSION},
            )
        finally:
            conn.close()

        return jsonify(
            {
                "status": "success",
                "request_id": request_id,
                "model_version": MODEL_VERSION,
                "origin": {"lat": origin[0], "lon": origin[1], "source": origin_source},
                "radius_m": radius_m,
                "search_mode": search_mode_out,
                "city": city or None,
                "data_source": data_source,
                "recommendations": recommendations,
            }
        )

    @app.post("/feedback")
    def feedback():
        payload = request.get_json(silent=True) or {}

        request_id_raw = payload.get("request_id")
        request_id = request_id_raw.strip() if isinstance(request_id_raw, str) else ""

        place_id_raw = payload.get("place_id")
        place_id = place_id_raw.strip() if isinstance(place_id_raw, str) else ""

        action_raw = payload.get("action")
        action = action_raw.strip().lower() if isinstance(action_raw, str) else "click"

        session_id_raw = payload.get("session_id")
        session_id = session_id_raw.strip() if isinstance(session_id_raw, str) else None

        if not request_id or not place_id:
            return jsonify({"status": "error", "message": "request_id and place_id are required"}), 400

        db_path = str(app.config["SMARTTRIP_DB_PATH"])
        conn = connect_db(db_path)
        try:
            log_event(
                conn,
                session_id=session_id,
                request_id=request_id,
                action=action,
                place_id=place_id,
                payload={"client": "web"},
            )

            if action not in {"click", "choose", "like"}:
                return jsonify({"status": "success", "trained": False})

            context, items = get_recommendation(conn, request_id)
            if not context or not items:
                return jsonify({"status": "success", "trained": False})

            clicked = None
            for p in items:
                if str(p.get("place_id") or "") == place_id:
                    clicked = p
                    break
            if clicked is None:
                return jsonify({"status": "success", "trained": False})

            others = [p for p in items if str(p.get("place_id") or "") != place_id]
            if not others:
                return jsonify({"status": "success", "trained": False})

            clicked_features = build_features_from_context(clicked, context)
            other_features = [build_features_from_context(p, context) for p in others]

            ensure_seed_global_weights(conn, seed_weights())
            weights_global = load_global_weights(conn)

            global_lr = 0.05
            user_lr = 0.18

            weights_global_new = pairwise_update(
                weights=weights_global,
                clicked_features=clicked_features,
                other_features=other_features,
                lr=global_lr,
            )
            weights_global_new = _clip_weights(weights_global_new)
            upsert_global_weights(conn, weights_global_new)

            if session_id:
                weights_user = load_user_weights(conn, session_id)
                combined = dict(weights_global_new)
                for f, w in weights_user.items():
                    combined[f] = float(combined.get(f, 0.0)) + float(w)

                combined_new = pairwise_update(
                    weights=combined,
                    clicked_features=clicked_features,
                    other_features=other_features,
                    lr=user_lr,
                )
                combined_new = _clip_weights(combined_new)
                user_offset_new = {
                    f: float(combined_new.get(f, 0.0)) - float(weights_global_new.get(f, 0.0))
                    for f in set(combined_new.keys()) | set(weights_global_new.keys())
                }
                user_offset_new = _clip_weights(user_offset_new)
                upsert_user_weights(conn, session_id, user_offset_new)

            return jsonify({"status": "success", "trained": True})
        finally:
            conn.close()

    @app.post("/chat")
    def chat():
        payload = request.get_json(silent=True) or {}

        lang = _normalize_lang(payload.get("lang"))

        session_id_raw = payload.get("session_id")
        session_id = session_id_raw.strip() if isinstance(session_id_raw, str) else None

        message_raw = payload.get("message")
        message = message_raw.strip() if isinstance(message_raw, str) else ""
        if not message:
            return jsonify({"status": "error", "message": "message is required"}), 400

        current = payload.get("current") if isinstance(payload.get("current"), dict) else {}
        updates, reply = parse_message(message, current=current, lang=lang)

        if updates.get("search_mode") == "city":
            city_value = updates.get("city")
            if isinstance(city_value, str) and city_value.strip():
                city_info = geocode_city(city_value.strip(), timeout_s=4.0)
                if city_info is None:
                    reply = (
                        "شهر پیدا نشد. لطفاً با املای دیگری امتحان کن (مثال: Tehran / تهران)."
                        if lang == "fa"
                        else "City not found. Try another spelling (e.g., Tehran / تهران)."
                    )
                    updates.pop("city", None)
                else:
                    updates["city"] = city_value.strip()
            else:
                reply = (
                    "کدوم شهر رو جستجو کنم؟ (مثال: Tehran / تهران)"
                    if lang == "fa"
                    else "Which city should I search? (e.g., Tehran / تهران)"
                )

        db_path = str(app.config["SMARTTRIP_DB_PATH"])
        conn = connect_db(db_path)
        try:
            log_event(
                conn,
                session_id=session_id,
                request_id=None,
                action="chat",
                payload={
                    "message": message[:500],
                    "updates": updates,
                },
            )
        finally:
            conn.close()

        return jsonify({"status": "success", "reply": reply, "updates": updates})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
