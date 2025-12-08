# LNP Formulation Platform

A comprehensive web-based platform for designing and calculating Lipid Nanoparticle (LNP) formulations, built with Streamlit.

## 🌟 Features

### 1. **pDNA Formulation Calculator** (Page 2)
Calculate precise volumes for pDNA-LNP formulations with:
- Customizable DNA scale and stock concentration
- Ionizable lipid-to-DNA ratio optimization
- Aqueous-to-ethanol ratio control
- Automatic N/P ratio calculation
- Formulation history tracking
- Bulk preparation support (with scaling factors)
- CSV export functionality

**Key Parameters:**
- DNA mass and concentration
- Lipid components: Ionizable, Helper (DSPC), Cholesterol, PEG-DMG
- Molecular weights and stock concentrations
- Molar ratios for each lipid component

### 2. **High-Throughput DOE Designer** (Page 6)
Professional Design of Experiments (DOE) tool for multi-component LNP optimization:

**Supported DOE Methods:**
- Full Factorial (2-Level & 3-Level)
- Fractional Factorial
- Plackett-Burman Screening
- Box-Behnken Response Surface
- Central Composite Design
- Mixture Design

**Features:**
- Interactive molar ratio range selection
- N/P ratio targeting and calculation
- Automated volume calculations for all components
- 3D design space visualization
- Response surface heatmaps
- Lab-ready run sheets with:
  - Replicate and block management
  - All component volumes (Ionizable, Helper, Cholesterol, PEG, Ethanol, DNA, Buffer)
  - N/P ratio tracking
  - Timestamps for record keeping
- Export to CSV and Excel formats

**Formulation Rules:**
- Total lipid-to-DNA mass ratio: 15:1
- Aqueous-to-organic phase ratio: 3:1
- DNA concentration: 0.56 μg/μL (default, adjustable)
- N/P ratio determined by ionizable lipid-to-DNA ratio

### 3. **Additional Pages**
- **Page 1:** General Information
- **Page 3:** mRNA Formulation
- **Page 4:** References
- **Page 5:** Methods

## 🚀 Getting Started

### Prerequisites
- Python 3.12 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yuexu95/LNP-formulation-V1.0.git
cd LNP-formulation-V1.0
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv312_new
source venv312_new/bin/activate  # On macOS/Linux
# or
venv312_new\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run 👋Homepage.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 Default Parameters

### Stock Concentrations (μg/μL = mg/mL)
- **Ionizable Lipid (SW102):** 100 μg/μL
- **Helper Lipid (DSPC):** 12.5 μg/μL
- **Cholesterol:** 20 μg/μL
- **PEG-Lipid (PEG2000-DMG):** 50 μg/μL

### Molecular Weights (g/mol)
- **Ionizable Lipid:** 710.182 g/mol
- **Helper Lipid:** 790.147 g/mol
- **Cholesterol:** 386.654 g/mol
- **PEG-Lipid:** 2509.2 g/mol

### Standard Molar Ratios
- **Ionizable:** 50%
- **Helper:** 10%
- **Cholesterol:** 38.5%
- **PEG:** 1.5%

## 📖 Usage Examples

### Example 1: pDNA Formulation (100 μg DNA)
```
Input:
- DNA Scale: 100 μg
- DNA Stock: 0.56 μg/μL
- Ionizable/DNA Ratio: 10
- Aqueous/Ethanol Ratio: 3

Output:
- Ionizable Lipid: 8.6 μL
- Helper Lipid: 15.3 μL
- Cholesterol: 18.0 μL
- PEG-DMG: 1.8 μL
- Ethanol: 16.2 μL
- DNA: 178.5 μL
- Buffer: 1.5 μL
- Total: 240 μL
- N/P Ratio: ~4.0
```

### Example 2: DOE Design
```
Design: Full Factorial (2-Level)
Variables: 
- Ionizable: 45-55%
- Cholesterol: 33.5-43.5%
- PEG: 0.5-2.5%
- N/P Ratio: 3-9

Result: 16 design points × replicates
- Comprehensive run sheet with volumes
- 3D visualization of design space
- Excel export for lab use
```

## 🔬 Scientific Background

### N/P Ratio Calculation
The N/P ratio represents the molar ratio of positively charged amine groups (N) from ionizable lipids to negatively charged phosphate groups (P) from DNA:

```
P (μmol) = DNA mass (μg) / 330
N (μmol) = Ionizable lipid moles × amines per molecule
N/P Ratio = N / P
```

For double-stranded DNA:
- Average MW per base pair ≈ 660 g/mol
- Each base pair contributes 2 phosphate groups
- Therefore: P = DNA mass / 330

### Phase Ratio
- **Organic Phase:** Lipids + Ethanol
- **Aqueous Phase:** DNA + Buffer
- **Ratio:** Aqueous:Organic = 3:1

This ratio ensures proper mixing and encapsulation efficiency.

## 📁 Project Structure

```
LNP-formulation/
├── 👋Homepage.py              # Main entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── pages/
│   ├── 1_🔬_General_info.py
│   ├── 2_🧬_pDNA_formulation.py
│   ├── 3_〰️_mRNA_formulation.py
│   ├── 4_📚_References.py
│   ├── 5_🧐_Methods.py
│   └── 6_🀄️_High-Throughput_Formulation.py
├── Data/                      # Data files
└── venv312_new/              # Virtual environment
```

## 🛠️ Technology Stack

- **Framework:** Streamlit 1.51.0
- **Data Processing:** pandas 2.3.3, numpy 2.3.5
- **Visualization:** plotly 6.5.0
- **File Export:** openpyxl 3.1.5
- **Python:** 3.12+

## 📝 Recent Updates

### Version 1.2 (December 2025)
- ✅ Implemented accurate 3:1 aqueous-to-organic phase ratio
- ✅ Added DNA parameter controls in DOE Designer
- ✅ Updated lipid-to-DNA mass ratio to 15:1 (based on experimental data)
- ✅ Added DNA volume column to run sheets
- ✅ Improved N/P ratio calculations
- ✅ Enhanced visualization with 3D scatter plots and heatmaps
- ✅ Fixed volume calculation algorithms for precision
- ✅ Added comprehensive formulation history tracking

## 🤝 Contributing

We welcome contributions! This project is under active development. Feel free to:

- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation
- Share your formulation protocols

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions, suggestions, or collaboration:
- **GitHub:** [yuexu95](https://github.com/yuexu95)
- **Repository:** [LNP-formulation-V1.0](https://github.com/yuexu95/LNP-formulation-V1.0)

## 📄 License

This project is open-source. Please cite appropriately if used in research or publications.

## 🙏 Acknowledgments

Special thanks to all contributors and users who help improve this platform with their feedback and suggestions.

---

**Note:** This platform is designed for research purposes. Please validate all calculations with your specific experimental protocols before use in critical applications.