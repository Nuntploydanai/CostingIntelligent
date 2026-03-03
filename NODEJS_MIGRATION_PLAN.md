# Node.js v2 Migration Plan

## Overview
Migrate from Python/FastAPI to Node.js/Express for better React integration and multi-developer support.

---

## Phase 1: Project Setup (1-2 days)

### 1.1 Initialize Node.js Project
```bash
mkdir costing-tool-v2
cd costing-tool-v2
npm init -y
npm install express cors body-parser
npm install --save-dev nodemon typescript @types/node @types/express
```

### 1.2 Project Structure
```
costing-tool-v2/
├── server/
│   ├── index.ts              # Express server
│   ├── routes/
│   │   ├── calculate.ts      # Main calculation endpoint
│   │   ├── dropdowns.ts      # Dropdown data endpoints
│   │   └── fabric.ts         # Fabric defaults endpoint
│   ├── services/
│   │   ├── fabrication.service.ts
│   │   ├── trims.service.ts
│   │   ├── embellishments.service.ts
│   │   ├── packing.service.ts
│   │   ├── manufacturing.service.ts
│   │   └── totalCost.service.ts
│   ├── utils/
│   │   ├── csvLoader.ts      # Load CSV files
│   │   └── helpers.ts        # Helper functions
│   └── types/
│       └── index.ts          # TypeScript interfaces
├── data/
│   └── master_clean/         # All CSV files
├── client/                    # React frontend (Phase 2)
└── package.json
```

---

## Phase 2: Backend Migration (3-5 days)

### 2.1 Core Calculation Services

#### fabrication.service.ts
```typescript
export interface FabricationInput {
  fabric_type: string;
  fabric_contents: string;
  using_part: string;
  weight_gsm_override?: number;
  price_unit: string;
  price_value?: number;
  material_coo: string;
}

export interface FabricationOutput {
  fixed_fabric_width: number;
  default_weight_gsm: number;
  default_price_yd: number;
  default_price_kilo: number;
  default_price_lb: number;
  total_cost: number;
}

export function computeFabricRow(input: FabricationInput): FabricationOutput {
  // Port logic from fabrication_calc.py
  // 1. Load CSV lookups
  // 2. Apply Excel formulas
  // 3. Return calculated values
}
```

#### manufacturing.service.ts
```typescript
export interface ManufacturingInput {
  gender: string;
  silhouette: string;
  seam: string;
  size: string;
  quantity: string;
  coo: string;
}

export function computeManufacturing(input: ManufacturingInput) {
  // Port logic from manufacturing_calc.py
  // 1. Lookup SAM minutes
  // 2. Lookup cost rate by country
  // 3. Lookup efficiency by quantity
  // 4. Calculate: (minutes / efficiency) * cost_rate
}
```

### 2.2 Total Cost Summary Service
```typescript
export function computeTotalCostSummary(inputs: TotalCostInput): TotalCostSummary {
  // Port logic from total_cost_calc.py
  // 1. Calculate all 10 cost items
  // 2. Calculate subtotal
  // 3. Apply supplier margin
  // 4. Calculate FOB
  // 5. Calculate FLC (FOB + Freight + GMO + Duty)
  // 6. Calculate per dozen values
}
```

### 2.3 Country Comparison Service
```typescript
const COMPARISON_COUNTRIES = [
  'INDIA',
  'BANGLADESH',
  'INDONESIA',
  'THAILAND',
  'CAMBODIA',
  'VIETNAM'
];

export function computeCountryComparison(inputs: CountryComparisonInput) {
  // Port logic from country_comparison_calc.py
  // Calculate FOB for all 6 countries
}
```

---

## Phase 3: API Endpoints (1-2 days)

### Express Server
```typescript
// server/index.ts
import express from 'express';
import cors from 'cors';
import { calculateRouter } from './routes/calculate';

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api', calculateRouter);

app.listen(8000, () => {
  console.log('Server running on http://localhost:8000');
});
```

### Calculate Route
```typescript
// server/routes/calculate.ts
router.post('/calculate', (req, res) => {
  const { development, fabrication, trims, embellishments, packing_label } = req.body;

  // 1. Calculate fabrication
  const fabricationResults = computeFabrication(fabrication);

  // 2. Calculate trims
  const trimsResults = computeTrims(trims);

  // 3. Calculate embellishments
  const embellishmentsResults = computeEmbellishments(embellishments);

  // 4. Calculate packing
  const packingResults = computePacking(packing_label);

  // 5. Calculate manufacturing
  const manufacturingResults = computeManufacturing(development);

  // 6. Calculate total cost summary
  const totalSummary = computeTotalCostSummary({
    fabrication: fabricationResults,
    trims: trimsResults,
    embellishments: embellishmentsResults,
    packing: packingResults,
    manufacturing: manufacturingResults
  });

  // 7. Calculate country comparison
  const countryComparison = computeCountryComparison({...});

  res.json({
    inputs: { development, fabrication },
    outputs: {
      fabrication: fabricationResults,
      trims: trimsResults,
      embellishments: embellishmentsResults,
      packing_label: packingResults,
      manufacturing: manufacturingResults,
      total_cost_summary: totalSummary,
      country_comparison: countryComparison
    }
  });
});
```

---

## Phase 4: React Frontend (5-7 days)

### 4.1 Setup React with Vite
```bash
cd client
npm create vite@latest . -- --template react-ts
npm install
```

### 4.2 Component Structure
```
client/src/
├── components/
│   ├── DevelopmentForm.tsx      # Step 1
│   ├── FabricationForm.tsx      # Step 2
│   ├── TrimsForm.tsx            # Step 3
│   ├── EmbellishmentsForm.tsx   # Step 4
│   ├── PackingForm.tsx          # Step 5
│   ├── ManufacturingDisplay.tsx # Step 6
│   ├── TotalCostSummary.tsx     # Summary
│   └── CountryComparison.tsx    # Country table
├── services/
│   └── api.ts                   # API calls
├── hooks/
│   └── useCalculator.ts         # Custom hook for calculations
└── types/
    └── index.ts                 # TypeScript interfaces
```

### 4.3 Key Components

#### DevelopmentForm.tsx
```typescript
export function DevelopmentForm({ onChange }: Props) {
  const [gender, setGender] = useState('');
  const [silhouette, setSilhouette] = useState('');
  // ... other fields

  useEffect(() => {
    onChange({ gender, silhouette, seam, color, size, pack, qty, coo, finish });
  }, [gender, silhouette, ...]);

  return (
    <div className="development-form">
      <select value={gender} onChange={(e) => setGender(e.target.value)}>
        {/* Options from API */}
      </select>
      {/* More inputs */}
    </div>
  );
}
```

#### TotalCostSummary.tsx
```typescript
export function TotalCostSummary({ summary }: Props) {
  return (
    <div className="total-cost-summary">
      <div className="summary-row">
        <span>1. Total Fabric Cost</span>
        <span>${summary.total_fabric_cost.toFixed(3)} ({summary.total_fabric_cost_pct.toFixed(3)}%)</span>
      </div>
      {/* More items */}
    </div>
  );
}
```

#### CountryComparison.tsx
```typescript
export function CountryComparison({ countries, selectedCountry }: Props) {
  return (
    <table>
      <thead>
        <tr>
          <th>Country</th>
          <th>Labour Cost</th>
          <th>FOB Cost</th>
        </tr>
      </thead>
      <tbody>
        {countries.map(country => (
          <tr key={country.country} className={country.country === selectedCountry ? 'selected' : ''}>
            <td>{country.country}</td>
            <td>${country.labour_cost.toFixed(3)}</td>
            <td>${country.fob_cost.toFixed(3)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

---

## Phase 5: Testing & Deployment (2-3 days)

### 5.1 Backend Testing
```typescript
// server/__tests__/fabrication.test.ts
describe('Fabrication Service', () => {
  test('should calculate fabric cost correctly', () => {
    const input = {
      fabric_type: 'Jersey',
      fabric_contents: 'Cotton/Spandex 95/5',
      // ...
    };
    const result = computeFabricRow(input);
    expect(result.total_cost).toBeCloseTo(0.14, 3);
  });
});
```

### 5.2 Frontend Testing
```typescript
// client/src/__tests__/TotalCostSummary.test.tsx
test('displays correct cost values', () => {
  render(<TotalCostSummary summary={mockSummary} />);
  expect(screen.getByText(/\$0\.140/)).toBeInTheDocument();
});
```

### 5.3 Deployment Options
- **Backend**: Render.com, Railway, or Heroku
- **Frontend**: Vercel, Netlify, or GitHub Pages
- **Database** (future): PostgreSQL or MongoDB for saving calculations

---

## Migration Timeline

| Week | Tasks | Deliverable |
|------|-------|-------------|
| 1 | Backend setup + Core services | Working API with calculation endpoints |
| 2 | API endpoints + Testing | Complete backend ready for frontend |
| 3 | React setup + Form components | Working forms with auto-calculation |
| 4 | Summary + Comparison components | Complete UI matching Python version |
| 5 | Testing + Deployment | Production-ready v2 |

---

## Benefits of Node.js v2

### 1. **Better Developer Experience**
- TypeScript for type safety
- Hot reload with nodemon
- Better error messages

### 2. **React Integration**
- Same language (JavaScript/TypeScript) on frontend and backend
- Easy to share types/interfaces
- Better state management

### 3. **Performance**
- Non-blocking I/O for better concurrency
- Faster JSON parsing
- Better for real-time features

### 4. **Future Features**
- Save/load calculations (database)
- User authentication
- Export to Excel/PDF
- Real-time collaboration
- Mobile app (React Native)

---

## Next Steps

1. ✅ **Push Python v1 to GitHub** (DONE)
2. **Create Node.js project structure**
3. **Port calculation logic to TypeScript**
4. **Build React frontend**
5. **Test and deploy**

---

**Estimated Total Time**: 4-5 weeks (part-time)

**Ready to start?** Let me know if you want me to create the initial Node.js project structure!
