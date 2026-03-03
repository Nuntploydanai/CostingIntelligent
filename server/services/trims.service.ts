import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { TrimsInput, TrimsOutput } from '../types';

export async function computeTrims(input: TrimsInput): Promise<TrimsOutput> {
  // Load CSV data
  const trimsUsageData = await loadCSV('dropdown_trims_usage.csv');
  const trimsPriceData = await loadCSV('dropdown_trims_price.csv');

  const trimsType = normalizeString(input.trims_type);
  const garmentPart = normalizeString(input.garment_part);

  // Find default usage
  const usageRow = trimsUsageData.find(row =>
    normalizeString(row.trims_type) === trimsType &&
    normalizeString(row.garment_part) === garmentPart
  );
  const defaultUsage = toFloat(usageRow?.usage) || 0;

  // Find default price
  const priceRow = trimsPriceData.find(row =>
    normalizeString(row.trims_type) === trimsType
  );
  const defaultPriceEach = toFloat(priceRow?.price_each) || 0;

  // Use overrides if provided
  const usage = toFloat(input.usage_override) || defaultUsage;
  const priceEach = toFloat(input.price_override) || defaultPriceEach;

  // Calculate total cost
  const totalCost = usage * priceEach;

  // Determine unit
  const unit = usageRow?.unit || 'pcs';

  return {
    unit,
    default_usage: Math.round(defaultUsage * 1000) / 1000,
    default_price_each: Math.round(defaultPriceEach * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}
