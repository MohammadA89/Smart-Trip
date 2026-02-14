from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple


_PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def normalize_text(text: str) -> str:
    s = (text or "").strip().lower()
    s = s.translate(_PERSIAN_DIGITS).translate(_ARABIC_DIGITS)
    s = re.sub(r"\s+", " ", s)
    return s


def _clean_city_candidate(candidate: str) -> str:
    c = (candidate or "").strip()
    if not c:
        return c

    # Cut on comma-like separators.
    c = re.split(r"[,\u060c]", c, maxsplit=1)[0].strip()

    # Stop at common connectors (Persian + English).
    stops = [
        " با ",
        " برای ",
        " نزدیک ",
        " اطراف ",
        " around ",
        " near ",
        " within ",
        " radius ",
        " with ",
        " budget ",
    ]
    for stop in stops:
        if stop in c:
            c = c.split(stop, 1)[0].strip()

    # Keep it reasonably short.
    c = c[:60].strip()
    return c


def extract_radius_km(text: str) -> Optional[float]:
    t = normalize_text(text)
    # "10km", "10 km", "10 کیلومتر"
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|kilometers?|کیلومتر)", t)
    if not m:
        m = re.search(r"radius\s*[:=]?\s*(\d+(?:\.\d+)?)", t)
    if not m:
        return None
    try:
        km = float(m.group(1))
    except Exception:
        return None
    if km <= 0:
        return None
    return km


def extract_city(text: str) -> Optional[str]:
    t = (text or "").strip()
    # "city: Tehran", "شهر تهران"
    m = re.search(r"city\s*[:=]\s*([^\n,]+)", t, flags=re.IGNORECASE)
    if m:
        return _clean_city_candidate(m.group(1))
    m = re.search(r"شهر\s*[:=]?\s*([^\n,]+)", t)
    if m:
        return _clean_city_candidate(m.group(1))
    # Persian common: "توی تهران", "در تهران"
    m = re.search(r"(?:توی|تو|در)\s+([^\n,]{2,40})", t)
    if m:
        return _clean_city_candidate(m.group(1))
    # "in Tehran"
    m = re.search(r"\bin\s+([A-Za-z\u0600-\u06FF][A-Za-z\u0600-\u06FF\\s]{1,40})", t)
    if m:
        return _clean_city_candidate(m.group(1))
    return None


def _normalize_lang(value: Any) -> str:
    s = str(value or "").strip().lower()
    if s.startswith("fa") or s in {"farsi", "persian", "فارسی"}:
        return "fa"
    return "en"


_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def _maybe_fa_digits(s: str, *, lang: str) -> str:
    if lang == "fa":
        return str(s).translate(_FA_DIGITS)
    return str(s)


def _label(value: Any, mapping: Dict[str, Dict[str, str]], *, lang: str) -> str:
    key = str(value or "").strip().lower()
    entry = mapping.get(key)
    if not entry:
        return key
    return entry.get(lang, entry.get("en", key))


_ACTIVITY_LABELS = {
    "nature": {"en": "nature", "fa": "طبیعت"},
    "cafe": {"en": "cafe", "fa": "کافه"},
    "restaurant": {"en": "restaurant", "fa": "رستوران"},
    "entertainment": {"en": "entertainment", "fa": "سرگرمی"},
}
_GROUP_LABELS = {
    "solo": {"en": "solo", "fa": "تنها"},
    "friends": {"en": "friends", "fa": "دوستان"},
    "family": {"en": "family", "fa": "خانواده"},
}
_BUDGET_LABELS = {
    "low": {"en": "low", "fa": "کم"},
    "medium": {"en": "medium", "fa": "متوسط"},
    "open": {"en": "open", "fa": "زیاد"},
}


def parse_message(
    message: str,
    current: Optional[Dict[str, Any]] = None,
    *,
    lang: str = "en",
) -> Tuple[Dict[str, Any], str]:
    """Extract preference updates from free text.

    Returns (prefs_update, assistant_reply).
    """
    current = dict(current or {})
    lang = _normalize_lang(lang)
    text = normalize_text(message)
    updates: Dict[str, Any] = {}

    # Activity
    if any(k in text for k in ["کافه", "cafe", "coffee", "espresso"]):
        updates["activity"] = "cafe"
    elif any(k in text for k in ["رستوران", "restaurant", "food", "dinner", "ناهار", "شام"]):
        updates["activity"] = "restaurant"
    elif any(
        k in text
        for k in [
            "سینما",
            "cinema",
            "movie",
            "تئاتر",
            "theatre",
            "bowling",
            "arcade",
            "سرگرمی",
        ]
    ):
        updates["activity"] = "entertainment"
    elif any(k in text for k in ["طبیعت", "nature", "پارک", "park", "green", "outdoor"]):
        updates["activity"] = "nature"

    # Group
    if any(k in text for k in ["خانواده", "family", "بچه", "kids"]):
        updates["group_type"] = "family"
    elif any(k in text for k in ["دوست", "friends", "رفیق"]):
        updates["group_type"] = "friends"
    elif any(k in text for k in ["تنها", "solo", "alone"]):
        updates["group_type"] = "solo"

    # Budget
    if any(k in text for k in ["ارزان", "cheap", "low budget", "کم"]):
        updates["budget"] = "low"
    elif any(k in text for k in ["متوسط", "medium", "normal"]):
        updates["budget"] = "medium"
    elif any(k in text for k in ["گران", "expensive", "open budget", "no limit", "زیاد"]):
        updates["budget"] = "open"

    # Car availability
    if any(k in text for k in ["بدون ماشین", "no car"]):
        updates["has_car"] = False
    elif any(k in text for k in ["ماشین دارم", "ماشین", "car", "drive"]):
        updates["has_car"] = True

    # People count: "4 نفر"
    m = re.search(r"(\d+)\s*(?:نفر|people|persons?)", text)
    if m:
        try:
            updates["people_count"] = int(m.group(1))
        except Exception:
            pass

    # Search mode
    if any(k in text for k in ["کل شهر", "تمام شهر", "whole city", "city wide", "city"]):
        updates["search_mode"] = "city"
    elif any(k in text for k in ["نزدیک", "nearby", "around", "اطراف"]):
        updates["search_mode"] = "radius"

    # Radius
    km = extract_radius_km(message)
    if km is not None:
        updates["radius_m"] = int(round(km * 1000))
        updates.setdefault("search_mode", "radius")

    # City
    city = extract_city(message)
    if city:
        updates.setdefault("search_mode", "city")
    if city:
        updates["city"] = city

    # Build reply
    activity = updates.get("activity") or current.get("activity")
    group_type = updates.get("group_type") or current.get("group_type")
    budget = updates.get("budget") or current.get("budget")
    search_mode = updates.get("search_mode") or current.get("search_mode") or "radius"
    radius_m = updates.get("radius_m") or current.get("radius_m")
    city_out = updates.get("city") or current.get("city")

    summary_parts = []
    if activity:
        if lang == "fa":
            summary_parts.append(f"فعالیت: {_label(activity, _ACTIVITY_LABELS, lang=lang)}")
        else:
            summary_parts.append(f"activity: {_label(activity, _ACTIVITY_LABELS, lang=lang)}")
    if group_type:
        if lang == "fa":
            summary_parts.append(f"همراهی: {_label(group_type, _GROUP_LABELS, lang=lang)}")
        else:
            summary_parts.append(f"group: {_label(group_type, _GROUP_LABELS, lang=lang)}")
    if budget:
        if lang == "fa":
            summary_parts.append(f"بودجه: {_label(budget, _BUDGET_LABELS, lang=lang)}")
        else:
            summary_parts.append(f"budget: {_label(budget, _BUDGET_LABELS, lang=lang)}")
    if search_mode == "city" and city_out:
        if lang == "fa":
            summary_parts.append(f"شهر: {city_out}")
        else:
            summary_parts.append(f"city: {city_out}")
    elif search_mode == "radius" and radius_m:
        try:
            km = f"{float(radius_m)/1000:.1f}"
            if lang == "fa":
                summary_parts.append(f"شعاع: {_maybe_fa_digits(km, lang=lang)} کیلومتر")
            else:
                summary_parts.append(f"radius: {km} km")
        except Exception:
            pass

    if summary_parts:
        if lang == "fa":
            reply = "باشه — " + "، ".join(summary_parts) + "."
        else:
            reply = "Got it — " + ", ".join(summary_parts) + "."
    else:
        reply = (
            "بگو دنبال چی هستی (مثال: «کافه دنج توی تهران با بودجه کم» یا «پارک نزدیک ۵ کیلومتر»)."
            if lang == "fa"
            else "Tell me what you want (e.g., “cozy cafe in Tehran with low budget” or “park nearby 5km”)."
        )

    return updates, reply
