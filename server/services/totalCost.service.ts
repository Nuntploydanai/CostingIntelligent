import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { TotalCostSummary, CountryComparison } from '../types';

export async function computeTotalCostSummary(params: {
  fabric_cost: number;
  trim_cost: number;
  print_embroidery_cost: number;
  display_packaging_cost: number;
  transit_packaging_cost: number;
  label_cost: number;
  labour_cost: number;
  gender: string;
  silhouette: string;
  size: string;
  supplier_margin_percent: number;
  product_testing_cost: number;
  other_cost: number;
  freight_cost: number;
  gmo_cost: number;
  duty_cost: number;
}): Promise<TotalCostSummary> {
  // Load sewing thread cost lookup
  const sewingThreadData = await loadCSV('sewing_thread_cost.csv');

  // Find sewing thread cost based on gender + silhouette
  const sewingThreadRow = sewingThreadData.find(row =>
    normalizeString(row.gender) === normalizeString(params.gender) &&
    normalizeString(row.silhouette) === normalizeString(params.silhouette)
  );
  const sewingThreadCost = toFloat(sewingThreadRow?.sewing_thread_cost) || 0;

  // Calculate all 10 cost items
  const total_fabric_cost = toFloat(params.fabric_cost) || 0;
  const total_trim_cost = toFloat(params.trim_cost) || 0;
  const total_display_packaging_cost = toFloat(params.display_packaging_cost) || 0;
  const total_transit_packaging_cost = toFloat(params.transit_packaging_cost) || 0;
  const total_label_cost = toFloat(params.label_cost) || 0;
  const total_sewing_thread_cost = sewingThreadCost;
  const total_labour_cost = toFloat(params.labour_cost) || 0;
  const total_product_testing_cost = toFloat(params.product_testing_cost) || 0;
  const total_print_embroidery_cost = toFloat(params.print_embroidery_cost) || 0;
  const total_other_cost = toFloat(params.other_cost) || 0;

  // Calculate subtotal (items 1-10)
  const subtotal =
    total_fabric_cost +
    total_trim_cost +
    total_display_packaging_cost +
    total_transit_packaging_cost +
    total_label_cost +
    total_sewing_thread_cost +
    total_labour_cost +
    total_product_testing_cost +
    total_print_embroidery_cost +
    total_other_cost;

  // Calculate supplier margin
  const marginDecimal = params.supplier_margin_percent / 100;
  const supplier_margin_amount = subtotal * marginDecimal;

  // Calculate FOB cost (subtotal + margin)
  const fob_cost = subtotal + supplier_margin_amount;

  // Additional costs
  const freight_cost = toFloat(params.freight_cost) || 0;
  const gmo_cost = toFloat(params.gmo_cost) || 0;
  const duty_cost = toFloat(params.duty_cost) || 0;

  // Calculate grand total (FOB + Freight + GMO + Duty)
  const grand_total = fob_cost + freight_cost + gmo_cost + duty_cost;

  // Calculate FOB/FLC per piece and per dozen
  const total_fob_per_piece = fob_cost;
  const total_fob_per_dozen = fob_cost * 12;
  const total_flc_per_piece = grand_total;
  const total_flc_per_dozen = grand_total * 12;

  // Calculate percentage proportions (relative to subtotal)
  const calcPct = (value: number) => (subtotal > 0 ? (value / subtotal) * 100 : 0);

  return {
    total_fabric_cost: Math.round(total_fabric_cost * 1000) / 1000,
    total_trim_cost: Math.round(total_trim_cost * 1000) / 1000,
    total_display_packaging_cost: Math.round(total_display_packaging_cost * 1000) / 1000,
    total_transit_packaging_cost: Math.round(total_transit_packaging_cost * 1000) / 1000,
    total_label_cost: Math.round(total_label_cost * 1000) / 1000,
    total_sewing_thread_cost: Math.round(total_sewing_thread_cost * 1000) / 1000,
    total_labour_cost: Math.round(total_labour_cost * 1000) / 1000,
    total_product_testing_cost: Math.round(total_product_testing_cost * 1000) / 1000,
    total_print_embroidery_cost: Math.round(total_print_embroidery_cost * 1000) / 1000,
    total_other_cost: Math.round(total_other_cost * 1000) / 1000,
    subtotal: Math.round(subtotal * 1000) / 1000,
    supplier_margin_percent: params.supplier_margin_percent,
    supplier_margin_amount: Math.round(supplier_margin_amount * 1000) / 1000,
    fob_cost: Math.round(fob_cost * 1000) / 1000,
    freight_cost: Math.round(freight_cost * 1000) / 1000,
    gmo_cost: Math.round(gmo_cost * 1000) / 1000,
    duty_cost: Math.round(duty_cost * 1000) / 1000,
    grand_total: Math.round(grand_total * 1000) / 1000,
    total_fob_per_piece: Math.round(total_fob_per_piece * 1000) / 1000,
    total_fob_per_dozen: Math.round(total_fob_per_dozen * 1000) / 1000,
    total_flc_per_piece: Math.round(total_flc_per_piece * 1000) / 1000,
    total_flc_per_dozen: Math.round(total_flc_per_dozen * 1000) / 1000,
    total_fabric_cost_pct: Math.round(calcPct(total_fabric_cost) * 100) / 100,
    total_trim_cost_pct: Math.round(calcPct(total_trim_cost) * 100) / 100,
    total_display_packaging_cost_pct: Math.round(calcPct(total_display_packaging_cost) * 100) / 100,
    total_transit_packaging_cost_pct: Math.round(calcPct(total_transit_packaging_cost) * 100) / 100,
    total_label_cost_pct: Math.round(calcPct(total_label_cost) * 100) / 100,
    total_sewing_thread_cost_pct: Math.round(calcPct(total_sewing_thread_cost) * 100) / 100,
    total_labour_cost_pct: Math.round(calcPct(total_labour_cost) * 100) / 100,
    total_product_testing_cost_pct: Math.round(calcPct(total_product_testing_cost) * 100) / 100,
    total_print_embroidery_cost_pct: Math.round(calcPct(total_print_embroidery_cost) * 100) / 100,
    total_other_cost_pct: Math.round(calcPct(total_other_cost) * 100) / 100,
    supplier_margin_amount_pct: Math.round(calcPct(supplier_margin_amount) * 100) / 100,
  };
}

// Country comparison calculation
const COMPARISON_COUNTRIES = [
  'INDIA',
  'BANGLADESH',
  'INDONESIA',
  'THAILAND',
  'CAMBODIA',
  'VIETNAM',
];

export async function computeCountryComparison(params: {
  fabric_cost: number;
  trim_cost: number;
  print_embroidery_cost: number;
  display_packaging_cost: number;
  transit_packaging_cost: number;
  label_cost: number;
  gender: string;
  silhouette: string;
  seam: string;
  size: string;
  quantity: string;
  supplier_margin_percent: number;
  product_testing_cost: number;
  other_cost: number;
  freight_cost: number;
  gmo_cost: number;
  duty_cost: number;
}): Promise<CountryComparison[]> {
  // Load manufacturing data for all countries
  const { computeManufacturing } = await import('./manufacturing.service');

  const results: CountryComparison[] = [];

  for (const country of COMPARISON_COUNTRIES) {
    // Get labour cost for this country
    const mfgResult = await computeManufacturing({
      gender: params.gender,
      silhouette: params.silhouette,
      seam: params.seam,
      size: params.size,
      quantity: params.quantity,
      coo: country,
    });

    const labour_cost = mfgResult.total_cost;

    // Calculate total cost summary for this country
    const summary = await computeTotalCostSummary({
      ...params,
      labour_cost,
    });

    results.push({
      country,
      labour_cost: summary.total_labour_cost,
      subtotal: summary.subtotal,
      margin_amount: summary.supplier_margin_amount,
      fob_cost: summary.fob_cost,
    });
  }

  return results;
}
