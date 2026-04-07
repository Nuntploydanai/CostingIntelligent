"""Step 6: Manufacturing Cost calculator with Excel parity.

Excel reference:
    W18 = Data link!K30
    W19 = Data link!L30
    W20 = Data link!Q30   (Kenya special override in workbook)
    W21 = W18 / W20 * W19

Key parity rules:
1. Minutes are not always the raw SAM lookup.
   Add +0.4 when any fabrication using_part == "Pocket bag".
2. Actual efficiency is:
      product_efficiency * quantity_efficiency
3. Missing lookups should raise an error instead of silently using fake defaults.
4. Kenya can use a workbook-specific efficiency override.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
MASTER_DIR = BASE_DIR / "master_clean"

KENYA_EFFICIENCY_OVERRIDE = 0.65
POCKET_BAG_MINUTES_ADDON = 0.4


def _norm(value: Any) -> str:
    return ("" if value is None else str(value)).strip()


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s or s == "-":
        return None
    try:
        return float(s)
    except Exception:
        return None


def _ci_lookup(mapping: dict[tuple[str, ...], float], key: tuple[str, ...]) -> float | None:
    exact = mapping.get(key)
    if exact is not None:
        return exact

    lowered = tuple(part.lower() for part in key)
    for existing_key, value in mapping.items():
        if tuple(part.lower() for part in existing_key) == lowered:
            return value
    return None


def _ci_lookup_str(mapping: dict[str, float], key: str) -> float | None:
    if key in mapping:
        return mapping[key]

    lowered = key.lower()
    for existing_key, value in mapping.items():
        if existing_key.lower() == lowered:
            return value
    return None


def _load_sam_minutes_lookup() -> dict[tuple[str, str, str, str], float]:
    path = MASTER_DIR / "sam_minutes_lookup.csv"
    out: dict[tuple[str, str, str, str], float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                _norm(row.get("gender")),
                _norm(row.get("product")),
                _norm(row.get("seam")),
                _norm(row.get("size")),
            )
            value = _to_float(row.get("sam_minutes"))
            if all(key) and value is not None:
                out[key] = value

    return out


def _load_product_efficiency_lookup() -> dict[tuple[str, str, str], float]:
    path = MASTER_DIR / "product_efficiency_lookup.csv"
    out: dict[tuple[str, str, str], float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                _norm(row.get("product")),
                _norm(row.get("seam")),
                _norm(row.get("size")),
            )
            value = _to_float(row.get("product_efficiency"))
            if all(key) and value is not None:
                out[key] = value

    return out


def _load_quantity_efficiency_lookup() -> dict[str, float]:
    path = MASTER_DIR / "efficiency_by_quantity.csv"
    out: dict[str, float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = _norm(row.get("quantity_range"))
            value = _to_float(row.get("efficiency"))
            if key and value is not None:
                out[key] = value

    return out


def _load_cost_rate_data() -> dict[str, float]:
    path = MASTER_DIR / "cost_rate.csv"
    out: dict[str, float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = _norm(row.get("country"))
            value = _to_float(row.get("cost_rate"))
            if key and value is not None:
                out[key] = value

    return out


def _load_manufacturing_data() -> dict[str, dict[str, float]]:
    path = MASTER_DIR / "manufacturing_cost_by_country.csv"
    out: dict[str, dict[str, float]] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            country = _norm(row.get("country"))
            if not country:
                continue

            out[country] = {
                "minutes": _to_float(row.get("minutes")) or 0.0,
                "cost_rate": _to_float(row.get("cost_rate")) or 0.0,
                "efficiency": _to_float(row.get("efficiency")) or 0.0,
                "total_cost": _to_float(row.get("total_cost")) or 0.0,
            }

    return out


def _has_pocket_bag(using_parts: list[str] | None) -> bool:
    if not using_parts:
        return False
    return any(_norm(part).lower() == "pocket bag" for part in using_parts)


def compute_manufacturing_for_coo(
    gender: str = "",
    silhouette: str = "",
    seam: str = "",
    size: str = "",
    quantity: str = "",
    coo: str = "",
    using_parts: list[str] | None = None,
) -> dict[str, Any]:
    sam_lookup = _load_sam_minutes_lookup()
    product_eff_lookup = _load_product_efficiency_lookup()
    quantity_eff_lookup = _load_quantity_efficiency_lookup()
    cost_rate_lookup = _load_cost_rate_data()

    gender = _norm(gender)
    silhouette = _norm(silhouette)
    seam = _norm(seam)
    size = _norm(size)
    quantity = _norm(quantity)
    coo = _norm(coo)

    base_minutes = _ci_lookup(sam_lookup, (gender, silhouette, seam, size))
    if base_minutes is None:
        raise ValueError(
            f"SAM minutes not found for gender={gender!r}, silhouette={silhouette!r}, "
            f"seam={seam!r}, size={size!r}"
        )

    minutes = base_minutes + (POCKET_BAG_MINUTES_ADDON if _has_pocket_bag(using_parts) else 0.0)

    product_efficiency = _ci_lookup(product_eff_lookup, (silhouette, seam, size))
    if product_efficiency is None:
        raise ValueError(
            f"Product efficiency not found for silhouette={silhouette!r}, seam={seam!r}, size={size!r}"
        )

    quantity_efficiency = _ci_lookup_str(quantity_eff_lookup, quantity)
    if quantity_efficiency is None:
        raise ValueError(f"Quantity efficiency not found for quantity={quantity!r}")

    actual_efficiency = product_efficiency * quantity_efficiency
    if coo.upper() == "KENYA":
        actual_efficiency = KENYA_EFFICIENCY_OVERRIDE

    cost_rate = _ci_lookup_str(cost_rate_lookup, coo)
    if cost_rate is None:
        raise ValueError(f"Cost rate not found for COO={coo!r}")

    total_cost = (minutes / actual_efficiency) * cost_rate if actual_efficiency else 0.0

   print("DEBUG STEP 6", {
    "gender": gender,
    "silhouette": silhouette,
    "seam": seam,
    "size": size,
    "quantity": quantity,
    "coo": coo,
    "product_efficiency": product_efficiency,
    "quantity_efficiency": quantity_efficiency,
    "actual_efficiency": actual_efficiency,
})
    
    return {
        "country": coo,
        "base_minutes": round(base_minutes, 3),
        "minutes": round(minutes, 3),
        "cost_rate": round(cost_rate, 6),
        "product_efficiency": round(product_efficiency, 3),
        "quantity_efficiency": round(quantity_efficiency, 3),
        "efficiency": round(actual_efficiency, 3),
        "total_cost": round(total_cost, 6),
        "pocket_bag_applied": _has_pocket_bag(using_parts),
    }


def compute_all_manufacturing_rows(
    gender: str = "",
    silhouette: str = "",
    seam: str = "",
    size: str = "",
    quantity: str = "",
    coo: str = "",
    using_parts: list[str] | None = None,
) -> list[dict[str, Any]]:
    cost_rate_lookup = _load_cost_rate_data()

    if coo:
        result = compute_manufacturing_for_coo(
            gender=gender,
            silhouette=silhouette,
            seam=seam,
            size=size,
            quantity=quantity,
            coo=coo,
            using_parts=using_parts,
        )
        return [result]

    results = []
    for country in sorted(cost_rate_lookup.keys()):
        result = compute_manufacturing_for_coo(
            gender=gender,
            silhouette=silhouette,
            seam=seam,
            size=size,
            quantity=quantity,
            coo=country,
            using_parts=using_parts,
        )
        results.append(result)

    return results


def get_country_list() -> list[str]:
    manufacturing_data = _load_manufacturing_data()
    return sorted(manufacturing_data.keys())
