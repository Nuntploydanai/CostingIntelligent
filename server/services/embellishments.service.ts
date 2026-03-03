import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { EmbellishmentInput, EmbellishmentOutput } from '../types';

export async function computeEmbellishment(input: EmbellishmentInput): Promise<EmbellishmentOutput> {
  // Load CSV data
  const embellishmentPriceData = await loadCSV('dropdown_print_embellishment_price.csv');

  const printingType = normalizeString(input.printing_embroidery);
  const dimension = normalizeString(input.dimension);

  // Find price
  const priceRow = embellishmentPriceData.find(row =>
    normalizeString(row.printing_embroidery) === printingType &&
    normalizeString(row.dimension) === dimension
  );

  const defaultPriceEach = toFloat(priceRow?.price_each) || 0;

  // Get usage (usually 1 for embellishments)
  const usage = toFloat(input.usage_unit) || 1;

  // Calculate total cost
  const totalCost = usage * defaultPriceEach;

  return {
    default_price_each: Math.round(defaultPriceEach * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}
