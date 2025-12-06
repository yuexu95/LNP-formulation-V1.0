import streamlit as st
import pandas as pd

st.set_page_config(page_title="Methods", page_icon="🔬", layout="wide")

st.title("🔬 Methods for pDNA-LNP Formulation")

# --- 左侧：标准操作流程 (SOP) ---
st.header("📝 Standard Operating Procedure (SOP)")

st.markdown("""
### Step 1: Prepare the Stock Solutions of Lipids 🧪
* **Ionizable lipid:** Weigh the mass (mg) and dissolve in Ethanol to reach target concentration (e.g., 10 mg/mL).
* **Cholesterol:** Weigh and dissolve in Ethanol (e.g., 10 mg/mL).
* **Helper Lipid (DSPC/DOPE):** Weigh and dissolve in Ethanol (e.g., 5 or 10 mg/mL). *Note: DSPC may require heating to 40-50°C to dissolve.*
* **PEG-lipid:** Weigh and dissolve in Ethanol (e.g., 5 or 10 mg/mL).

### Step 2: Prepare the Aqueous Phase (Phase A) 💧
* Dilute the **pDNA** in Citrate Buffer (10 mM, pH 4.0) to the target concentration.
* *Calculation Tip:* Ensure the final volume of the aqueous phase matches your planned Flow Rate Ratio (usually 3:1 Aqueous:Ethanol).

### Step 3: Prepare the Organic Phase (Phase B) 🥃
* Combine the four lipid stock solutions into a single tube based on the calculated molar ratios.
* Add pure Ethanol to reach the final target volume for the organic phase.
* **Critical:** Ensure the lipid mix is clear and homogenous before mixing.

### Step 4: Microfluidic Mixing / Formulation ⚡
* **Setup:** Load Phase A (pDNA) and Phase B (Lipids) into the microfluidic device (e.g., NanoAssemblr or custom T-junction).
* **Parameters:** Set the **Flow Rate Ratio (FRR)** (typically 3:1 Aqueous:Organic) and **Total Flow Rate (TFR)** (e.g., 12 mL/min).
* **Collection:** Discard the first and last few drops (waste) to ensure steady-state mixing, then collect the LNP solution.

### Step 5: Downstream Processing (Buffer Exchange) 🔄
* **Dialysis:** Transfer the LNP solution into a dialysis cassette (e.g., 20k-100k MWCO).
* **Buffer:** Dialyze against 1x PBS (pH 7.4) for at least 6-12 hours (change buffer once) to remove ethanol and neutralize pH.
* *Alternative:* Use Tangential Flow Filtration (TFF) for larger scales.

### Step 6: Filtration & QC 🔍
* **Sterilization:** Filter the final LNP through a 0.22 μm PES syringe filter.
* **Characterization:**
    * **Size & PDI:** Dynamic Light Scattering (DLS).
    * **Encapsulation Efficiency (EE%):** RiboGreen assay (with and without Triton X-100).
    * **pDNA Integrity:** Gel electrophoresis.
""")

st.markdown("---")

# --- 右侧/下侧：交互式计算器 ---
st.header("🧮 LNP Formulation Calculator")
st.info("Input your parameters below to generate the pipetting recipe.")

# 1. 创建输入列
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Target Specs")
    pdna_mass_ug = st.number_input("Total pDNA required (μg)", value=100.0, step=10.0)
    np_ratio = st.number_input("N/P Ratio (Nitrogen/Phosphate)", value=6.0, step=0.5)
    frr = st.selectbox("Flow Rate Ratio (Aq:Eth)", options=[3, 1], index=0)

with col2:
    st.subheader("2. Molecular Weights (g/mol)")
    mw_ionizable = st.number_input("MW Ionizable Lipid", value=1000.0)
    mw_chol = st.number_input("MW Cholesterol", value=386.65)
    mw_helper = st.number_input("MW Helper (DSPC)", value=790.15)
    mw_peg = st.number_input("MW PEG-Lipid", value=2500.0)
    avg_mw_nucleotide = 330.0 # Average MW per nucleotide for DNA

with col3:
    st.subheader("3. Molar Ratios (%)")
    mol_ionizable = st.number_input("Ionizable Lipid %", value=50.0)
    mol_chol = st.number_input("Cholesterol %", value=38.5)
    mol_helper = st.number_input("Helper Lipid %", value=10.0)
    mol_peg = st.number_input("PEG-Lipid %", value=1.5)
    
    total_mol = mol_ionizable + mol_chol + mol_helper + mol_peg
    if total_mol != 100:
        st.error(f"Total Molar % is {total_mol}%. It should be 100%!")

# 4. 库存浓度输入
st.subheader("4. Stock Concentrations (mg/mL)")
sc_cols = st.columns(4)
c_ion = sc_cols[0].number_input("Conc. Ionizable", value=10.0)
c_chol = sc_cols[1].number_input("Conc. Cholesterol", value=10.0)
c_help = sc_cols[2].number_input("Conc. Helper", value=10.0)
c_peg = sc_cols[3].number_input("Conc. PEG", value=5.0)

# --- 计算逻辑 ---
if st.button("Calculate Recipe 🚀"):
    if total_mol != 100:
        st.error("Please fix molar ratios to sum to 100% first.")
    else:
        # Step A: Calculate Moles of Phosphate in DNA
        # 1 ug DNA = 3030 pmol phosphate (approx, assuming avg MW nucleotide ~330)
        # More precise: Mass (g) / avg_MW_nucleotide (330) = Moles of nucleotides (Phosphate)
        moles_phosphate = (pdna_mass_ug * 1e-6) / avg_mw_nucleotide
        
        # Step B: Calculate Moles of Ionizable Lipid needed (based on N/P)
        # Assuming 1 Nitrogen per ionizable lipid molecule for simplicity (Adjust if multi-amine)
        moles_ionizable = moles_phosphate * np_ratio
        
        # Step C: Calculate Total Moles of all lipids
        # moles_ionizable represents X% of total. 
        # Total Moles = moles_ionizable / (mol_ionizable / 100)
        total_moles_lipid = moles_ionizable / (mol_ionizable / 100)
        
        # Step D: Calculate Mass required for each lipid
        mass_ion_mg = (total_moles_lipid * (mol_ionizable/100) * mw_ionizable) * 1000
        mass_chol_mg = (total_moles_lipid * (mol_chol/100) * mw_chol) * 1000
        mass_helper_mg = (total_moles_lipid * (mol_helper/100) * mw_helper) * 1000
        mass_peg_mg = (total_moles_lipid * (mol_peg/100) * mw_peg) * 1000
        
        # Step E: Calculate Volumes from Stocks
        vol_ion_ul = (mass_ion_mg / c_ion) * 1000
        vol_chol_ul = (mass_chol_mg / c_chol) * 1000
        vol_helper_ul = (mass_helper_mg / c_help) * 1000
        vol_peg_ul = (mass_peg_mg / c_peg) * 1000
        
        total_lipid_vol_ul = vol_ion_ul + vol_chol_ul + vol_helper_ul + vol_peg_ul
        
        # Step F: Phases Volumes
        # Aqueous Phase Volume depends on final DNA concentration desired, but strictly speaking
        # in microfluidics, we usually fix the ratio.
        # Let's assume we want to use ALL the lipid volume generated above as the "Organic Phase"
        # BUT usually we add extra Ethanol to reach the correct FRR.
        
        # Calculation strategy: 
        # 1. Total Organic Phase Vol needed?
        # Usually we define DNA conc first. Let's simplify:
        # We present the "Lipid Mix Recipe" first.
        
        st.success("Calculation Successful!")
        
        # Display Recipe DataFrame
        recipe_data = {
            "Component": ["Ionizable Lipid", "Cholesterol", "Helper Lipid", "PEG Lipid"],
            "Mass Required (mg)": [f"{mass_ion_mg:.4f}", f"{mass_chol_mg:.4f}", f"{mass_helper_mg:.4f}", f"{mass_peg_mg:.4f}"],
            "Stock Conc (mg/mL)": [c_ion, c_chol, c_help, c_peg],
            "Volume to Add (μL)": [f"**{vol_ion_ul:.2f}**", f"**{vol_chol_ul:.2f}**", f"**{vol_helper_ul:.2f}**", f"**{vol_peg_ul:.2f}**"]
        }
        st.table(pd.DataFrame(recipe_data))
        
        st.markdown("### 🧪 Preparation Summary")
        st.write(f"1. **Lipid Mix (Organic Phase):** Mix the volumes above. Total Lipid Volume = **{total_lipid_vol_ul:.2f} μL**.")
        
        # Calculate Solvent needed
        # If FRR is 3:1. Let's say we simply top up ethanol to a convenient number or use as is.
        # Let's calculate the Aqueous volume needed based on the FRR.
        aq_vol_ul = total_lipid_vol_ul * frr
        final_total_vol_ul = aq_vol_ul + total_lipid_vol_ul
        
        st.write(f"2. **Add Pure Ethanol (Optional):** If you need a larger dead volume, add ethanol. Current Volume: {total_lipid_vol_ul:.2f} μL.")
        st.write(f"3. **Aqueous Phase (DNA):** Dilute **{pdna_mass_ug} μg** of pDNA into Citrate buffer to a total volume of **{aq_vol_ul:.2f} μL**.")
        st.write(f"4. **Run Microfluidics:** Flow Rate Ratio = {frr}:1.")