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
        if s == "":
            return None
        try:
            return float(s)
        except Exception:
            return None
    return None


def _load_kv_csv(path: Path, key_col: str, val_col: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            k = (row.get(key_col) or "").strip()
            if not k:
                continue
            out[k] = row.get(val_col)
    return out


def _load_product_part_key_map() -> dict[tuple[str, str], str]:
    """Load silhouette+seam to K7 key mapping."""
    path = MASTER_DIR / "product_part_key_map.csv"
    out: dict[tuple[str, str], str] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            sil = _norm(row.get("silhouette"))
            seam = _norm(row.get("seam"))
            key = _norm(row.get("k7_key"))
            if sil and seam and key:
                out[(sil, seam)] = key
    return out


def _load_fabric_usage_lookup() -> dict[tuple[str, str], float]:
    """Load K7 key + Using Part to usage mapping."""
    path = MASTER_DIR / "fabric_usage_lookup.csv"
    out: dict[tuple[str, str], float] = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            k7_key = _norm(row.get("k7_key"))
            using_part = _norm(row.get("using_part"))
            usage = _to_float(row.get("usage"))
            if k7_key and using_part and usage is not None:
                out[(k7_key, using_part)] = float(usage)
    return out


def compute_fabric_defaults(fabric_type: str, fabric_contents: str) -> dict[str, Any]:
    """Return default price/lb from Fabric Price lookup."""
    fabric_type = _norm(fabric_type)
    fabric_contents = _norm(fabric_contents)
    key = f"{fabric_type}{fabric_contents}" if (fabric_type or fabric_contents) else ""

    lookup_path = MASTER_DIR / "fabric_price_lookup.csv"
    price_lookup = _load_kv_csv(lookup_path, "key", "value") if lookup_path.exists() else {}
    default_price_lb = _to_float(price_lookup.get(key))

    return {
        "key": key,
        "default_price_lb": default_price_lb,
    }


def _conversion_price_yd_kilo(
    *,
    fabric_type: str,
    price_lb: float | None,
    price_unit: str,
    price_value: float | None,
    weight_gsm: float,
    fabric_finishing: str,
    color_design: str,
) -> tuple[float | str, float | str]:
    """Calculate DEFAULT (PRICE/YD) and DEFAULT (PRICE/KILO) per Excel formulas.

    Complete trace of Conversion sheet formulas:
    - Q7 = IFERROR(Conversion!O18, "-")
    - S7 = IFERROR(Conversion!K20, 0)
    - K20 = O18/(J3*1.3946/1000)
    - O18 = IFERROR(M18, "Please select yarn contents")
    - M18 = (M16+V6)*V18
    - M16 = (K16*K13)*0.9144
    - K16 = E23+V6
    - E23 = (C23/0.9144)/C13
    - C23 = IF(ISBLANK(U7), A24, C24)
    - A24 = Data link P7 = effective price
    - C24 = price unit conversion based on U6
    - V6 = V5*T4/1000 (finishing cost)
    - V18 = color factor (Solid=1, white=0.95, Heather=1.1, Others=1.07)
    """

    if price_lb is None and price_value is None:
        return "-", 0.0

    if not fabric_type or weight_gsm == 0:
        return "-", 0.0

    # Constants from Conversion sheet
    B2 = 60.0  # Fixed width in inches
    B3 = weight_gsm  # Default GSM (equals weight_gsm in this context)

    # Width calculations
    J2 = B2
    J3 = weight_gsm
    K3 = J2 * 0.0254
    L3 = J3 / 1000.0
    K13 = L3 * K3

    # Price lookup (A24 = Data link P7)
    A24 = price_lb if price_lb is not None else 0.0

    # Price unit conversion factors
    C3 = B2 * 0.0254
    D3 = B3 / 1000.0
    C13 = D3 * C3
    C11 = C13 * 2.20462262  # Lbs conversion
    C4 = C3 * D3 * 35.274  # Ounces conversion

    # C23 = IF(ISBLANK(U7), A24, C24)
    unit = _norm(price_unit)
    if price_value is not None:
        # User provided a price value - convert based on unit
        if unit == "Price / Yds":
            C24 = price_value
        elif unit == "Price / Kgs":
            C24 = price_value * C13 * 0.9144
        elif unit == "Price / Meters":
            C24 = price_value * 0.9144
        elif unit == "Price / Lbs":
            C24 = price_value * C11 * 0.9144
        elif unit == "Price / Ounces":
            C24 = price_value * C4 * 0.9144
        else:
            C24 = A24
        C23 = C24
    else:
        # No override - use default
        C23 = A24

    # E23 = (C23/0.9144)/C13
    E23 = (C23 / 0.9144) / C13

    # V6 (finishing cost) = V5*T4/1000
    V4 = weight_gsm
    V5 = (V4 * 1.19599) * 1.6667

    # T4 = finishing lookup from Fabric Price AR:AS
    finishing_lookup = {
        "Wicking": 0.06615,
        "Odor Control": 0.11025000000000001,
        "Xtemp": 0.33075,
        "Odor Control + Wicking": 0.1764,
        "Xtemp + Odor Control": 0.44100000000000006,
        "None": 0.0,
        "OTHER": 0.0,
    }
    T4 = finishing_lookup.get(_norm(fabric_finishing), 0.0)

    V6 = V5 * T4 / 1000.0

    # K16 = E23 + V6
    K16 = E23 + V6

    # M16 = (K16*K13)*0.9144
    M16 = (K16 * K13) * 0.9144

    # V18 = color factor
    cd = _norm(color_design)
    if cd == "Solid":
        V18 = 1.0
    elif cd == "white":
        V18 = 0.95
    elif cd == "Heather":
        V18 = 1.1
    elif cd == "Others":
        V18 = 1.07
    else:
        V18 = 0.0

    # M18 = (M16+V6)*V18
    M18 = (M16 + V6) * V18

    # O18 = M18 (price/yd)
    O18 = M18

    # K20 = O18/(J3*1.3946/1000)
    denom = J3 * 1.3946 / 1000.0
    K20 = O18 / denom if denom != 0 else 0.0

    return round(O18, 3), round(K20, 3)


def compute_fabric_row(row: dict[str, Any]) -> dict[str, Any]:
    """Fabrication row calculation (Excel-parity).

    Implements complete Conversion sheet formula chain for Q7/S7.
    """

    fabric_type = _norm(row.get("fabric_type"))
    fabric_contents = _norm(row.get("fabric_contents"))
    using_part = _norm(row.get("using_part"))
    material_coo = _norm(row.get("material_coo"))

    silhouette = _norm(row.get("silhouette"))
    seam = _norm(row.get("seam"))
    gender = _norm(row.get("gender"))
    size = _norm(row.get("size"))

    # Get default price/lb from lookup
    defaults = compute_fabric_defaults(fabric_type, fabric_contents)
    default_price_lb = defaults.get("default_price_lb")

    # Price override
    override_val = _to_float(row.get("price_value"))
    price_lb = override_val if override_val is not None else default_price_lb

    # Fixed fabric width (always 60" when using part selected)
    fixed_width_display = "60\"" if using_part else ""

    # Default weight (GSM) based on fabric type
    default_gsm_map = {
        "Jersey": 160.0,
        "Rib1x1": 180.0,
        "Rib2x1": 180.0,
        "Mesh": 150.0,
        "Fleece": 220.0,
    }
    weight_input = _to_float(row.get("weight_gsm_override"))

    if weight_input is not None:
        default_weight_display = 0  # Show 0 when user fills weight
        effective_gsm = weight_input
    else:
        default_weight_display = default_gsm_map.get(fabric_type, 0)
        effective_gsm = default_weight_display if default_weight_display else 0.0

    # Calculate price/yd and price/kilo using complete Conversion formula chain
    price_unit = _norm(row.get("price_unit") or "Price / Lbs")
    fabric_finishing = _norm(row.get("fabric_finishing") or "")
    color_design = _norm(row.get("color_design") or "Solid")

    price_yd, price_kilo = _conversion_price_yd_kilo(
        fabric_type=fabric_type,
        price_lb=default_price_lb,
        price_unit=price_unit,
        price_value=override_val,
        weight_gsm=effective_gsm,
        fabric_finishing=fabric_finishing,
        color_design=color_design,
    )

    # K7 key lookup (silhouette + seam)
    k7_map = _load_product_part_key_map()
    k7_key = k7_map.get((silhouette, seam), "-")

    # R7 usage lookup (K7 key + Using Part)
    usage_lookup = _load_fabric_usage_lookup()
    if not fabric_contents:
        usage_val = 0.0
    else:
        if not k7_key or k7_key == "-" or not using_part:
            usage_val = "X"
        else:
            usage_val = usage_lookup.get((k7_key, using_part), "X")

    # Gender multiplier (U7)
    if gender.upper() == "MEN":
        gender_mult = 1.0
    elif gender.upper() == "WOMEN":
        gender_mult = 0.85
    elif gender.upper() == "KIDS":
        gender_mult = 0.75
    else:
        gender_mult = 0.0

    # Size multiplier (V7)
    if size.upper() == "S-XL":
        size_mult = 1.0
    elif size.upper() == "2XL-3XL":
        size_mult = 1.15
    elif size.upper() == "S-3XL":
        size_mult = 1.1
    else:
        size_mult = 0.0

    # Silhouette multiplier (B26) - simplified, can add full lookup if needed
    silhouette_mult = 1.0  # Default for T-Shirt (Crew Neck)

    # Import factor (T7)
    if material_coo == "Domestic":
        import_factor = 1.0
    elif material_coo == "Import":
        import_factor = 1.05
    else:
        import_factor = 0.0

    # Calculate Total Cost (Y7 chain)
    if isinstance(usage_val, (int, float)) and isinstance(price_yd, (int, float)):
        # U7 = R7 * gender_mult
        U7 = float(usage_val) * gender_mult
        # V7 = U7 * size_mult
        V7 = U7 * size_mult
        # W7 = V7 * silhouette_mult
        W7 = V7 * silhouette_mult
        # X7 = W7 * price_yd
        X7 = W7 * float(price_yd)
        # Y7 = X7 * import_factor
        Y7 = X7 * import_factor
        total_cost = round(Y7, 3)
    else:
        total_cost = 0.0

    return {
        "fabric_type": fabric_type,
        "fabric_contents": fabric_contents,
        "using_part": using_part,
        "material_coo": material_coo,
        "key": defaults.get("key"),
        "fixed_fabric_width": fixed_width_display,
        "default_weight_gsm": default_weight_display,
        "weight_gsm": effective_gsm,
        "default_price_lb": default_price_lb,
        "price_lb": price_lb,
        "default_price_yd": price_yd,
        "default_price_kilo": price_kilo,
        "usage": usage_val,
        "total_cost": total_cost,
        "note": "Step 2 Excel-parity: Complete Conversion sheet formula chain for Q7/S7.",
    }
