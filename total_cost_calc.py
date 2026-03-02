"""
Total Cost Summary Calculator
Aggregates costs from all steps
"""
from __future__ import annotations

from typing import Any


def compute_total_cost_summary(
    fabric_total: float = 0.0,
    trims_total: float = 0.0,
    display_packaging_total: float = 0.0,
    transit_packaging_total: float = 0.0,
    label_total: float = 0.0,
    sewing_thread_cost: float = 0.0,
    manufacturing_total: float = 0.0,
    product_testing_cost: float = 0.0,
    embellishment_total: float = 0.0,
) -> dict[str, Any]:
    """Calculate total cost summary.

    Excel formulas:
    - AC6 (Total Fabric Cost) = Y7 + Y8 + Y9
    - AC7 (Total Trim Cost) = Y13 + Y14 + Y15
    - AC8 (Total Display Packaging Cost) = O24
    - AC9 (Total Transit Packaging Cost) = O25
    - AC10 (Total Label cost) = O26
    - AC11 (Total Sewing Thread cost) = Data link X26
    - AC12 (Total Labour) = Y21
    - AC13 (Total Product Testing Cost) = Data link X25
    - AC14 (Total print/embroidery cost) = O19 + O20
    """

    # Calculate grand total
    grand_total = (
        fabric_total
        + trims_total
        + display_packaging_total
        + transit_packaging_total
        + label_total
        + sewing_thread_cost
        + manufacturing_total
        + product_testing_cost
        + embellishment_total
    )

    return {
        "total_fabric_cost": round(fabric_total, 3),
        "total_trims_cost": round(trims_total, 3),
        "total_display_packaging_cost": round(display_packaging_total, 3),
        "total_transit_packaging_cost": round(transit_packaging_total, 3),
        "total_label_cost": round(label_total, 3),
        "total_sewing_thread_cost": round(sewing_thread_cost, 3),
        "total_manufacturing_cost": round(manufacturing_total, 3),
        "total_product_testing_cost": round(product_testing_cost, 3),
        "total_embellishment_cost": round(embellishment_total, 3),
        "grand_total": round(grand_total, 3),
        "note": "Total Cost Summary - aggregates all steps",
    }
