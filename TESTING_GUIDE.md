# 🚀 Quick Start Guide - Node.js v2

## Prerequisites

- Node.js 18+ installed
- npm or yarn

---

## ⚡ Quick Test (3 steps)

### 1️⃣ Install Dependencies

```bash
# Install backend dependencies
npm install

# Install frontend dependencies
cd client
npm install
cd ..
```

### 2️⃣ Start Development Server

**Option A: Start both servers (backend + frontend)**

Windows:
```bash
start-dev.bat
```

Mac/Linux:
```bash
npm run dev
```

**Option B: Start servers separately**

Terminal 1 (Backend):
```bash
npm run server:dev
```

Terminal 2 (Frontend):
```bash
cd client
npm run dev
```

### 3️⃣ Open Browser

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/health

---

## 🎯 Testing the App

### Test Scenario 1: Basic Calculation

1. **Step 1: Development**
   - Gender: **Men**
   - Silhouette: **Tank Top/A Shirt**
   - Seam: **Side Seam**
   - Size: **S**
   - Ideal Quantity: **1K-3K**
   - COO: **BANGLADESH**

2. **Step 2: Fabrication**
   - Fabric Type: **Jersey**
   - Fabric Contents: **Cotton/Spandex 95/5**
   - Price Unit: **Price / YD**
   - Price Value: (leave empty for default)

3. **Check Results:**
   - ✅ Total Cost Summary should appear
   - ✅ All values show **3 decimal places**
   - ✅ Country Comparison shows **6 countries**
   - ✅ Selected COO (BANGLADESH) is **highlighted**

### Test Scenario 2: Custom Prices

1. Same as Scenario 1, but:
   - Price Value: **2.5** (override default price)
   - Supplier Margin: **10%**
   - Freight Cost: **0.05**
   - GMO Cost: **0.03**

2. **Verify:**
   - ✅ FOB cost = Subtotal + Margin
   - ✅ FLC cost = FOB + Freight + GMO + Duty
   - ✅ Per dozen = Per piece × 12

---

## 🧪 API Testing

### Health Check
```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "ok",
  "timestamp": "2024-..."
}
```

### Get Dropdown Data
```bash
curl http://localhost:8000/api/dropdown/gender
```

Expected:
```json
{
  "values": ["Men", "Women", "Kids"]
}
```

### Calculate Cost (POST)
```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "development": {
      "gender": "Men",
      "silhouette": "Tank Top/A Shirt",
      "seam": "Side Seam",
      "color_design": "",
      "size": "S",
      "pack_count": "",
      "ideal_quantity": "1K-3K",
      "coo": "BANGLADESH",
      "fabric_finishing": ""
    },
    "fabrication": [{
      "fabric_type": "Jersey",
      "fabric_contents": "Cotton/Spandex 95/5",
      "using_part": "Self Fabric",
      "weight_gsm_override": "",
      "price_unit": "Price / YD",
      "price_value": "",
      "material_coo": ""
    }],
    "trims": [],
    "embellishments": [],
    "packing_label": {},
    "supplier_margin_percent": 7,
    "freight_cost": 0,
    "gmo_cost": 0,
    "duty_cost": 0,
    "additional_cost": 0
  }'
```

Expected Response:
```json
{
  "outputs": {
    "total_cost_summary": {
      "subtotal": 18.319,
      "fob_cost": 19.601,
      "grand_total": 19.601,
      ...
    },
    "country_comparison": [
      {
        "country": "INDIA",
        "fob_cost": 19.586
      },
      ...
    ]
  }
}
```

---

## 🐛 Troubleshooting

### Error: "Cannot find module 'csv-parser'"
**Solution:**
```bash
npm install csv-parser
```

### Error: "Port 8000 already in use"
**Solution:**
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Error: "Failed to load dropdown data"
**Solution:**
- Check if CSV files exist in `data/master_clean/`
- Run: `Copy-Item -Path "master_clean\*.csv" -Destination "data\master_clean\" -Force`

### Frontend shows "Calculating..." forever
**Solution:**
- Check backend console for errors
- Verify backend is running on http://localhost:8000
- Check browser console (F12) for errors

---

## 📊 Expected Results

### Total Cost Summary (Example)

| Item | Cost ($) | Proportion (%) |
|------|----------|----------------|
| 1. Total Fabric Cost | 18.160 | 99.130% |
| 2. Total Trim Cost | 0.000 | 0.000% |
| ... | ... | ... |
| **Subtotal** | **18.319** | **100.000%** |
| **FOB Cost** | **19.601** | |

### Country Comparison (Example)

| Country | Labour Cost | FOB Cost |
|---------|-------------|----------|
| INDIA | 0.131 | 19.586 |
| **BANGLADESH** | **0.145** | **19.601** |
| INDONESIA | 0.126 | 19.581 |
| THAILAND | 0.271 | 19.736 |
| CAMBODIA | 0.228 | 19.690 |
| VIETNAM | 0.219 | 19.680 |

---

## 📁 Project Structure

```
basicshirts_web/
├── server/                    # Backend (Node.js + Express)
│   ├── index.ts              # Main server (all logic included)
│   ├── services/             # Calculation services
│   ├── utils/                # Utilities
│   └── types/                # TypeScript interfaces
├── client/                    # Frontend (React + Vite)
│   ├── src/
│   │   ├── App.tsx           # Main React component
│   │   ├── main.tsx          # Entry point
│   │   └── index.css         # Styles
│   ├── index.html
│   └── package.json
├── data/                      # Master data
│   └── master_clean/         # CSV files
├── package.json              # Backend package
├── tsconfig.json             # TypeScript config
├── start-dev.bat             # Dev startup script
└── start-production.bat      # Production startup script
```

---

## 🎨 Features

✅ **6-Step Cost Calculation**
✅ **16 Cost Items** with % proportions
✅ **3 Decimal Places** (Excel parity)
✅ **Country Comparison** (6 countries)
✅ **Auto-calculation** (500ms debounce)
✅ **Responsive Design**
✅ **TypeScript** (type safety)
✅ **Modern UI** (clean design)

---

## 🚀 Production Build

```bash
# Build frontend
cd client
npm run build

# Start production server (serves frontend)
cd ..
npm start
```

Server runs on: **http://localhost:8000**

---

## 📝 Notes

- **Backend port**: 8000 (configurable via PORT env var)
- **Frontend port**: 5173 (Vite dev server)
- **API prefix**: `/api/*`
- **CSV files**: `data/master_clean/*.csv`

---

## 🔗 Links

- **GitHub**: https://github.com/Nuntploydanai/CostingIntelligent
- **Branch**: nodejs-v2
- **Issues**: Report bugs on GitHub

---

**Ready to test? Run `start-dev.bat` and open http://localhost:5173!** 🎯
