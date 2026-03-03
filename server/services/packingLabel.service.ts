import { loadCSV, toFloat, normalizeString } from '../utils/csvLoader';
import { PackingLabelInput, PackingLabelOutput } from '../types';

export async function computePackingLabel(input: PackingLabelInput): Promise<PackingLabelOutput> {
  // Load CSV data
  const displayPackagingData = await loadCSV('dropdown_display_packaging.csv');
  const transitPackageData = await loadCSV('dropdown_transit_package.csv');
  const labelData = await loadCSV('dropdown_label.csv');

  // Get pack count (default to 1 if not provided)
  const packCount = toFloat(input.pack_count) || 1;

  // Calculate display packaging
  const displayPackagingRow = displayPackagingData.find(row =>
    normalizeString(row.display_packaging) === normalizeString(input.display_packaging)
  );
  const displayPackagingDefaultUsage = toFloat(displayPackagingRow?.usage) || 0;
  const displayPackagingDefaultPrice = toFloat(displayPackagingRow?.price_each) || 0;
  const displayPackagingTotal = (displayPackagingDefaultUsage / packCount) * displayPackagingDefaultPrice;

  // Calculate transit package
  const transitPackageRow = transitPackageData.find(row =>
    normalizeString(row.transit_package) === normalizeString(input.transit_package)
  );
  const transitPackageDefaultUsage = toFloat(transitPackageRow?.usage) || 0;
  const transitPackageDefaultPrice = toFloat(transitPackageRow?.price_each) || 0;
  const transitPackageTotal = (transitPackageDefaultUsage / packCount) * transitPackageDefaultPrice;

  // Calculate label
  const labelRow = labelData.find(row =>
    normalizeString(row.label) === normalizeString(input.label_type)
  );
  const labelDefaultUsage = toFloat(labelRow?.usage) || 0;
  const labelDefaultPrice = toFloat(labelRow?.price_each) || 0;
  const labelTotal = (labelDefaultUsage / packCount) * labelDefaultPrice;

  return {
    display_packaging: {
      default_usage: Math.round(displayPackagingDefaultUsage * 1000) / 1000,
      total: Math.round(displayPackagingTotal * 1000) / 1000,
    },
    transit_package: {
      default_usage: Math.round(transitPackageDefaultUsage * 1000) / 1000,
      total: Math.round(transitPackageTotal * 1000) / 1000,
    },
    label: {
      default_usage: Math.round(labelDefaultUsage * 1000) / 1000,
      total: Math.round(labelTotal * 1000) / 1000,
    },
  };
}
