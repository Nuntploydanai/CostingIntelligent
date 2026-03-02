from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from basicshirts_web.app.excelish import eval_formula, ExcelEvalError

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "master"
OUT = ROOT / "master_clean"


def _read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return [row for row in csv.reader(f)]


def _write_csv(path: Path, rows: list[list[Any]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)


def _coerce_number(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, ExcelEvalError):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip()
        if s == "":
            return None
        # strip trailing text like " lb"
        m = re.match(r"^(-?\d+(?:\.\d+)?)", s)
        if m:
            try:
                return float(m.group(1))
            except Exception:
                return None
        return None
    return None


def _excel_resolver(cell_map: dict[str, Any]):
    def resolve(name: str) -> Any:
        u = name.upper()
        if u == "TRUE":
            return True
        if u == "FALSE":
            return False
        if name in cell_map:
            return cell_map[name]
        return 0

    return resolve


def eval_table_grid(grid: list[list[str]], origin_row: int = 1, origin_col: int = 1) -> dict[str, Any]:
    """Evaluate a rectangular CSV grid as if it started at A1.

    Returns cell_map like {'A1': 'Header', 'B2': 123.0, ...}.

    Supports basic formulas via excelish; also supports CONCATENATE.
    """

    # Fill raw values
    cell_map: dict[str, Any] = {}

    def col_letter(c: int) -> str:
        s = ""
        while c:
            c, r = divmod(c - 1, 26)
            s = chr(65 + r) + s
        return s

    for r_i, row in enumerate(grid, start=origin_row):
        for c_i, val in enumerate(row, start=origin_col):
            addr = f"{col_letter(c_i)}{r_i}"
            cell_map[addr] = val

    # Iteratively evaluate formulas
    def try_eval_formula(expr: str) -> Any:
        if not isinstance(expr, str):
            return expr
        s = expr.strip()
        if not s.startswith("="):
            return expr
        inner = s[1:]
        # Excel percent literals like 150% or 100%- 13%
        inner = re.sub(r"(\d+(?:\.\d+)?)%", lambda m: str(float(m.group(1)) / 100.0), inner)

        # very small support for CONCATENATE (common in master extracts)
        if inner.upper().startswith("CONCATENATE"):
            # CONCATENATE(A2," ",B2)
            m = re.match(r"(?i)CONCATENATE\((.*)\)\s*$", inner)
            if not m:
                return ExcelEvalError("bad-concatenate")
            args_str = m.group(1)
            # split by commas not inside quotes
            args = []
            cur = ""
            inq = False
            for ch in args_str:
                if ch == '"':
                    inq = not inq
                    cur += ch
                elif ch == "," and not inq:
                    args.append(cur)
                    cur = ""
                else:
                    cur += ch
            if cur:
                args.append(cur)
            parts: list[str] = []
            for a in args:
                a = a.strip()
                if a.startswith('"') and a.endswith('"'):
                    parts.append(a[1:-1].replace('""', '"'))
                else:
                    v = cell_map.get(a, "")
                    if isinstance(v, ExcelEvalError):
                        v = ""
                    parts.append(str(v))
            return "".join(parts)

        return eval_formula(inner, _excel_resolver(cell_map))

    # Evaluate until stable
    for _ in range(50):
        changed = 0
        for k, v in list(cell_map.items()):
            if isinstance(v, str) and v.strip().startswith("="):
                newv = try_eval_formula(v)
                if newv != v:
                    cell_map[k] = newv
                    changed += 1
        if changed == 0:
            break

    # Coerce numbers where possible
    for k, v in list(cell_map.items()):
        if isinstance(v, str) and not v.strip().startswith("="):
            num = _coerce_number(v)
            if num is not None and v.strip() not in ("",):
                cell_map[k] = num
    return cell_map


def build_cost_rate():
    grid = _read_csv(MASTER / "cost_rate__cost_rate_1_1__r1c1.csv")
    cell_map = eval_table_grid(grid)

    # header row is row 1, data starts row 2; columns:
    # A: COUNTRY, ... O: Cost Rate/SAM
    out_rows = [["country", "local_area", "exchange_rate_to_usd", "cost_rate_sam_usd"]]

    # find last row by scanning A column
    for r in range(2, 200):
        country = cell_map.get(f"A{r}")
        if country in (None, ""):
            break
        local_area = cell_map.get(f"B{r}")
        exch = _coerce_number(cell_map.get(f"M{r}"))
        cost_rate_sam = _coerce_number(cell_map.get(f"O{r}"))
        out_rows.append([country, local_area, exch, cost_rate_sam])

    _write_csv(OUT / "cost_rate.csv", out_rows)


def build_packing_trims():
    grid = _read_csv(MASTER / "packing_trims__packing_trims_1_10__r1c10.csv")
    cell_map = eval_table_grid(grid)

    out_rows = [["trims", "using_part", "size", "cost"]]
    # headers row 1, data rows start row 2
    for r in range(2, 1000):
        trims = cell_map.get(f"B{r}")
        if trims in (None, ""):
            break
        using_part = cell_map.get(f"C{r}")
        small = _coerce_number(cell_map.get(f"D{r}"))
        large = _coerce_number(cell_map.get(f"E{r}"))
        if small is not None:
            out_rows.append([trims, using_part, "SMALL", small])
        if large is not None:
            out_rows.append([trims, using_part, "LARGE", large])

    _write_csv(OUT / "packing_trims.csv", out_rows)


def build_sam_product_eff():
    grid = _read_csv(MASTER / "sam_product_eff__sam_product_eff_1_1__r1c1.csv")
    cell_map = eval_table_grid(grid)

    out_rows = [["gender", "product_shape", "side_seam", "size", "sam", "eff_pct"]]

    for r in range(2, 500):
        gender = cell_map.get(f"A{r}")
        if gender in (None, ""):
            break
        prod = cell_map.get(f"B{r}")
        seam = cell_map.get(f"C{r}")
        size = cell_map.get(f"D{r}")
        sam = _coerce_number(cell_map.get(f"E{r}"))
        eff = _coerce_number(cell_map.get(f"G{r}"))
        out_rows.append([gender, prod, seam, size, sam, eff])

    _write_csv(OUT / "sam_product_eff.csv", out_rows)


def build_fabric_price():
    # Use the simple table that exists in fabric_price_1_50 extract
    grid = _read_csv(MASTER / "fabric_price__fabric_price_1_50__r1c50.csv")
    cell_map = eval_table_grid(grid)

    out_rows = [["item", "fabric", "type", "weight_gsm", "cut_width_in", "price_per_yd_usd"]]
    for r in range(2, 1000):
        item = cell_map.get(f"A{r}")
        if item in (None, ""):
            break
        fabric = cell_map.get(f"B{r}")
        ftype = cell_map.get(f"C{r}")
        weight = _coerce_number(cell_map.get(f"D{r}"))
        width = _coerce_number(cell_map.get(f"E{r}"))
        price = _coerce_number(cell_map.get(f"F{r}"))
        out_rows.append([item, fabric, ftype, weight, width, price])

    _write_csv(OUT / "fabric_price.csv", out_rows)


def build_conversion_constants():
    out_rows = [
        ["key", "value"],
        ["inch_to_meter", 0.0254],
        ["yard_to_meter", 0.9144],
        ["kg_to_oz", 35.274],
        ["lb_to_oz", 16.0],
        ["lb_to_kg", 0.453592],
        ["oz_to_kg", 0.0283495],
        ["lb_to_kg_factor", 0.453592],
        ["kg_to_lb_factor", 2.20462262],
    ]
    _write_csv(OUT / "conversion_constants.csv", out_rows)


def main():
    build_conversion_constants()
    build_cost_rate()
    build_packing_trims()
    build_sam_product_eff()
    build_fabric_price()


if __name__ == "__main__":
    main()
