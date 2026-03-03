from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from fabrication_calc import compute_fabric_row, compute_fabric_defaults
from trims_calc import compute_trim_row
from embellishments_calc import compute_embellishment_row
from packing_label_calc import compute_packing_label
from manufacturing_calc import compute_all_manufacturing_rows
from total_cost_calc import compute_total_cost_summary
from country_comparison_calc import compute_fob_by_country

BASE_DIR = Path(__file__).resolve().parent
MASTER_DIR = BASE_DIR / "master_clean"
WEB_DIR = BASE_DIR / "web"

app = FastAPI(title="Basic Shirts Costing Demo", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculateRequest(BaseModel):
    development: dict[str, Any] = {}
    fabrication: list[dict[str, Any]] = []
    trims: list[dict[str, Any]] = []
    embellishments: list[dict[str, Any]] = []
    packing_label: dict[str, Any] = {}
    supplier_margin_percent: float = 7.0  # Default to 7% (Excel default)
    freight_cost: float = 0.0
    gmo_cost: float = 0.0
    duty_cost: float = 0.0
    additional_cost: float = 0.0


def read_dropdown(name: str) -> list[str]:
    path = MASTER_DIR / f"dropdown_{name}.csv"
    if not path.exists():
        raise HTTPException(404, f"dropdown not found: {name}")
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        if "value" not in r.fieldnames:
            raise HTTPException(500, f"invalid dropdown schema: {path.name}")
        out = []
        for row in r:
            v = (row.get("value") or "").strip()
            if v:
                out.append(v)
        return out


@app.get("/")
def root():
    # serve the demo UI
    index = WEB_DIR / "index.html"
    if not index.exists():
        return {"ok": True, "msg": "UI not found. Create basicshirts_web/web/index.html"}
    return FileResponse(index)


@app.get("/api/dropdowns")
def list_dropdowns():
    if not MASTER_DIR.exists():
        return []
    out = []
    for p in sorted(MASTER_DIR.glob("dropdown_*.csv")):
        out.append(p.stem.replace("dropdown_", ""))
    return out


@app.get("/api/dropdown/{name}")
def get_dropdown(name: str):
    return {"name": name, "values": read_dropdown(name)}


@app.get("/api/fabric/defaults")
def fabric_defaults(fabric_type: str = "", fabric_contents: str = ""):
    return compute_fabric_defaults(fabric_type, fabric_contents)


@app.get("/api/embellishment/dimensions")
def embellishment_dimensions(printing_embroidery: str = ""):
    """Return valid Dimension options for a given Printing/Embroidery type.

    Excel behavior: Dimension list depends on selected Printing/Embroidery.
    We derive this from master_clean/print_embroidery_price_lookup.csv keys.
    """

    import csv

    pe = (printing_embroidery or "").strip()
    path = MASTER_DIR / "print_embroidery_price_lookup.csv"
    if not path.exists():
        return {"printing_embroidery": pe, "values": []}

    dims: list[str] = []
    seen = set()
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            pt = (row.get("printing_embroidery") or "").strip()
            dim = (row.get("dimension") or "").strip()
            if not dim:
                continue
            if pe and pt != pe:
                continue
            if dim in seen:
                continue
            seen.add(dim)
            dims.append(dim)

    return {"printing_embroidery": pe, "values": dims}


@app.post("/api/calculate")
def calculate(req: CalculateRequest):
    """Demo calculation endpoint.

    For now this endpoint:
    - validates values against dropdown master lists where possible
    - echoes the normalized payload back
    - returns placeholder calculated outputs

    Next steps: implement real fabrication cost + total cost summary.
    """

    # validate some common development fields
    dropdown_map = {
        "gender": "gender",
        "silhouette": "silhouette_pattern",
        "size": "size",
        "coo": "coo",
        "fabric_finishing": "fabric_finishing",
        "ideal_quantity": "quantity",
        "pack_count": "packing_no",
        "color_design": "color",
        "seam": "seam",
    }

    normalized_dev = {}
    for k, v in req.development.items():
        if isinstance(v, str):
            v = v.strip()
        normalized_dev[k] = v

        if k in dropdown_map and v:
            dd = dropdown_map[k]
            options = set(read_dropdown(dd))
            if v not in options:
                raise HTTPException(400, f"Invalid value for {k}: {v!r}. Not in dropdown_{dd}.csv")

    # validate fabrication rows
    fab_rows = []
    for i, row in enumerate(req.fabrication):
        r = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        # Back-compat: older UI used price_override
        if "price_override" in r and "price_value" not in r:
            r["price_value"] = r.get("price_override")
        if "price_unit" not in r:
            r["price_unit"] = "Price / Lbs"
        # basic dropdown checks
        # Fabrication dropdown columns in the source workbook are inconsistent to auto-map reliably
        # (e.g., "Jersey" is a Fabric Type but isn't present in our extracted DropDown sheet columns).
        # Validate against the correct master dropdown sources (aligned to Excel intent)
        for field, ddname in [
            ("fabric_type", "fabric_type"),
            ("fabric_contents", "fabric_contents"),
            ("using_part", "using_part"),
            ("material_coo", "material_coo"),
        ]:
            val = r.get(field)
            if isinstance(val, str) and val:
                options = set(read_dropdown(ddname))
                if val not in options:
                    raise HTTPException(400, f"Row {i+1}: invalid {field}={val!r} (not in dropdown_{ddname}.csv)")
        fab_rows.append(r)

    # Fabrication calc (row-level) — merge required Step 1 context (Excel Data link E25/E26/E27/E29)
    ctx = {
        "gender": normalized_dev.get("gender"),
        "silhouette": normalized_dev.get("silhouette"),
        "seam": normalized_dev.get("seam"),
        "size": normalized_dev.get("size"),
        "fabric_finishing": normalized_dev.get("fabric_finishing"),
        "color_design": normalized_dev.get("color_design"),
    }
    fab_calc = [compute_fabric_row({**r, **ctx}) for r in fab_rows]

    total_fabric_cost = None
    try:
        vals = [x.get("total_cost") for x in fab_calc if isinstance(x.get("total_cost"), (int, float))]
        total_fabric_cost = round(sum(vals), 3) if vals else None
    except Exception:
        total_fabric_cost = None

    # Step 3: Trims rows
    trim_rows = []
    for i, row in enumerate(req.trims):
        r = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        for field, ddname in [
            ("trims_type", "trims_type"),
            ("garment_part", "garment_part_trim"),
            ("material_coo", "material_coo"),
        ]:
            val = r.get(field)
            if isinstance(val, str) and val:
                options = set(read_dropdown(ddname))
                if val not in options:
                    raise HTTPException(400, f"Trim row {i+1}: invalid {field}={val!r} (not in dropdown_{ddname}.csv)")
        trim_rows.append(r)

    trim_ctx = {
        "gender": normalized_dev.get("gender"),
        "size": normalized_dev.get("size"),
    }
    trim_calc = [compute_trim_row({**r, **trim_ctx}) for r in trim_rows]

    # Step 4: Embellishments
    emb_rows = []
    for i, row in enumerate(req.embellishments):
        r = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        for field, ddname in [
            ("printing_embroidery", "printing_embroidery"),
            ("dimension", "print_dimension"),
        ]:
            val = r.get(field)
            if isinstance(val, str) and val:
                options = set(read_dropdown(ddname))
                if val not in options:
                    raise HTTPException(400, f"Embellishment row {i+1}: invalid {field}={val!r} (not in dropdown_{ddname}.csv)")
        emb_rows.append(r)

    emb_calc = [compute_embellishment_row(r) for r in emb_rows]

    # Step 5: Packing and Label (uses pack_count + 3 detail fields)
    step5 = compute_packing_label({
        "pack_count": normalized_dev.get("pack_count"),
        "display_packaging": (req.packing_label or {}).get("display_packaging"),
        "transit_package": (req.packing_label or {}).get("transit_package"),
        "label_type": (req.packing_label or {}).get("label_type"),
    })

    # Step 6: Manufacturing Cost (based on COO selected in Step 1)
    manufacturing_rows = compute_all_manufacturing_rows(
        gender=normalized_dev.get("gender", ""),
        silhouette=normalized_dev.get("silhouette", ""),
        seam=normalized_dev.get("seam", ""),
        size=normalized_dev.get("size", ""),
        quantity=normalized_dev.get("ideal_quantity", ""),
        coo=normalized_dev.get("coo", ""),
    )

    # Calculate totals from each step
    fabric_cost = sum([r.get("total_cost", 0) or 0 for r in fab_calc])

    # Trims cost: EXCLUDE sewing thread (it's calculated separately in total_cost_summary)
    trim_cost = sum([
        r.get("total_cost", 0) or 0
        for r in trim_calc
        if not (r.get("trims_type") or "").lower().strip().startswith("sewing thread")
    ])

    print_embroidery_cost = sum([r.get("total_cost", 0) or 0 for r in emb_calc])

    packing = step5 or {}
    display_packaging_cost = packing.get("display_packaging", {}).get("total", 0) or 0
    transit_packaging_cost = packing.get("transit_package", {}).get("total", 0) or 0
    label_cost = packing.get("label", {}).get("total", 0) or 0

    # Get manufacturing (labour) cost for selected COO
    coo = normalized_dev.get("coo", "INDIA")
    mfg_row = next((r for r in manufacturing_rows if r.get("country") == coo), manufacturing_rows[0] if manufacturing_rows else {})
    labour_cost = mfg_row.get("total_cost", 0) or 0

    # Calculate total cost summary
    total_summary = compute_total_cost_summary(
        fabric_cost=fabric_cost,
        trim_cost=trim_cost,
        print_embroidery_cost=print_embroidery_cost,
        display_packaging_cost=display_packaging_cost,
        transit_packaging_cost=transit_packaging_cost,
        label_cost=label_cost,
        labour_cost=labour_cost,
        gender=normalized_dev.get("gender", ""),
        silhouette=normalized_dev.get("silhouette", ""),
        size=normalized_dev.get("size", ""),
        supplier_margin_percent=req.supplier_margin_percent,
        product_testing_cost=0.01,
        other_cost=req.additional_cost,  # Use user input
        freight_cost=req.freight_cost,
        gmo_cost=req.gmo_cost,
        duty_cost=req.duty_cost,
    )

    # Calculate FOB cost for all countries (comparison table)
    country_comparison = compute_fob_by_country(
        fabric_cost=fabric_cost,
        trim_cost=trim_cost,
        print_embroidery_cost=print_embroidery_cost,
        display_packaging_cost=display_packaging_cost,
        transit_packaging_cost=transit_packaging_cost,
        label_cost=label_cost,
        gender=normalized_dev.get("gender", ""),
        silhouette=normalized_dev.get("silhouette", ""),
        seam=normalized_dev.get("seam", ""),
        size=normalized_dev.get("size", ""),
        quantity=normalized_dev.get("ideal_quantity", ""),
        supplier_margin_percent=req.supplier_margin_percent,
        product_testing_cost=0.01,
        other_cost=0.0,
        freight_cost=0.0,
        gmo_cost=0.0,
        duty_cost=0.0,
    )

    outputs = {
        "fabrication": {
            "rows": fab_calc,
            "total_fabric_cost": total_fabric_cost,
        },
        "trims": {
            "rows": trim_calc,
        },
        "embellishments": {
            "rows": emb_calc,
        },
        "packing_label": step5,
        "manufacturing": {
            "rows": manufacturing_rows,
        },
        "total_cost_summary": total_summary,
        "country_comparison": country_comparison,
        "note": "Step 1–6: Fabrication + Trims + Embellishments + Packing&Label + Manufacturing (Excelish).",
    }

    return {
        "inputs": {"development": normalized_dev, "fabrication": fab_rows},
        "outputs": outputs,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
