# Basic Shirts Costing Tool v2 (Node.js)

> Complete Excel-parity costing tool with Node.js/Express backend and React frontend

## 🚀 Features

- ✅ **6-Step Cost Calculation**: Development → Fabrication → Trims → Embellishments → Packing → Manufacturing
- ✅ **Excel-Parity Calculations**: All formulas match Excel exactly (3 decimal places)
- ✅ **Country Comparison**: Compare FOB costs across 6 countries (India, Bangladesh, Indonesia, Thailand, Cambodia, Vietnam)
- ✅ **16 Cost Items**: Complete breakdown with % proportions
- ✅ **Fillable Inputs**: Freight, GMO, Duty, Additional Cost
- ✅ **Summary Calculations**: FOB/FLC per piece and per dozen
- ✅ **TypeScript**: Full type safety
- ✅ **React Frontend**: Modern UI with auto-calculation

## 📊 Tech Stack

**Backend:**
- Node.js + Express
- TypeScript
- CSV parsing

**Frontend:**
- React + TypeScript
- Vite
- Modern CSS

## 🏃 Quick Start

### Backend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run server:dev
```

Server runs on: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

Client runs on: `http://localhost:5173`

### Full Stack Development

```bash
# Run both backend and frontend
npm run dev
```

## 📁 Project Structure

```
basicshirts_web/
├── server/                 # Backend (Node.js + Express)
│   ├── index.ts           # Main server file
│   ├── services/          # Business logic
│   │   ├── fabrication.service.ts
│   │   ├── manufacturing.service.ts
│   │   └── totalCost.service.ts
│   ├── utils/             # Utilities
│   │   └── csvLoader.ts
│   └── types/             # TypeScript interfaces
│       └── index.ts
├── client/                # Frontend (React)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API calls
│   │   └── App.tsx
│   └── package.json
├── data/                  # Master data CSVs
│   └── master_clean/
├── package.json
└── tsconfig.json
```

## 🔌 API Endpoints

### Dropdown Data
```http
GET /api/dropdown/:name
```

**Response:**
```json
{
  "values": ["Men", "Women", "Kids"]
}
```

### Calculate Cost
```http
POST /api/calculate
```

**Request:**
```json
{
  "development": {
    "gender": "Men",
    "silhouette": "Tank Top/A Shirt",
    "seam": "Side Seam",
    "coo": "BANGLADESH"
  },
  "fabrication": [{
    "fabric_type": "Jersey",
    "fabric_contents": "Cotton/Spandex 95/5"
  }],
  "supplier_margin_percent": 7,
  "freight_cost": 0,
  "gmo_cost": 0,
  "duty_cost": 0,
  "additional_cost": 0
}
```

**Response:**
```json
{
  "outputs": {
    "total_cost_summary": {
      "subtotal": 18.319,
      "fob_cost": 19.601,
      "grand_total": 19.601
    },
    "country_comparison": [
      {
        "country": "BANGLADESH",
        "labour_cost": 0.145,
        "fob_cost": 19.601
      }
    ]
  }
}
```

## 🧮 Cost Calculation Logic

### Manufacturing Cost Formula
```
Total Cost = (SAM Minutes / Efficiency) × Cost Rate
```

Where:
- **SAM Minutes**: From lookup table (Gender + Silhouette + Seam + Size)
- **Efficiency**: From lookup table (based on quantity range)
- **Cost Rate**: From lookup table (varies by country)

### FOB Cost Formula
```
Subtotal = Sum of all 10 cost items
Supplier Margin = Subtotal × (Margin %)
FOB = Subtotal + Supplier Margin
```

### FLC Cost Formula
```
FLC = FOB + Freight + GMO + Duty
```

## 📊 Country Comparison

The tool calculates FOB cost for all 6 countries automatically:

| Country | Labour Cost | FOB Cost |
|---------|-------------|----------|
| INDIA | $0.131 | $19.586 |
| BANGLADESH | $0.145 | $19.601 |
| INDONESIA | $0.126 | $19.581 |
| THAILAND | $0.271 | $19.736 |
| CAMBODIA | $0.228 | $19.690 |
| VIETNAM | $0.219 | $19.680 |

## 🎯 Excel Parity

All calculations match Excel exactly:
- ✅ 3 decimal places for all values
- ✅ Same formulas and lookups
- ✅ Same rounding behavior
- ✅ Same country comparison logic

## 🔧 Development

### Build for Production

```bash
# Build backend
npm run build

# Build frontend
cd client && npm run build

# Start production server
npm start
```

### Environment Variables

Create `.env` file:
```env
PORT=8000
NODE_ENV=production
```

## 📝 Version History

- **v1.0** (Python/FastAPI) - HTML prototype with Excel parity
- **v2.0** (Node.js/React) - Full stack TypeScript implementation

## 🤝 Contributing

1. Create feature branch
2. Commit changes
3. Push to branch
4. Open Pull Request

## 📄 License

MIT

## 🙏 Acknowledgments

- Original Excel tool by Nunt
- Python v1 implementation
- Node.js migration plan

---

**Repository**: https://github.com/Nuntploydanai/CostingIntelligent  
**Author**: Nunt  
**Version**: 2.0.0
