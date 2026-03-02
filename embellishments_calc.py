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
        # Handle "X13" → 13.0 (usage_unit dropdown format)
        if s.upper().startswith("X") and len(s) > 1:
            try:
                return float(s[1:])
            except Exception:
                return None
        try:
            return float(s)
        except Exception:
            return None
    return None


def _load_price_lookup() -> dict[tuple[str, str], float]:
    path = MASTER_DIR / "print_embroidery_price_lookup.csv"
    out: dict[tuple[str, str], float] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            pt = _norm(row.get("printing_embroidery"))
            dim = _norm(row.get("dimension"))
            price = _to_float(row.get("default_price_each"))
            if pt and dim and price is not None:
                out[(pt, dim)] = float(price)
    return out


def compute_embellishment_row(row: dict[str, Any]) -> dict[str, Any]:
    """Step 4: Embellishments (Printing/Embroidery) row calc.

    Excel mapping (from your screenshots):
    - H22 = Basic Shirts G19 (printing/embroidery)
    - J22 = Basic Shirts I19 (dimension)
    - Data link N22 = IF(OR(ISBLANK(H22),ISBLANK(J22)),"-", IFERROR(XLOOKUP(H22&J22, A&A&B:B, G:G),"Select Print Type & Dimension"))
    - Basic Shirts M19 = Data link N22 (default price/each)
    - Total (O19) = IFERROR(M19*K19,"-") where K19 is Usage/Unit input

    We implement: total = default_price_each * usage_unit when both numeric.
    """

    pt = _norm(row.get("printing_embroidery"))
    dim = _norm(row.get("dimension"))
    usage = _to_float(row.get("usage_unit"))

    lookup = _load_price_lookup()

    # default price/each (Data link N22)
    if not pt or not dim:
        default_price: Any = "-"
    else:
        default_price = lookup.get((pt, dim))
        if default_price is None:
            default_price = "Select Print Type & Dimension"

    # total (Basic Shirts O19)
    total: Any
    if isinstance(default_price, (int, float)) and usage is not None:
        total = round(float(default_price) * float(usage), 3)
    else:
        total = "-"

    return {
        "printing_embroidery": pt,
        "dimension": dim,
        "usage_unit": usage,
        "default_price_each": default_price,
        "total_cost": total,
        "note": "Step 4 Excelish: default price from Print_ and_Embroidery lookup; total=price*usage.",
    }
