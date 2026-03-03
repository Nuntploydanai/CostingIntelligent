# React + Python Architecture Plan

## Technology Stack

### Frontend (React)
- **Framework**: React 18
- **Styling**: Material-UI (MUI) or Tailwind CSS
- **State Management**: React Query + Context API
- **Form Handling**: React Hook Form + Yup
- **API Calls**: Axios
- **Drag-and-Drop**: React DnD or dnd-kit
- **Charts**: Chart.js or Recharts
- **Routing**: React Router v6
- **Build Tool**: Vite (faster than CRA)

### Backend (Python - Keep Current)
- **Framework**: FastAPI
- **Validation**: Pydantic
- **Excel Processing**: OpenPyXL
- **CORS**: fastapi.middleware.cors

### Deployment
- **Frontend**: Vercel (auto-deploys from GitHub)
- **Backend**: Railway or Render (free tier)
- **Database**: (future) PostgreSQL or MongoDB

---

## Project Structure

```
CostingIntelligent/
├── backend/                      # Python API
│   ├── server.py                 # FastAPI server
│   ├── fabrication_calc.py       # Step 2 calculations
│   ├── trims_calc.py             # Step 3 calculations
│   ├── embellishments_calc.py    # Step 4 calculations
│   ├── packing_label_calc.py     # Step 5 calculations
│   ├── manufacturing_calc.py     # Step 6 calculations
│   ├── master_clean/             # CSV data files
│   ├── requirements.txt          # Python dependencies
│   └── README.md
│
├── frontend/                     # React App
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── src/
│   │   ├── components/
│   │   │   ├── steps/
│   │   │   │   ├── Step1Development.jsx
│   │   │   │   ├── Step2Fabrication.jsx
│   │   │   │   ├── Step3Trims.jsx
│   │   │   │   ├── Step4Embellishments.jsx
│   │   │   │   ├── Step5PackingLabel.jsx
│   │   │   │   └── Step6Manufacturing.jsx
│   │   │   ├── common/
│   │   │   │   ├── InputField.jsx
│   │   │   │   ├── SelectField.jsx
│   │   │   │   ├── ReadOnlyField.jsx
│   │   │   │   └── TotalSummary.jsx
│   │   │   └── layout/
│   │   │       ├── Header.jsx
│   │   │       └── Navigation.jsx
│   │   ├── hooks/
│   │   │   ├── useApi.js         # API call hook
│   │   │   └── useFormState.js   # Form state hook
│   │   ├── services/
│   │   │   └── api.js            # API service
│   │   ├── context/
│   │   │   └── AppContext.jsx    # Global state
│   │   ├── utils/
│   │   │   └── helpers.js        # Helper functions
│   │   ├── App.jsx               # Main app component
│   │   ├── index.jsx             # Entry point
│   │   └── index.css             # Global styles
│   ├── public/
│   │   └── index.html
│   └── README.md
│
├── mobile/                       # Future: React Native
│   └── (will be created later)
│
└── README.md                     # Main project documentation
```

---

## Development Workflow

### 1. Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
# API runs on http://localhost:8000
```

### 2. Frontend Development
```bash
cd frontend
npm install
npm run dev
# React runs on http://localhost:5173
# Calls backend API at http://localhost:8000
```

### 3. Deployment
- Push to GitHub
- Vercel auto-deploys frontend
- Railway auto-deploys backend

---

## API Endpoints (Backend)

```
GET  /api/dropdowns              # List all dropdowns
GET  /api/dropdown/{name}        # Get dropdown options
GET  /api/fabric/defaults        # Get fabric defaults
GET  /api/embellishment/dimensions # Get embellishment dimensions
POST /api/calculate              # Calculate all steps
```

---

## Component Architecture

### Step Components (Smart Components)
- Manage their own state
- Call API endpoints
- Handle user interactions
- Pass data to common components

### Common Components (Dumb Components)
- Reusable UI elements
- Receive props only
- Emit events to parents
- No API calls

### Context/State Management
- Global app state (current step, selected values)
- API state management (React Query)
- Form state (React Hook Form)

---

## Mobile App (React Native)

### Code Reuse
- 70-80% of React components can be reused
- Only UI components need to change (React Native components)
- Business logic stays the same
- API calls stay the same

### Structure
```
mobile/
├── src/
│   ├── components/  (React Native components)
│   ├── screens/     (React Native screens)
│   └── navigation/  (React Navigation)
└── App.js
```

---

## Benefits

### 1. Team Scalability
- Frontend team works on React
- Backend team works on Python
- Clear separation of concerns

### 2. Code Quality
- TypeScript for type safety
- ESLint + Prettier for formatting
- Unit tests with Jest
- E2E tests with Cypress

### 3. Performance
- Vite for fast builds
- Code splitting
- Lazy loading
- Optimized bundle size

### 4. Developer Experience
- Hot Module Replacement (HMR)
- Fast refresh
- Better error messages
- Rich ecosystem

### 5. Deployment
- Automatic deployments from GitHub
- Preview deployments for PRs
- Easy rollbacks
- Environment variables

---

## Timeline Estimate

### Phase 1: Setup (1-2 days)
- [ ] Create React app with Vite
- [ ] Setup project structure
- [ ] Configure Material-UI
- [ ] Setup API service

### Phase 2: Core Components (1 week)
- [ ] Build common components (Input, Select, etc.)
- [ ] Build Step 1 component
- [ ] Build Step 2 component
- [ ] Connect to backend API

### Phase 3: All Steps (1 week)
- [ ] Build Steps 3-6 components
- [ ] Add auto-calculate feature
- [ ] Add total summary
- [ ] Test all calculations

### Phase 4: Enhancements (1 week)
- [ ] Add drag-and-drop for rows
- [ ] Add real-time validation
- [ ] Add charts/visualizations
- [ ] Improve styling

### Phase 5: Testing & Deployment (3-5 days)
- [ ] Write unit tests
- [ ] Write E2E tests
- [ ] Deploy to Vercel/Railway
- [ ] Setup CI/CD

### Total: 4-5 weeks

---

## Next Steps

1. **Decide on UI library** (Material-UI vs Tailwind)
2. **Create React app**
3. **Migrate Step 1 component first**
4. **Test API connection**
5. **Continue with other steps**

---

Ready to start? Let me know which step you want to begin with! 🚀
