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
  const asset = (p: string) => `/${p}`
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CalculateResponse | null>(null)

  const newFabricRow = () => ({
    fabric_type: '',
    fabric_contents: '',
    using_part: '',
    weight_gsm_override: '',
    price_unit: 'Price / YD',
    price_value: '',
    material_coo: ''
  })

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

  const [fabrication, setFabrication] = useState([newFabricRow()])
  const [fabricContentsOptions, setFabricContentsOptions] = useState<string[][]>([[]])

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

  // Admin data upload/download (lookup CSV only)
  const [lookupFiles, setLookupFiles] = useState<string[]>([])
  const [selectedLookupFile, setSelectedLookupFile] = useState('')
  const [uploadStatus, setUploadStatus] = useState('')

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

    fetch('/api/admin/lookup-files')
      .then(res => res.json())
      .then(data => {
        const files = data?.files || []
        setLookupFiles(files)
        setSelectedLookupFile(files[0] || '')
      })
      .catch(() => {
        setLookupFiles([])
        setSelectedLookupFile('')
      })
  }, [])

  // Auto-calculate with debounce
  const calculateCost = useCallback(async () => {
    // Step 6 (Manufacturing) should calculate from Step 1 even if Step 2+ are empty
    if (!development.gender || !development.silhouette || !development.seam || !development.size || !development.ideal_quantity || !development.coo) {
      return
    }

    if (invalidFabricationRows.length > 0) {
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          development,
          fabrication: fabrication.filter(fabricationHasValue),
          trims: trims.filter(trimsHasValue),
          embellishments: embellishments.filter(embellishmentHasValue),
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

  const flagCodeByCountry: Record<string, string> = {
    BANGLADESH: 'bd',
    INDIA: 'in',
    INDONESIA: 'id',
    THAILAND: 'th',
    CAMBODIA: 'kh',
    VIETNAM: 'vn',
    CHINA: 'cn',
    'SOUTH AFRICA': 'za',
    PAKISTAN: 'pk',
    MALAYSIA: 'my',
    LAOS: 'la',
    'SRI LANKA': 'lk',
    KENYA: 'ke',
    EGYPT: 'eg',
    JORDAN: 'jo',
    OTHER: 'unknown',
  }

  const flagPath = (country: string) => {
    const code = flagCodeByCountry[(country || '').toUpperCase()]
    return code ? `/flags/${code}.svg` : '/flags/unknown.svg'
  }

  const imageSheetMap: Record<string, string> = {
    // Source: Excel "Image" sheet (sheet15), row-anchored drawing map
    'men|tank top/a shirt': '/excel_media/image59.png',
    'men|t-shirt (crew neck)': '/excel_media/image64.jpeg',
    'men|t-shirt (v neck)': '/excel_media/image58.png',
    'men|long sleeve shirt (crew neck)': '/excel_media/image61.jpeg',
    'men|long sleeve shirt (v neck)': '/excel_media/image63.png',
    'men|sleeveless shirt (crew neck)': '/excel_media/image60.png',
    'men|sleeveless shirt (v neck)': '/excel_media/image62.jpeg',

    'women|tank top/a shirt': '/excel_media/image68.jpeg',
    'women|t-shirt (crew neck)': '/excel_media/image66.jpeg',
    'women|t-shirt (v neck)': '/excel_media/image67.png',
    'women|long sleeve shirt (crew neck)': '/excel_media/image70.jpeg',
    'women|long sleeve shirt (v neck)': '/excel_media/image65.jpeg',
    'women|sleeveless shirt (crew neck)': '/excel_media/image69.jpeg',
    'women|sleeveless shirt (v neck)': '/excel_media/image71.png',

    'kids|tank top/a shirt': '/excel_media/image75.png',
    'kids|t-shirt (crew neck)': '/excel_media/image77.png',
    'kids|t-shirt (v neck)': '/excel_media/image78.png',
    'kids|long sleeve shirt (crew neck)': '/excel_media/image76.png',
    'kids|long sleeve shirt (v neck)': '/excel_media/image72.png',
    'kids|sleeveless shirt (crew neck)': '/excel_media/image74.png',
    'kids|sleeveless shirt (v neck)': '/excel_media/image73.png',
  }

  const dimensionsByPrintType: Record<string, string[]> = {
  'Rubber_Print': ['1X1 cm','2X2 cm','3X3 cm','4X4 cm','2X1 cm','3X1 cm','4X1 cm','5X1 cm','6X1 cm','7 X1 cm','8X1 cm','9X1 cm','10X1 cm'],
  'Heat_Transfer': ['20X10 mm','30X10 mm','30X30 mm','40X20 mm','40X30 mm','40X40 mm','50X20 mm','50X30 mm','50X40 mm','50X50 mm'],
  'Embroidery': ['27 mm x 18 mm(1162 Stitch)','35 mm x 24 mm(1745 Stitch)','43 mm x 29 mm(2404 Stitch)','55 mm x 37 mm(3195 Stitch)','60 mm x 41 mm(3343 Stitch)','27 mm x 18 mm(2271 Stitch)','35 mm x 24 mm(3004 Stitch)','35 mm x 24 mm(2284 Stitch)','29 mm x 43 mm(3053 Stitch)','41 mm x 60 mm(3994 Stitch)','36 mm x 54 mm(3659 Stitch)'],
  'Pignment_Print': ['Fabric  base White 1-3 colours','Fabric base Solid 1-3 colours','Fabric  base  Solid AOP','Fabric base White  AOP'],
  'Reactive_Print': ['Fabric  base White 1-3 colours','Fabric base Solid 1-3 colours','Fabric  base  Solid AOP','Fabric base White  AOP'],
  'Digital_Print': ['AOP'],
  'Sublimation_Print': ['AOP'],
}

  const normalizePackCount = (value: string) => (value || '').replace(/^X/i, '')

  const fabricationHasValue = (row: any) => {
    return Boolean(row.fabric_type || row.fabric_contents || row.using_part || row.weight_gsm_override || row.price_value || row.material_coo)
  }

  const trimsHasValue = (row: any) => {
    return Boolean(row.trims_type || row.garment_part || row.usage_override || row.price_override || row.material_coo)
  }

  const embellishmentHasValue = (row: any) => {
    return Boolean(row.printing_embroidery || row.dimension || row.usage_unit)
  }

  const invalidFabricationRows = fabrication
    .map((row, idx) => ({ row, idx }))
    .filter(({ row }) => (row.fabric_type || row.fabric_contents) && !row.using_part)
    .map(({ idx }) => idx)

  const modelPhotoBySilhouette = (silhouette: string, gender: string, _color: string) => {
    const g = (gender || '').trim().toLowerCase()
    const s = (silhouette || '').trim().toLowerCase()

    // default state: show Gildan logo before user makes selections
    if (!g && !s) return asset('brand/gildan-logo.jpg')

    const direct = imageSheetMap[`${g}|${s}`]
    if (direct) return direct

    // fallback if combo not found
    return asset('brand/gildan-logo.jpg')
  }

  const fetchFabricContents = async (fabricType: string, rowIndex: number) => {
  if (!fabricType) {
    setFabricContentsOptions(prev => prev.map((opts, i) => i === rowIndex ? [] : opts))
    return
  }
  try {
    const res = await fetch(`/api/dropdown/fabric_contents_for_type?type=${encodeURIComponent(fabricType)}`)
    const data = await res.json()
    setFabricContentsOptions(prev => prev.map((opts, i) => i === rowIndex ? (data.values || []) : opts))
  } catch {
    setFabricContentsOptions(prev => prev.map((opts, i) => i === rowIndex ? [] : opts))
  }
}
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
    setFabrication([newFabricRow()])
    setFabricContentsOptions([[]])
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

  const downloadLookupFile = () => {
    if (!selectedLookupFile) return
    window.open(`/api/admin/lookup-files/${selectedLookupFile}/download`, '_blank')
  }

  const uploadLookupFile = async (file: File | null) => {
    if (!file || !selectedLookupFile) return
    setUploadStatus('Uploading...')
    const content = await file.text()

    const response = await fetch(`/api/admin/lookup-files/${selectedLookupFile}/upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })

    const data = await response.json()
    if (!response.ok) {
      setUploadStatus(`❌ ${data?.error || 'Upload failed'}`)
      return
    }

    setUploadStatus(`✅ Uploaded ${selectedLookupFile} (${data.rows} rows). Backup: ${data.backup}`)
  }

  return (
    <div className="container theme-midnight">
      <header className="brand-header">
        <div className="brand-title-wrap">
          <img src={asset('brand/gildan-mark.svg')} alt="Gildan" className="brand-logo" onError={(e) => { e.currentTarget.src = asset('brand/gildan-logo.jpg') }} />
          <h1>BASIC-A TSHIRT QUICK COST TOOLS</h1>
        </div>
        <div className="header-actions">
          <button onClick={clearForm} className="clear-button">
            Clear Form
          </button>
        </div>
      </header>

      <div className="main-content">
        <section className="card">
          <div className="section-head-row">
            <h2>Admin Data (Lookup CSV Upload/Download)</h2>
          </div>
          <div className="form-grid">
            <div className="form-group">
              <label>Editable Lookup File</label>
              <select value={selectedLookupFile} onChange={e => setSelectedLookupFile(e.target.value)}>
                {lookupFiles.map(file => <option key={file} value={file}>{file}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Download Current CSV</label>
              <button className="clear-button" style={{ background: '#0b2f59' }} onClick={downloadLookupFile}>Download</button>
            </div>
            <div className="form-group">
              <label>Upload Updated CSV (same header/order)</label>
              <input
                type="file"
                accept=".csv,text/csv"
                onChange={e => uploadLookupFile(e.target.files?.[0] || null)}
              />
            </div>
          </div>
          {uploadStatus ? <p style={{ marginTop: 10 }}>{uploadStatus}</p> : null}
        </section>

        {/* Step 1: Development */}
        <section className="card">
          <h2>Step 1: Development</h2>
          <div className="dev-layout">
            <div className="preview-wrap">
              <img
                src={modelPhotoBySilhouette(development.silhouette, development.gender, development.color_design)}
                alt="Garment"
                className="preview-photo"
              />
            </div>

            <div className="dev-form-grid">
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
                  value={normalizePackCount(development.pack_count)}
                  onChange={e => setDevelopment({ ...development, pack_count: normalizePackCount(e.target.value) })}
                >
                  <option value="">Select...</option>
                  {dropdowns.pack_count?.map(v => {
                    const n = normalizePackCount(v)
                    return <option key={v} value={n}>{n}</option>
                  })}
                </select>
              </div>

              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  COO (Country of Origin)
                  <img className="country-flag-img" src={flagPath(development.coo)} alt="flag" />
                </label>
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
          </div>
        </section>

        {/* Step 2: Fabrication */}
        <section className="card">
          <div className="section-head-row">
            <h2>Step 2: Fabrication (Up to 3 Fabric Types)</h2>
            <div style={{ display: 'flex', gap: 8 }}>
              <button
                className="clear-button"
                onClick={() => {
                  if (fabrication.length >= 3) return
                  setFabrication([...fabrication, newFabricRow()])
                  setFabricContentsOptions(prev => [...prev, []])   // ← add this
                }}
                style={{ background: fabrication.length >= 3 ? '#94a3b8' : '#0b2f59' }}
              >
                + Add Fabric Type
              </button>
            </div>
          </div>

          {fabrication.map((row, i) => (
            <div key={i} className="fabric-row-card">
              <div className="section-head-row" style={{ marginBottom: 10 }}>
                <h3 style={{ margin: 0, color: '#0b3f77' }}>Fabric Row {i + 1}</h3>
                {fabrication.length > 1 && (
                  <button
                    className="clear-button"
                    style={{ background: '#b91c1c' }}
                    onClick={() => {
                    setFabrication(fabrication.filter((_, idx) => idx !== i))
                    setFabricContentsOptions(prev => prev.filter((_, idx) => idx !== i))
                    }}
                    
                    
                  >
                    Remove
                  </button>
                )}
              </div>

              {invalidFabricationRows.includes(i) && (
                <div className="inline-alert">⚠ Please select <strong>Using Part</strong> for this row.</div>
              )}

              <div className="form-grid">
                <div className="form-group">
                  <label>Fabric Type</label>
                  <select value={row.fabric_type} onChange={e => {const val = e.target.value; setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, fabric_type: val, fabric_contents: '' } : r)); fetchFabricContents(val, i)}}>
                    <option value="">Select...</option>
                    {dropdowns.fabric_type?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Fabric Contents</label>
                  <select value={row.fabric_contents} onChange={e => setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, fabric_contents: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {fabricContentsOptions[i]?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Using Part</label>
                  <select value={row.using_part} onChange={e => setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, using_part: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.using_part?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Weight (GSM)</label>
                  <input type="number" step="0.001" value={row.weight_gsm_override} onChange={e => setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, weight_gsm_override: e.target.value } : r))} />
                </div>

                <div className="form-group">
                  <label>Price Unit</label>
                  <select value={row.price_unit} onChange={e => setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, price_unit: e.target.value } : r))}>
                    {dropdowns.price_unit?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Price Value</label>
                  <input type="number" step="0.001" value={row.price_value} onChange={e => setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, price_value: e.target.value } : r))} />
                </div>

                <div className="form-group">
                  <label>Material COO</label>
                  <select value={row.material_coo} onChange={e => setFabrication(fabrication.map((r, idx) => idx === i ? { ...r, material_coo: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.material_coo?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Fixed Fabric Width</label>
                  <input readOnly value={result?.outputs.fabrication.rows?.[i]?.fixed_fabric_width?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Default Weight (GSM)</label>
                  <input readOnly value={result?.outputs.fabrication.rows?.[i]?.default_weight_gsm?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Default (Price/YD)</label>
                  <input readOnly value={result?.outputs.fabrication.rows?.[i]?.default_price_yd?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Default (Price/Kilo)</label>
                  <input readOnly value={result?.outputs.fabrication.rows?.[i]?.default_price_kilo?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Price / Lbs (default)</label>
                  <input readOnly value={result?.outputs.fabrication.rows?.[i]?.default_price_lb?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Total Cost</label>
                  <input readOnly value={result?.outputs.fabrication.rows?.[i]?.total_cost?.toFixed?.(3) ?? ''} />
                </div>
              </div>
            </div>
          ))}

          <div style={{ marginTop: 12, fontWeight: 700, color: '#0b3f77' }}>
            Fabric Total Cost: ${(result?.outputs.fabrication.total_fabric_cost ?? 0).toFixed(2)}
          </div>
        </section>

        {/* Step 3: Trims */}
        <section className="card">
          <div className="section-head-row">
            <h2>Step 3: Trims & Sewn in Label (Up to 3 Types)</h2>
            <button
              className="clear-button"
              onClick={() => {
                if (trims.length >= 3) return
                setTrims([...trims, { trims_type: '', garment_part: '', usage_override: '', price_override: '', material_coo: '' }])
              }}
              style={{ background: trims.length >= 3 ? '#94a3b8' : '#0b2f59' }}
            >
              + Add Trim Type
            </button>
          </div>

          {trims.map((row, i) => (
            <div key={i} className="fabric-row-card">
              <div className="section-head-row" style={{ marginBottom: 10 }}>
                <h3 style={{ margin: 0, color: '#0b3f77' }}>Trim Row {i + 1}</h3>
                {trims.length > 1 && (
                  <button className="clear-button" style={{ background: '#b91c1c' }} onClick={() => setTrims(trims.filter((_, idx) => idx !== i))}>
                    Remove
                  </button>
                )}
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label>Trims Type</label>
                  <select value={row.trims_type} onChange={e => setTrims(trims.map((r, idx) => idx === i ? { ...r, trims_type: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.trims_type?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Garment Part</label>
                  <select value={row.garment_part} onChange={e => setTrims(trims.map((r, idx) => idx === i ? { ...r, garment_part: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.garment_part_trim?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Usage (Yard/Piece) (optional input)</label>
                  <input type="number" step="0.001" value={row.usage_override} onChange={e => setTrims(trims.map((r, idx) => idx === i ? { ...r, usage_override: e.target.value } : r))} />
                </div>

                <div className="form-group">
                  <label>Price / Unit (optional input)</label>
                  <input type="number" step="0.001" value={row.price_override} onChange={e => setTrims(trims.map((r, idx) => idx === i ? { ...r, price_override: e.target.value } : r))} />
                </div>

                <div className="form-group">
                  <label>Material COO</label>
                  <select value={row.material_coo} onChange={e => setTrims(trims.map((r, idx) => idx === i ? { ...r, material_coo: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.material_coo?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Unit</label>
                  <input readOnly value={result?.outputs.trims.rows?.[i]?.unit ?? ''} />
                </div>

                <div className="form-group">
                  <label>Default Usage (YD/piece)</label>
                  <input readOnly value={result?.outputs.trims.rows?.[i]?.default_usage?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Default Price/each</label>
                  <input readOnly value={result?.outputs.trims.rows?.[i]?.default_price_each?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Total cost</label>
                  <input readOnly value={result?.outputs.trims.rows?.[i]?.total_cost?.toFixed?.(3) ?? ''} />
                </div>
              </div>
            </div>
          ))}

          <div style={{ marginTop: 12, fontWeight: 700, color: '#0b3f77' }}>
            Trim Total Cost: ${(result?.outputs.trims.total_trim_cost ?? 0).toFixed(2)}
          </div>
        </section>

        {/* Step 4: Embellishments */}
        <section className="card">
          <div className="section-head-row">
            <h2>Step 4: Embellishments (Up to 3 Types)</h2>
            <button
              className="clear-button"
              onClick={() => {
                if (embellishments.length >= 3) return
                setEmbellishments([...embellishments, { printing_embroidery: '', dimension: '', usage_unit: '' }])
              }}
              style={{ background: embellishments.length >= 3 ? '#94a3b8' : '#0b2f59' }}
            >
              + Add Embellishment
            </button>
          </div>

          {embellishments.map((row, i) => (
            <div key={i} className="fabric-row-card">
              <div className="section-head-row" style={{ marginBottom: 10 }}>
                <h3 style={{ margin: 0, color: '#0b3f77' }}>Embellishment Row {i + 1}</h3>
                {embellishments.length > 1 && (
                  <button className="clear-button" style={{ background: '#b91c1c' }} onClick={() => setEmbellishments(embellishments.filter((_, idx) => idx !== i))}>
                    Remove
                  </button>
                )}
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label>Printing/Embroidery</label>
                  <select value={row.printing_embroidery} onChange={e => setEmbellishments(embellishments.map((r, idx) => idx === i ? { ...r, printing_embroidery: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.printing_embroidery?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Dimension</label>
                  <select value={row.dimension} onChange={e => setEmbellishments(embellishments.map((r, idx) => idx === i ? { ...r, dimension: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {(dimensionsByPrintType[row.printing_embroidery] || dropdowns.print_dimension || []).map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Usage / Unit</label>
                  <select value={row.usage_unit} onChange={e => setEmbellishments(embellishments.map((r, idx) => idx === i ? { ...r, usage_unit: e.target.value } : r))}>
                    <option value="">Select...</option>
                    {dropdowns.usage_unit?.map(v => <option key={v} value={v}>{v}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label>Default Price / Each</label>
                  <input readOnly value={result?.outputs.embellishments.rows?.[i]?.default_price_each?.toFixed?.(3) ?? ''} />
                </div>

                <div className="form-group">
                  <label>Total</label>
                  <input readOnly value={result?.outputs.embellishments.rows?.[i]?.total_cost?.toFixed?.(3) ?? ''} />
                </div>
              </div>
            </div>
          ))}

          <div style={{ marginTop: 12, fontWeight: 700, color: '#0b3f77' }}>
            Embellishment Total Cost: ${(result?.outputs.embellishments.total_embellishment_cost ?? 0).toFixed(2)}
          </div>
        </section>

        {/* Step 5: Packing & Label */}
        <section className="card">
          <h2>Step 5: Packing and Label</h2>
          {/* Display Packaging Row */}
          <h3 style={{ marginTop: '1rem', marginBottom: '0.5rem', color: '#1e3a5f' }}>Display Packaging</h3>
          <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
            <div className="form-group">
              <label>Details</label>
              <select
                value={packingLabel.display_packaging}
                onChange={e => setPackingLabel({ ...packingLabel, display_packaging: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.display_packaging?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Default Usage</label>
              <input readOnly value={result?.outputs.packing_label.display_packaging.default_usage?.toFixed?.(2) ?? ''} />
            </div>
            <div className="form-group">
              <label>Total</label>
              <input readOnly value={result?.outputs.packing_label.display_packaging.total?.toFixed?.(2) ?? ''} />
            </div>
          </div>

          {/* Transit Package Row */}
          <h3 style={{ marginTop: '1rem', marginBottom: '0.5rem', color: '#1e3a5f' }}>Transit Package</h3>
          <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
            <div className="form-group">
              <label>Details</label>
              <select
                value={packingLabel.transit_package}
                onChange={e => setPackingLabel({ ...packingLabel, transit_package: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.transit_package?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Default Usage</label>
              <input readOnly value={result?.outputs.packing_label.transit_package.default_usage?.toFixed?.(2) ?? ''} />
            </div>
            <div className="form-group">
              <label>Total</label>
              <input readOnly value={result?.outputs.packing_label.transit_package.total?.toFixed?.(2) ?? ''} />
            </div>
          </div>

          {/* Label Row */}
          <h3 style={{ marginTop: '1rem', marginBottom: '0.5rem', color: '#1e3a5f' }}>Label</h3>
          <div className="form-grid" style={{ gridTemplateColumns: '1fr 1fr 1fr' }}>
            <div className="form-group">
              <label>Details</label>
              <select
                value={packingLabel.label_type}
                onChange={e => setPackingLabel({ ...packingLabel, label_type: e.target.value })}
              >
                <option value="">Select...</option>
                {dropdowns.label?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Default Usage</label>
              <input readOnly value={result?.outputs.packing_label.label.default_usage?.toFixed?.(2) ?? ''} />
            </div>
            <div className="form-group">
              <label>Total</label>
              <input readOnly value={result?.outputs.packing_label.label.total?.toFixed?.(2) ?? ''} />
            </div>
          </div>

  
         
        </section>

        {/* Step 6: Manufacturing */}
        <section className="card">
          <h2>Step 6: Manufacturing Cost</h2>
          {!result ? (
            <p style={{ color: '#6B7280' }}>
              Manufacturing cost based on COO selected in Step 1.
            </p>
          ) : (
            <div className="form-grid">
              <div className="form-group">
                <label>Minutes</label>
                <input readOnly value={result.outputs.manufacturing.rows?.[0]?.minutes?.toFixed?.(3) ?? ''} />
              </div>
              <div className="form-group">
                <label>Cost Rate</label>
                <input readOnly value={result.outputs.manufacturing.rows?.[0]?.cost_rate?.toFixed?.(3) ?? ''} />
              </div>
              <div className="form-group">
                <label>Efficiency</label>
                <input readOnly value={result.outputs.manufacturing.rows?.[0]?.efficiency?.toFixed?.(3) ?? ''} />
              </div>
              <div className="form-group">
                <label>Total Cost</label>
                <input readOnly value={result.outputs.manufacturing.rows?.[0]?.total_cost?.toFixed?.(3) ?? ''} />
              </div>
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
                value={supplierMarginPercent || ''}
                onChange={e => setSupplierMarginPercent(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>Freight Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={freightCost || ''}
                onChange={e => setFreightCost(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>GMO Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={gmoCost || ''}
                onChange={e => setGmoCost(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>Duty Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={dutyCost || ''}
                onChange={e => setDutyCost(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="form-group">
              <label>Additional Cost ($)</label>
              <input
                type="number"
                step="0.001"
                value={additionalCost || ''}
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
                    <span className="cost">${item.cost.toFixed(2)}</span>
                    <span className="pct">{item.pct.toFixed(2)}%</span>
                  </div>
                ))}

                <div className="summary-row subtotal">
                  <span>Subtotal (Items 1-10)</span>
                  <span>${result.outputs.total_cost_summary.subtotal.toFixed(2)}</span>
                  <span>100.00%</span>
                </div>

                <div className="summary-row">
                  <span>11. Supplier Margin ({result.outputs.total_cost_summary.supplier_margin_percent}%)</span>
                  <span>${result.outputs.total_cost_summary.supplier_margin_amount.toFixed(2)}</span>
                  <span>{result.outputs.total_cost_summary.supplier_margin_amount_pct.toFixed(2)}%</span>
                </div>

                <div className="summary-row fob">
                  <span><strong>FOB Cost</strong></span>
                  <span><strong>${result.outputs.total_cost_summary.fob_cost.toFixed(2)}</strong></span>
                  <span></span>
                </div>

                <div className="summary-row">
                  <span>12. Freight Cost</span>
                  <span>${result.outputs.total_cost_summary.freight_cost.toFixed(2)}</span>
                  <span></span>
                </div>

                <div className="summary-row">
                  <span>13. GMO Cost</span>
                  <span>${result.outputs.total_cost_summary.gmo_cost.toFixed(2)}</span>
                  <span></span>
                </div>

                <div className="summary-row">
                  <span>14. Duty Cost</span>
                  <span>${result.outputs.total_cost_summary.duty_cost.toFixed(2)}</span>
                  <span></span>
                </div>

                <div className="summary-row grand-total">
                  <span><strong>Grand Total (FLC)</strong></span>
                  <span><strong>${result.outputs.total_cost_summary.grand_total.toFixed(2)}</strong></span>
                  <span></span>
                </div>
              </div>

              {/* Summary Stats */}
              <div className="summary-stats">
                <div className="stat-box">
                  <label>Total FOB per PIECE</label>
                  <span>${result.outputs.total_cost_summary.total_fob_per_piece.toFixed(2)}</span>
                </div>
                <div className="stat-box">
                  <label>Total FOB per DOZEN</label>
                  <span>${result.outputs.total_cost_summary.total_fob_per_dozen.toFixed(2)}</span>
                </div>
                <div className="stat-box">
                  <label>Total FLC per PIECE</label>
                  <span>${result.outputs.total_cost_summary.total_flc_per_piece.toFixed(2)}</span>
                </div>
                <div className="stat-box">
                  <label>Total FLC per DOZEN</label>
                  <span>${result.outputs.total_cost_summary.total_flc_per_dozen.toFixed(2)}</span>
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
                      <td>
                        <strong style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                          <img className="country-flag-img" src={flagPath(country.country)} alt="flag" />
                          {country.country}
                        </strong>
                      </td>
                      <td>${country.labour_cost.toFixed(2)}</td>
                      <td>${country.subtotal.toFixed(2)}</td>
                      <td>${country.margin_amount.toFixed(2)}</td>
                      <td className="fob">${country.fob_cost.toFixed(2)}</td>
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
