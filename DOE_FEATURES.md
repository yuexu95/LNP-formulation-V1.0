# LNP-Flow: Professional DOE Designer - Features Overview

## 🀄 High-Throughput Formulation Page (Page 6)

### Complete DOE Design Suite

#### 1. **DOE Design Types Supported**

- **Full Factorial (2-Level)**: 2^5 = 32 runs
  - Tests all combinations of high/low levels
  - Best for initial exploration of design space
  - Comprehensive but requires more experiments

- **Full Factorial (3-Level)**: 3^5 = 243 runs
  - Tests 3 levels per factor (low, center, high)
  - More detailed mapping of design space
  - Better for identifying non-linear relationships

- **Fractional Factorial**: 2^(5-1) = 16 runs
  - Reduced subset of full factorial
  - More efficient for many factors
  - Assumes some interactions are negligible

- **Plackett-Burman**: 12-20 runs
  - Screening design for 7+ factors
  - Identifies most important variables quickly
  - Efficient but with fewer degrees of freedom

- **Box-Behnken**: ~26 runs
  - Response surface methodology design
  - Efficient for optimizing near a target
  - Includes center points for curvature detection
  - Fewer runs than full factorial

- **Central Composite**: ~30 runs
  - Full factorial + axial + center points
  - Comprehensive response surface modeling
  - Best after initial screening phases
  - Allows fitting of quadratic polynomial models

- **Mixture Design**: Variable runs
  - Optimized for proportional components
  - Perfect for LNP formulation ratios (sum to 100%)
  - Simplex lattice design

#### 2. **Design Space Parameters**

**Molar Ratio Variables:**
- Ionizable Lipid % (default: 40-50%)
- Cholesterol % (default: 35-45%)
- PEG-Lipid % (default: 1-3%)
- Helper Lipid % (auto-calculated: 100% - Ion% - Chol% - PEG%)

**Process Parameters:**
- Total Flow Rate (TFR) in mL/min (default: 8-15)
- Flow Rate Ratio (FRR) - Aqueous:Ethanol (default: 2-4)

**Experiment Configuration:**
- Number of Replicates (1-5)
- Number of Blocks (for experimental runs on different days)
- Center Points (for response surface designs)

#### 3. **Interactive 3D Visualizations**

**Tab 1: 3D Molar Ratio Space**
- X-axis: Ionizable Lipid %
- Y-axis: Cholesterol %
- Z-axis: PEG-Lipid %
- Color: Helper Lipid %
- Interactive rotation, zoom, and hover information

**Tab 2: 3D Process Parameter Space**
- X-axis: Total Flow Rate (mL/min)
- Y-axis: Flow Rate Ratio
- Z-axis: Ionizable Lipid %
- Color: Cholesterol %
- Visualizes process parameter interactions

**Tab 3: 2D Molar Ratio View**
- Ionizable % vs PEG % (color = Cholesterol %)
- Quick reference for formulation space

**Tab 4: 2D Process Parameter View**
- TFR vs FRR (color = Ionizable %)
- Quick reference for process conditions

**3D Volume Distribution:**
- X-axis: Ionizable Lipid Volume (µL)
- Y-axis: Helper Lipid Volume (µL)
- Z-axis: PEG-Lipid Volume (µL)
- Color: Total Flow Rate
- Shows actual pipetting volume requirements

#### 4. **Response Surface Heatmaps**

**Heatmap 1: Total Volume vs Ionizable% and TFR**
- Shows how total volume changes across the design space
- Useful for understanding volume constraints

**Heatmap 2: Helper Volume vs Cholesterol% and FRR**
- Shows helper lipid volume variation
- Helps identify formulations with optimal component ratios

#### 5. **Volume Calculation Engine**

The system converts molar percentages to pipetting volumes using:

1. **Molar % → Moles**
   - Using weighted average molecular weight
   - Assumes total lipid concentration of 15 mg/mL

2. **Moles → Mass (mg)**
   - Each component mass = moles × molecular weight

3. **Mass → Volume (µL)**
   - Each component volume = mass / stock concentration

4. **Total Volume Composition**
   - Lipid organic phase + Ethanol + Aqueous buffer
   - Automatically calculated to reach target well volume

#### 6. **Run Sheet Generation**

Each experiment includes:
- Block number (for experimental organization)
- Run ID (unique identifier)
- Experiment number (design point)
- Replicate number
- Molar percentages (Ion%, Helper%, Chol%, PEG%)
- Process parameters (TFR, FRR)
- Pipetting volumes (µL) for each component
- Ethanol and buffer volumes
- Total volume
- Timestamp
- Notes field (for experimental observations)

#### 7. **Export Formats**

**CSV Export:**
- Universal format readable by all lab automation systems
- Direct import into LIMS
- Compatible with liquid handlers and plate readers

**Excel Export (Multiple Sheets):**
- **Run Sheet**: Complete experimental plan with volumes
- **Design Matrix**: Factor levels for each design point
- **Summary**: Metadata and experimental parameters

#### 8. **Statistics & Analysis**

**Coverage Reports:**
- Molar ratio ranges (min → max for each component)
- Process parameter ranges
- Volume ranges for each lipid component

**Design Efficiency:**
- Total number of experiments
- Replicate structure
- Block organization

#### 9. **Component Database**

Customizable lipid properties:
- Molecular Weight (MW) in g/mol
- Stock Concentration in mg/mL

Default values:
- Ionizable Lipid: MW 710.182, Stock 100 mg/mL
- Helper Lipid (DSPC): MW 790.147, Stock 12.5 mg/mL
- Cholesterol: MW 386.654, Stock 20 mg/mL
- PEG-Lipid (DMG-PEG2K): MW 2509.2, Stock 50 mg/mL

#### 10. **Advanced Features**

- **Design Type Information**: Descriptions and best use cases for each DOE method
- **Interactive Tabs**: Easy navigation between design selection, advanced options, and visualizations
- **Responsive UI**: Adapts to screen size for both desktop and tablet viewing
- **Real-time Calculations**: Volume calculations update instantly as parameters change
- **Hover Information**: Detailed tooltips on all 3D visualizations

---

## How to Use

1. **Configure Component Properties** (Sidebar)
   - Update molecular weights and stock concentrations if using different lipids
   - Set target N/P ratio

2. **Select DOE Design Type** (Design Selection Tab)
   - Choose appropriate design for your objectives
   - Adjust molar ratio ranges and process parameters
   - Set number of replicates and blocks

3. **Generate Design** (Click "Generate DOE Design")
   - System validates parameter ranges
   - Creates design matrix
   - Calculates pipetting volumes
   - Displays results

4. **Visualize Results**
   - Use 3D views to understand design space coverage
   - Check response surface heatmaps for interactions
   - Review 3D volume distribution

5. **Export Results**
   - Download CSV for lab information management system
   - Download Excel for detailed analysis and documentation
   - Use run sheet directly with lab automation

---

## Mathematical Foundations

### N/P Ratio Calculation
```
N/P Ratio = (moles of amine groups) / (moles of phosphate groups)
P ≈ DNA mass (µg) / 330 g/mol (for dsDNA)
N = sum of amine groups from ionizable lipids
```

### Molar Ratio Normalization
```
For 3 user-controlled factors (Ion%, Chol%, PEG%):
Helper% = 100% - Ion% - Chol% - PEG%

All factors must satisfy: Sum = 100%
```

### Volume Conversion
```
1. Average MW = Σ(component% × component_MW) / 100
2. Moles = (Target Lipid Mass) / (Average MW)
3. Component Moles = (Component%) × (Total Moles) / 100
4. Component Volume (µL) = (Component Mass / Stock Concentration) × 1000
```

---

## Best Practices

1. **Screening Phase**: Start with Plackett-Burman or Fractional Factorial
2. **Optimization Phase**: Use Box-Behnken or Central Composite
3. **Validation Phase**: Use 2-3 replicates for statistical significance
4. **Block Design**: Use multiple blocks if running experiments over different days
5. **Volume Constraints**: Check pipetting volume ranges are compatible with your equipment

---

## Supported Features

✅ 7 DOE design types  
✅ 3D interactive visualizations  
✅ Response surface analysis  
✅ Automatic volume calculation  
✅ CSV and Excel export  
✅ Customizable components  
✅ Replicate and block design  
✅ Real-time parameter validation  

---

## Technical Stack

- **Framework**: Streamlit 1.52.1
- **Visualization**: Plotly (2D and 3D charts)
- **Data Analysis**: Pandas, NumPy
- **Export**: OpenPyXL for Excel
- **Python Version**: 3.14

---

Generated: December 2025
Version: 2.0 (Professional DOE Suite)
