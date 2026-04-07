import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<ManufacturingOutput> {
  const costRateData   = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');
  const samProdEffData = await loadCSV('sam_product_eff.csv');

  // Normalise all input strings (trim whitespace only)
  const gender     = normalizeString(input.gender    ?? '');
  const silhouette = normalizeString(input.silhouette ?? '');
  const seam       = normalizeString(input.seam       ?? '');
  const size       = normalizeString(input.size       ?? '');
  const quantity   = normalizeString(input.quantity   ?? '');
  const coo        = normalizeString(input.coo        ?? '');

  // ── Lookup row in sam_product_eff.csv ─────────────────────────────────────
  // Columns: gender | product_shape | side_seam | size | sam | eff_pct
  // Compare case-insensitively to handle any capitalisation differences.
  const prodRow = samProdEffData.find(row =>
    normalizeString(row.gender        ?? '').toLowerCase() === gender.toLowerCase()     &&
    normalizeString(row.product_shape ?? '').toLowerCase() === silhouette.toLowerCase() &&
    normalizeString(row.side_seam     ?? '').toLowerCase() === seam.toLowerCase()       &&
    normalizeString(row.size          ?? '').toLowerCase() === size.toLowerCase()
  );

  // SAM minutes — comes from the `sam` column of sam_product_eff.csv
  const baseMinutes = toFloat(prodRow?.sam) ?? 0;

  // Product efficiency factor — e.g. 0.9 for Long Sleeve Shirt / Side Seam
  // Defaults to 1.0 if the row is not found (neutral — no adjustment)
  const productEfficiency = toFloat(prodRow?.eff_pct) ?? 1.0;

  // ── Cost rate for the selected country ───────────────────────────────────
  const costRateRow = costRateData.find(row =>
    normalizeString(row.country ?? '').toLowerCase() === coo.toLowerCase()
  );
  const costRate = toFloat(costRateRow?.cost_rate) ?? 0;

  // ── Base efficiency from quantity range ───────────────────────────────────
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range ?? '').toLowerCase() === quantity.toLowerCase()
  );
  const baseEfficiency = toFloat(efficiencyRow?.efficiency) ?? 0.738;

  // ── Final efficiency = base × product factor ──────────────────────────────
  // Example: 0.70 (3,001–10,000 pcs) × 0.90 (Long Sleeve / Side Seam) = 0.63
  const efficiency = baseEfficiency * productEfficiency;

  // ── Total manufacturing cost ──────────────────────────────────────────────
  let totalCost = 0;
  if (efficiency > 0 && baseMinutes > 0) {
    totalCost = (baseMinutes / efficiency) * costRate;
  }

  return {
    country:    coo,
    minutes:    Math.round(baseMinutes  * 1000) / 1000,
    cost_rate:  Math.round(costRate     * 1000) / 1000,
    efficiency: Math.round(efficiency   * 1000) / 1000,
    total_cost: Math.round(totalCost    * 1000) / 1000,
  };
}

export async function computeAllManufacturing(
  input: ManufacturingInput
): Promise<ManufacturingOutput[]> {
  const costRateData = await loadCSV('cost_rate.csv');

  if (input.coo) {
    return [await computeManufacturing(input)];
  }

  const countries = costRateData
    .map(row => normalizeString(row.country ?? ''))
    .filter(c => c);

  const results: ManufacturingOutput[] = [];
  for (const country of countries) {
    results.push(await computeManufacturing({ ...input, coo: country }));
  }
  return results;
}
