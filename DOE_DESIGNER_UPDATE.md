# DOE Designer Update Summary

**Date:** 2025-01-XX  
**File:** `pages/6_🀄️_High-Throughput_Formulation.py`  
**Changes:** Added categorical DOE factors and replaced N/P ratio with Ionizable lipid/DNA mass ratio

---

## Major Changes

### 1. Added Categorical Factors

The DOE Designer now supports two new categorical factors:

#### Helper Lipid Types
- **Options:** DSPC, DPPC, DOPE, SM
- **Default:** DSPC
- **MWs:** 790.147, 734.095, 744.174, 725.096 g/mol
- **Concentrations:** 12.5 mg/mL (default for all)

#### Cholesterol Types
- **Options:** Cholesterol, Cholesterol-PEG
- **Default:** Cholesterol
- **MWs:** 386.654, 1114.5 g/mol
- **Concentrations:** 20.0, 10.0 mg/mL

**Usage:**
- Select one or more helper lipid types
- Select one or more cholesterol types
- DOE automatically creates all combinations with your continuous variable ranges

### 2. Replaced N/P Ratio with Ionizable/DNA Mass Ratio

#### Old Variable
- **N/P Ratio:** Amine-to-phosphate molar ratio (0.5-15.0 range)
- **Calculation:** Based on ionizable lipid moles and DNA moles
- **Issues:** Less direct control over formulation

#### New Variable
- **Ionizable/DNA Mass Ratio:** Direct mass ratio of ionizable lipid to DNA
- **Range:** 5.0 - 15.0 (μg ionizable / μg DNA)
- **Default:** 5.0 - 15.0
- **Advantages:**
  - More intuitive and directly related to formulation concentration
  - Easier to control experimentally
  - Better alignment with literature values
  - Clearer relationship to particle properties

### 3. Updated Variable Ranges Section

**Old Interface:**
```
Ionizable Lipid: Min % / Max %
Cholesterol: Min % / Max %
PEG-Lipid: Min % / Max %
N/P Ratio: Min / Max
```

**New Interface:**
```
Ionizable Lipid %: Min / Max
Cholesterol %: Min / Max
PEG-Lipid %: Min / Max
Ionizable/DNA Mass Ratio: Min / Max

[Lipid Type Selection]
Helper Lipid Types: [Multiselect]
Cholesterol Types: [Multiselect]
```

### 4. Updated Design Generation Functions

All design generation functions now:
1. Extract continuous variable ranges only (exclude categorical factors)
2. Generate design matrices for continuous variables
3. Automatically expand with all combinations of categorical factors

**Affected Functions:**
- `generate_2level_factorial()` ✅
- `generate_3level_factorial()` ✅
- `generate_fractional_factorial()` ✅
- `generate_plackett_burman()` ✅
- `generate_box_behnken()` ✅
- `generate_central_composite()` ✅
- `generate_mixture_design()` ✅

**New Helper Functions:**
- `extract_continuous_ranges()` - Filters out categorical factors
- `expand_design_with_categorical()` - Creates all combinations with helper/chol types

### 5. Updated Run Sheet Generation

#### Added Columns
- **Helper_Type:** Selected helper lipid type for each run
- **Chol_Type:** Selected cholesterol type for each run
- **Ion_DNA_Target:** Target ionizable/DNA mass ratio (from DOE design)
- **Ion_DNA_Calc:** Calculated ionizable/DNA mass ratio

#### Removed Columns
- NP_Ratio_Target
- NP_Ratio_Calc

#### Ion/DNA Calculation
```python
ion_mass_ug = vol_ionizable_ul × conc_ionizable_ug/ul
ion_dna_ratio = ion_mass_ug / dna_mass_ug
```

### 6. Updated Validation & Statistics

#### Validation
- Checks that at least one helper lipid type is selected
- Checks that at least one cholesterol type is selected
- Validates continuous variable ranges (Min < Max)

#### Statistics Display
Changed from:
```
N/P: {np_min:.1f} → {np_max:.1f}
```

To:
```
Ion/DNA: {ion_dna_min:.1f} → {ion_dna_max:.1f}
```

### 7. Updated Excel Export Summary

**Old:**
```
N/P Ratio Range: 1.0 - 15.0
```

**New:**
```
Ion/DNA Ratio Range: 5.0 - 15.0
```

---

## Example Usage

### Scenario 1: Compare Two Helper Lipids
1. Select Helper Types: DSPC, DPPC
2. Select Chol Types: Cholesterol
3. Ion %: 45-55%, Chol %: 33.5-43.5%, PEG %: 0.5-2.5%
4. Ion/DNA Ratio: 8.0-12.0
5. **Result:** Design matrix with all combinations of:
   - Ionizable/Cholesterol/PEG percentages
   - 2 helper lipid types × 1 cholesterol type = 2x expansion factor

### Scenario 2: Screen Cholesterol Variants
1. Select Helper Types: DSPC
2. Select Chol Types: Cholesterol, Cholesterol-PEG
3. Design type: Plackett-Burman
4. **Result:** 12-run screening with both cholesterol types

### Scenario 3: Full Optimization
1. Select Helper Types: DSPC, DPPC, DOPE
2. Select Chol Types: Cholesterol, Cholesterol-PEG
3. Design type: Central Composite
4. **Result:** Comprehensive response surface with 3×2 = 6x categorical combinations

---

## Data Integration

### Helper Lipid Properties
| Type | MW (g/mol) | Stock (mg/mL) | Key Properties |
|------|-----------|---------------|---|
| DSPC | 790.147 | 12.5 | Standard, high stability |
| DPPC | 734.095 | 12.5 | Longer acyl chains |
| DOPE | 744.174 | 12.5 | Unsaturated, fusogenic |
| SM | 725.096 | 12.5 | Natural composition |

### Cholesterol Properties
| Type | MW (g/mol) | Stock (mg/mL) | Key Features |
|------|-----------|---------------|---|
| Cholesterol | 386.654 | 20.0 | Standard, rigid |
| Cholesterol-PEG | 1114.5 | 10.0 | Stealth, PEGylated |

---

## DNA Concentration

**Updated Default:** 0.56 mg/mL (was 1.00 mg/mL)
- Based on experimental data analysis
- Matches pDNA formulation protocol
- More accurate for typical DNA stock solutions

---

## Calculation Logic

### Ionizable/DNA Mass Ratio Relationship to N/P Ratio

```
Given:
  - Total Lipid/DNA = 15:1 (mass ratio)
  - Ionizable % = 50.04%
  - DNA MW = 330 g/mol
  - Ionizable MW = 710.182 g/mol

Derivation:
  Ionizable_mass = Total_lipid_mass × 0.5004
  Ionizable_moles = Ionizable_mass / MW_ion
  DNA_moles = DNA_mass / 330
  N/P = Ionizable_moles / DNA_moles
      = (Ionizable_mass / 710.182) / (DNA_mass / 330)
      = (Ionizable_mass / DNA_mass) × (330 / 710.182)
      ≈ Ion_DNA_mass_ratio × 0.464

Example:
  Ion_DNA_mass_ratio = 8.6
  N/P ≈ 8.6 × 0.464 ≈ 4.0
```

---

## Backwards Compatibility

⚠️ **Note:** This update changes the design variable structure
- Old designs with N/P ratio cannot be directly loaded
- New designs will include Helper_Type and Chol_Type columns
- Run sheets will have Ion_DNA columns instead of NP_Ratio columns
- All formulation calculations remain unchanged (15:1 lipid/DNA, 3:1 aqueous/organic)

---

## Files Modified

- ✅ `pages/6_🀄️_High-Throughput_Formulation.py`
  - Lines 1-250: UI configuration with helper/chol type selectors
  - Lines 250-300: Design generation functions (updated to handle categorical factors)
  - Lines 600-670: generate_run_sheet() function (updated column names)
  - Lines 880-950: Results display and statistics (updated variable names)

---

## Testing Recommendations

1. **Test Categorical Expansion**
   - Select 2 helper types + 2 chol types = should generate 4x more rows
   - Verify all combinations appear in run sheet

2. **Test Ion/DNA Ratio Calculation**
   - Verify Ion/DNA ratio matches manual calculation
   - Check ratio values are within expected range (5-15)

3. **Test All DOE Types**
   - Each design method should work with categorical factors
   - Verify run counts are reasonable

4. **Test Export**
   - CSV should include Helper_Type, Chol_Type, Ion_DNA_Target, Ion_DNA_Calc
   - Excel summary should show Ion/DNA ratio range

---

**Status:** ✅ Implementation Complete  
**Error Checking:** ✅ No syntax errors  
**Ready for Testing:** ✅ Yes
