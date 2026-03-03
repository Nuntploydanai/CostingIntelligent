"""
Total Cost Calculator - Implements Excel formulas exactly
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


def _load_sewing_thread_cost() -> dict[tuple[str, str], float]:
    """Load sewing thread cost lookup table."""
    path = MASTER_DIR / "sewing_thread_cost.csv"
    out: dict[tuple[str, str], float] = {}

    if not path.exists():
        return out

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            gender = _norm(row.get("gender"))
            silhouette = _norm(row.get("silhouette"))
            cost = _to_float(row.get("sewing_thread_cost"))

            if gender and silhouette and cost is not None:
                out[(gender, silhouette)] = float(cost)

    return out


def compute_total_cost_summary(
    # From Step 2
    fabric_cost: float = 0.0,
    # From Step 3
    trim_cost: float = 0.0,
    # From Step 4
    print_embroidery_cost: float = 0.0,
    # From Step 5
    display_packaging_cost: float = 0.0,
    transit_packaging_cost: float = 0.0,
    label_cost: float = 0.0,
    # From Step 6
    labour_cost: float = 0.0,
    # Step 1 inputs
    gender: str = "",
    silhouette: str = "",
    size: str = "",
    # User input
    supplier_margin_percent: float = 10.0,
    # Additional costs
    product_testing_cost: float = 0.01,  # Default from Excel
    other_cost: float = 0.0,
    freight_cost: float = 0.0,
    gmo_cost: float = 0.0,
    duty_cost: float = 0.0,
) -> dict[str, Any]:
    """Calculate complete total cost summary matching Excel formulas."""

    # Normalize inputs
    gender = _norm(gender)
    silhouette = _norm(silhouette)
    size = _norm(size)

    # 1. Total Fabric Cost (from fabrication)
    total_fabric_cost = _to_float(fabric_cost) or 0.0

    # 2. Total Trim Cost (from trims, excluding sewing thread)
    total_trim_cost = _to_float(trim_cost) or 0.0

    # 3. Total Display Packaging Cost (from packing)
    total_display_packaging_cost = _to_float(display_packaging_cost) or 0.0

    # 4. Total Transit Packaging Cost (from packing)
    total_transit_packaging_cost = _to_float(transit_packaging_cost) or 0.0

    # 5. Total Label Cost (from packing)
    total_label_cost = _to_float(label_cost) or 0.0

    # 6. Total Sewing Thread Cost (lookup by silhouette)
    sewing_thread_lookup = _load_sewing_thread_cost()
    total_sewing_thread_cost = sewing_thread_lookup.get((gender, silhouette), 0.0)

    # 7. Total Labour Cost (from manufacturing)
    total_labour_cost = _to_float(labour_cost) or 0.0

    # 8. Total Product Testing Cost (fixed $0.01 per piece)
    total_product_testing_cost = _to_float(product_testing_cost) or 0.0

    # 9. Total Print/Embroidery Cost (from embellishments)
    total_print_embroidery_cost = _to_float(print_embroidery_cost) or 0.0

    # 10. Total Other Cost (user input)
    total_other_cost = _to_float(other_cost) or 0.0

    # Calculate subtotal (items 1-10)
    subtotal = (
        total_fabric_cost +
        total_trim_cost +
        total_display_packaging_cost +
        total_transit_packaging_cost +
        total_label_cost +
        total_sewing_thread_cost +
        total_labour_cost +
        total_product_testing_cost +
        total_print_embroidery_cost +
        total_other_cost
    )

    # 11. Calculate Supplier Margin Amount
    margin_decimal = supplier_margin_percent / 100.0
    supplier_margin_amount = subtotal * margin_decimal

    # 12. Calculate FOB Cost (subtotal + margin)
    fob_cost = subtotal + supplier_margin_amount

    # 13-15. Additional costs
    total_freight_cost = _to_float(freight_cost) or 0.0
    total_gmo_cost = _to_float(gmo_cost) or 0.0
    total_duty_cost = _to_float(duty_cost) or 0.0

    # Calculate Grand Total (FOB + Freight + GMO + Duty)
    grand_total = fob_cost + total_freight_cost + total_gmo_cost + total_duty_cost

    # Calculate additional summary items
    total_fob_per_piece = fob_cost
    total_fob_per_dozen = fob_cost * 12
    total_flc_per_piece = grand_total  # FLC = FOB + Freight + GMO + Duty
    total_flc_per_dozen = grand_total * 12

    # Calculate % proportions (relative to subtotal, like Excel AB column)
    def calc_percent(value, total):
        if not total or total == 0:
            return 0.0
        return (value / total) * 100

    return {
        # Cost values
        "total_fabric_cost": round(total_fabric_cost, 6),
        "total_trim_cost": round(total_trim_cost, 6),
        "total_display_packaging_cost": round(total_display_packaging_cost, 6),
        "total_transit_packaging_cost": round(total_transit_packaging_cost, 6),
        "total_label_cost": round(total_label_cost, 6),
        "total_sewing_thread_cost": round(total_sewing_thread_cost, 6),
        "total_labour_cost": round(total_labour_cost, 6),
        "total_product_testing_cost": round(total_product_testing_cost, 6),
        "total_print_embroidery_cost": round(total_print_embroidery_cost, 6),
        "total_other_cost": round(total_other_cost, 6),
        "subtotal": round(subtotal, 6),
        "supplier_margin_percent": supplier_margin_percent,
        "supplier_margin_amount": round(supplier_margin_amount, 6),
        "fob_cost": round(fob_cost, 6),
        "freight_cost": round(total_freight_cost, 6),
        "gmo_cost": round(total_gmo_cost, 6),
        "duty_cost": round(total_duty_cost, 6),
        "grand_total": round(grand_total, 6),
        "total_fob_per_piece": round(total_fob_per_piece, 6),
        "total_fob_per_dozen": round(total_fob_per_dozen, 6),
        "total_flc_per_piece": round(total_flc_per_piece, 6),
        "total_flc_per_dozen": round(total_flc_per_dozen, 6),

        # Percentage proportions (relative to subtotal)
        "total_fabric_cost_pct": round(calc_percent(total_fabric_cost, subtotal), 2),
        "total_trim_cost_pct": round(calc_percent(total_trim_cost, subtotal), 2),
        "total_display_packaging_cost_pct": round(calc_percent(total_display_packaging_cost, subtotal), 2),
        "total_transit_packaging_cost_pct": round(calc_percent(total_transit_packaging_cost, subtotal), 2),
        "total_label_cost_pct": round(calc_percent(total_label_cost, subtotal), 2),
        "total_sewing_thread_cost_pct": round(calc_percent(total_sewing_thread_cost, subtotal), 2),
        "total_labour_cost_pct": round(calc_percent(total_labour_cost, subtotal), 2),
        "total_product_testing_cost_pct": round(calc_percent(total_product_testing_cost, subtotal), 2),
        "total_print_embroidery_cost_pct": round(calc_percent(total_print_embroidery_cost, subtotal), 2),
        "total_other_cost_pct": round(calc_percent(total_other_cost, subtotal), 2),
        "supplier_margin_amount_pct": round(calc_percent(supplier_margin_amount, subtotal), 2),
    }
