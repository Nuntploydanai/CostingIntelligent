import express, { Request, Response } from 'express';
import cors from 'cors';
import path from 'path';
import fs from 'fs';
import csv from 'csv-parser';

// Utility functions
// Try multiple possible locations for data
let DATA_DIR = path.join(__dirname, '../data/master_clean');
if (!fs.existsSync(DATA_DIR)) {
  DATA_DIR = path.join(__dirname, './data/master_clean');
}
if (!fs.existsSync(DATA_DIR)) {
  DATA_DIR = path.join(process.cwd(), 'data/master_clean');
}

console.log('📁 Data directory:', DATA_DIR);
console.log('📁 Exists:', fs.existsSync(DATA_DIR));

async function loadCSV(filename: string): Promise<any[]> {
  return new Promise((resolve, reject) => {
    const results: any[] = [];
    const filePath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filePath)) {
      console.log('❌ File not found:', filePath);
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

// ==================== FABRICATION ====================
function normPriceUnit(u: string): string {
  return normalizeString(u).toLowerCase();
}

function conversionPriceYdKilo(args: {
  fabric_type: string;
  price_lb: number | null;
  price_unit: string;
  price_value: number | null;
  weight_gsm: number;
  fabric_finishing: string;
  color_design: string;
}): [number | string, number | string] {
  const { fabric_type, price_lb, price_unit, price_value, weight_gsm, fabric_finishing, color_design } = args;
  if ((price_lb == null && price_value == null) || !fabric_type || weight_gsm === 0) return ['-', 0.0];

  const B2 = 60.0;
  const B3 = weight_gsm;
  const J2 = B2;
  const J3 = weight_gsm;
  const K3 = J2 * 0.0254;
  const L3 = J3 / 1000.0;
  const K13 = L3 * K3;

  const A24 = price_lb ?? 0.0;
  const C3 = B2 * 0.0254;
  const D3 = B3 / 1000.0;
  const C13 = D3 * C3;
  const C11 = C13 * 2.20462262;
  const C4 = C3 * D3 * 35.274;

  let C23 = A24;
  if (price_value != null) {
    const unit = normPriceUnit(price_unit);
    let C24 = A24;
    if (unit.includes('yd')) C24 = price_value;
    else if (unit.includes('kg')) C24 = price_value * C13 * 0.9144;
    else if (unit.includes('meter')) C24 = price_value * 0.9144;
    else if (unit.includes('lb')) C24 = price_value * C11 * 0.9144;
    else if (unit.includes('ounce')) C24 = price_value * C4 * 0.9144;
    C23 = C24;
  }

  const E23 = (C23 / 0.9144) / C13;
  const V4 = weight_gsm;
  const V5 = (V4 * 1.19599) * 1.6667;
  const finishingLookup: Record<string, number> = {
    'Wicking': 0.06615,
    'Odor Control': 0.11025,
    'Xtemp': 0.33075,
    'Odor Control + Wicking': 0.1764,
    'Xtemp + Odor Control': 0.441,
    'None': 0.0,
    'OTHER': 0.0,
  };
  const T4 = finishingLookup[normalizeString(fabric_finishing)] ?? 0.0;
  const V6 = V5 * T4 / 1000.0;
  const K16 = E23 + V6;
  const M16 = (K16 * K13) * 0.9144;

  const cd = normalizeString(color_design);
  const V18 = cd === 'Solid' ? 1.0 : cd === 'white' ? 0.95 : cd === 'Heather' ? 1.1 : cd === 'Others' ? 1.07 : 0.0;

  const M18 = (M16 + V6) * V18;
  const O18 = M18;
  const denom = J3 * 1.3946 / 1000.0;
  const K20 = denom !== 0 ? O18 / denom : 0.0;
  return [Math.round(O18 * 1000) / 1000, Math.round(K20 * 1000) / 1000];
}

async function computeFabrication(input: any) {
  const fabricPriceLookup = await loadCSV('fabric_price_lookup.csv');
  const keyMapRows = await loadCSV('product_part_key_map.csv');
  const usageRows = await loadCSV('fabric_usage_lookup.csv');

  const fabric_type = normalizeString(input.fabric_type);
  const fabric_contents = normalizeString(input.fabric_contents);
  const using_part = normalizeString(input.using_part);
  const material_coo = normalizeString(input.material_coo);
  const silhouette = normalizeString(input.silhouette);
  const seam = normalizeString(input.seam);
  const gender = normalizeString(input.gender);
  const size = normalizeString(input.size);

  const key = `${fabric_type}${fabric_contents}`;
  const defaultPriceLb = toFloat((fabricPriceLookup.find(r => normalizeString(r.key) === key) || {}).value);
  const overrideVal = toFloat(input.price_value);

  const fixedFabricWidth = using_part ? 60.0 : 0.0;

  const defaultGsmMap: Record<string, number> = {
    Jersey: 160.0,
    Rib1x1: 180.0,
    Rib2x1: 180.0,
    Mesh: 150.0,
    Fleece: 220.0,
  };

  const weightInput = toFloat(input.weight_gsm_override);
  const defaultWeightDisplay = weightInput != null ? 0 : (defaultGsmMap[fabric_type] ?? 0);
  const effectiveGsm = weightInput ?? defaultWeightDisplay ?? 0;

  const [defaultPriceYd, defaultPriceKilo] = conversionPriceYdKilo({
    fabric_type,
    price_lb: defaultPriceLb,
    price_unit: normalizeString(input.price_unit || 'Price / Lbs'),
    price_value: overrideVal,
    weight_gsm: effectiveGsm,
    fabric_finishing: normalizeString(input.fabric_finishing || ''),
    color_design: normalizeString(input.color_design || 'Solid'),
  });

  const k7Key = normalizeString((keyMapRows.find(r => normalizeString(r.silhouette) === silhouette && normalizeString(r.seam) === seam) || {}).k7_key);
  let usageVal: number | null = null;
  if (fabric_contents && k7Key && using_part) {
    usageVal = toFloat((usageRows.find(r => normalizeString(r.k7_key) === k7Key && normalizeString(r.using_part) === using_part) || {}).usage);
  }

  const genderMult = gender.toUpperCase() === 'MEN' ? 1 : gender.toUpperCase() === 'WOMEN' ? 0.85 : gender.toUpperCase() === 'KIDS' ? 0.75 : 0;
  const sizeMult = size.toUpperCase() === 'S-XL' ? 1 : size.toUpperCase() === '2XL-3XL' ? 1.15 : size.toUpperCase() === 'S-3XL' ? 1.1 : 0;
  const silhouetteMult = 1.0;
  const importFactor = material_coo === 'Domestic' ? 1 : material_coo === 'Import' ? 1.05 : 0;

  let totalCost = 0;
  if (usageVal != null && typeof defaultPriceYd === 'number') {
    const U7 = usageVal * genderMult;
    const V7 = U7 * sizeMult;
    const W7 = V7 * silhouetteMult;
    const X7 = W7 * defaultPriceYd;
    const Y7 = X7 * importFactor;
    totalCost = Math.round(Y7 * 1000) / 1000;
  }

  return {
    fixed_fabric_width: Math.round(fixedFabricWidth * 1000) / 1000,
    default_weight_gsm: Math.round((defaultWeightDisplay || 0) * 1000) / 1000,
    default_price_yd: typeof defaultPriceYd === 'number' ? defaultPriceYd : 0,
    default_price_kilo: typeof defaultPriceKilo === 'number' ? defaultPriceKilo : 0,
    default_price_lb: Math.round((defaultPriceLb || 0) * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}

// ==================== TRIMS ====================
async function computeTrims(input: any) {
  const trimsPriceData = await loadCSV('packing_trims_item_price_unit.csv');
  const trimsUsageData = await loadCSV('packing_trims_usage.csv');

  const trimsType = normalizeString(input.trims_type);
  const garmentPart = normalizeString(input.garment_part);

  const priceRow = trimsPriceData.find(row =>
    normalizeString(row.trims_type) === trimsType
  );
  const defaultPriceEach = toFloat(priceRow?.default_price_each) || 0;

  const usageRow = trimsUsageData.find(row =>
    normalizeString(row.trims_type) === trimsType &&
    normalizeString(row.garment_part) === garmentPart
  );
  const defaultUsage = toFloat(usageRow?.usage_small) || 0;

  const usage = toFloat(input.usage_override) || defaultUsage;
  const priceEach = toFloat(input.price_override) || defaultPriceEach;

  const totalCost = usage * priceEach;

  const unit = priceRow?.unit || 'pcs';

  return {
    unit,
    default_usage: Math.round(defaultUsage * 1000) / 1000,
    default_price_each: Math.round(defaultPriceEach * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}

// ==================== EMBELLISHMENTS ====================
async function computeEmbellishment(input: any) {
  const embellishmentPriceData = await loadCSV('print_embroidery_price_lookup.csv');

  const printingType = normalizeString(input.printing_embroidery);
  const dimension = normalizeString(input.dimension);

  const priceRow = embellishmentPriceData.find(row =>
    normalizeString(row.printing_embroidery) === printingType &&
    normalizeString(row.dimension) === dimension
  );

  const defaultPriceEach = toFloat(priceRow?.price_each) || 0;
  const usage = toFloat(input.usage_unit) || 1;

  const totalCost = usage * defaultPriceEach;

  return {
    default_price_each: Math.round(defaultPriceEach * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}

// ==================== PACKING & LABEL ====================
async function computePackingLabel(input: any) {
  const displayPackagingData = await loadCSV('label_display_packaging_price.csv');

  const packCount = toFloat(input.pack_count) || 1;

  const displayPackagingRow = displayPackagingData.find(row =>
    normalizeString(row.display_packaging) === normalizeString(input.display_packaging)
  );
  const displayPackagingDefaultPrice = toFloat(displayPackagingRow?.price) || 0;
  const displayPackagingDefaultUsage = 1 / packCount;
  const displayPackagingTotal = displayPackagingDefaultUsage * displayPackagingDefaultPrice;

  const transitPackageValue = toFloat(input.transit_package) ?? 0;
  const transitPackageDefaultUsage = transitPackageValue > 0 ? 1 : 0;
  const transitPackageTotal = transitPackageValue > 0 ? (0.9 / transitPackageValue) : 0;

  const labelDefaultUsage = input.label_type ? 1 : 0;
  const labelBaseMap: { [key: string]: number } = {
    'pad print': 0.0085,
    'heat transfer': 0.03,
    'woven label': 0.028,
  };
  const labelBase = labelBaseMap[normalizeString(input.label_type).toLowerCase()] || 0;
  const labelTotal = input.label_type ? (labelBase * 1.03) : 0;

  return {
    display_packaging: {
      default_usage: Math.round(displayPackagingDefaultUsage * 1000) / 1000,
      total: Math.round(displayPackagingTotal * 1000) / 1000,
    },
    transit_package: {
      default_usage: transitPackageDefaultUsage,
      total: Math.round(transitPackageTotal * 1000) / 1000,
    },
    label: {
      default_usage: labelDefaultUsage,
      total: Math.round(labelTotal * 1000) / 1000,
    },
  };
}

// ==================== MANUFACTURING ====================
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

// ==================== TOTAL COST SUMMARY ====================
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
  const total_product_testing_cost = 0.01;
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

// ==================== COUNTRY COMPARISON ====================
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

// ==================== EXPRESS SERVER ====================
const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors({
  origin: ['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173'],
  credentials: true
}));

app.use(express.json());

// Load dropdown data (with aliases to match Python/web UI names)
const DROPDOWN_ALIASES: Record<string, string> = {
  silhouette: 'silhouette_pattern',
  color_design: 'color',
  ideal_quantity: 'quantity',
  pack_count: 'packing_no',
  garment_part_trim: 'garment_part_trim',
};

function pickDropdownValue(row: any): string {
  const direct = (row?.value ?? '').toString().trim();
  if (direct) return direct;
  // fallback: first non-empty cell in the row
  for (const v of Object.values(row || {})) {
    const s = (v ?? '').toString().trim();
    if (s) return s;
  }
  return '';
}

async function loadDropdown(name: string): Promise<string[]> {
  const realName = DROPDOWN_ALIASES[name] || name;
  const data = await loadCSV(`dropdown_${realName}.csv`);
  const values = data.map(pickDropdownValue).filter(Boolean);
  // de-dup while preserving order
  return [...new Set(values)];
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

// Main calculation endpoint
app.post('/api/calculate', async (req: Request, res: Response) => {
  try {
    const input = req.body;

    // 1. Calculate fabrication
    const fabricationResults = [];
    let totalFabricCost = 0;
    for (const fab of input.fabrication) {
      const result = await computeFabrication({
        ...fab,
        silhouette: input.development?.silhouette,
        seam: input.development?.seam,
        gender: input.development?.gender,
        size: input.development?.size,
        fabric_finishing: input.development?.fabric_finishing,
        color_design: input.development?.color_design,
      });
      fabricationResults.push(result);
      totalFabricCost += result.total_cost;
    }

    // 2. Calculate trims
    const trimsResults = [];
    let totalTrimCost = 0;
    for (const trim of input.trims) {
      const result = await computeTrims(trim);
      trimsResults.push(result);
      totalTrimCost += result.total_cost;
    }

    // 3. Calculate embellishments
    const embellishmentResults = [];
    let totalEmbellishmentCost = 0;
    for (const emb of input.embellishments) {
      const result = await computeEmbellishment(emb);
      embellishmentResults.push(result);
      totalEmbellishmentCost += result.total_cost;
    }

    // 4. Calculate packing & label
    const packingLabelResult = await computePackingLabel(input.packing_label || {});
    const totalDisplayPackagingCost = packingLabelResult.display_packaging.total;
    const totalTransitPackagingCost = packingLabelResult.transit_package.total;
    const totalLabelCost = packingLabelResult.label.total;

    // 5. Calculate manufacturing
    const manufacturingResult = await computeManufacturing({
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      seam: input.development.seam,
      size: input.development.size,
      quantity: input.development.ideal_quantity,
      coo: input.development.coo,
    });
    const labourCost = manufacturingResult.total_cost;

    // 6. Calculate total cost summary
    const totalSummary = await computeTotalCostSummary({
      fabric_cost: totalFabricCost,
      trim_cost: totalTrimCost,
      print_embroidery_cost: totalEmbellishmentCost,
      display_packaging_cost: totalDisplayPackagingCost,
      transit_packaging_cost: totalTransitPackagingCost,
      label_cost: totalLabelCost,
      labour_cost: labourCost,
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      size: input.development.size,
      supplier_margin_percent: input.supplier_margin_percent,
      other_cost: input.additional_cost,
      freight_cost: input.freight_cost,
      gmo_cost: input.gmo_cost,
      duty_cost: input.duty_cost,
    });

    // 7. Calculate country comparison
    const countryComparison = await computeCountryComparison({
      fabric_cost: totalFabricCost,
      trim_cost: totalTrimCost,
      print_embroidery_cost: totalEmbellishmentCost,
      display_packaging_cost: totalDisplayPackagingCost,
      transit_packaging_cost: totalTransitPackagingCost,
      label_cost: totalLabelCost,
      gender: input.development.gender,
      silhouette: input.development.silhouette,
      seam: input.development.seam,
      size: input.development.size,
      quantity: input.development.ideal_quantity,
      supplier_margin_percent: input.supplier_margin_percent,
      other_cost: input.additional_cost,
      freight_cost: input.freight_cost,
      gmo_cost: input.gmo_cost,
      duty_cost: input.duty_cost,
    });

    res.json({
      inputs: { development: input.development, fabrication: input.fabrication },
      outputs: {
        fabrication: { rows: fabricationResults, total_fabric_cost: totalFabricCost },
        trims: { rows: trimsResults, total_trim_cost: totalTrimCost },
        embellishments: { rows: embellishmentResults, total_embellishment_cost: totalEmbellishmentCost },
        packing_label: packingLabelResult,
        manufacturing: { rows: [manufacturingResult] },
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

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 API: http://localhost:${PORT}/api/calculate`);
});
