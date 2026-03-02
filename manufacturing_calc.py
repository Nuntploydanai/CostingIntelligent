"""
Step 6: Manufacturing Cost Calculator
Implements Excel-parity manufacturing cost calculation
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
MASTER_DIR = BASE_DIR / "master_clean"


def _norm(s: Any) -> str:
    return ("" if s is None else str(s)).strip()


def _to_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip()
        if s == "" or s == "-":
            return None
        try:
            return float(s)
        except Exception:
            return None
    return None


def _load_sam_minutes_lookup() -> dict[tuple[str, str, str, str], float]:
    """Load SAM (minutes) lookup table."""
    path = MASTER_DIR / "sam_minutes_lookup.csv"
    out: dict[tuple[str, str, str, str], float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            gender = _norm(row.get("gender"))
            product = _norm(row.get("product"))
            seam = _norm(row.get("seam"))
            size = _norm(row.get("size"))
            sam = _to_float(row.get("sam_minutes"))

            if gender and product and seam and size and sam is not None:
                out[(gender, product, seam, size)] = float(sam)

    return out


def _load_cost_rate_data() -> dict[str, float]:
    """Load cost rate data by country."""
    path = MASTER_DIR / "cost_rate.csv"
    out: dict[str, float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            country = _norm(row.get("country"))
            cost_rate = _to_float(row.get("cost_rate"))

            if country and cost_rate is not None:
                out[country] = float(cost_rate)

    return out


def _load_efficiency_data() -> dict[str, float]:
    """Load efficiency data by quantity range."""
    path = MASTER_DIR / "efficiency_by_quantity.csv"
    out: dict[str, float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            quantity = _norm(row.get("quantity_range"))
            efficiency = _to_float(row.get("efficiency"))

            if quantity and efficiency is not None:
                out[quantity] = float(efficiency)

    return out


def _load_manufacturing_data() -> dict[str, dict[str, float]]:
    """Load manufacturing cost data by country."""
    path = MASTER_DIR / "manufacturing_cost_by_country.csv"
    out: dict[str, dict[str, float]] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
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


def compute_manufacturing_for_coo(
    gender: str = "",
    silhouette: str = "",
    seam: str = "",
    size: str = "",
    quantity: str = "",
    coo: str = "",
) -> dict[str, Any]:
    """Calculate manufacturing cost for a specific COO (Country of Origin).

    Returns a single dict with:
    - minutes (W18)
    - cost_rate (W19)
    - efficiency (W20)
    - total_cost (W21)
    """

    sam_lookup = _load_sam_minutes_lookup()
    cost_rate_lookup = _load_cost_rate_data()
    efficiency_lookup = _load_efficiency_data()

    # Normalize inputs
    gender = _norm(gender)
    silhouette = _norm(silhouette)
    seam = _norm(seam)
    size = _norm(size)
    quantity = _norm(quantity)
    coo = _norm(coo)

    # Try lookup with exact match first
    key = (gender, silhouette, seam, size)
    base_minutes = sam_lookup.get(key, 0.0)

    # If not found, try case-insensitive match
    if base_minutes == 0.0 and silhouette:
        for (g, p, s, sz), minutes in sam_lookup.items():
            if (g == gender and
                s == seam and
                sz == size and
                p.lower() == silhouette.lower()):
                base_minutes = minutes
                break

    # Get efficiency based on quantity
    efficiency = efficiency_lookup.get(quantity, 0.738)  # Default to 0.738 if not found

    # Get cost rate for COO
    cost_rate = cost_rate_lookup.get(coo, 0.0)

    # Calculate total cost: (minutes / efficiency) * cost_rate
    if efficiency > 0 and base_minutes > 0:
        total_cost = (base_minutes / efficiency) * cost_rate
    else:
        total_cost = 0.0

    return {
        "country": coo,
        "minutes": round(base_minutes, 3),
        "cost_rate": round(cost_rate, 6),
        "efficiency": round(efficiency, 3),
        "total_cost": round(total_cost, 6),
    }


def compute_all_manufacturing_rows(
    gender: str = "",
    silhouette: str = "",
    seam: str = "",
    size: str = "",
    quantity: str = "",
    coo: str = "",
) -> list[dict[str, Any]]:
    """Calculate manufacturing cost for ALL countries (for backward compatibility).

    Returns a list with one dict per country, matching Excel rows 30-35.
    Primarily used to return the selected COO's data.
    """

    # For the webapp, we only return the selected COO's data
    result = compute_manufacturing_for_coo(gender, silhouette, seam, size, quantity, coo)

    # Return as a list for backward compatibility
    return [result]



def get_country_list() -> list[str]:
    """Return list of available countries for dropdown."""
    manufacturing_data = _load_manufacturing_data()
    return sorted(manufacturing_data.keys())
