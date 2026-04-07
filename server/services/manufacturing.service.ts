import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<ManufacturingOutput> {
  const costRateData = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');
  const samProdEffData = await loadCSV('sam_product_eff.csv');

  const gender = normalizeString(input.gender);
  const silhouette = normalizeString(input.silhouette);
  const seam = normalizeString(input.seam);
  const size = normalizeString(input.size);
  const quantity = normalizeString(input.quantity);
  const coo = normalizeString(input.coo);

  // ─── SAM minutes + product efficiency ────────────────────────────────────
  // sam_product_eff.csv contains BOTH the SAM minutes (column: sam) AND the
  // product efficiency factor (column: eff_pct) in the same row.
  // Match on gender / product_shape / side_seam / size (case-insensitive).
  const prodEffRow = samProdEffData.find(row => {
    const rowGender   = normalizeString(row.gender        ?? '').toLowerCase();
    const rowProduct  = normalizeString(row.product_shape ?? '').toLowerCase();
    const rowSeam     = normalizeString(row.side_seam     ?? '').toLowerCase();
    const rowSize     = normalizeString(row.size          ?? '').toLowerCase();

    return (
      rowGender  === gender.toLowerCase()    &&
      rowProduct === silhouette.toLowerCase() &&
      rowSeam    === seam.toLowerCase()       &&
      rowSize    === size.toLowerCase()
    );
  });

  // BUG FIX: use sam column from sam_product_eff.csv for minutes
  const baseMinutes = toFloat(prodEffRow?.sam) || 0;

  // BUG FIX: apply product efficiency factor (e.g. 0.90 for Long Sleeve / Side Seam)
  // Excel formula: final_efficiency = base_efficiency × eff_pct
  const productEfficiency = toFloat(prodEffRow?.eff_pct) || 1.0;

  // ─── Cost rate ───────────────────────────────────────────────────────────
  const costRateRow = costRateData.find(row =>
    normalizeString(row.country).toLowerCase() === coo.toLowerCase()
  );
  const costRate = toFloat(costRateRow?.cost_rate) || 0;

  // ─── Base efficiency by quantity range ──────────────────────────────────
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range).toLowerCase() === quantity.toLowerCase()
  );
  const baseEfficiency = toFloat(efficiencyRow?.efficiency) || 0.738;

  // ─── Final efficiency = base × product factor ────────────────────────────
  // Example: 0.70 (base for 3,001–10,000 pcs) × 0.90 (Long Sleeve / Side Seam) = 0.63
  const efficiency = baseEfficiency * productEfficiency;

  // ─── Total cost: (minutes / efficiency) × cost_rate ─────────────────────
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
    const result = await computeManufacturing(input);
    return [result];
  }

  const results: ManufacturingOutput[] = [];
  const countries = costRateData
    .map(row => normalizeString(row.country))
    .filter(c => c);

  for (const country of countries) {
    const result = await computeManufacturing({ ...input, coo: country });
    results.push(result);
  }

  return results;
}
