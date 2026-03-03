import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { ManufacturingInput, ManufacturingOutput } from '../types';

export async function computeManufacturing(input: ManufacturingInput): Promise<ManufacturingOutput> {
  // Load CSV data
  const samMinutesData = await loadCSV('sam_minutes_lookup.csv');
  const costRateData = await loadCSV('cost_rate.csv');
  const efficiencyData = await loadCSV('efficiency_by_quantity.csv');

  // Normalize inputs
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
    // Try case-insensitive match
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

  // Find efficiency based on quantity
  const efficiencyRow = efficiencyData.find(row =>
    normalizeString(row.quantity_range) === quantity
  );
  const efficiency = toFloat(efficiencyRow?.efficiency) || 0.738; // Default to 0.738

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
  // Load all countries
  const costRateData = await loadCSV('cost_rate.csv');

  // If COO is specified, only return that country
  if (input.coo) {
    const result = await computeManufacturing(input);
    return [result];
  }

  // Otherwise, return ALL countries for comparison
  const results: ManufacturingOutput[] = [];
  const countries = costRateData
    .map(row => normalizeString(row.country))
    .filter(c => c); // Remove empty strings

  for (const country of countries) {
    const result = await computeManufacturing({
      ...input,
      coo: country,
    });
    results.push(result);
  }

  return results;
}
