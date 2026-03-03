"""
Calculate FOB cost for all countries
"""
from __future__ import annotations

from typing import Any

from total_cost_calc import compute_total_cost_summary
from manufacturing_calc import compute_all_manufacturing_rows


# Fixed list of countries to show in comparison (matching Excel)
COMPARISON_COUNTRIES = [
    "INDIA",
    "BANGLADESH",
    "INDONESIA",
    "THAILAND",
    "CAMBODIA",
    "VIETNAM",
]


def compute_fob_by_country(
    # All costs except labour (same for all countries)
    fabric_cost: float = 0.0,
    trim_cost: float = 0.0,
    print_embroidery_cost: float = 0.0,
    display_packaging_cost: float = 0.0,
    transit_packaging_cost: float = 0.0,
    label_cost: float = 0.0,
    # Step 1 inputs
    gender: str = "",
    silhouette: str = "",
    seam: str = "",
    size: str = "",
    quantity: str = "",
    # User input
    supplier_margin_percent: float = 7.0,
    # Additional costs
    product_testing_cost: float = 0.01,
    other_cost: float = 0.0,
    freight_cost: float = 0.0,
    gmo_cost: float = 0.0,
    duty_cost: float = 0.0,
) -> list[dict[str, Any]]:
    """
    Calculate FOB cost for each country.

    Returns list of dicts with:
    - country
    - labour_cost
    - subtotal
    - margin_amount
    - fob_cost
    """

    # Get manufacturing costs for all countries
    mfg_rows = compute_all_manufacturing_rows(
        gender=gender,
        silhouette=silhouette,
        seam=seam,
        size=size,
        quantity=quantity,
        coo="",  # Empty = all countries
    )

    results = []

    # Filter to only show the 6 comparison countries
    for mfg_row in mfg_rows:
        country = mfg_row.get("country", "")

        # Skip countries not in our comparison list
        if country not in COMPARISON_COUNTRIES:
            continue

        labour_cost = mfg_row.get("total_cost", 0) or 0

        # Calculate total cost summary for this country
        summary = compute_total_cost_summary(
            fabric_cost=fabric_cost,
            trim_cost=trim_cost,
            print_embroidery_cost=print_embroidery_cost,
            display_packaging_cost=display_packaging_cost,
            transit_packaging_cost=transit_packaging_cost,
            label_cost=label_cost,
            labour_cost=labour_cost,  # Country-specific
            gender=gender,
            silhouette=silhouette,
            size=size,
            supplier_margin_percent=supplier_margin_percent,
            product_testing_cost=product_testing_cost,
            other_cost=other_cost,
            freight_cost=freight_cost,
            gmo_cost=gmo_cost,
            duty_cost=duty_cost,
        )

        results.append({
            "country": country,
            "labour_cost": summary["total_labour_cost"],
            "subtotal": summary["subtotal"],
            "margin_amount": summary["supplier_margin_amount"],
            "fob_cost": summary["fob_cost"],
        })

    return results
