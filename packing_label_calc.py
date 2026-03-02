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


def _load_display_packaging_price() -> dict[str, float]:
    path = MASTER_DIR / "label_display_packaging_price.csv"
    out: dict[str, float] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            k = _norm(row.get("display_packaging"))
            v = _to_float(row.get("price"))
            if k and v is not None:
                out[k] = float(v)
    return out


def compute_packing_label(rows: dict[str, Any]) -> dict[str, Any]:
    """Step 5: Packing and Label (Excelish).

    Inputs expected (from Basic Shirts sheet):
    - pack_count (D21)
    - display_packaging (I24)
    - transit_package (I25)
    - label_type (I26)

    Outputs match Basic Shirts cells:
    - K24 (default usage display packaging) = Data link V22 = 1/pack_count
    - O24 total display packaging = IFERROR(Data link X22,"-")
      where X22 = W22*V22 and W22 = XLOOKUP(U22, Label!A:B)

    - K25 default usage transit = IF(ISBLANK(I25),0,1)
    - O25 total transit = IFERROR(Data link X23,"-")
      where X23 = IFERROR(W23/V23,"-") and W23=0.9 and V23=I25

    - K26 default usage label = IF(ISBLANK(I26),0,1)
    - O26 total label = IFERROR(Data link X24,"-")
      where X24=W24*1.03 and W24=IFS(V24=...)

    This function returns per-line objects.
    """

    pack_count = _to_float(rows.get("pack_count"))

    display_packaging = _norm(rows.get("display_packaging"))
    transit_package = _to_float(rows.get("transit_package"))
    label_type = _norm(rows.get("label_type"))

    price_lookup = _load_display_packaging_price()

    # Display Packaging
    # V22 = 1/E30 (pack_count)
    v22 = None
    if pack_count is not None and pack_count != 0:
        v22 = 1.0 / float(pack_count)

    w22 = price_lookup.get(display_packaging) if display_packaging else None
    x22: Any
    if w22 is None or v22 is None:
        x22 = "-"
    else:
        x22 = round(float(w22) * float(v22), 3)

    # Transit Package
    # K25 = IF(ISBLANK(I25),0,1)
    k25 = 0 if transit_package is None else 1
    if transit_package is None or transit_package == 0:
        x23: Any = "-"
    else:
        x23 = round(0.9 / float(transit_package), 3)

    # Label
    # K26 = IF(ISBLANK(I26),0,1)
    k26 = 0 if not label_type else 1
    base_map = {
        "pad print": 0.0085,
        "heat transfer": 0.03,
        "woven label": 0.028,
    }
    w24 = base_map.get(label_type.lower(), 0.0) if label_type else 0.0
    x24: Any
    if not label_type:
        x24 = "-"
    else:
        x24 = round(float(w24) * 1.03, 3)

    return {
        "display_packaging": {
            "details": display_packaging,
            "default_usage": v22 if v22 is not None else "-",
            "total": x22,
        },
        "transit_package": {
            "details": transit_package,
            "default_usage": k25,
            "total": x23,
        },
        "label": {
            "details": label_type,
            "default_usage": k26,
            "total": x24,
        },
        "note": "Step 5 Excelish: Display Packaging + Transit Package + Label.",
    }
