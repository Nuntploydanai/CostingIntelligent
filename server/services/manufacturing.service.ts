import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<ManufacturingOutput> {
  const costRateData   = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');
  const samProdEffData = await loadCSV('sam_product_eff.csv');

  // --- Normalize all input strings (trim whitespace only) ---
  const gender     = normalizeString(input.gender     ?? '');
  const silhouette = normalizeString(input.silhouette ?? '');
  const seam       = normalizeString(input.seam       ?? '');
  const size       = normalizeString(input.size       ?? '');
  const quantity   = normalizeString(input.quantity   ?? '');
  const coo        = normalizeString(input.coo        ?? '');

  // --- DEBUG: Log what the server actually receives ---
  console.log('[MFG] Input received:', JSON.stringify({ gender, silhouette, seam, size, quantity, coo }));
  console.log('[MFG] sam_product_eff rows loaded:', samProdEffData.length);
  if (samProdEffData.length > 0) {
    console.log('[MFG] First CSV row sample:', JSON.stringify(samProdEffData[0]));
  }

  // --- Lookup row in sam_product_eff.csv ---
  // Columns: gender | product_shape | side_seam | size | sam | eff_pct
  const prodRow = samProdEffData.find(row =>
    normalizeString(row.gender        ?? '').toLowerCase() === gender.toLowerCase()     &&
    normalizeString(row.product_shape ?? '').toLowerCase() === silhouette.toLowerCase() &&
    normalizeString(row.side_seam     ?? '').toLowerCase() === seam.toLowerCase()       &&
    normalizeString(row.size          ?? '').toLowerCase() === size.toLowerCase()
  );

  // --- DEBUG: Show what was found (or not) ---
  console.log('[MFG] prodRow found:', JSON.stringify(prodRow ?? null));

  // SAM minutes and product efficiency factor from same row
  const baseMinutes       = toFloat(prodRow?.sam)     ?? 0;
  const productEfficiency = toFloat(prodRow?.eff_pct) ?? 1.0;

  console.log('[MFG] baseMinutes:', baseMinutes, '| productEfficiency:', productEfficiency);

  // --- Cost rate for selected country ---
  const costRateRow = costRateData.find(row =>
    normalizeString(row.country ?? '').toLowerCase() === coo.toLowerCase()
  );
  const costRate = toFloat(costRateRow?.cost_rate) ?? 0;

  // --- Base efficiency from quantity range ---
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range ?? '').toLowerCase() === quantity.toLowerCase()
  );
  const baseEfficiency = toFloat(efficiencyRow?.efficiency) ?? 0.738;

  // --- Final efficiency = base x product factor ---
  // Example: 0.70 (3,001-10,000 pcs) x 0.90 (Long Sleeve / Side Seam) = 0.63
  const efficiency = baseEfficiency * productEfficiency;

  console.log('[MFG] baseEfficiency:', baseEfficiency, '| final efficiency:', efficiency);

  // --- Total manufacturing cost ---
  let totalCost = 0;
  if (efficiency > 0 && baseMinutes > 0) {
    totalCost = (baseMinutes / efficiency) * costRate;
  }

  console.log('[MFG] costRate:', costRate, '| totalCost:', totalCost);

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
