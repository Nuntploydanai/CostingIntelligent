import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<ManufacturingOutput> {
  const samMinutesData = await loadCSV('sam_minutes_lookup.csv');
  const costRateData = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');
  const samProdEffData = await loadCSV('sam_product_eff.csv');

  const gender = normalizeString(input.gender);
  const silhouette = normalizeString(input.silhouette);
  const seam = normalizeString(input.seam);
  const size = normalizeString(input.size);
  const quantity = normalizeString(input.quantity);
  const coo = normalizeString(input.coo);

  // Find SAM minutes
  let baseMinutes = 0;
  const samRow = samMinutesData.find(row =>
    normalizeString(row.gender) === gender &&
    normalizeString(row.product) === silhouette &&
    normalizeString(row.seam) === seam &&
    normalizeString(row.size) === size
  );
  if (samRow) {
    baseMinutes = toFloat(samRow.sam_minutes) || 0;
  } else {
    const samRowCI = samMinutesData.find(row =>
      normalizeString(row.gender).toLowerCase() === gender.toLowerCase() &&
      normalizeString(row.product).toLowerCase() === silhouette.toLowerCase() &&
      normalizeString(row.seam).toLowerCase() === seam.toLowerCase() &&
      normalizeString(row.size).toLowerCase() === size.toLowerCase()
    );
    if (samRowCI) {
      baseMinutes = toFloat(samRowCI.sam_minutes) || 0;
    }
  }

  // Find cost rate for country
  const costRateRow = costRateData.find(row =>
    normalizeString(row.country) === coo
  );
  const costRate = toFloat(costRateRow?.cost_rate) || 0;

  // Find BASE efficiency by quantity range
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range) === quantity
  );
  const baseEfficiency = toFloat(efficiencyRow?.efficiency) || 0.738;

  // BUG FIX: Find product efficiency factor from sam_product_eff.csv
  // Excel: final_efficiency = base_efficiency × eff_pct (by gender/silhouette/seam/size)
  const prodEffRow = samProdEffData.find(row =>
    normalizeString(row.gender).toLowerCase() === gender.toLowerCase() &&
    normalizeString(row.product_shape).toLowerCase() === silhouette.toLowerCase() &&
    normalizeString(row.side_seam).toLowerCase() === seam.toLowerCase() &&
    normalizeString(row.size).toLowerCase() === size.toLowerCase()
  );
  const productEfficiency = toFloat(prodEffRow?.eff_pct) || 1.0;

  // Final efficiency = base × product factor (e.g. 0.70 × 0.90 = 0.63)
  const efficiency = baseEfficiency * productEfficiency;

  // Calculate total cost: (minutes / efficiency) * cost_rate
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
