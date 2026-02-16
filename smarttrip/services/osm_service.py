from __future__ import annotations

import json
import socket
import time
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


_DEFAULTS_BY_ACTIVITY = {
    "nature": {
        "price_tier": 1,
        "rating": 4.6,
        "best_for": ["family", "friends", "solo"],
        "ideal_people": (2, 12),
    },
    "cafe": {"price_tier": 2, "rating": 4.3, "best_for": ["friends", "solo"], "ideal_people": (1, 5)},
    "restaurant": {
        "price_tier": 2,
        "rating": 4.4,
        "best_for": ["family", "friends", "solo"],
        "ideal_people": (2, 6),
    },
    "entertainment": {
        "price_tier": 2,
        "rating": 4.2,
        "best_for": ["friends", "family"],
        "ideal_people": (2, 10),
    },
}

_ACTIVITY_FAMILY = {
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


def _activity_filters(activity: str) -> List[Tuple[str, str]]:
    activity = (activity or "").strip().lower()
    if activity == "fast_food":
        return [("amenity", "fast_food"), ("amenity", "food_court")]
    if activity == "juice":
        return [("amenity", "juice_bar"), ("amenity", "cafe")]
    if activity == "ice_cream":
        return [("amenity", "ice_cream")]
    if activity == "park":
        return [("leisure", "park"), ("leisure", "garden")]
    if activity == "attraction":
        return [("tourism", "attraction"), ("tourism", "viewpoint"), ("tourism", "picnic_site")]
    if activity == "nature_tourism":
        return [
            ("boundary", "national_park"),
            ("leisure", "nature_reserve"),
            ("tourism", "viewpoint"),
            ("tourism", "picnic_site"),
            ("natural", "beach"),
            ("natural", "wood"),
        ]
    if activity == "historical":
        return [("historic", "monument"), ("historic", "castle"), ("historic", "yes"), ("tourism", "museum")]
    if activity == "cinema":
        return [("amenity", "cinema")]
    if activity == "amusement_park":
        return [("tourism", "theme_park"), ("leisure", "amusement_arcade"), ("leisure", "water_park")]
    if activity == "theatre":
        return [("amenity", "theatre"), ("amenity", "arts_centre")]
    if activity == "museum":
        return [("tourism", "museum"), ("tourism", "gallery")]
    if activity == "pool":
        return [("leisure", "swimming_pool"), ("sport", "swimming")]
    if activity == "hotel":
        return [("tourism", "hotel"), ("tourism", "motel")]
    if activity == "eco_lodge":
        return [("tourism", "guest_house"), ("tourism", "chalet"), ("tourism", "camp_site")]
    if activity == "hostel":
        return [("tourism", "hostel"), ("tourism", "guest_house"), ("tourism", "apartment")]
    if activity == "market":
        return [("shop", "supermarket"), ("amenity", "marketplace")]
    if activity == "shopping_mall":
        return [("shop", "mall"), ("shop", "department_store"), ("building", "retail")]
    if activity == "cafe":
        return [("amenity", "cafe"), ("amenity", "ice_cream")]
    if activity == "restaurant":
        return [("amenity", "restaurant"), ("amenity", "fast_food"), ("amenity", "food_court")]
    if activity == "entertainment":
        return [
            ("amenity", "cinema"),
            ("amenity", "theatre"),
            ("amenity", "arts_centre"),
            ("leisure", "bowling_alley"),
            ("leisure", "amusement_arcade"),
            ("leisure", "water_park"),
            ("tourism", "attraction"),
            ("tourism", "museum"),
            ("tourism", "gallery"),
            ("tourism", "zoo"),
            ("tourism", "theme_park"),
            ("tourism", "aquarium"),
        ]
    # nature
    return [
        ("leisure", "park"),
        ("leisure", "garden"),
        ("boundary", "national_park"),
        ("leisure", "nature_reserve"),
        ("tourism", "viewpoint"),
        ("tourism", "picnic_site"),
    ]


def _score_popularity(tags: Dict[str, Any]) -> int:
    if not tags:
        return 10

    score = 0

    name = tags.get("name") or tags.get("brand") or tags.get("operator") or tags.get("name:en")
    score += 18 if name else 6

    if tags.get("wikipedia") or tags.get("wikipedia:en"):
        score += 30
    if tags.get("wikidata"):
        score += 25

    if tags.get("website") or tags.get("contact:website"):
        score += 8
    if tags.get("opening_hours"):
        score += 4
    if tags.get("phone") or tags.get("contact:phone") or tags.get("email") or tags.get("contact:email"):
        score += 4
    if tags.get("image") or tags.get("wikimedia_commons"):
        score += 4
    if tags.get("contact:instagram") or tags.get("contact:facebook") or tags.get("contact:twitter"):
        score += 4

    tourism = str(tags.get("tourism") or "").strip().lower()
    if tourism in {"attraction", "museum", "gallery", "zoo", "theme_park", "aquarium"}:
        score += 18
    elif tourism in {"viewpoint", "picnic_site"}:
        score += 10

    historic = str(tags.get("historic") or "").strip().lower()
    if historic and historic != "no":
        score += 10

    if tags.get("heritage"):
        score += 8

    amenity = str(tags.get("amenity") or "").strip().lower()
    if amenity in {"restaurant", "cafe", "cinema", "theatre", "arts_centre"}:
        score += 6

    leisure = str(tags.get("leisure") or "").strip().lower()
    if leisure in {"park", "garden", "nature_reserve", "water_park", "bowling_alley", "amusement_arcade"}:
        score += 6

    if any(str(k).startswith("addr:") for k in tags.keys()):
        score += 3

    return int(max(0, min(100, score)))


_OVERPASS_URL_PRIMARY = "https://overpass-api.de/api/interpreter"
_OVERPASS_URL_FALLBACKS = [
    # Useful when the primary is rate-limited.
    "https://overpass.kumi.systems/api/interpreter",
]

_CACHE_TTL_S = 60.0
_cache: Dict[Tuple[float, float, int, str], Tuple[float, List[Dict[str, Any]]]] = {}
_CITY_CACHE_TTL_S = 300.0
_city_cache: Dict[Tuple[str, str], Tuple[float, List[Dict[str, Any]]]] = {}

_GEOCODE_TTL_S = 24 * 60 * 60.0
_geocode_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}

_NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
_HTTP_USER_AGENT = "SmartTrip/1.0 (learning project)"


def _cache_key(lat: float, lon: float, radius: int, activity: str) -> Tuple[float, float, int, str]:
    # Rounded to reduce cache misses while still being location-accurate.
    return (round(float(lat), 4), round(float(lon), 4), int(radius), (activity or "").strip().lower())


def _read_overpass_json(query: str, *, timeout_s: float) -> Optional[Dict[str, Any]]:
    """Return parsed Overpass JSON response, or None on failure."""

    urls = [_OVERPASS_URL_PRIMARY, *_OVERPASS_URL_FALLBACKS]

    for url in urls:
        try:
            req = Request(url, data=query.encode("utf-8"), headers={"User-Agent": _HTTP_USER_AGENT})
            with urlopen(req, timeout=timeout_s) as resp:
                raw = resp.read()
            # Overpass returns UTF-8 JSON.
            return json.loads(raw.decode("utf-8"))
        except socket.timeout:
            return None
        except HTTPError as e:
            # Try a fallback endpoint for common transient errors.
            if getattr(e, "code", None) in {429, 502, 503, 504} and url != urls[-1]:
                continue
            return None
        except URLError as e:
            if isinstance(getattr(e, "reason", None), socket.timeout):
                return None
            # Otherwise, try the next endpoint (e.g., DNS/connection issues).
            if url != urls[-1]:
                continue
            return None
        except Exception:
            return None
    return None


def _read_json_url(
    url: str, *, timeout_s: float, headers: Optional[Dict[str, str]] = None
) -> Optional[Any]:
    try:
        req = Request(url, headers=headers or {})
        with urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read()
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None


def geocode_city(city: str, *, timeout_s: float = 6.0) -> Optional[Dict[str, Any]]:
    """Resolve a city name to a center point and (when possible) an Overpass area id."""
    city = (city or "").strip()
    if not city:
        return None

    key = city.casefold()
    cached = _geocode_cache.get(key)
    now = time.time()
    if cached and (now - cached[0]) <= _GEOCODE_TTL_S:
        return dict(cached[1])

    params = {
        "format": "jsonv2",
        "q": city,
        "limit": 1,
        "addressdetails": 0,
    }
    url = f"{_NOMINATIM_SEARCH_URL}?{urlencode(params)}"
    headers = {"User-Agent": _HTTP_USER_AGENT}

    data = _read_json_url(url, timeout_s=timeout_s, headers=headers)
    if not isinstance(data, list) or not data:
        return None

    item = data[0]
    if not isinstance(item, dict):
        return None

    try:
        lat = float(item.get("lat"))
        lon = float(item.get("lon"))
    except (TypeError, ValueError):
        return None

    osm_type = str(item.get("osm_type") or "")
    try:
        osm_id = int(item.get("osm_id"))
    except (TypeError, ValueError):
        osm_id = None

    area_id: Optional[int] = None
    if osm_id is not None:
        if osm_type == "relation":
            area_id = 3600000000 + osm_id
        elif osm_type == "way":
            area_id = 2400000000 + osm_id

    bbox_raw = item.get("boundingbox")
    bbox: Optional[Tuple[float, float, float, float]] = None
    if isinstance(bbox_raw, list) and len(bbox_raw) == 4:
        # Nominatim returns [south, north, west, east]. Overpass expects (south, west, north, east).
        try:
            south = float(bbox_raw[0])
            north = float(bbox_raw[1])
            west = float(bbox_raw[2])
            east = float(bbox_raw[3])
            bbox = (south, west, north, east)
        except (TypeError, ValueError):
            bbox = None

    result = {
        "query": city,
        "lat": lat,
        "lon": lon,
        "osm_type": osm_type or None,
        "osm_id": osm_id,
        "area_id": area_id,
        "bbox": bbox,
        "display_name": item.get("display_name"),
    }

    _geocode_cache[key] = (now, dict(result))
    return result


def _element_center(element: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    if element.get("type") == "node":
        lat = element.get("lat")
        lon = element.get("lon")
    else:
        center = element.get("center") or {}
        lat = center.get("lat")
        lon = center.get("lon")

    try:
        return (float(lat), float(lon))
    except (TypeError, ValueError):
        return None


def get_places_city(
    city: str,
    *,
    activity: str = "nature",
    timeout_s: float = 10.0,
    limit: int = 120,
) -> List[Dict[str, Any]]:
    """Fetch places from OSM scoped to a whole city using Nominatim + Overpass."""
    city = (city or "").strip()
    if not city:
        return []

    activity = (activity or "").strip().lower() or "nature"
    timeout_s = float(timeout_s)
    timeout_s = max(1.5, min(20.0, timeout_s))
    limit = int(limit)
    limit = max(1, min(250, limit))
    # City queries can be expensive. Keep a moderate candidate pool.
    candidate_limit = max(120, min(350, limit * 2))

    cache_key = (city.casefold(), activity)
    cached = _city_cache.get(cache_key)
    now = time.time()
    if cached and (now - cached[0]) <= _CITY_CACHE_TTL_S:
        return list(cached[1])

    geo = geocode_city(city, timeout_s=min(6.0, timeout_s))
    if not geo:
        return []

    filters = _activity_filters(activity)
    family = _ACTIVITY_FAMILY.get(activity, activity)
    defaults = _DEFAULTS_BY_ACTIVITY.get(family, _DEFAULTS_BY_ACTIVITY["nature"])

    overpass_timeout = int(max(5, min(25, round(timeout_s))))

    area_id = geo.get("area_id")
    bbox = geo.get("bbox")

    queries: List[str] = []
    if isinstance(area_id, int):
        blocks = [f'nwr["{k}"="{v}"](area.searchArea);' for k, v in filters]
        queries.append(
            f"[out:json][timeout:{overpass_timeout}];"
            f"area({area_id})->.searchArea;(\n  "
            + "\n  ".join(blocks)
            + f"\n);\nout center qt {candidate_limit};"
        )
    if isinstance(bbox, tuple) and len(bbox) == 4:
        south, west, north, east = bbox
        blocks = [f'nwr[\"{k}\"=\"{v}\"]({south},{west},{north},{east});' for k, v in filters]
        queries.append(
            f"[out:json][timeout:{overpass_timeout}];(\n  "
            + "\n  ".join(blocks)
            + f"\n);\nout center qt {candidate_limit};"
        )

    if not queries:
        return []

    data: Optional[Dict[str, Any]] = None
    for query in queries:
        data = _read_overpass_json(query, timeout_s=timeout_s)
        if data is None:
            continue
        elements = data.get("elements")
        if isinstance(elements, list) and not elements and query != queries[-1]:
            # If the first query returns an empty result set (common with some
            # area ids), try the next strategy (e.g., bbox).
            continue
        break

    if data is None:
        return []

    elements = data.get("elements") or []
    if not isinstance(elements, list):
        return []

    places: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, float, float]] = set()

    for element in elements:
        if not isinstance(element, dict):
            continue
        center = _element_center(element)
        if not center:
            continue
        el_lat, el_lon = center

        tags = element.get("tags") or {}
        if not isinstance(tags, dict):
            tags = {}
        popularity_score = _score_popularity(tags)

        rating_tag = tags.get("rating") or tags.get("stars")
        rating_override: Optional[float]
        try:
            rating_override = float(rating_tag) if rating_tag is not None else None
        except (TypeError, ValueError):
            rating_override = None
        if rating_override is not None and not (0.0 <= rating_override <= 5.0):
            rating_override = None

        name = (
            tags.get("name")
            or tags.get("brand")
            or tags.get("operator")
            or tags.get("name:en")
            or "Unnamed place"
        )

        sig = (str(name).strip().lower(), round(el_lat, 6), round(el_lon, 6))
        if sig in seen:
            continue
        seen.add(sig)

        places.append(
            {
                "name": str(name),
                "lat": float(el_lat),
                "lon": float(el_lon),
                "type": activity,
                "city": city,
                "osm_id": element.get("id"),
                "osm_kind": element.get("type"),
                "popularity_score": popularity_score,
                **(dict(defaults, rating=rating_override) if rating_override is not None else defaults),
            }
        )
        if len(places) >= candidate_limit:
            break

    places.sort(key=lambda p: (p.get("popularity_score", 0), p.get("rating", 0)), reverse=True)
    places = places[:limit]
    _city_cache[cache_key] = (now, list(places))
    return places


def get_places(
    lat: float,
    lon: float,
    *,
    radius: int = 5000,
    activity: str = "nature",
    timeout_s: float = 8.0,
    limit: int = 40,
) -> List[Dict[str, Any]]:
    """Fetch nearby places from OSM via Overpass.

    Returns an empty list when Overpass is unavailable or the query fails.
    """
    activity = (activity or "").strip().lower() or "nature"
    radius = int(radius)
    radius = max(250, min(20000, radius))
    timeout_s = float(timeout_s)
    timeout_s = max(1.5, min(15.0, timeout_s))
    limit = int(limit)
    limit = max(1, min(200, limit))
    candidate_limit = max(100, min(280, limit * 2))

    family = _ACTIVITY_FAMILY.get(activity, activity)
    defaults = _DEFAULTS_BY_ACTIVITY.get(family, _DEFAULTS_BY_ACTIVITY["nature"])

    key = _cache_key(lat, lon, radius, activity)
    cached = _cache.get(key)
    now = time.time()
    if cached and (now - cached[0]) <= _CACHE_TTL_S:
        return list(cached[1])

    filters = _activity_filters(activity)
    blocks = [
        f'nwr["{k}"="{v}"](around:{radius},{float(lat)},{float(lon)});' for k, v in filters
    ]

    overpass_timeout = int(max(5, min(25, round(timeout_s))))
    # Ask Overpass to cap output to keep responses fast.
    query = (
        f"[out:json][timeout:{overpass_timeout}];(\n  "
        + "\n  ".join(blocks)
        + f"\n);\nout center qt {candidate_limit};"
    )

    data = _read_overpass_json(query, timeout_s=timeout_s)
    if not data:
        return []

    elements = data.get("elements") or []
    if not isinstance(elements, list):
        return []

    places: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, float, float]] = set()

    for element in elements:
        if not isinstance(element, dict):
            continue
        center = _element_center(element)
        if not center:
            continue
        el_lat, el_lon = center

        tags = element.get("tags") or {}
        if not isinstance(tags, dict):
            tags = {}
        popularity_score = _score_popularity(tags)

        rating_tag = tags.get("rating") or tags.get("stars")
        rating_override: Optional[float]
        try:
            rating_override = float(rating_tag) if rating_tag is not None else None
        except (TypeError, ValueError):
            rating_override = None
        if rating_override is not None and not (0.0 <= rating_override <= 5.0):
            rating_override = None
        name = (
            tags.get("name")
            or tags.get("brand")
            or tags.get("operator")
            or tags.get("name:en")
            or "Unnamed place"
        )

        sig = (str(name).strip().lower(), round(el_lat, 6), round(el_lon, 6))
        if sig in seen:
            continue
        seen.add(sig)

        places.append(
            {
                "name": str(name),
                "lat": float(el_lat),
                "lon": float(el_lon),
                "type": activity,
                "osm_id": element.get("id"),
                "osm_kind": element.get("type"),
                "popularity_score": popularity_score,
                **(dict(defaults, rating=rating_override) if rating_override is not None else defaults),
            }
        )
        if len(places) >= candidate_limit:
            break

    places.sort(key=lambda p: (p.get("popularity_score", 0), p.get("rating", 0)), reverse=True)
    places = places[:limit]
    _cache[key] = (now, list(places))
    return places
