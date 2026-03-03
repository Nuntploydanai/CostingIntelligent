import express, { Request, Response } from 'express';
import cors from 'cors';
import path from 'path';
import fs from 'fs';
import csv from 'csv-parser';

// Utility functions
const DATA_DIR = path.join(__dirname, '../data/master_clean');

async function loadCSV(filename: string): Promise<any[]> {
  return new Promise((resolve, reject) => {
    const results: any[] = [];
    const filePath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filePath)) {
      resolve([]);
      return;
    }

    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', (error) => reject(error));
  });
}

function normalizeString(value: any): string {
  if (value === null || value === undefined) return '';
  return String(value).trim();
}

function toFloat(value: any): number | null {
  if (value === null || value === undefined) return null;
  if (typeof value === 'number') return value;
  if (typeof value === 'string') {
    const s = value.trim();
    if (s === '' || s === '-') return null;
    const num = parseFloat(s);
    return isNaN(num) ? null : num;
  }
  return null;
}

// Services
async function computeFabrication(input: any) {
  const fabricWidthData = await loadCSV('dropdown_fabric_width.csv');
  const fabricPriceData = await loadCSV('dropdown_fabric_price.csv');
  const fabricUsageData = await loadCSV('dropdown_fabric_usage.csv');

  const widthRow = fabricWidthData.find(row =>
    normalizeString(row.fabric_type) === normalizeString(input.fabric_type) &&
    normalizeString(row.fabric_contents) === normalizeString(input.fabric_contents)
  );
  const fixedFabricWidth = toFloat(widthRow?.fabric_width) || 60;

  const priceRow = fabricPriceData.find(row =>
    normalizeString(row.fabric_type) === normalizeString(input.fabric_type) &&
    normalizeString(row.fabric_contents) === normalizeString(input.fabric_contents)
  );
  const defaultWeightGsm = toFloat(priceRow?.weight_gsm) || 200;
  const defaultPriceYd = toFloat(priceRow?.price_yd) || 0;
  const defaultPriceKilo = toFloat(priceRow?.price_kilo) || 0;
  const defaultPriceLb = toFloat(priceRow?.price_lb) || 0;

  const usageRow = fabricUsageData.find(row =>
    normalizeString(row.fabric_type) === normalizeString(input.fabric_type) &&
    normalizeString(row.fabric_contents) === normalizeString(input.fabric_contents) &&
    normalizeString(row.using_part) === normalizeString(input.using_part)
  );
  const defaultUsage = toFloat(usageRow?.usage_yd) || 0;

  let totalCost = 0;
  if (input.price_unit === 'Price / YD') {
    const pricePerYd = toFloat(input.price_value) || defaultPriceYd;
    totalCost = defaultUsage * pricePerYd;
  } else if (input.price_unit === 'Price / KILO') {
    const pricePerKilo = toFloat(input.price_value) || defaultPriceKilo;
    const weightGsm = toFloat(input.weight_gsm_override) || defaultWeightGsm;
    totalCost = (defaultUsage * weightGsm * pricePerKilo) / 1000;
  } else if (input.price_unit === 'Price / LB') {
    const pricePerLb = toFloat(input.price_value) || defaultPriceLb;
    const weightGsm = toFloat(input.weight_gsm_override) || defaultWeightGsm;
    const pricePerKilo = pricePerLb * 2.20462;
    totalCost = (defaultUsage * weightGsm * pricePerKilo) / 1000;
  }

  return {
    fixed_fabric_width: Math.round(fixedFabricWidth * 1000) / 1000,
    default_weight_gsm: Math.round(defaultWeightGsm * 1000) / 1000,
    default_price_yd: Math.round(defaultPriceYd * 1000) / 1000,
    default_price_kilo: Math.round(defaultPriceKilo * 1000) / 1000,
    default_price_lb: Math.round(defaultPriceLb * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}

async function computeManufacturing(input: any) {
  const samMinutesData = await loadCSV('sam_minutes_lookup.csv');
  const costRateData = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');

  const gender = normalizeString(input.gender);
  const silhouette = normalizeString(input.silhouette);
  const seam = normalizeString(input.seam);
  const size = normalizeString(input.size);
  const quantity = normalizeString(input.quantity);
  const coo = normalizeString(input.coo);

  let baseMinutes = 0;
  const samRow = samMinutesData.find(row =>
    normalizeString(row.gender).toLowerCase() === gender.toLowerCase() &&
    normalizeString(row.product).toLowerCase() === silhouette.toLowerCase() &&
    normalizeString(row.seam).toLowerCase() === seam.toLowerCase() &&
    normalizeString(row.size).toLowerCase() === size.toLowerCase()
  );
  if (samRow) {
    baseMinutes = toFloat(samRow.sam_minutes) || 0;
  }

  const costRateRow = costRateData.find(row =>
    normalizeString(row.country) === coo
  );
  const costRate = toFloat(costRateRow?.cost_rate) || 0;

  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range) === quantity
  );
  const efficiency = toFloat(efficiencyRow?.efficiency) || 0.738;

  let totalCost = 0;
  if (efficiency > 0 && baseMinutes > 0) {
    totalCost = (baseMinutes / efficiency) * costRate;
  }

  return {
    country: coo,
    minutes: Math.round(baseMinutes * 1000) / 1000,
    cost_rate: Math.round(costRate * 1000) / 1000,
    efficiency: Math.round(efficiency * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}

async function computeTotalCostSummary(params: any) {
  const sewingThreadData = await loadCSV('sewing_thread_cost.csv');

  const sewingThreadRow = sewingThreadData.find(row =>
    normalizeString(row.gender) === normalizeString(params.gender) &&
    normalizeString(row.silhouette) === normalizeString(params.silhouette)
  );
  const sewingThreadCost = toFloat(sewingThreadRow?.sewing_thread_cost) || 0;

  const total_fabric_cost = toFloat(params.fabric_cost) || 0;
  const total_trim_cost = toFloat(params.trim_cost) || 0;
  const total_display_packaging_cost = toFloat(params.display_packaging_cost) || 0;
  const total_transit_packaging_cost = toFloat(params.transit_packaging_cost) || 0;
  const total_label_cost = toFloat(params.label_cost) || 0;
  const total_sewing_thread_cost = sewingThreadCost;
  const total_labour_cost = toFloat(params.labour_cost) || 0;
  const total_product_testing_cost = toFloat(params.product_testing_cost) || 0;
  const total_print_embroidery_cost = toFloat(params.print_embroidery_cost) || 0;
  const total_other_cost = toFloat(params.other_cost) || 0;

  const subtotal =
    total_fabric_cost +
    total_trim_cost +
    total_display_packaging_cost +
    total_transit_packaging_cost +
    total_label_cost +
    total_sewing_thread_cost +
    total_labour_cost +
    total_product_testing_cost +
    total_print_embroidery_cost +
    total_other_cost;

  const marginDecimal = params.supplier_margin_percent / 100;
  const supplier_margin_amount = subtotal * marginDecimal;
  const fob_cost = subtotal + supplier_margin_amount;

  const freight_cost = toFloat(params.freight_cost) || 0;
  const gmo_cost = toFloat(params.gmo_cost) || 0;
  const duty_cost = toFloat(params.duty_cost) || 0;
  const grand_total = fob_cost + freight_cost + gmo_cost + duty_cost;

  const total_fob_per_piece = fob_cost;
  const total_fob_per_dozen = fob_cost * 12;
  const total_flc_per_piece = grand_total;
  const total_flc_per_dozen = grand_total * 12;

  const calcPct = (value: number) => (subtotal > 0 ? (value / subtotal) * 100 : 0);

  return {
    total_fabric_cost: Math.round(total_fabric_cost * 1000) / 1000,
    total_trim_cost: Math.round(total_trim_cost * 1000) / 1000,
    total_display_packaging_cost: Math.round(total_display_packaging_cost * 1000) / 1000,
    total_transit_packaging_cost: Math.round(total_transit_packaging_cost * 1000) / 1000,
    total_label_cost: Math.round(total_label_cost * 1000) / 1000,
    total_sewing_thread_cost: Math.round(total_sewing_thread_cost * 1000) / 1000,
    total_labour_cost: Math.round(total_labour_cost * 1000) / 1000,
    total_product_testing_cost: Math.round(total_product_testing_cost * 1000) / 1000,
    total_print_embroidery_cost: Math.round(total_print_embroidery_cost * 1000) / 1000,
    total_other_cost: Math.round(total_other_cost * 1000) / 1000,
    subtotal: Math.round(subtotal * 1000) / 1000,
    supplier_margin_percent: params.supplier_margin_percent,
    supplier_margin_amount: Math.round(supplier_margin_amount * 1000) / 1000,
    fob_cost: Math.round(fob_cost * 1000) / 1000,
    freight_cost: Math.round(freight_cost * 1000) / 1000,
    gmo_cost: Math.round(gmo_cost * 1000) / 1000,
    duty_cost: Math.round(duty_cost * 1000) / 1000,
    grand_total: Math.round(grand_total * 1000) / 1000,
    total_fob_per_piece: Math.round(total_fob_per_piece * 1000) / 1000,
    total_fob_per_dozen: Math.round(total_fob_per_dozen * 1000) / 1000,
    total_flc_per_piece: Math.round(total_flc_per_piece * 1000) / 1000,
    total_flc_per_dozen: Math.round(total_flc_per_dozen * 1000) / 1000,
    total_fabric_cost_pct: Math.round(calcPct(total_fabric_cost) * 100) / 100,
    total_trim_cost_pct: Math.round(calcPct(total_trim_cost) * 100) / 100,
    total_display_packaging_cost_pct: Math.round(calcPct(total_display_packaging_cost) * 100) / 100,
    total_transit_packaging_cost_pct: Math.round(calcPct(total_transit_packaging_cost) * 100) / 100,
    total_label_cost_pct: Math.round(calcPct(total_label_cost) * 100) / 100,
    total_sewing_thread_cost_pct: Math.round(calcPct(total_sewing_thread_cost) * 100) / 100,
    total_labour_cost_pct: Math.round(calcPct(total_labour_cost) * 100) / 100,
    total_product_testing_cost_pct: Math.round(calcPct(total_product_testing_cost) * 100) / 100,
    total_print_embroidery_cost_pct: Math.round(calcPct(total_print_embroidery_cost) * 100) / 100,
    total_other_cost_pct: Math.round(calcPct(total_other_cost) * 100) / 100,
    supplier_margin_amount_pct: Math.round(calcPct(supplier_margin_amount) * 100) / 100,
  };
}

const COMPARISON_COUNTRIES = ['INDIA', 'BANGLADESH', 'INDONESIA', 'THAILAND', 'CAMBODIA', 'VIETNAM'];

async function computeCountryComparison(params: any) {
  const results: any[] = [];

  for (const country of COMPARISON_COUNTRIES) {
    const mfgResult = await computeManufacturing({
      ...params,
      coo: country,
    });

    const summary = await computeTotalCostSummary({
      ...params,
      labour_cost: mfgResult.total_cost,
    });

    results.push({
      country,
      labour_cost: summary.total_labour_cost,
      subtotal: summary.subtotal,
      margin_amount: summary.supplier_margin_amount,
      fob_cost: summary.fob_cost,
    });
  }

  return results;
}

// Express app
const app = express();
const PORT = process.env.PORT || 8000;

// CORS configuration for production
app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? ['https://your-app-name.onrender.com']
    : ['http://localhost:5173', 'http://localhost:3000'],
  credentials: true
}));

app.use(express.json());

// Serve static files from client build
const clientBuildPath = path.join(__dirname, '../client/dist');
if (fs.existsSync(clientBuildPath)) {
  app.use(express.static(clientBuildPath));
}

async function loadDropdown(name: string): Promise<string[]> {
  const data = await loadCSV(`dropdown_${name}.csv`);
  return data.map(row => row.value).filter(v => v);
}

// API Routes
app.get('/api/dropdown/:name', async (req: Request, res: Response) => {
  try {
    const values = await loadDropdown(req.params.name);
    res.json({ values });
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/calculate', async (req: Request, res: Response) => {
  try {
    const input = req.body;

    // Calculate fabrication
    const fabricationResults = [];
    let totalFabricCost = 0;
    for (const fab of input.fabrication) {
      const result = await computeFabrication(fab);
      fabricationResults.push(result);
      totalFabricCost += result.total_cost;
    }

    // Calculate manufacturing
    const manufacturingResults = [await computeManufacturing({
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      seam: input.development.seam,
      size: input.development.size,
      quantity: input.development.ideal_quantity,
      coo: input.development.coo,
    })];

    const labourCost = manufacturingResults[0]?.total_cost || 0;

    // Calculate total cost summary
    const totalSummary = await computeTotalCostSummary({
      fabric_cost: totalFabricCost,
      trim_cost: 0,
      print_embroidery_cost: 0,
      display_packaging_cost: 0,
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

    // Calculate country comparison
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

    res.json({
      inputs: { development: input.development, fabrication: input.fabrication },
      outputs: {
        fabrication: { rows: fabricationResults, total_fabric_cost: totalFabricCost },
        trims: { rows: [] },
        embellishments: { rows: [] },
        packing_label: {
          display_packaging: { default_usage: 0, total: 0 },
          transit_package: { default_usage: 0, total: 0 },
          label: { default_usage: 0, total: 0 },
        },
        manufacturing: { rows: manufacturingResults },
        total_cost_summary: totalSummary,
        country_comparison: countryComparison,
      },
    });
  } catch (error: any) {
    console.error('Calculation error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve React app for all other routes (SPA)
app.get('*', (req: Request, res: Response) => {
  if (fs.existsSync(path.join(clientBuildPath, 'index.html'))) {
    res.sendFile(path.join(clientBuildPath, 'index.html'));
  } else {
    res.status(404).json({ error: 'Frontend not built' });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
});
