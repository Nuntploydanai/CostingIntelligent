import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { FabricationInput, FabricationOutput } from '../types';

// ─── Constants ────────────────────────────────────────────────────────────────
const METERS_PER_INCH = 0.0254;
const METERS_PER_YARD = 0.9144;
const LBS_PER_KG      = 2.20462;

// ─── Finishing cost lookup (T4 from Excel Conversion sheet) ──────────────────
const FINISHING_FACTORS: Record<string, number> = {
  'Wicking':                0.06615,
  'Odor Control':           0.11025,
  'Xtemp':                  0.33075,
  'Odor Control + Wicking': 0.17640,
  'Xtemp + Odor Control':   0.44100,
  'None':                   0.0,
  'OTHER':                  0.0,
};

// ─── Color/design factor (V18 from Excel Conversion sheet) ───────────────────
const COLOR_FACTORS: Record<string, number> = {
  'Solid':   1.0,
  'White':   0.95,
  'Heather': 1.1,
  'Others':  1.07,
};

// ─── Gender multiplier (U7) ───────────────────────────────────────────────────
const GENDER_MULTS: Record<string, number> = {
  'Men':   1.0,
  'Women': 0.85,
  'Kids':  0.75,
};

// ─── Size multiplier (V7) ─────────────────────────────────────────────────────
const SIZE_MULTS: Record<string, number> = {
  'S-XL':    1.0,
  'S-3XL':   1.1,
  '2XL-3XL': 1.15,
};

/**
 * Calculate price per yard following the Python/Excel Conversion sheet formula.
 * Implements: E23 → K16 → M16 → M18(O18)
 *
 * Formula chain:
 *   C23  = price converted to $/yd from user's unit
 *   E23  = C23 back to $/kg
 *   V6   = finishing cost in $/kg
 *   K16  = E23 + V6  (total $/kg including finishing)
 *   M16  = K16 * kgPerM * 0.9144  ($/yd)
 *   O18  = (M16 + V6) * colorFactor  (final $/yd)
 */
function calcPricePerYard(
  priceUnit:       string,
  priceValue:      number | null,
  defaultPriceLb:  number | null,
  gsm:             number,
  widthInches:     number,
  fabricFinishing: string,
  colorDesign:     string,
): number {
  if ((!priceValue && !defaultPriceLb) || gsm === 0) return 0;

  const widthM  = widthInches * METERS_PER_INCH;   // width in metres
  const kgPerM  = (gsm / 1000) * widthM;           // kg per linear metre of fabric
  const lbsPerM = kgPerM * LBS_PER_KG;             // lbs per linear metre

  // ── Convert user price → $/yd (C23) ────────────────────────────────────────
  const unit = (priceUnit ?? '').toLowerCase().trim();
  let C23: number;

  if (priceValue !== null && priceValue > 0) {
    if (unit.includes('yd') || unit.includes('yard')) {
      C23 = priceValue;                                       // already $/yd
    } else if (unit.includes('kg') || unit.includes('kilo')) {
      C23 = priceValue * kgPerM * METERS_PER_YARD;           // $/kg → $/yd
    } else if (unit.includes('meter') || unit.includes('mtr')) {
      C23 = priceValue * METERS_PER_YARD;                    // $/m → $/yd
    } else if (unit.includes('oz') || unit.includes('ounce')) {
      const ozPerM = kgPerM * 35.274;
      C23 = priceValue * ozPerM * METERS_PER_YARD;           // $/oz → $/yd
    } else {
      // Default: treat as $/lb
      C23 = priceValue * lbsPerM * METERS_PER_YARD;          // $/lb → $/yd
    }
  } else {
    // No user price — use default $/lb from lookup
    C23 = (defaultPriceLb ?? 0) * lbsPerM * METERS_PER_YARD;
  }

  // ── E23: convert C23 ($/yd) back to $/kg ───────────────────────────────────
  const E23 = (C23 / METERS_PER_YARD) / kgPerM;

  // ── V6: finishing cost in $/kg ──────────────────────────────────────────────
  const T4 = FINISHING_FACTORS[normalizeString(fabricFinishing)] ?? 0.0;
  const V5 = (gsm * 1.19599) * 1.6667;
  const V6 = V5 * T4 / 1000.0;

  // ── K16: total $/kg (price + finishing) ────────────────────────────────────
  const K16 = E23 + V6;

  // ── M16: $/yd from total $/kg ───────────────────────────────────────────────
  const M16 = (K16 * kgPerM) * METERS_PER_YARD;

  // ── Color/design factor ─────────────────────────────────────────────────────
  const V18 = COLOR_FACTORS[normalizeString(colorDesign)] ?? 1.0;

  // ── O18: final price/yd ─────────────────────────────────────────────────────
  const O18 = (M16 + V6) * V18;

  return O18;
}

// ─── Main calculation ─────────────────────────────────────────────────────────

export async function computeFabrication(input: FabricationInput): Promise<FabricationOutput> {

  // Load all required CSV look-up tables
  const productPartKeyMap = await loadCSV('product_part_key_map.csv');
  const fabricWidthMap    = await loadCSV('fabric_width_condition_map.csv');
  const fabricUsageLookup = await loadCSV('fabric_usage_lookup.csv');
  const fabricPriceLookup = await loadCSV('fabric_price_lookup.csv');
  const fabricTypeGsm     = await loadCSV('fabric_type_default_gsm.csv');

  // ── Normalize inputs ────────────────────────────────────────────────────────
  const silhouette      = normalizeString(input.silhouette      ?? '');
  const seam            = normalizeString(input.seam            ?? '');
  const size            = normalizeString(input.size            ?? 'S-XL');
  const gender          = normalizeString(input.gender          ?? 'Men');
  const usingPart       = normalizeString(input.using_part      ?? 'Whole Garment');
  const fabricType      = normalizeString(input.fabric_type     ?? '');
  const fabricCont      = normalizeString(input.fabric_contents ?? '');
  const priceUnit       = normalizeString(input.price_unit      ?? '');
  const materialCoo     = normalizeString(input.material_coo    ?? '');
  const fabricFinishing = normalizeString(input.fabric_finishing ?? 'None');
  const colorDesign     = normalizeString(input.color_design    ?? 'Solid');
  const priceValue      = toFloat(input.price_value)            ?? 0;

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
  const fabricConstruction = seam.toLowerCase().includes('side') ? 'OPEN WIDTH' : 'TUBULAR';

  // ── Step 4: Get default GSM for the fabric type ────────────────────────────
  const gsmRow = fabricTypeGsm.find(r =>
    normalizeString(r.fabric_type ?? '').toLowerCase() === fabricType.toLowerCase()
  );
  const defaultWeightGsm = toFloat(gsmRow?.default_gsm) ?? 0;

  // Use user-entered GSM if provided, otherwise use default from CSV
  const userGsmInput = toFloat(input.weight_gsm_override);
  const effectiveGsm = (userGsmInput !== null && userGsmInput > 0)
    ? userGsmInput
    : defaultWeightGsm;
  // Display 0 when user has overridden GSM (matches Excel behaviour)
  const displayDefaultGsm = (userGsmInput !== null && userGsmInput > 0) ? 0 : defaultWeightGsm;

  // ── Step 5: Get default price/lb from fabric_price_lookup.csv ─────────────
  const lookupKey  = fabricType + fabricCont;
  const priceRow   = fabricPriceLookup.find(r =>
    normalizeString(r.key ?? '') === lookupKey
  );
  const defaultPriceLb = toFloat(priceRow?.value) ?? 0;

  // ── Step 6: Look up BASE consumption (S-XL) from fabric_usage_lookup.csv ──
  const usageRow = fabricUsageLookup.find(r =>
    normalizeString(r.fabric     ?? '').toLowerCase() === fabricConstruction.toLowerCase() &&
    normalizeString(r.k7_key    ?? '').toLowerCase() === k7Key.toLowerCase() &&
    normalizeString(r.using_part ?? '').toLowerCase() === usingPart.toLowerCase()
  );
  // Always use S-XL as the base consumption value
  const consumptionBase = toFloat(usageRow?.['usage_s_xl']) ?? 0;

  console.log('[FAB] k7Key:', k7Key, '| construction:', fabricConstruction, '| usingPart:', usingPart);
  console.log('[FAB] consumptionBase(S-XL):', consumptionBase);

  // ── Step 7: Apply gender and size multipliers ──────────────────────────────
  //   U7 = base × genderMult
  //   V7 = U7 × sizeMult
  const genderMult      = GENDER_MULTS[gender] ?? 0;
  const sizeMult        = SIZE_MULTS[size]     ?? 0;
  const consumptionYards = consumptionBase * genderMult * sizeMult;

  console.log('[FAB] gender:', gender, genderMult, '| size:', size, sizeMult, '| consumptionYards:', consumptionYards);

  // ── Step 8: Calculate price per yard (Excel Conversion sheet formula) ──────
  const pricePerYard = calcPricePerYard(
    priceUnit,
    priceValue > 0 ? priceValue : null,
    defaultPriceLb,
    effectiveGsm,
    fixedFabricWidth,
    fabricFinishing,
    colorDesign,
  );

  // Default price/yd: uses DEFAULT price/lb with effective GSM (for display)
  const defaultPriceYd = calcPricePerYard(
    'Price / Lbs',
    null,
    defaultPriceLb,
    effectiveGsm,
    fixedFabricWidth,
    fabricFinishing,
    colorDesign,
  );

  // Default price/kilo: $/lb × LBS_PER_KG
  const defaultPriceKilo = defaultPriceLb * LBS_PER_KG;

  console.log('[FAB] effectiveGsm:', effectiveGsm, '| pricePerYard:', pricePerYard, '| defaultPriceYd:', defaultPriceYd);

  // ── Step 9: CIF multiplier (Import = 1.05, Domestic = 1.0) ────────────────
  const cooMultiplier = materialCoo.toLowerCase() === 'import' ? 1.05 : 1.0;

  // ── Step 10: Total cost ────────────────────────────────────────────────────
  //   Y7 = consumptionYards × pricePerYard × importFactor
  const totalCost = consumptionYards * pricePerYard * cooMultiplier;

  console.log('[FAB] totalCost:', totalCost, '| cooMultiplier:', cooMultiplier);

  return {
    fixed_fabric_width: Math.round(fixedFabricWidth * 1000) / 1000,
    default_weight_gsm: Math.round(displayDefaultGsm  * 1000) / 1000,
    default_price_yd:   Math.round(defaultPriceYd    * 1000) / 1000,
    default_price_kilo: Math.round(defaultPriceKilo  * 1000) / 1000,
    default_price_lb:   Math.round(defaultPriceLb    * 1000) / 1000,
    total_cost:         Math.round(totalCost         * 1000) / 1000,
  };
}
