import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { FabricationInput, FabricationOutput } from '../types';

// ─── Unit conversion constants ────────────────────────────────────────────────
const METERS_PER_INCH = 0.0254;
const METERS_PER_YARD = 0.9144;
const LBS_PER_KG      = 2.20462;

/**
 * Convert user price (per lb / per kg / per yd) → price per yard of fabric.
 *
 * Formula for weight-based units:
 *   weight_kg_per_yard = GSM (g/m2) * widthInches * METERS_PER_INCH * METERS_PER_YARD / 1000
 *   price_per_yd       = price_per_unit * weight_kg_per_yard [* LBS_PER_KG if lb]
 */
function calcPricePerYard(
  priceUnit:  string,
  priceValue: number,
  gsm:        number,
  widthIn:    number,
): number {
  const widthM      = widthIn * METERS_PER_INCH;
  const kgPerYard   = gsm * widthM * METERS_PER_YARD / 1000;

  const unit = priceUnit.toLowerCase().trim();

  if (unit.includes('yd') || unit.includes('yds') || unit.includes('yard')) {
    return priceValue;
  }
  if (unit.includes('lb') || unit.includes('lbs') || unit.includes('pound')) {
    return priceValue * kgPerYard * LBS_PER_KG;
  }
  if (unit.includes('kg') || unit.includes('kilo') || unit.includes('kgs')) {
    return priceValue * kgPerYard;
  }
  if (unit.includes('meter') || unit.includes('mtr')) {
    // price per meter -> price per yard: 1 yd = 0.9144 m
    return priceValue * METERS_PER_YARD;
  }
  if (unit.includes('oz') || unit.includes('ounce')) {
    // price per oz -> price per lb -> price per yard
    return (priceValue / 16) * kgPerYard * LBS_PER_KG;
  }

  // Default: treat as price per lb
  return priceValue * kgPerYard * LBS_PER_KG;
}

// ─── Main calculation ─────────────────────────────────────────────────────────

export async function computeFabrication(input: FabricationInput): Promise<FabricationOutput> {

  // Load all required CSV look-up tables
  const productPartKeyMap = await loadCSV('product_part_key_map.csv');   // silhouette+seam -> k7_key
  const fabricWidthMap    = await loadCSV('fabric_width_condition_map.csv'); // silhouette+seam -> width_in
  const fabricUsageLookup = await loadCSV('fabric_usage_lookup.csv');    // fabric+design+part -> usage cols
  const fabricPriceLookup = await loadCSV('fabric_price_lookup.csv');    // fabricType+contents -> default price/lb
  const fabricTypeGsm     = await loadCSV('fabric_type_default_gsm.csv'); // fabric_type -> default_gsm

  // ── Normalize inputs ────────────────────────────────────────────────────────
  const silhouette  = normalizeString(input.silhouette   ?? '');
  const seam        = normalizeString(input.seam         ?? '');
  const size        = normalizeString(input.size         ?? 'S-XL');
  const usingPart   = normalizeString(input.using_part   ?? 'Whole Garment');
  const fabricType  = normalizeString(input.fabric_type  ?? '');
  const fabricCont  = normalizeString(input.fabric_contents ?? '');
  const priceUnit   = normalizeString(input.price_unit   ?? '');
  const materialCoo = normalizeString(input.material_coo ?? '');

  const priceValue  = toFloat(input.price_value)        ?? 0;

  // ── Step 1: Map silhouette + seam → k7_key ─────────────────────────────────
  const keyRow = productPartKeyMap.find(r =>
    normalizeString(r.silhouette ?? '').toLowerCase() === silhouette.toLowerCase() &&
    normalizeString(r.seam       ?? '').toLowerCase() === seam.toLowerCase()
  );
  const k7Key = normalizeString(keyRow?.k7_key ?? '');

  // ── Step 2: Get fixed fabric width from silhouette + seam ──────────────────
  const widthRow = fabricWidthMap.find(r =>
    normalizeString(r.silhouette ?? '').toLowerCase() === silhouette.toLowerCase() &&
    normalizeString(r.seam       ?? '').toLowerCase() === seam.toLowerCase()
  );
  const fixedFabricWidth = toFloat(widthRow?.width_in) ?? 60;

  // ── Step 3: Determine OPEN WIDTH vs TUBULAR from seam type ─────────────────
  //   Side Seam = fabric cut & sewn (OPEN WIDTH roll)
  //   No Seam   = seamless tubular knit (TUBULAR)
  const fabricConstruction = seam.toLowerCase().includes('side') ? 'OPEN WIDTH' : 'TUBULAR';

  // ── Step 4: Get default GSM for the fabric type ────────────────────────────
  const gsmRow = fabricTypeGsm.find(r =>
    normalizeString(r.fabric_type ?? '').toLowerCase() === fabricType.toLowerCase()
  );
  const defaultWeightGsm = toFloat(gsmRow?.default_gsm) ?? 160;
  const userGsm          = toFloat(input.weight_gsm_override) || defaultWeightGsm;

  // ── Step 5: Get default price/lb from fabric_price_lookup.csv ─────────────
  //   Key is fabricType concatenated with fabricContents (no separator)
  //   e.g. "JerseyBCI Cotton /100"
  const lookupKey  = fabricType + fabricCont;
  const priceRow   = fabricPriceLookup.find(r =>
    normalizeString(r.key ?? '') === lookupKey
  );
  const defaultPriceLb = toFloat(priceRow?.value) ?? 0;

  // ── Step 6: Select the right usage column based on size ───────────────────
  //   S-XL     -> usage_s_xl
  //   2XL-3XL  -> usage_2xl_3xl
  //   S-3XL    -> usage_s_3xl  (weighted average covering the full S–3XL range)
  const usageColumn =
    size === '2XL-3XL' ? 'usage_2xl_3xl' :
    size === 'S-3XL'   ? 'usage_s_3xl'   :
                         'usage_s_xl';

  // ── Step 7: Look up fabric consumption in yards ────────────────────────────
  const usageRow = fabricUsageLookup.find(r =>
    normalizeString(r.fabric     ?? '').toLowerCase() === fabricConstruction.toLowerCase() &&
    normalizeString(r.k7_key    ?? '').toLowerCase() === k7Key.toLowerCase() &&
    normalizeString(r.using_part ?? '').toLowerCase() === usingPart.toLowerCase()
  );
  const consumptionYards = toFloat(usageRow?.[usageColumn]) ?? 0;

  console.log('[FAB] k7Key:', k7Key, '| construction:', fabricConstruction, '| usingPart:', usingPart);
  console.log('[FAB] usageColumn:', usageColumn, '| consumptionYards:', consumptionYards);

  // ── Step 8: Calculate price per yard ──────────────────────────────────────
  //   Use the user-entered price if provided, otherwise fall back to default
  const activePriceValue = priceValue > 0 ? priceValue : defaultPriceLb;
  const pricePerYard     = calcPricePerYard(priceUnit, activePriceValue, userGsm, fixedFabricWidth);

  // Default price/yd and default price/kilo (for display, using DEFAULT price/lb and DEFAULT GSM)
  const defaultPriceYd   = calcPricePerYard('Price / LB', defaultPriceLb, defaultWeightGsm, fixedFabricWidth);
  const defaultPriceKilo = defaultPriceLb / LBS_PER_KG;

  console.log('[FAB] pricePerYard:', pricePerYard, '| defaultPriceYd:', defaultPriceYd);

  // ── Step 9: CIF multiplier (Import = x1.05, Domestic = x1.0) ──────────────
  const cooMultiplier = materialCoo.toLowerCase() === 'import' ? 1.05 : 1.0;

  // ── Step 10: Total cost ────────────────────────────────────────────────────
  //   Formula: consumption (yards) x price_per_yard x CIF_multiplier
  const totalCost = consumptionYards * pricePerYard * cooMultiplier;

  console.log('[FAB] totalCost:', totalCost, '| cooMultiplier:', cooMultiplier);

  return {
    fixed_fabric_width: Math.round(fixedFabricWidth * 1000) / 1000,
    default_weight_gsm: Math.round(defaultWeightGsm  * 1000) / 1000,
    default_price_yd:   Math.round(defaultPriceYd    * 1000) / 1000,
    default_price_kilo: Math.round(defaultPriceKilo  * 1000) / 1000,
    default_price_lb:   Math.round(defaultPriceLb    * 1000) / 1000,
    total_cost:         Math.round(totalCost          * 1000) / 1000,
  };
}
