import csv
from pathlib import Path

ROOT = Path(r"C:\Users\dploy\.openclaw\workspace\basicshirts_web")
MASTER = ROOT / "master_clean"

EXPECTED = {
    # Minimal sanity expectations for Fabrication
    "dropdown_fabric_type.csv": ["Jersey", "Mesh", "Rib1x1"],
    "dropdown_fabric_contents.csv": ["Cotton/Spandex 95/5"],
    "dropdown_using_part.csv": ["Whole Garment"],
    "dropdown_material_coo.csv": ["Import", "Domestic"],
}


def read_values(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return { (row.get("value") or "").strip() for row in r if (row.get("value") or "").strip() }


errors = []
for fname, must_have in EXPECTED.items():
    p = MASTER / fname
    if not p.exists():
        errors.append(f"missing {fname}")
        continue
    vals = read_values(p)
    for m in must_have:
        if m not in vals:
            errors.append(f"{fname} missing expected value: {m!r}")

if errors:
    raise SystemExit("QA FAILED:\n" + "\n".join(errors))

print("QA OK")
