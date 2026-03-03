import express, { Request, Response } from 'express';
import cors from 'cors';
import { CalculateRequest, CalculateResponse } from './types';
import { computeFabrication } from './services/fabrication.service';
import { computeManufacturing } from './services/manufacturing.service';
import { computeTotalCostSummary, computeCountryComparison } from './services/totalCost.service';

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from client build (for production)
app.use(express.static('client/dist'));

// Helper to load dropdown data
async function loadDropdown(name: string): Promise<string[]> {
  const { loadCSV } = await import('./utils/csvLoader');
  const data = await loadCSV(`dropdown_${name}.csv`);
  return data.map(row => row.value).filter(v => v);
}

// Dropdown endpoints
app.get('/api/dropdown/:name', async (req: Request, res: Response) => {
  try {
    const name = req.params.name;
    const values = await loadDropdown(name);
    res.json({ values });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Main calculation endpoint
app.post('/api/calculate', async (req: Request, res: Response) => {
  try {
    const input: CalculateRequest = req.body;

    // 1. Calculate fabrication
    const fabricationResults = [];
    let totalFabricCost = 0;

    for (const fab of input.fabrication) {
      const result = await computeFabrication(fab);
      fabricationResults.push(result);
      totalFabricCost += result.total_cost;
    }

    // 2. Calculate manufacturing
    const manufacturingResults = await computeManufacturing({
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      seam: input.development.seam,
      size: input.development.size,
      quantity: input.development.ideal_quantity,
      coo: input.development.coo,
    });

    // Get labour cost for selected COO
    const labourCost = manufacturingResults[0]?.total_cost || 0;

    // 3. Calculate total cost summary
    const totalSummary = await computeTotalCostSummary({
      fabric_cost: totalFabricCost,
      trim_cost: 0, // TODO: Add trims calculation
      print_embroidery_cost: 0, // TODO: Add embellishments calculation
      display_packaging_cost: 0, // TODO: Add packing calculation
      transit_packaging_cost: 0,
      label_cost: 0,
      labour_cost: labourCost,
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      size: input.development.size,
      supplier_margin_percent: input.supplier_margin_percent,
      product_testing_cost: 0.01,
      other_cost: input.additional_cost,
      freight_cost: input.freight_cost,
      gmo_cost: input.gmo_cost,
      duty_cost: input.duty_cost,
    });

    // 4. Calculate country comparison
    const countryComparison = await computeCountryComparison({
      fabric_cost: totalFabricCost,
      trim_cost: 0,
      print_embroidery_cost: 0,
      display_packaging_cost: 0,
      transit_packaging_cost: 0,
      label_cost: 0,
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      seam: input.development.seam,
      size: input.development.size,
      quantity: input.development.ideal_quantity,
      supplier_margin_percent: input.supplier_margin_percent,
      product_testing_cost: 0.01,
      other_cost: input.additional_cost,
      freight_cost: input.freight_cost,
      gmo_cost: input.gmo_cost,
      duty_cost: input.duty_cost,
    });

    const response: CalculateResponse = {
      inputs: {
        development: input.development,
        fabrication: input.fabrication,
      },
      outputs: {
        fabrication: {
          rows: fabricationResults,
          total_fabric_cost: totalFabricCost,
        },
        trims: {
          rows: [], // TODO: Add trims
        },
        embellishments: {
          rows: [], // TODO: Add embellishments
        },
        packing_label: {
          display_packaging: { default_usage: 0, total: 0 },
          transit_package: { default_usage: 0, total: 0 },
          label: { default_usage: 0, total: 0 },
        },
        manufacturing: {
          rows: manufacturingResults,
        },
        total_cost_summary: totalSummary,
        country_comparison: countryComparison,
      },
    };

    res.json(response);
  } catch (error) {
    console.error('Calculation error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Health check
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📊 API endpoints:`);
  console.log(`   - GET  /api/dropdown/:name`);
  console.log(`   - POST /api/calculate`);
  console.log(`   - GET  /api/health`);
});
