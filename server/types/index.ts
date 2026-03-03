// TypeScript interfaces for all data structures

export interface DevelopmentInput {
  gender: string;
  silhouette: string;
  seam: string;
  color_design: string;
  size: string;
  pack_count: string;
  ideal_quantity: string;
  coo: string;
  fabric_finishing: string;
}

export interface FabricationInput {
  fabric_type: string;
  fabric_contents: string;
  using_part: string;
  weight_gsm_override: string;
  price_unit: string;
  price_value: string;
  material_coo: string;
}

export interface FabricationOutput {
  fixed_fabric_width: number;
  default_weight_gsm: number;
  default_price_yd: number;
  default_price_kilo: number;
  default_price_lb: number;
  total_cost: number;
}

export interface TrimsInput {
  trims_type: string;
  garment_part: string;
  usage_override: string;
  price_override: string;
  material_coo: string;
}

export interface TrimsOutput {
  unit: string;
  default_usage: number;
  default_price_each: number;
  total_cost: number;
}

export interface EmbellishmentInput {
  printing_embroidery: string;
  dimension: string;
  usage_unit: string;
}

export interface EmbellishmentOutput {
  default_price_each: number;
  total_cost: number;
}

export interface PackingLabelInput {
  display_packaging: string;
  transit_package: string;
  label_type: string;
}

export interface PackingLabelOutput {
  display_packaging: {
    default_usage: number;
    total: number;
  };
  transit_package: {
    default_usage: number;
    total: number;
  };
  label: {
    default_usage: number;
    total: number;
  };
}

export interface ManufacturingInput {
  gender: string;
  silhouette: string;
  seam: string;
  size: string;
  quantity: string;
  coo: string;
}

export interface ManufacturingOutput {
  country: string;
  minutes: number;
  cost_rate: number;
  efficiency: number;
  total_cost: number;
}

export interface TotalCostSummary {
  total_fabric_cost: number;
  total_trim_cost: number;
  total_display_packaging_cost: number;
  total_transit_packaging_cost: number;
  total_label_cost: number;
  total_sewing_thread_cost: number;
  total_labour_cost: number;
  total_product_testing_cost: number;
  total_print_embroidery_cost: number;
  total_other_cost: number;
  subtotal: number;
  supplier_margin_percent: number;
  supplier_margin_amount: number;
  fob_cost: number;
  freight_cost: number;
  gmo_cost: number;
  duty_cost: number;
  grand_total: number;
  total_fob_per_piece: number;
  total_fob_per_dozen: number;
  total_flc_per_piece: number;
  total_flc_per_dozen: number;
  total_fabric_cost_pct: number;
  total_trim_cost_pct: number;
  total_display_packaging_cost_pct: number;
  total_transit_packaging_cost_pct: number;
  total_label_cost_pct: number;
  total_sewing_thread_cost_pct: number;
  total_labour_cost_pct: number;
  total_product_testing_cost_pct: number;
  total_print_embroidery_cost_pct: number;
  total_other_cost_pct: number;
  supplier_margin_amount_pct: number;
}

export interface CountryComparison {
  country: string;
  labour_cost: number;
  subtotal: number;
  margin_amount: number;
  fob_cost: number;
}

export interface CalculateRequest {
  development: DevelopmentInput;
  fabrication: FabricationInput[];
  trims: TrimsInput[];
  embellishments: EmbellishmentInput[];
  packing_label: PackingLabelInput;
  supplier_margin_percent: number;
  freight_cost: number;
  gmo_cost: number;
  duty_cost: number;
  additional_cost: number;
}

export interface CalculateResponse {
  inputs: {
    development: DevelopmentInput;
    fabrication: FabricationInput[];
  };
  outputs: {
    fabrication: {
      rows: FabricationOutput[];
      total_fabric_cost: number;
    };
    trims: {
      rows: TrimsOutput[];
    };
    embellishments: {
      rows: EmbellishmentOutput[];
    };
    packing_label: PackingLabelOutput;
    manufacturing: {
      rows: ManufacturingOutput[];
    };
    total_cost_summary: TotalCostSummary;
    country_comparison: CountryComparison[];
  };
}
