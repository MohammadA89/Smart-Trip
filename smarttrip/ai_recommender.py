from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Optional, Tuple


MODEL_VERSION = "ml-v3"

# Calibrate the UI-facing score so it doesn't saturate at 100 for most places.
# (The model is pairwise-learned and only needs a monotonic score for ranking.)
_SCORE_INTERCEPT = -4.5
_SCORE_TEMPERATURE = 1.0


def seed_weights() -> Dict[str, float]:
    # Reasonable cold-start weights (online-learned afterwards).
    return {
        "bias": 0.0,
        "activity_fit": 1.7,
        "distance_fit": 1.2,
        "group_fit": 1.1,
        "budget_fit": 0.9,
        "people_fit": 0.7,
        "quality": 1.0,
        "popularity": 1.15,
        "city_mode": -0.15,
    }


def sigmoid(z: float) -> float:
    # Numerically stable sigmoid.
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    ez = math.exp(z)
    return ez / (1.0 + ez)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r_km = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r_km * c


def _canonical_activity(activity: Any) -> str:
    a = str(activity or "").strip().lower()
    return a if a in {"nature", "cafe", "restaurant", "entertainment"} else "nature"


def _canonical_group(group_type: Any) -> str:
    g = str(group_type or "").strip().lower()
    return g if g in {"solo", "friends", "family"} else "friends"


def _canonical_budget(budget: Any) -> str:
    b = str(budget or "").strip().lower()
    if b in {"low", "cheap", "کم"}:
        return "low"
    if b in {"open", "high", "زیاد"}:
        return "open"
    return "medium"


def _normalize_lang(value: Any) -> str:
    s = str(value or "").strip().lower()
    if s.startswith("fa") or s in {"farsi", "persian", "فارسی"}:
        return "fa"
    return "en"


_SIGNAL_FA = {
    "activity match": "تناسب با فعالیت",
    "nearby": "نزدیکی",
    "group fit": "تناسب با همراهی",
    "budget fit": "تناسب با بودجه",
    "good for your group size": "مناسب برای تعداد نفرات",
    "highly rated": "امتیاز بالا",
    "popular": "محبوبیت",
}


def _budget_tier(budget: str) -> int:
    return {"low": 1, "medium": 2, "open": 3}.get(_canonical_budget(budget), 2)


def place_id(place: Dict[str, Any]) -> str:
    kind = place.get("osm_kind")
    oid = place.get("osm_id")
    if kind and oid is not None:
        return f"osm:{kind}:{oid}"

    name = str(place.get("name") or "demo").strip().lower()
    try:
        lat = float(place.get("lat"))
        lon = float(place.get("lon"))
        return f"demo:{name}:{lat:.5f}:{lon:.5f}"
    except Exception:
        return f"demo:{name}"


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _people_fit(people_count: Any, ideal_people: Any) -> float:
    try:
        people = int(people_count)
    except Exception:
        people = 2

    try:
        low = int(ideal_people[0])
        high = int(ideal_people[1])
    except Exception:
        low, high = 2, 6

    if low <= people <= high:
        return 1.0

    gap = min(abs(people - low), abs(people - high))
    return float(math.exp(-gap / 2.5))


def build_features(
    place: Dict[str, Any],
    *,
    user_activity: str,
    user_group_type: str,
    user_budget: str,
    people_count: Any,
    has_car: Any,
    origin: Tuple[float, float],
    search_mode: str = "radius",
) -> Tuple[Dict[str, float], float]:
    activity = _canonical_activity(user_activity)
    group = _canonical_group(user_group_type)
    budget = _canonical_budget(user_budget)
    has_car_bool = bool(has_car)

    place_type = _canonical_activity(place.get("type") or place.get("activity") or activity)
    if place_type == activity:
        activity_fit = 1.0
    elif {place_type, activity} == {"cafe", "restaurant"}:
        activity_fit = 0.65
    else:
        activity_fit = 0.25

    best_for = place.get("best_for") or []
    best_for_set = {str(x).strip().lower() for x in best_for}
    group_fit = 1.0 if group in best_for_set else 0.35

    rating = _safe_float(place.get("rating"), 4.2)
    quality = max(0.0, min(1.0, rating / 5.0))

    popularity_raw = _safe_float(place.get("popularity_score"), float("nan"))
    if math.isfinite(popularity_raw):
        popularity = max(0.0, min(1.0, popularity_raw / 100.0))
    else:
        popularity = quality

    user_tier = _budget_tier(budget)
    place_tier = int(_safe_float(place.get("price_tier"), 2))
    if budget == "open":
        budget_fit = 1.0
    elif place_tier <= user_tier:
        budget_fit = 1.0
    elif place_tier == user_tier + 1:
        budget_fit = 0.55
    else:
        budget_fit = 0.25

    ideal_people = place.get("ideal_people") or (2, 6)
    people_fit = _people_fit(people_count, ideal_people)

    plat = _safe_float(place.get("lat"), float("nan"))
    plon = _safe_float(place.get("lon"), float("nan"))
    if math.isfinite(plat) and math.isfinite(plon):
        distance_km = haversine_km(origin[0], origin[1], plat, plon)
    else:
        distance_km = _safe_float(place.get("distance_km") or place.get("distance"), 5.0)

    tau_km = 4.8 if has_car_bool else 2.4
    distance_fit = float(math.exp(-max(0.0, distance_km) / tau_km))

    city_mode = 1.0 if str(search_mode).strip().lower() == "city" else 0.0
    # City search is meant to find the best places across the whole city,
    # not "near the city center", so distance shouldn't affect ranking.
    if city_mode >= 0.5:
        distance_fit = 0.0

    features = {
        "bias": 1.0,
        "activity_fit": float(activity_fit),
        "distance_fit": float(distance_fit),
        "group_fit": float(group_fit),
        "budget_fit": float(budget_fit),
        "people_fit": float(people_fit),
        "quality": float(quality),
        "popularity": float(popularity),
        "city_mode": float(city_mode),
    }
    return features, float(distance_km)


def _dot(weights: Dict[str, float], features: Dict[str, float]) -> float:
    return sum(float(weights.get(k, 0.0)) * float(v) for k, v in features.items())


def score_place(
    place: Dict[str, Any],
    *,
    context: Dict[str, Any],
    weights: Dict[str, float],
) -> Dict[str, Any]:
    features, distance_km = build_features(
        place,
        user_activity=str(context.get("user_activity") or "nature"),
        user_group_type=str(context.get("user_group_type") or "friends"),
        user_budget=str(context.get("user_budget") or "medium"),
        people_count=context.get("people_count", 2),
        has_car=context.get("has_car", False),
        origin=tuple(context.get("origin") or (0.0, 0.0)),  # type: ignore[arg-type]
        search_mode=str(context.get("search_mode") or "radius"),
    )

    logit = _dot(weights, features)
    calibrated = (float(logit) + float(_SCORE_INTERCEPT)) / float(_SCORE_TEMPERATURE)
    p_like = sigmoid(calibrated)
    score = int(round(p_like * 100))
    is_city = str(context.get("search_mode") or "radius").strip().lower() == "city"
    lang = _normalize_lang(context.get("lang"))

    # Breakdown (0..max) derived from current learned weights.
    breakdown = {
        "activity": round(sigmoid(weights.get("activity_fit", 0.0) * features["activity_fit"]) * 30, 2),
        "distance": 0.0
        if is_city
        else round(sigmoid(weights.get("distance_fit", 0.0) * features["distance_fit"]) * 25, 2),
        "group": round(sigmoid(weights.get("group_fit", 0.0) * features["group_fit"]) * 20, 2),
        "budget": round(sigmoid(weights.get("budget_fit", 0.0) * features["budget_fit"]) * 15, 2),
        "people": round(sigmoid(weights.get("people_fit", 0.0) * features["people_fit"]) * 10, 2),
        "quality": round(
            sigmoid(
                (weights.get("quality", 0.0) * features["quality"])
                + (weights.get("popularity", 0.0) * features.get("popularity", 0.0))
            )
            * 10,
            2,
        ),
        "max_raw": 110,
    }

    signals = [
        ("activity match", weights.get("activity_fit", 0.0) * features["activity_fit"]),
        ("nearby", 0.0 if is_city else weights.get("distance_fit", 0.0) * features["distance_fit"]),
        ("group fit", weights.get("group_fit", 0.0) * features["group_fit"]),
        ("budget fit", weights.get("budget_fit", 0.0) * features["budget_fit"]),
        ("good for your group size", weights.get("people_fit", 0.0) * features["people_fit"]),
        ("highly rated", weights.get("quality", 0.0) * features["quality"]),
        ("popular", weights.get("popularity", 0.0) * features.get("popularity", 0.0)),
    ]
    signals.sort(key=lambda x: x[1], reverse=True)
    top = [s[0] for s in signals[:2] if s[1] > 0]
    if lang == "fa":
        top_fa = [_SIGNAL_FA.get(x, x) for x in top]
        if len(top_fa) >= 2:
            explanation = f"پیشنهاد شده چون {top_fa[0]} و {top_fa[1]} دارد."
        elif len(top_fa) == 1:
            explanation = f"پیشنهاد شده چون {top_fa[0]} دارد."
        else:
            explanation = "پیشنهاد شده بر اساس ترجیحات شما و رفتارهای قبلی."
    else:
        if len(top) >= 2:
            explanation = f"Recommended because it has {top[0]} and {top[1]}."
        elif len(top) == 1:
            explanation = f"Recommended because it is {top[0]}."
        else:
            explanation = "Recommended based on your preferences and past behavior."

    scored = dict(place)
    scored.update(
        {
            "place_id": place_id(place),
            "distance_km": round(float(distance_km), 2),
            "score": score,
            "score_raw": round(float(logit), 4),
            "breakdown": breakdown,
            "explanation": explanation,
        }
    )
    return scored


def rank_places(
    places: Iterable[Dict[str, Any]],
    *,
    context: Dict[str, Any],
    weights: Dict[str, float],
    limit: int = 5,
) -> List[Dict[str, Any]]:
    scored = [score_place(p, context=context, weights=weights) for p in places]
    is_city = str(context.get("search_mode") or "radius").strip().lower() == "city"
    if is_city:
        scored.sort(
            key=lambda x: (
                float(x.get("score_raw", 0.0)),
                float(x.get("popularity_score", 0.0)),
                float(x.get("rating", 0.0)),
            ),
            reverse=True,
        )
    else:
        scored.sort(
            key=lambda x: (
                float(x.get("score_raw", 0.0)),
                -float(x.get("distance_km", 9999.0)),
            ),
            reverse=True,
        )
    return scored[: max(1, int(limit))]


def pairwise_update(
    *,
    weights: Dict[str, float],
    clicked_features: Dict[str, float],
    other_features: List[Dict[str, float]],
    lr: float,
    l2: float = 0.0005,
) -> Dict[str, float]:
    """Return updated weights after a single pairwise-ranking step."""
    lr = float(lr)
    if lr <= 0:
        return dict(weights)

    updated = dict(weights)
    for other in other_features:
        # diff = w·(x_clicked - x_other)
        diff_vec = {k: clicked_features.get(k, 0.0) - other.get(k, 0.0) for k in clicked_features.keys()}
        diff = _dot(updated, diff_vec)
        p = sigmoid(diff)
        scale = (1.0 - p) * lr

        for k, dv in diff_vec.items():
            updated[k] = float(updated.get(k, 0.0)) + (scale * float(dv))

    # Light L2 shrinkage for stability.
    if l2 > 0:
        for k, w in list(updated.items()):
            updated[k] = float(w) * (1.0 - (l2 * lr))
    return updated


def build_features_from_context(place: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
    features, _ = build_features(
        place,
        user_activity=str(context.get("user_activity") or "nature"),
        user_group_type=str(context.get("user_group_type") or "friends"),
        user_budget=str(context.get("user_budget") or "medium"),
        people_count=context.get("people_count", 2),
        has_car=context.get("has_car", False),
        origin=tuple(context.get("origin") or (0.0, 0.0)),  # type: ignore[arg-type]
        search_mode=str(context.get("search_mode") or "radius"),
    )
    return features
