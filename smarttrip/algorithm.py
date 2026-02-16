"""Scoring-based recommendation algorithm for SmartTrip.

This module is intentionally lightweight (no external deps) so the UI can work
even when live POI sources (e.g., OSM/Overpass) are unavailable.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Tuple

Budget = str  # "low" | "medium" | "open"
GroupType = str  # "solo" | "friends" | "family"
ActivityType = str  # "nature" | "cafe" | "restaurant" | "entertainment"


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometers."""
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


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _budget_tier(budget: Budget) -> int:
    return {"low": 1, "medium": 2, "open": 3}.get(budget, 2)


def _canonical_activity(activity: str) -> ActivityType:
    activity = (activity or "").strip().lower()
    alias = {
        "fast_food": "restaurant",
        "juice": "cafe",
        "ice_cream": "cafe",
        "park": "nature",
        "attraction": "nature",
        "nature_tourism": "nature",
        "historical": "nature",
        "cinema": "entertainment",
        "amusement_park": "entertainment",
        "theatre": "entertainment",
        "museum": "entertainment",
        "pool": "entertainment",
        "hotel": "entertainment",
        "eco_lodge": "nature",
        "hostel": "entertainment",
        "market": "entertainment",
        "shopping_mall": "entertainment",
    }
    activity = alias.get(activity, activity)
    if activity in {"nature", "cafe", "restaurant", "entertainment"}:
        return activity  # type: ignore[return-value]
    return "nature"


def _canonical_group(group_type: str) -> GroupType:
    group_type = (group_type or "").strip().lower()
    if group_type in {"solo", "friends", "family"}:
        return group_type  # type: ignore[return-value]
    return "friends"


def _canonical_budget(budget: str) -> Budget:
    budget = (budget or "").strip().lower()
    if budget in {"low", "medium", "open"}:
        return budget  # type: ignore[return-value]
    return "medium"


def _safe_int(value: Any, default: int, low: int, high: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(low, min(high, parsed))


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def enrich_place(place: Dict[str, Any], activity_fallback: str) -> Dict[str, Any]:
    """Fill missing fields with sensible defaults for scoring."""
    activity = _canonical_activity(place.get("type") or activity_fallback)

    enriched: Dict[str, Any] = dict(place)
    enriched["type"] = activity
    enriched.setdefault("name", "Unknown")

    # Heuristic defaults when only OSM tags exist.
    if "rating" not in enriched:
        enriched["rating"] = 4.4 if activity == "nature" else 4.2
    if "price_tier" not in enriched:
        enriched["price_tier"] = {"nature": 1, "cafe": 2, "restaurant": 2, "entertainment": 2}.get(
            activity, 2
        )
    if "best_for" not in enriched:
        enriched["best_for"] = {
            "nature": ["family", "friends", "solo"],
            "cafe": ["friends", "solo"],
            "restaurant": ["family", "friends", "solo"],
            "entertainment": ["friends", "family"],
        }.get(activity, ["friends"])
    if "ideal_people" not in enriched:
        enriched["ideal_people"] = {
            "nature": (2, 8),
            "cafe": (1, 5),
            "restaurant": (2, 6),
            "entertainment": (2, 10),
        }.get(activity, (2, 6))

    return enriched


def score_place(
    place: Dict[str, Any],
    *,
    user_activity: str,
    user_group_type: str,
    user_budget: str,
    people_count: Any,
    has_car: Any,
    origin: Tuple[float, float],
) -> Dict[str, Any]:
    """Return a scored place with a breakdown and explanation."""
    activity = _canonical_activity(user_activity)
    group_type = _canonical_group(user_group_type)
    budget = _canonical_budget(user_budget)
    people = _safe_int(people_count, default=2, low=1, high=12)
    has_car_bool = bool(has_car)
    origin_lat, origin_lon = origin

    place = enrich_place(place, activity_fallback=activity)

    place_lat = _safe_float(place.get("lat"), float("nan"))
    place_lon = _safe_float(place.get("lon"), float("nan"))

    if math.isfinite(place_lat) and math.isfinite(place_lon):
        distance_km = haversine_km(origin_lat, origin_lon, place_lat, place_lon)
    else:
        distance_km = _safe_float(place.get("distance_km") or place.get("distance"), 5.0)

    # --- Scoring model (raw 0..110, later normalized to 0..100) ---
    activity_score_max = 30.0
    distance_score_max = 25.0
    group_score_max = 20.0
    budget_score_max = 15.0
    people_score_max = 10.0
    rating_score_max = 10.0
    raw_max = (
        activity_score_max
        + distance_score_max
        + group_score_max
        + budget_score_max
        + people_score_max
        + rating_score_max
    )

    # Activity match (with a small "near match" boost for cafe/restaurant).
    place_type: ActivityType = _canonical_activity(place.get("type"))
    if place_type == activity:
        activity_score = activity_score_max
    elif {place_type, activity} == {"cafe", "restaurant"}:
        activity_score = 18.0
    else:
        activity_score = 6.0

    # Distance: exponential decay, with a wider tolerance when user has a car.
    tau_km = 4.5 if has_car_bool else 2.2
    distance_score = distance_score_max * math.exp(-distance_km / tau_km)
    distance_score = clamp(distance_score, 0.0, distance_score_max)

    # Group compatibility.
    best_for = place.get("best_for") or []
    best_for_set = {str(x).strip().lower() for x in best_for}
    group_score = group_score_max if group_type in best_for_set else 7.0

    # Budget fit.
    user_tier = _budget_tier(budget)
    place_tier = _safe_int(place.get("price_tier"), default=2, low=1, high=3)
    if budget == "open":
        budget_score = budget_score_max
    elif place_tier <= user_tier:
        budget_score = budget_score_max
    elif place_tier == user_tier + 1:
        budget_score = 7.5
    else:
        budget_score = 4.0

    # People count fit.
    ideal_people = place.get("ideal_people") or (2, 6)
    try:
        min_people = int(ideal_people[0])
        max_people = int(ideal_people[1])
    except Exception:
        min_people, max_people = 2, 6
    if min_people <= people <= max_people:
        people_score = people_score_max
    else:
        # linearly fall off outside the ideal range
        gap = min(abs(people - min_people), abs(people - max_people))
        people_score = clamp(people_score_max - (gap * 2.5), 0.0, people_score_max)

    # Rating quality (if present).
    rating = clamp(_safe_float(place.get("rating"), 4.3), 0.0, 5.0)
    rating_score = (rating / 5.0) * rating_score_max

    raw = activity_score + distance_score + group_score + budget_score + people_score + rating_score
    normalized = int(round((raw / raw_max) * 100))

    breakdown = {
        "activity": round(activity_score, 2),
        "distance": round(distance_score, 2),
        "group": round(group_score, 2),
        "budget": round(budget_score, 2),
        "people": round(people_score, 2),
        "quality": round(rating_score, 2),
        "max_raw": raw_max,
    }

    # Explanation: highlight the top 2 signals.
    signals = [
        ("Activity match", activity_score / activity_score_max),
        ("Nearby", distance_score / distance_score_max),
        ("Group fit", group_score / group_score_max),
        ("Budget fit", budget_score / budget_score_max),
        ("Good for your group size", people_score / people_score_max),
    ]
    signals.sort(key=lambda x: x[1], reverse=True)
    top = [s[0] for s in signals[:2]]
    explanation = (
        f"Recommended because it has {top[0].lower()} and {top[1].lower()}."
        if len(top) == 2
        else "Recommended because it matches your preferences."
    )

    scored = dict(place)
    scored.update(
        {
            "distance_km": round(distance_km, 2),
            "score": normalized,
            "score_raw": round(raw, 2),
            "breakdown": breakdown,
            "explanation": explanation,
        }
    )
    return scored


def recommend_places(
    places: Iterable[Dict[str, Any]],
    *,
    user_activity: str,
    user_group_type: str,
    user_budget: str,
    people_count: Any,
    has_car: Any,
    origin: Tuple[float, float],
    limit: int = 5,
) -> List[Dict[str, Any]]:
    scored = [
        score_place(
            p,
            user_activity=user_activity,
            user_group_type=user_group_type,
            user_budget=user_budget,
            people_count=people_count,
            has_car=has_car,
            origin=origin,
        )
        for p in places
    ]
    scored.sort(key=lambda x: (x.get("score", 0), -x.get("distance_km", 9999)), reverse=True)
    return scored[: max(1, limit)]


def demo_places(center_lat: float, center_lon: float) -> List[Dict[str, Any]]:
    """High-quality demo POIs around a center point (deterministic)."""
    catalog = [
        ("Aurora Park", "nature", 0.012, -0.006, 1, 4.7, ["family", "friends", "solo"], (2, 10)),
        ("Neon Brew Café", "cafe", -0.008, 0.010, 2, 4.5, ["friends", "solo"], (1, 5)),
        ("Skyline Bistro", "restaurant", 0.004, 0.014, 2, 4.6, ["family", "friends", "solo"], (2, 6)),
        ("Pulse Arcade", "entertainment", -0.014, -0.004, 2, 4.4, ["friends", "family"], (2, 10)),
        ("Crystal Garden", "nature", 0.018, 0.003, 1, 4.8, ["family", "friends", "solo"], (2, 10)),
        ("Midnight Espresso", "cafe", -0.003, -0.015, 2, 4.3, ["friends", "solo"], (1, 4)),
        ("Orbit Cinema", "entertainment", 0.010, 0.020, 2, 4.2, ["friends", "family"], (2, 8)),
        ("Nova Diner", "restaurant", -0.020, 0.006, 3, 4.5, ["friends", "family"], (2, 8)),
        ("Riverwalk Green", "nature", 0.006, -0.020, 1, 4.6, ["family", "friends", "solo"], (2, 12)),
        ("Electric Lounge", "entertainment", -0.010, 0.018, 3, 4.3, ["friends"], (2, 8)),
    ]

    places: List[Dict[str, Any]] = []
    for name, ptype, dlat, dlon, price_tier, rating, best_for, ideal_people in catalog:
        places.append(
            {
                "name": name,
                "type": ptype,
                "lat": center_lat + dlat,
                "lon": center_lon + dlon,
                "price_tier": price_tier,
                "rating": rating,
                "best_for": best_for,
                "ideal_people": ideal_people,
            }
        )
    return places
