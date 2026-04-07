import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<any> {
  const costRateData   = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');
  const samProdEffData = await loadCSV('sam_product_eff.csv');
  const samMinutesData = await loadCSV('sam_minutes_lookup.csv');

  const gender     = normalizeString(input.gender);
  const silhouette = normalizeString(input.silhouette);
  const seam       = normalizeString(input.seam);
  const size       = normalizeString(input.size);
  const quantity   = normalizeString(input.quantity);
  const coo        = normalizeString(input.coo);

  // ── Product efficiency + SAM minutes from sam_product_eff.csv ────────────
  const prodEffRow = samProdEffData.find(row => {
    const keys = Object.keys(row);
    const productKey = keys.find(k => k.toLowerCase().includes('product')) || 'product_shape';
    const seamKey    = keys.find(k => k.toLowerCase().includes('seam'))    || 'side_seam';
    return (
      normalizeString(row.gender        ?? '').toLowerCase() === gender.toLowerCase()     &&
      normalizeString(row[productKey]   ?? '').toLowerCase() === silhouette.toLowerCase() &&
      normalizeString(row[seamKey]      ?? '').toLowerCase() === seam.toLowerCase()       &&
      normalizeString(row.size          ?? '').toLowerCase() === size.toLowerCase()
    );
  });

  // SAM minutes: from sam_product_eff.csv (sam column), fallback to sam_minutes_lookup.csv
  let baseMinutes = toFloat(prodEffRow?.sam) || 0;
  let minutesSource = 'sam_product_eff';
  if (!baseMinutes) {
    const samRow = samMinutesData.find(row => {
      const keys = Object.keys(row);
      const productKey = keys.find(k => k.toLowerCase().includes('product')) || 'product';
      const seamKey    = keys.find(k => k.toLowerCase().includes('seam'))    || 'seam';
      return (
        normalizeString(row.gender      ?? '').toLowerCase() === gender.toLowerCase()     &&
        normalizeString(row[productKey] ?? '').toLowerCase() === silhouette.toLowerCase() &&
        normalizeString(row[seamKey]    ?? '').toLowerCase() === seam.toLowerCase()       &&
        normalizeString(row.size        ?? '').toLowerCase() === size.toLowerCase()
      );
    });
    baseMinutes = toFloat(samRow?.sam_minutes) || toFloat(samRow?.sam) || 0;
    minutesSource = 'sam_minutes_lookup';
  }

  const productEfficiency = toFloat(prodEffRow?.eff_pct) || 1.0;

  // ── Cost rate ─────────────────────────────────────────────────────────────
  const costRateRow = costRateData.find(row =>
    normalizeString(row.country).toLowerCase() === coo.toLowerCase()
  );
  const costRate = toFloat(costRateRow?.cost_rate) || 0;

  // ── Base efficiency by quantity ────────────────────────────────────────────
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range).toLowerCase() === quantity.toLowerCase()
  );
  const baseEfficiency = toFloat(efficiencyRow?.efficiency) || 0.738;

  // ── Final efficiency = base × product factor ───────────────────────────────
  const efficiency = baseEfficiency * productEfficiency;

  let totalCost = 0;
  if (efficiency > 0 && baseMinutes > 0) {
    totalCost = (baseMinutes / efficiency) * costRate;
  }

  // ── TEMPORARY DEBUG: included in response so you can read in browser ───────
  const _debug = {
    sam_product_eff_rows: samProdEffData.length,
    sam_product_eff_first_row: samProdEffData[0] || null,
    prod_eff_row_found: !!prodEffRow,
    prod_eff_row: prodEffRow || null,
    input_received: { gender, silhouette, seam, size, quantity, coo },
    base_efficiency: baseEfficiency,
    product_efficiency: productEfficiency,
    final_efficiency: efficiency,
    minutes_source: minutesSource,
  };

  return {
    country:    coo,
    minutes:    Math.round(baseMinutes  * 1000) / 1000,
    cost_rate:  Math.round(costRate     * 1000) / 1000,
    efficiency: Math.round(efficiency   * 1000) / 1000,
    total_cost: Math.round(totalCost    * 1000) / 1000,
    _debug,
  };
}

export async function computeAllManufacturing(
  input: ManufacturingInput
): Promise<any[]> {
  const costRateData = await loadCSV('cost_rate.csv');

  if (input.coo) {
    const result = await computeManufacturing(input);
    return [result];
  }

  const results: any[] = [];
  const countries = costRateData
    .map(row => normalizeString(row.country))
    .filter(c => c);

  for (const country of countries) {
    const result = await computeManufacturing({ ...input, coo: country });
    results.push(result);
  }

  return results;
}
