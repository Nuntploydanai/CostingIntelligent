import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { FabricationInput, FabricationOutput } from '../types';

export async function computeFabrication(input: FabricationInput): Promise<FabricationOutput> {
  const fabricWidthData = await loadCSV('dropdown_fabric_width.csv');
  const fabricPriceData = await loadCSV('dropdown_fabric_price.csv');
  const fabricUsageData = await loadCSV('dropdown_fabric_usage.csv');

  const widthRow = fabricWidthData.find(row =>
    row.fabric_type === input.fabric_type &&
    row.fabric_contents === input.fabric_contents
  );
  const fixedFabricWidth = toFloat(widthRow?.fabric_width) || 60;

  const priceRow = fabricPriceData.find(row =>
    row.fabric_type === input.fabric_type &&
    row.fabric_contents === input.fabric_contents
  );
  const defaultWeightGsm = toFloat(priceRow?.weight_gsm) || 200;
  const defaultPriceYd = toFloat(priceRow?.price_yd) || 0;
  const defaultPriceKilo = toFloat(priceRow?.price_kilo) || 0;
  const defaultPriceLb = toFloat(priceRow?.price_lb) || 0;

  const usageRow = fabricUsageData.find(row =>
    row.fabric_type === input.fabric_type &&
    row.fabric_contents === input.fabric_contents &&
    row.using_part === input.using_part
  );
  const defaultUsage = toFloat(usageRow?.usage_yd) || 0;

  const materialCoo = normalizeString(input.material_coo);
  const cooMultiplier = materialCoo === 'Import' ? 1.05 : 1.0;

  let totalCost = 0;

  if (input.price_unit === 'Price / YD') {
    const pricePerYd = toFloat(input.price_value) || defaultPriceYd;
    totalCost = defaultUsage * pricePerYd;
  } else if (input.price_unit === 'Price / KILO') {
    const pricePerKilo = toFloat(input.price_value) || defaultPriceKilo;
    const weightGsm = toFloat(input.weight_gsm_override) || defaultWeightGsm;
    totalCost = (defaultUsage * 1.0 * weightGsm * pricePerKilo) / 1000;
  } else if (input.price_unit === 'Price / LB') {
    const pricePerLb = toFloat(input.price_value) || defaultPriceLb;
    const weightGsm = toFloat(input.weight_gsm_override) || defaultWeightGsm;
    const pricePerKilo = pricePerLb * 2.20462;
    totalCost = (defaultUsage * 1.0 * weightGsm * pricePerKilo) / 1000;
  }

  totalCost = totalCost * cooMultiplier;

  return {
    fixed_fabric_width: Math.round(fixedFabricWidth * 1000) / 1000,
    default_weight_gsm: Math.round(defaultWeightGsm * 1000) / 1000,
    default_price_yd: Math.round(defaultPriceYd * 1000) / 1000,
    default_price_kilo: Math.round(defaultPriceKilo * 1000) / 1000,
    default_price_lb: Math.round(defaultPriceLb * 1000) / 1000,
    total_cost: Math.round(totalCost * 1000) / 1000,
  };
}
