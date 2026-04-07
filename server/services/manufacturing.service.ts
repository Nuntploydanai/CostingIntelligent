import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<ManufacturingOutput> {
  const costRateData    = await loadCSV('cost_rate.csv');
  const efficiencyData  = await loadCSV('efficiency_by_quantity.csv');
  const samProdEffData  = await loadCSV('sam_product_eff.csv');
  const samMinutesData  = await loadCSV('sam_minutes_lookup.csv');

  const gender    = normalizeString(input.gender);
  const silhouette = normalizeString(input.silhouette);
  const seam      = normalizeString(input.seam);
  const size      = normalizeString(input.size);
  const quantity  = normalizeString(input.quantity);
  const coo       = normalizeString(input.coo);

  // ── DEBUG: log first row of sam_product_eff.csv to verify column names ──
  if (samProdEffData.length > 0) {
    console.log('[DEBUG] sam_product_eff.csv columns:', Object.keys(samProdEffData[0]));
    console.log('[DEBUG] sam_product_eff.csv first row:', samProdEffData[0]);
  }
  console.log('[DEBUG] Looking for → gender:', gender, '| silhouette:', silhouette, '| seam:', seam, '| size:', size);

  // ── Find product efficiency (eff_pct) + SAM minutes from sam_product_eff.csv ──
  // Try matching with multiple possible column name variants
  const prodEffRow = samProdEffData.find(row => {
    const keys = Object.keys(row);
    // detect actual column names dynamically
    const productKey = keys.find(k => k.toLowerCase().includes('product')) || 'product_shape';
    const seamKey    = keys.find(k => k.toLowerCase().includes('seam'))    || 'side_seam';

    const rowGender  = normalizeString(row.gender           ?? '').toLowerCase();
    const rowProduct = normalizeString(row[productKey]      ?? '').toLowerCase();
    const rowSeam    = normalizeString(row[seamKey]         ?? '').toLowerCase();
    const rowSize    = normalizeString(row.size             ?? '').toLowerCase();

    console.log('[DEBUG] Comparing row:', { rowGender, rowProduct, rowSeam, rowSize },
      'vs input:', { gender: gender.toLowerCase(), silhouette: silhouette.toLowerCase(), seam: seam.toLowerCase(), size: size.toLowerCase() });

    return (
      rowGender  === gender.toLowerCase()     &&
      rowProduct === silhouette.toLowerCase() &&
      rowSeam    === seam.toLowerCase()       &&
      rowSize    === size.toLowerCase()
    );
  });

  console.log('[DEBUG] prodEffRow found:', prodEffRow);

  // SAM minutes: try sam_product_eff.csv first, fall back to sam_minutes_lookup.csv
  let baseMinutes = toFloat(prodEffRow?.sam) || 0;
  if (!baseMinutes) {
    const samRow = samMinutesData.find(row => {
      const keys = Object.keys(row);
      const productKey = keys.find(k => k.toLowerCase().includes('product')) || 'product';
      const seamKey    = keys.find(k => k.toLowerCase().includes('seam'))    || 'seam';
      return (
        normalizeString(row.gender         ?? '').toLowerCase() === gender.toLowerCase()     &&
        normalizeString(row[productKey]    ?? '').toLowerCase() === silhouette.toLowerCase() &&
        normalizeString(row[seamKey]       ?? '').toLowerCase() === seam.toLowerCase()       &&
        normalizeString(row.size          ?? '').toLowerCase() === size.toLowerCase()
      );
    });
    baseMinutes = toFloat(samRow?.sam_minutes) || toFloat(samRow?.sam) || 0;
    console.log('[DEBUG] sam_minutes_lookup fallback row:', samRow, '→ minutes:', baseMinutes);
  }

  // Product efficiency factor (e.g. 0.9 for Long Sleeve / Side Seam)
  const productEfficiency = toFloat(prodEffRow?.eff_pct) || 1.0;

  // ── Cost rate ────────────────────────────────────────────────────────────
  const costRateRow = costRateData.find(row =>
    normalizeString(row.country).toLowerCase() === coo.toLowerCase()
  );
  const costRate = toFloat(costRateRow?.cost_rate) || 0;

  // ── Base efficiency by quantity range ────────────────────────────────────
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range).toLowerCase() === quantity.toLowerCase()
  );
  const baseEfficiency = toFloat(efficiencyRow?.efficiency) || 0.738;

  // ── Final efficiency = base × product factor ──────────────────────────
  // e.g. 0.70 × 0.90 = 0.63
  const efficiency = baseEfficiency * productEfficiency;

  console.log('[DEBUG] baseEfficiency:', baseEfficiency, '| productEfficiency:', productEfficiency, '| final efficiency:', efficiency);
  console.log('[DEBUG] baseMinutes:', baseMinutes, '| costRate:', costRate, '| totalCost:', (baseMinutes / efficiency) * costRate);

  // ── Total cost ────────────────────────────────────────────────────────────
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
