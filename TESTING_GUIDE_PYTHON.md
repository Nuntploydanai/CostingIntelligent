# 🧪 COMPREHENSIVE TESTING GUIDE - Python Version

## ✅ Current Status
- Branch: **main** (Python/FastAPI)
- Server: http://127.0.0.1:8000
- Status: **READY TO TEST**

---

## 📋 TEST SCENARIOS

### **TEST 1: Basic Calculation (Single Fabric)**

#### **Step 1: Development**
- Gender: **Men**
- Silhouette: **Tank Top/A Shirt**
- Seam: **Side Seam**
- Color Design: (leave empty)
- Size: **S**
- Pack Count: (leave empty)
- Ideal Quantity: **1K-3K**
- COO: **BANGLADESH**
- Fabric Finishing: (leave empty)

#### **Step 2: Fabrication (1 fabric)**
- Fabric Type: **Jersey**
- Fabric Contents: **Cotton/Spandex 95/5**
- Using Part: **Self Fabric**
- Weight GSM Override: (leave empty)
- Price Unit: **Price / YD**
- Price Value: (leave empty)
- Material COO: (leave empty)

#### **Step 3: Trims**
- Leave empty for now

#### **Step 4: Embellishments**
- Leave empty for now

#### **Step 5: Packing & Label**
- Display Packaging: (leave empty)
- Transit Package: (leave empty)
- Label Type: (leave empty)

#### **Step 6: Manufacturing**
- Should auto-calculate based on Development inputs

#### **Additional Costs:**
- Supplier Margin: **7%**
- Freight: **0**
- GMO: **0**
- Duty: **0**
- Additional: **0**

---

### **✅ EXPECTED RESULTS:**

#### **Total Cost Summary:**
```
1. Total Fabric Cost           $18.160    ~99.130%
2. Total Trim Cost              $0.000     0.000%
3. Display Packaging Cost       $0.000     0.000%
4. Transit Packaging Cost       $0.000     0.000%
5. Label Cost                   $0.000     0.000%
6. Sewing Thread Cost           $0.014     ~0.076%
7. Labour Cost                  $0.145     ~0.791%
8. Product Testing Cost         $0.010     ~0.055%
9. Print/Embroidery Cost        $0.000     0.000%
10. Other Cost                  $0.000     0.000%

Subtotal                        $18.319   100.000%
11. Supplier Margin (7%)        $1.282     6.998%

FOB Cost                        $19.601
Grand Total (FLC)               $19.601
```

#### **Country Comparison:**
```
INDIA          $19.586
BANGLADESH     $19.601  ← SELECTED
INDONESIA      $19.581
THAILAND       $19.736
CAMBODIA       $19.690
VIETNAM        $19.680
```

---

### **TEST 2: With Custom Fabric Price**

#### **Same as TEST 1, but:**
- Price Value: **2.50** (override default price)

#### **Expected:**
- Fabric cost should be HIGHER
- FOB cost should be HIGHER
- All % proportions should change

---

### **TEST 3: With Additional Costs**

#### **Same as TEST 1, but:**
- Freight: **0.05**
- GMO: **0.03**
- Duty: **0.02**

#### **Expected:**
- FOB Cost: $19.601 (same)
- Grand Total (FLC): $19.601 + 0.05 + 0.03 + 0.02 = **$19.701**

---

### **TEST 4: Different Silhouette**

#### **Same as TEST 1, but:**
- Silhouette: **Basic Collar Shirt** (instead of Tank Top/A Shirt)

#### **Expected:**
- Different SAM minutes
- Different labour cost
- Different FOB cost

---

### **TEST 5: Different COO**

#### **Same as TEST 1, but:**
- COO: **INDIA** (instead of BANGLADESH)

#### **Expected:**
- Different labour cost (India vs Bangladesh)
- Different FOB cost
- INDIA row should be highlighted in country comparison

---

## 🎯 WHAT TO CHECK:

### **✅ Functionality:**
- [ ] All dropdowns load correctly
- [ ] Auto-calculation works (500ms delay)
- [ ] All values show 3 decimal places
- [ ] Country comparison shows 6 countries
- [ ] Selected COO is highlighted
- [ ] FOB/FLC calculations are correct

### **✅ Excel Parity:**
- [ ] Calculations match Excel formulas
- [ ] Same rounding behavior (3 decimals)
- [ ] Same cost items (16 total)
- [ ] Same country comparison logic

### **✅ UI/UX:**
- [ ] Clear layout
- [ ] Easy to understand
- [ ] Responsive (works on different screen sizes)
- [ ] Highlighted important values

---

## 🐛 IF YOU FIND ISSUES:

**Tell me:**
1. Which test you were running
2. What you expected to see
3. What you actually saw
4. Screenshot if possible

---

## 📊 COMPARISON WITH EXCEL:

**If you have Excel file, compare:**
- Total Fabric Cost
- Labour Cost
- FOB Cost
- Country Comparison values

---

## ✅ WHEN TESTING IS COMPLETE:

**Tell me:**
- "All tests passed!" → I'll start fixing Node.js version
- "Found issues:" → I'll fix Python version first

---

**Start with TEST 1 and work through each test!** 🚀

**Take screenshots of any issues you find!** 📸
