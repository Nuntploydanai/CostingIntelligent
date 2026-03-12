import { useState, useEffect, useCallback } from 'react'

interface DropdownData {
  [key: string]: string[]
}

interface CalculateResponse {
  outputs: {
    fabrication: {
      rows: any[]
      total_fabric_cost: number
    }
    trims: {
      rows: any[]
      total_trim_cost: number
    }
    embellishments: {
      rows: any[]
      total_embellishment_cost: number
    }
    packing_label: {
      display_packaging: { default_usage: number; total: number }
      transit_package: { default_usage: number; total: number }
      label: { default_usage: number; total: number }
    }
    manufacturing: {
      rows: any[]
    }
    total_cost_summary: {
      total_fabric_cost: number
      total_trim_cost: number
      total_display_packaging_cost: number
      total_transit_packaging_cost: number
      total_label_cost: number
      total_sewing_thread_cost: number
      total_labour_cost: number
      total_product_testing_cost: number
      total_print_embroidery_cost: number
      total_other_cost: number
      subtotal: number
      supplier_margin_percent: number
      supplier_margin_amount: number
      fob_cost: number
      freight_cost: number
      gmo_cost: number
      duty_cost: number
      grand_total: number
      total_fob_per_piece: number
      total_fob_per_dozen: number
      total_flc_per_piece: number
      total_flc_per_dozen: number
      total_fabric_cost_pct: number
      total_trim_cost_pct: number
      total_display_packaging_cost_pct: number
      total_transit_packaging_cost_pct: number
      total_label_cost_pct: number
      total_sewing_thread_cost_pct: number
      total_labour_cost_pct: number
      total_product_testing_cost_pct: number
      total_print_embroidery_cost_pct: number
      total_other_cost_pct: number
      supplier_margin_amount_pct: number
    }
    country_comparison: Array<{
      country: string
      labour_cost: number
      subtotal: number
      margin_amount: number
      fob_cost: number
    }>
  }
}

function App() {
  const [dropdowns, setDropdowns] = useState<DropdownData>({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CalculateResponse | null>(null)

  // Form state
  const [development, setDevelopment] = useState({
    gender: '',
    silhouette: '',
    seam: '',
    color_design: '',
    size: '',
    pack_count: '',
    ideal_quantity: '',
    coo: '',
    fabric_finishing: ''
  })

  const [fabrication, setFabrication] = useState([{
    fabric_type: '',
    fabric_contents: '',
    using_part: 'Self Fabric',
    weight_gsm_override: '',
    price_unit: 'Price / YD',
    price_value: '',
    material_coo: ''
  }])

  const [trims, setTrims] = useState([{
    trims_type: '',
    garment_part: '',
    usage_override: '',
    price_override: '',
    material_coo: ''
  }])

  const [embellishments, setEmbellishments] = useState([{
    printing_embroidery: '',
    dimension: '',
    usage_unit: ''
  }])

  const [packingLabel, setPackingLabel] = useState({
    pack_count: '',
    display_packaging: '',
    transit_package: '',
    label_type: ''
  })

  const [supplierMarginPercent, setSupplierMarginPercent] = useState(7)
  const [freightCost, setFreightCost] = useState(0)
  const [gmoCost, setGmoCost] = useState(0)
  const [dutyCost, setDutyCost] = useState(0)
  const [additionalCost, setAdditionalCost] = useState(0)

  // Load dropdowns
  useEffect(() => {
    const dropdownNames = [
      'gender', 'silhouette', 'seam', 'color_design', 'size',
      'pack_count', 'ideal_quantity', 'coo', 'fabric_finishing',
      'fabric_type', 'fabric_contents', 'using_part', 'price_unit',
      'material_coo', 'trims_type', 'garment_part_trim', 'printing_embroidery',
      'print_dimension', 'usage_unit', 'display_packaging', 'transit_package', 'label'
    ]

    Promise.all(
      dropdownNames.map(name =>
        fetch(`/api/dropdown/${name}`)
          .then(res => res.json())
          .then(data => ({ name, values: data.values || [] }))
      )
    ).then(results => {
      const dropdownMap: DropdownData = {}
      results.forEach(({ name, values }) => {
        dropdownMap[name] = values
      })
      setDropdowns(dropdownMap)
    })
  }, [])

  // Auto-calculate with debounce
  const calculateCost = useCallback(async () => {
    if (!development.gender || !development.silhouette || !fabrication[0].fabric_type) {
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          development,
          fabrication,
          trims,
          embellishments,
          packing_label: packingLabel,
          supplier_margin_percent: supplierMarginPercent,
          freight_cost: freightCost,
          gmo_cost: gmoCost,
          duty_cost: dutyCost,
          additional_cost: additionalCost
        })
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Calculation error:', error)
    } finally {
      setLoading(false)
    }
  }, [development, fabrication, trims, embellishments, packingLabel, supplierMarginPercent, freightCost, gmoCost, dutyCost, additionalCost])

  // Debounced calculation
  useEffect(() => {
    const timer = setTimeout(() => {
      calculateCost()
    }, 500)

    return () => clearTimeout(timer)
  }, [calculateCost])

  // Clear form function
  const clearForm = () => {
    setDevelopment({
      gender: '',
      silhouette: '',
      seam: '',
      color_design: '',
      size: '',
      pack_count: '',
      ideal_quantity: '',
      coo: '',
      fabric_finishing: ''
    })
    setFabrication([{
      fabric_type: '',
      fabric_contents: '',
      using_part: 'Self Fabric',
      weight_gsm_override: '',
      price_unit: 'Price / YD',
      price_value: '',
      material_coo: ''
    }])
    setTrims([{
      trims_type: '',
      garment_part: '',
      usage_override: '',
      price_override: '',
      material_coo: ''
    }])
    setEmbellishments([{
      printing_embroidery: '',
      dimension: '',
      usage_unit: ''
    }])
    setPackingLabel({
      pack_count: '',
      display_packaging: '',
      transit_package: '',
      label_type: ''
    })
    setSupplierMarginPercent(7)
    setFreightCost(0)
    setGmoCost(0)
    setDutyCost(0)
    setAdditionalCost(0)
    setResult(null)
  }

  return (
    <div className="container">
      <header>
        <h1>👕 Basic Shirts Costing Tool v2</h1>
        <p>Excel-Parity Cost Calculator (Node.js + React)</p>
        <button onClick={clearForm} className="clear-button">
          🔄 Clear Form
        </button>
      </header>

      <div className="main-content">
        {/* Step 1: Development */}
        <section className="card">
          <h2>Step 1: Development</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Gender</label>
              <select
                value={development.gender}
                onChange={e => setDevelopment({ ...development, gender: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.gender?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Silhouette</label>
              <select
                value={development.silhouette}
                onChange={e => setDevelopment({ ...development, silhouette: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.silhouette?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Seam</label>
              <select
                value={development.seam}
                onChange={e => setDevelopment({ ...development, seam: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.seam?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Color / Design</label>
              <select
                value={development.color_design}
                onChange={e => setDevelopment({ ...development, color_design: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.color_design?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Size</label>
              <select
                value={development.size}
                onChange={e => setDevelopment({ ...development, size: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.size?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Ideal Quantity</label>
              <select
                value={development.ideal_quantity}
                onChange={e => setDevelopment({ ...development, ideal_quantity: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.ideal_quantity?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Pack count / Pack</label>
              <select
                value={development.pack_count}
                onChange={e => setDevelopment({ ...development, pack_count: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.pack_count?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>COO (Country of Origin)</label>
              <select
                value={development.coo}
                onChange={e => setDevelopment({ ...development, coo: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.coo?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Fabric Finishing</label>
              <select
                value={development.fabric_finishing}
                onChange={e => setDevelopment({ ...development, fabric_finishing: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.fabric_finishing?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>
        </section>

        {/* Step 2: Fabrication */}
        <section className="card">
          <h2>Step 2: Fabrication</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Fabric Type</label>
              <select
                value={fabrication[0].fabric_type}
                onChange={e => setFabrication([{ ...fabrication[0], fabric_type: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.fabric_type?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Fabric Contents</label>
              <select
                value={fabrication[0].fabric_contents}
                onChange={e => setFabrication([{ ...fabrication[0], fabric_contents: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.fabric_contents?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Using Part</label>
              <select
                value={fabrication[0].using_part}
                onChange={e => setFabrication([{ ...fabrication[0], using_part: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.using_part?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Weight (GSM)</label>
              <input
                type="number"
                step="0.001"
                value={fabrication[0].weight_gsm_override}
                onChange={e => setFabrication([{ ...fabrication[0], weight_gsm_override: e.target.value }])}
              />
            </div>

            <div className="form-group">
              <label>Price Unit</label>
              <select
                value={fabrication[0].price_unit}
                onChange={e => setFabrication([{ ...fabrication[0], price_unit: e.target.value }])}
              >
                {dropdowns.price_unit?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Price Value</label>
              <input
                type="number"
                step="0.001"
                placeholder="Override price..."
                value={fabrication[0].price_value}
                onChange={e => setFabrication([{ ...fabrication[0], price_value: e.target.value }])}
              />
            </div>

            <div className="form-group">
              <label>Material COO</label>
              <select
                value={fabrication[0].material_coo}
                onChange={e => setFabrication([{ ...fabrication[0], material_coo: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.material_coo?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Fixed Fabric Width</label>
              <input readOnly value={result?.outputs.fabrication.rows?.[0]?.fixed_fabric_width?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>Default Weight (GSM)</label>
              <input readOnly value={result?.outputs.fabrication.rows?.[0]?.default_weight_gsm?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>DEFAULT (PRICE/YD)</label>
              <input readOnly value={result?.outputs.fabrication.rows?.[0]?.default_price_yd?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>DEFAULT (PRICE/KILO)</label>
              <input readOnly value={result?.outputs.fabrication.rows?.[0]?.default_price_kilo?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>PRICE / Lbs (default)</label>
              <input readOnly value={result?.outputs.fabrication.rows?.[0]?.default_price_lb?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>TOTAL COST</label>
              <input readOnly value={result?.outputs.fabrication.rows?.[0]?.total_cost?.toFixed?.(3) ?? ''} />
            </div>
          </div>
        </section>

        {/* Step 3: Trims */}
        <section className="card">
          <h2>Step 3: Trims & Sewn in Label</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Trims Type</label>
              <select
                value={trims[0].trims_type}
                onChange={e => setTrims([{ ...trims[0], trims_type: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.trims_type?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Garment Part</label>
              <select
                value={trims[0].garment_part}
                onChange={e => setTrims([{ ...trims[0], garment_part: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.garment_part_trim?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Usage (Yard/Piece) (optional input)</label>
              <input
                type="number"
                step="0.001"
                value={trims[0].usage_override}
                onChange={e => setTrims([{ ...trims[0], usage_override: e.target.value }])}
              />
            </div>

            <div className="form-group">
              <label>Price / Unit (optional input)</label>
              <input
                type="number"
                step="0.001"
                value={trims[0].price_override}
                onChange={e => setTrims([{ ...trims[0], price_override: e.target.value }])}
              />
            </div>

            <div className="form-group">
              <label>Material COO</label>
              <select
                value={trims[0].material_coo}
                onChange={e => setTrims([{ ...trims[0], material_coo: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.material_coo?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>UNIT</label>
              <input readOnly value={result?.outputs.trims.rows?.[0]?.unit ?? ''} />
            </div>

            <div className="form-group">
              <label>DEFAULT USAGE (YD/PIECE)</label>
              <input readOnly value={result?.outputs.trims.rows?.[0]?.default_usage?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>DEFAULT PRICE/EACH</label>
              <input readOnly value={result?.outputs.trims.rows?.[0]?.default_price_each?.toFixed?.(3) ?? ''} />
            </div>

            <div className="form-group">
              <label>TOTAL COST</label>
              <input readOnly value={result?.outputs.trims.rows?.[0]?.total_cost?.toFixed?.(3) ?? ''} />
            </div>
          </div>
        </section>

        {/* Step 4: Embellishments */}
        <section className="card">
          <h2>Step 4: Embellishments</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Printing/Embroidery</label>
              <select
                value={embellishments[0].printing_embroidery}
                onChange={e => setEmbellishments([{ ...embellishments[0], printing_embroidery: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.printing_embroidery?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Dimension</label>
              <select
                value={embellishments[0].dimension}
                onChange={e => setEmbellishments([{ ...embellishments[0], dimension: e.target.value }])}
              >
                <option value="">Select...</option>
                {dropdowns.print_dimension?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>
        </section>

        {/* Step 5: Packing & Label */}
        <section className="card">
          <h2>Step 5: Packing & Label</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Pack Count</label>
              <input
                type="number"
                placeholder="e.g., 6"
                value={packingLabel.pack_count}
                onChange={e => setPackingLabel({ ...packingLabel, pack_count: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Display Packaging</label>
              <select
                value={packingLabel.display_packaging}
                onChange={e => setPackingLabel({ ...packingLabel, display_packaging: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.display_packaging?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label>Transit Package</label>
              <input
                type="number"
                placeholder="e.g., 24"
                value={packingLabel.transit_package}
                onChange={e => setPackingLabel({ ...packingLabel, transit_package: e.target.value })}
              />
            </div>

            <div className="form-group">
              <label>Label Type</label>
              <select
                value={packingLabel.label_type}
                onChange={e => setPackingLabel({ ...packingLabel, label_type: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.label?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>
        </section>

        {/* Step 6: Manufacturing */}
        <section className="card">
          <h2>Step 6: Manufacturing</h2>
          {!result ? (
            <p style={{ color: '#6B7280' }}>
              Labour cost will be calculated automatically after Step 1-5 inputs.
            </p>
          ) : (
            <div className="summary-table">
              <div className="summary-header">
                <span>Country</span>
                <span>Minutes</span>
                <span>Labour Cost ($)</span>
              </div>
              {result.outputs.manufacturing.rows.map((row, i) => (
                <div key={i} className="summary-row">
                  <span>{row.country || development.coo || '-'}</span>
                  <span>{(row.minutes ?? 0).toFixed(3)}</span>
                  <span className="cost">${(row.total_cost ?? 0).toFixed(3)}</span>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Fillable Inputs */}
        <section className="card">
          <h2>Additional Costs</h2>
          <div className="form-grid">
            <div className="form-group">
              <label>Supplier Margin (%)</label>
              <input
                type="number"
                step="0.1"
                value={supplierMarginPercent}
                onChange={e => setSupplierMarginPercent(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>Freight Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={freightCost}
                onChange={e => setFreightCost(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>GMO Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={gmoCost}
                onChange={e => setGmoCost(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>Duty Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={dutyCost}
                onChange={e => setDutyCost(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>Additional Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={additionalCost}
                onChange={e => setAdditionalCost(parseFloat(e.target.value) || 0)}
              />
            </div>
          </div>
        </section>

        {/* Loading Indicator */}
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Calculating...</p>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <>
            {/* Total Cost Summary */}
            <section className="card">
              <h2>📊 Total Cost Summary</h2>
              <div className="summary-table">
                <div className="summary-header">
                  <span>Item</span>
                  <span>Cost ($)</span>
                  <span>Proportion (%)</span>
                </div>

                {[
                  { label: '1. Total Fabric Cost', cost: result.outputs.total_cost_summary.total_fabric_cost, pct: result.outputs.total_cost_summary.total_fabric_cost_pct },
                  { label: '2. Total Trim Cost', cost: result.outputs.total_cost_summary.total_trim_cost, pct: result.outputs.total_cost_summary.total_trim_cost_pct },
                  { label: '3. Display Packaging Cost', cost: result.outputs.total_cost_summary.total_display_packaging_cost, pct: result.outputs.total_cost_summary.total_display_packaging_cost_pct },
                  { label: '4. Transit Packaging Cost', cost: result.outputs.total_cost_summary.total_transit_packaging_cost, pct: result.outputs.total_cost_summary.total_transit_packaging_cost_pct },
                  { label: '5. Label Cost', cost: result.outputs.total_cost_summary.total_label_cost, pct: result.outputs.total_cost_summary.total_label_cost_pct },
                  { label: '6. Sewing Thread Cost', cost: result.outputs.total_cost_summary.total_sewing_thread_cost, pct: result.outputs.total_cost_summary.total_sewing_thread_cost_pct },
                  { label: '7. Labour Cost', cost: result.outputs.total_cost_summary.total_labour_cost, pct: result.outputs.total_cost_summary.total_labour_cost_pct },
                  { label: '8. Product Testing Cost', cost: result.outputs.total_cost_summary.total_product_testing_cost, pct: result.outputs.total_cost_summary.total_product_testing_cost_pct },
                  { label: '9. Print/Embroidery Cost', cost: result.outputs.total_cost_summary.total_print_embroidery_cost, pct: result.outputs.total_cost_summary.total_print_embroidery_cost_pct },
                  { label: '10. Other Cost', cost: result.outputs.total_cost_summary.total_other_cost, pct: result.outputs.total_cost_summary.total_other_cost_pct },
                ].map((item, i) => (
                  <div key={i} className="summary-row">
                    <span>{item.label}</span>
                    <span className="cost">${item.cost.toFixed(3)}</span>
                    <span className="pct">{item.pct.toFixed(3)}%</span>
                  </div>
                ))}

                <div className="summary-row subtotal">
                  <span>Subtotal (Items 1-10)</span>
                  <span>${result.outputs.total_cost_summary.subtotal.toFixed(3)}</span>
                  <span>100.000%</span>
                </div>

                <div className="summary-row">
                  <span>11. Supplier Margin ({result.outputs.total_cost_summary.supplier_margin_percent}%)</span>
                  <span>${result.outputs.total_cost_summary.supplier_margin_amount.toFixed(3)}</span>
                  <span>{result.outputs.total_cost_summary.supplier_margin_amount_pct.toFixed(3)}%</span>
                </div>

                <div className="summary-row fob">
                  <span><strong>FOB Cost</strong></span>
                  <span><strong>${result.outputs.total_cost_summary.fob_cost.toFixed(3)}</strong></span>
                  <span></span>
                </div>

                <div className="summary-row">
                  <span>12. Freight Cost</span>
                  <span>${result.outputs.total_cost_summary.freight_cost.toFixed(3)}</span>
                  <span></span>
                </div>

                <div className="summary-row">
                  <span>13. GMO Cost</span>
                  <span>${result.outputs.total_cost_summary.gmo_cost.toFixed(3)}</span>
                  <span></span>
                </div>

                <div className="summary-row">
                  <span>14. Duty Cost</span>
                  <span>${result.outputs.total_cost_summary.duty_cost.toFixed(3)}</span>
                  <span></span>
                </div>

                <div className="summary-row grand-total">
                  <span><strong>Grand Total (FLC)</strong></span>
                  <span><strong>${result.outputs.total_cost_summary.grand_total.toFixed(3)}</strong></span>
                  <span></span>
                </div>
              </div>

              {/* Summary Stats */}
              <div className="summary-stats">
                <div className="stat-box">
                  <label>Total FOB per PIECE</label>
                  <span>${result.outputs.total_cost_summary.total_fob_per_piece.toFixed(3)}</span>
                </div>
                <div className="stat-box">
                  <label>Total FOB per DOZEN</label>
                  <span>${result.outputs.total_cost_summary.total_fob_per_dozen.toFixed(3)}</span>
                </div>
                <div className="stat-box">
                  <label>Total FLC per PIECE</label>
                  <span>${result.outputs.total_cost_summary.total_flc_per_piece.toFixed(3)}</span>
                </div>
                <div className="stat-box">
                  <label>Total FLC per DOZEN</label>
                  <span>${result.outputs.total_cost_summary.total_flc_per_dozen.toFixed(3)}</span>
                </div>
              </div>
            </section>

            {/* Country Comparison */}
            <section className="card">
              <h2>🌍 Country Comparison</h2>
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th>Country</th>
                    <th>Labour Cost</th>
                    <th>Subtotal</th>
                    <th>Margin</th>
                    <th>FOB Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {result.outputs.country_comparison.map((country, i) => (
                    <tr
                      key={i}
                      className={country.country === development.coo ? 'selected' : ''}
                    >
                      <td><strong>{country.country}</strong></td>
                      <td>${country.labour_cost.toFixed(3)}</td>
                      <td>${country.subtotal.toFixed(3)}</td>
                      <td>${country.margin_amount.toFixed(3)}</td>
                      <td className="fob">${country.fob_cost.toFixed(3)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          </>
        )}
      </div>

      <footer>
        <p>Node.js v2 | <a href="https://github.com/Nuntploydanai/CostingIntelligent" target="_blank" rel="noopener">GitHub</a></p>
      </footer>
    </div>
  )
}

export default App
