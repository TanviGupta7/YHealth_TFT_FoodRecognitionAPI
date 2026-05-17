"""
Lightweight Indian-food heuristics, confidence re-ranking, and meal insights.
Uses model labels + simple image colour cues (no extra ML).
"""

import io
import logging
from typing import Optional

from PIL import Image

from nutrition_data import normalize_label, resolve_food

logger = logging.getLogger(__name__)

# Food-101 labels often confused with Indian dishes
RICE_LIKE = {
    "rice", "fried rice", "risotto", "bibimbap", "paella", "pilaf",
}
BIRYANI_LIKE = {"bibimbap", "paella", "risotto", "fried rice"}
CURRY_LIKE = {
    "curry", "chicken curry", "dal", "lentils", "chana masala",
    "miso soup", "clam chowder", "hot and sour soup",
}
BREAD_LIKE = {"naan", "roti", "garlic bread", "bread", "pita", "bruschetta"}
CREPE_LIKE = {"french toast", "pancakes", "crepe", "waffles", "spring rolls", "bruschetta"}
IDLI_LIKE = {"deviled eggs", "eggs benedict", "edamame", "miso soup"}
POHA_MISLABEL = {"beet salad", "fried rice", "bread pudding", "omelette", "frozen yogurt", "oatmeal"}
SOUTH_INDIAN = {"dosa", "idli", "samosa"}
SNACK_FRIED = {"onion rings", "french fries", "falafel", "spring rolls"}

INDIAN_SYNTHETIC = {
    "poha", "pulao", "jeera rice", "paneer butter masala", "butter chicken",
    "dal makhani", "chole bhature", "rajma chawal", "dosa", "idli", "butter naan",
    "pakora", "dhokla", "upma", "pav bhaji", "biryani", "palak paneer",
}

# Boost applied when colour + label hints align (added to score before re-sort)
INDIAN_BOOST = 0.14
GENERIC_RICE_PENALTY = 0.10
CLOSE_MARGIN = 0.10  # top-two labels within this → apply demotion logic


def _color_hints(image_bytes: Optional[bytes]) -> dict:
    """Simple RGB ratios from a downscaled image."""
    hints = {
        "orange": 0.0,
        "yellow": 0.0,
        "white": 0.0,
        "green": 0.0,
        "brown": 0.0,
    }
    if not image_bytes:
        return hints

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((96, 96))
        pixels = list(img.getdata())
        n = len(pixels) or 1
        for r, g, b in pixels:
            if r > 140 and g > 70 and b < 90 and r > b + 30:
                hints["orange"] += 1
            if r > 160 and g > 140 and b < 120:
                hints["yellow"] += 1
            if r > 200 and g > 200 and b > 200:
                hints["white"] += 1
            if g > r + 15 and g > b + 15 and 60 < g < 200:
                hints["green"] += 1
            if 80 < r < 180 and 50 < g < 140 and b < 100:
                hints["brown"] += 1
        for k in hints:
            hints[k] /= n
    except Exception as exc:
        logger.debug("Color analysis skipped: %s", exc)

    return hints


def _mk(label: str, score: float) -> dict:
    return {"label": label, "score": min(float(score), 0.99)}


def _labels_set(predictions: list[dict]) -> set[str]:
    return {normalize_label(p["label"]) for p in predictions}


def _score_map(predictions: list[dict]) -> dict[str, float]:
    return {normalize_label(p["label"]): float(p["score"]) for p in predictions}


def _rerank(predictions: list[dict], colors: dict) -> list[dict]:
    """Boost Indian interpretations; penalise generic rice when cues disagree."""
    if not predictions:
        return predictions

    adjusted = []
    for p in predictions:
        key = normalize_label(p["label"])
        score = float(p["score"])

        # Penalise easy-overpredicted rice dishes when confidence is weak
        if key in BIRYANI_LIKE and score < 0.42:
            score -= GENERIC_RICE_PENALTY
        if key == "fried rice" and colors["yellow"] > 0.12 and score < 0.50:
            score -= GENERIC_RICE_PENALTY

        # Boost labels that map to Indian dishes via nutrition_data
        if key in CURRY_LIKE and colors["orange"] > 0.08:
            score += INDIAN_BOOST * 0.8
        if key in POHA_MISLABEL and colors["yellow"] > 0.10:
            score += INDIAN_BOOST
        if key in CREPE_LIKE and colors["brown"] > 0.08:
            score += INDIAN_BOOST * 0.6
        if key in IDLI_LIKE and colors["white"] > 0.15:
            score += INDIAN_BOOST * 0.7
        if key in BREAD_LIKE and colors["orange"] > 0.06:
            score += INDIAN_BOOST * 0.5

        adjusted.append(_mk(p["label"], max(score, 0.01)))

    adjusted.sort(key=lambda x: x["score"], reverse=True)
    return adjusted


def _plate_combos(predictions: list[dict], colors: dict) -> list[dict]:
    """Multi-item Indian plate rules (curry + rice, naan + curry, etc.)."""
    if not predictions:
        return predictions

    labels = _labels_set(predictions)
    sm = _score_map(predictions)
    top = float(predictions[0]["score"])

    has_curry = bool(labels & CURRY_LIKE) or colors["orange"] > 0.12
    has_rice = bool(labels & RICE_LIKE) or colors["yellow"] > 0.10 or colors["white"] > 0.18
    has_bread = bool(labels & BREAD_LIKE)
    has_rajma = "lentils" in labels or "chickpeas" in labels or "rajma" in labels

    # Curry + rice → Jeera Rice + Paneer Butter Masala (not generic fried rice / biryani)
    if has_curry and has_rice:
        curry_score = max(
            (sm.get(k, 0) for k in CURRY_LIKE if k in sm),
            default=top,
        )
        rice_score = max(
            (sm.get(k, 0) for k in RICE_LIKE if k in sm),
            default=top * 0.85,
        )
        if has_rajma and ("lentils" in labels or "chickpeas" in labels):
            return [
                _mk("rajma chawal", max(curry_score, top)),
                _mk("jeera rice", rice_score * 0.9),
            ]
        return [
            _mk("curry", max(curry_score, top)),
            _mk("rice", max(rice_score, top * 0.88)),
        ]

    # Naan / bread + orange gravy
    if has_bread and has_curry:
        return [
            _mk("curry", top),
            _mk("naan", max(sm.get("garlic bread", 0), sm.get("bread", 0), top * 0.82)),
        ]

    # Yellow flattened rice cues → Poha (not fried rice / biryani)
    if colors["yellow"] > 0.11 and (labels & POHA_MISLABEL or "fried rice" in labels):
        poha_score = max(top, 0.48)
        if labels & CURRY_LIKE:
            return [_mk("poha", poha_score), _mk("curry", top * 0.75)]
        return [_mk("poha", poha_score)] + predictions[:2]

    # Strong yellow + orange + rice-like → Biryani (layered rice plate)
    if colors["yellow"] > 0.10 and colors["orange"] > 0.09 and labels & BIRYANI_LIKE:
        b_s = max((sm.get(k, 0) for k in BIRYANI_LIKE), default=top)
        if b_s >= 0.32:
            items = [_mk("biryani", max(b_s, top))]
            if has_curry:
                items.append(_mk("curry", top * 0.78))
            return items[:3]

    # Yellow rice without gravy → Pulao (not Biryani)
    if colors["yellow"] > 0.09 and labels & BIRYANI_LIKE:
        biryani_s = max((sm.get(k, 0) for k in BIRYANI_LIKE), default=0)
        if biryani_s < 0.45 and colors["orange"] < 0.08:
            return [_mk("pulao", max(biryani_s, 0.40))] + predictions[:2]

    # Crispy crepe / dosa-like
    if labels & CREPE_LIKE and top < 0.55:
        dosa_s = max(top, 0.44)
        if "sambar" not in labels and colors["white"] > 0.08:
            return [_mk("dosa", dosa_s)] + predictions[:1]

    # White round steamed → Idli
    if labels & IDLI_LIKE and colors["white"] > 0.14 and top < 0.50:
        return [_mk("idli", max(top, 0.42))] + predictions[:1]

    # Chole / chana signals
    if "chana masala" in labels or ("chickpeas" in labels and colors["orange"] > 0.08):
        return [_mk("chana masala", max(sm.get("chana masala", 0), sm.get("chickpeas", 0), top))]

    # Pav bhaji: mashed veg + bread cues
    if "pav bhaji" in labels or (
        colors["orange"] > 0.10 and "hamburger" in labels and top < 0.40
    ):
        return [_mk("pav bhaji", max(top, 0.43))]

    # Upma: grain + yellow, omelette mislabel
    if "omelette" in labels and colors["yellow"] > 0.10 and top < 0.45:
        return [_mk("upma", max(top, 0.41))]

    # Dhokla
    if ("cup cakes" in labels or "cheesecake" in labels) and top < 0.52:
        return [_mk("dhokla", max(top, 0.40))]

    # Pakora / samosa snacks
    if labels & SNACK_FRIED and top < 0.38:
        if "onion rings" in labels or "falafel" in labels:
            return [_mk("pakora", max(top, 0.38))]
        if "samosa" in labels:
            return [_mk("samosa", max(sm.get("samosa", 0), top))]

    # Demote lone weak biryani when fried rice is close second
    if len(predictions) >= 2:
        k0 = normalize_label(predictions[0]["label"])
        k1 = normalize_label(predictions[1]["label"])
        s0, s1 = float(predictions[0]["score"]), float(predictions[1]["score"])
        if k0 in BIRYANI_LIKE and k1 in {"fried rice", "rice", "risotto"} and (s0 - s1) < CLOSE_MARGIN:
            if colors["orange"] > 0.08:
                return [_mk("curry", s0 + 0.05), _mk("rice", s1 + 0.03)]
            return [_mk("pulao", s1 + 0.05), _mk("curry", s0 * 0.9)]

    return predictions


def _dedupe_rice_dishes(predictions: list[dict]) -> list[dict]:
    """Avoid duplicate rice dishes (e.g. Pulao + Jeera Rice) on single-item misreads."""
    if len(predictions) <= 1:
        return predictions

    rice_tokens = ("rice", "biryani", "pulao", "poha", "fried rice")
    seen_rice = False
    out = []
    for p in predictions:
        _, display = resolve_food(p["label"])
        dl = display.lower()
        is_rice = any(tok in dl for tok in rice_tokens)
        if is_rice:
            if seen_rice:
                continue
            seen_rice = True
        out.append(p)
    return out or predictions


def enhance_predictions(predictions: list[dict], image_bytes: Optional[bytes] = None) -> list[dict]:
    """Full pipeline: colour cues → re-rank → Indian plate rules → dedupe."""
    if not predictions:
        return predictions

    colors = _color_hints(image_bytes)
    preds = _rerank(list(predictions), colors)
    preds = _plate_combos(preds, colors)
    preds = _dedupe_rice_dishes(preds)

    # Ensure sorted and cap length for downstream MAX_ITEMS
    preds.sort(key=lambda x: x["score"], reverse=True)
    return preds[:5]


def get_meal_insight(total_macros: dict) -> str:
    cal = int(total_macros.get("calories", 0))
    if cal <= 0:
        return ""

    protein_g = float(total_macros.get("protein_g", 0))
    carbs_g = float(total_macros.get("carbs_g", 0))
    fat_g = float(total_macros.get("fat_g", 0))

    p_cal = protein_g * 4
    c_cal = carbs_g * 4
    f_cal = fat_g * 9
    total_energy = p_cal + c_cal + f_cal or cal

    p_ratio = p_cal / total_energy
    c_ratio = c_cal / total_energy

    if protein_g >= 30 and p_ratio >= 0.28:
        return "High Protein Meal"
    if c_ratio >= 0.55 or carbs_g >= 70:
        return "Carb Heavy Meal"
    if cal >= 650:
        return "Energy Dense Meal"
    if 0.22 <= p_ratio <= 0.35 and 0.38 <= c_ratio <= 0.52:
        return "Balanced Meal"
    return "Moderate Meal"
