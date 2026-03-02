# Basic Shirts Costing Demo (Step 1–2)

This is a **very small demo** to let you *see something*:
- Dropdowns load from `master_clean/dropdown_*.csv`
- UI submits selected values to a FastAPI backend
- Backend validates that selected values exist in the dropdown CSVs
- Backend returns the normalized payload + placeholder outputs

## 1) Install dependencies (one-time)

From a terminal in this repo folder:

```powershell
python -m pip install fastapi uvicorn
```

## 2) Run the backend

```powershell
cd C:\Users\dploy\.openclaw\workspace\basicshirts_web
python server.py
```

You should see Uvicorn running on: `http://127.0.0.1:8000`

## 3) Open the demo UI

Open in browser:
- http://127.0.0.1:8000/

Or open Swagger (API testing):
- http://127.0.0.1:8000/docs

## Notes
- This is not the final calculator yet.
- Next step is to implement real Fabrication calculations inside `/api/calculate`.
