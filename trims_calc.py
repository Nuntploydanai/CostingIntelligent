from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
MASTER_DIR = BASE_DIR / "master_clean"


def _norm(x: Any) -> str:
    return ("" if x is None else str(x)).strip()


def _to_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip()
        if s == "":
            return None
        try:
            return float(s)
        except Exception:
            return None
    return None


def _load_item_price_unit() -> dict[str, dict[str, Any]]:
    path = MASTER_DIR / "packing_trims_item_price_unit.csv"
    out: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            item = _norm(row.get("trims_type"))
            if not item:
                continue
            out[item] = {
                "default_price_each": _to_float(row.get("default_price_each")),
                "unit": _norm(row.get("unit")),
            }
    return out


def _load_usage() -> dict[tuple[str, str], dict[str, float | None]]:
    path = MASTER_DIR / "packing_trims_usage.csv"
    out: dict[tuple[str, str], dict[str, float | None]] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            item = _norm(row.get("trims_type"))
            part = _norm(row.get("garment_part"))
            if not item or not part:
                continue
            out[(item, part)] = {
                "usage_small": _to_float(row.get("usage_small")),
                "usage_large": _to_float(row.get("usage_large")),
            }
    return out


def _import_factor(material_coo: str) -> float:
    v = _norm(material_coo)
    if v == "Domestic":
        return 1.0
    if v == "Import":
        return 1.05
    # Excel falls back to "1" in inner IF; we follow that
    return 1.0


def _gender_factor(gender: str) -> float:
    g = _norm(gender).upper()
    if g == "MEN":
        return 1.0
    if g == "WOMEN":
        return 0.95
    if g == "KIDS":
        return 0.85
    return 0.0


def _size_multiplier(size: str) -> float:
    """Excel Data link X17 size rule for Step 3.

    User confirmed sizes are S-XL and 2XL-3XL in this workbook.
    """

    s = _norm(size)
    if s == "S-XL":
        return 1.0
    if s == "2XL-3XL":
        return 1.15
    return 0.0


def compute_trim_row(row: dict[str, Any]) -> dict[str, Any]:
    """Step 3: Trims & Sewn in label (Excelish for row 1).

    Mirrors Data link row 17 and Basic Shirts wrappers.
    """

    trims_type = _norm(row.get("trims_type"))
    garment_part = _norm(row.get("garment_part"))
    material_coo = _norm(row.get("material_coo"))

    gender = _norm(row.get("gender"))
    size = _norm(row.get("size"))

    usage_override = _to_float(row.get("usage_override"))
    price_override = _to_float(row.get("price_override"))

    item_map = _load_item_price_unit()
    usage_map = _load_usage()

    # UNIT: XLOOKUP(G13, Packing&Trims!B:B, D:D)
    unit = item_map.get(trims_type, {}).get("unit") if trims_type else ""

    # Default usage: Data link O17 uses SMALL (M) via K+L->M.
    default_usage_val = None
    if trims_type and garment_part:
        default_usage_val = (usage_map.get((trims_type, garment_part), {}) or {}).get("usage_small")

    # Basic Shirts O13 wrapper: if override blank -> show Data link O17 else show 0
    default_usage_display: Any
    if usage_override is None:
        default_usage_display = "-" if not trims_type else (default_usage_val if default_usage_val is not None else "Please select garment part")
    else:
        default_usage_display = 0

    # Default price/each: Data link S17 lookup B->C.
    default_price_each_val = item_map.get(trims_type, {}).get("default_price_each") if trims_type else None

    # Basic Shirts Q13 wrapper: if price override blank -> show Data link S17 else show 0
    default_price_display: Any
    if price_override is None:
        default_price_display = "-" if not trims_type else (default_price_each_val if default_price_each_val is not None else "-")
    else:
        default_price_display = 0

    # R17 = Q13 + U13 (effective price)
    effective_price = ((default_price_each_val or 0.0) if price_override is None else 0.0) + (price_override or 0.0)

    # V17 import/domestic factor
    v17 = _import_factor(material_coo)

    # W17 = R17*V17*(M13+O13)
    effective_usage = (usage_override or 0.0) + (default_usage_val if usage_override is None and default_usage_val is not None else 0.0)
    w17 = effective_price * v17 * effective_usage

    # X17 size adjustment (only for yard path in Excel)
    x17 = w17 * _size_multiplier(size)

    # Y17 chooses by unit
    if unit == "YARD":
        y17 = x17
    elif unit == "PIECE":
        y17 = w17
    else:
        y17 = 0.0

    # Z17 gender factor
    z17 = y17 * _gender_factor(gender)

    total_cost_display: Any = round(z17, 3)

    return {
        "trims_type": trims_type,
        "garment_part": garment_part,
        "unit": unit,
        "default_usage": default_usage_display,
        "default_price_each": default_price_display,
        "total_cost": total_cost_display,
        "note": "Step 3 Excelish: O17/S17/W17/X17/Y17/Z17 rebuilt from Packing&Trims masters + wrappers (size S-XL vs 2XL-3XL).",
    }
