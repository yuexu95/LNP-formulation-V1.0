import streamlit as st
import pandas as pd

st.set_page_config(page_title="Methods", page_icon="🔬", layout="wide")

st.title("🔬 Standard Operating Protocol: Preparation and Characterization of pDNA-LNPs")

st.markdown("""
Plasmid DNA-Lipid Nanoparticles (pDNA-LNPs) represent a significant advancement in non-viral gene delivery. 
Unlike viral vectors, LNPs offer a synthetic and highly customizable platform with reduced immunogenicity 
and streamlined manufacturing. This protocol provides comprehensive guidance for formulation, surface 
functionalization, and characterization of pDNA-LNPs.
""")


# Section 1: Foundational Principles
st.header("1. Foundational Principles of pDNA-LNP Design")

st.markdown("""
A stable and effective formulation requires careful engineering of each component to overcome biological 
barriers and safety concerns.
""")

with st.expander("1.1 Core Components and Their Functions"):
    st.markdown("""
    | Component | Examples | Function | Key Properties |
    |-----------|----------|----------|----------------|
    | **Plasmid DNA (pDNA)** | MAGE-A3, MUC1, EGFP, tdTomato | Genetic cargo encoding therapeutic proteins, antigens, or reporters | Circular, double-stranded DNA |
    | **Cationic/Ionizable Lipids** | D-Lin-MC3-DMA, SM-102, ALC-0315, 5A2-SC8, HGT5000 | pDNA encapsulation via electrostatic interaction | Tertiary amine, pKa 6.0-7.0 |
    | **Helper Lipids** | DOPE, DSPC | Lipid bilayer stabilization, membrane fusion, endosomal escape | Phospholipids |
    | **Structural Lipids** | Cholesterol | Membrane fluidity, rigidity, and integrity | Modulates stability during circulation |
    | **PEGylated Lipids** | DMG-PEG2K | "Stealth" coating, reduces opsonization | Increases circulation time |
    """)

with st.expander("1.2 Key Design Challenges"):
    st.markdown("""
    **Challenge 1: Innate Immune Recognition**
    - pDNA-LNPs can induce acute inflammation via cGAS-STING pathway activation
    - Triggers massive cytokine release (IFN-β, IL-6) leading to systemic toxicity
    - **Solution**: Incorporate nitro-oleic acid (NOA) at 0.2–0.8 mole ratio to inhibit STING
    
    **Challenge 2: Nuclear Delivery Barrier**
    - pDNA must reach the nucleus for transcription (unlike mRNA which only needs cytoplasm)
    - Nuclear entry is a primary limitation for efficiency
    - **Solution**: Optimize formulation and use physical enhancement methods
    """)


# Section 2: Materials
st.header("2. Required Materials and Reagents")

st.markdown("""
High-quality, GMP-grade materials are essential for reproducible and safe formulations.
""")

col1, col2 = st.columns(2)

with st.expander("2.1 Lipid Components"):
    lipid_data = {
        "Lipid Category": ["Cationic/Ionizable", "Helper (Phospholipid)", "Structural", "PEGylated"],
        "Examples": ["C12-200, DODAP, HGT5000, 5A2-SC8", "DOPE, DSPC", "Cholesterol", "DMG-PEG2K"],
        "Molar Ratio (%)": ["5-50", "10-50", "15-60", "0.25-12.5"]
    }
    st.table(pd.DataFrame(lipid_data))

with st.expander("2.2 Solvents and Buffers"):
    st.markdown("""
    - **Ethanol**: ACS grade or higher, Absolute (200 proof)
    - **Citrate Buffer**: 10 mM, pH 4.0-4.5 (for pDNA dissolution)
    - **PBS**: 1x, pH 7.4 (for dialysis and neutralization)
    - **Water**: Nuclease-free, HPLC grade
    
    ⚠️ **Critical**: pH 4.0 ensures ionizable lipids are protonated (+) for pDNA binding.  
    pH 7.4 deprotonates lipids to neutral state, reducing toxicity.
    """)


# Section 3: Formulation Protocol
st.header("3. Step-by-Step LNP Formulation Protocol")
with st.expander("3.1 Preparation of pDNA-LNPs via Rapid Mixing"):
    st.markdown("""
    Formation of pDNA-LNPs is a controlled self-assembly process driven by rapid mixing of lipid-ethanol 
    and pDNA-aqueous phases.
    """)
with st.expander("Step 1: Preparation of the Lipid Phase (Organic Phase)"):
    st.markdown("""
    1. Weigh individual lipid components (ionizable lipid, helper lipid, cholesterol, PEG-lipid)
    2. Dissolve completely in **absolute ethanol**
    3. Combine according to predetermined molar ratios (e.g., 40:20:35:5 for HGT5000:DOPE:cholesterol:DMG-PEG2K)
    4. Ensure complete dissolution and homogeneity
    """)

with st.expander("Step 2: Preparation of the Aqueous Phase"):
    st.markdown("""
    1. Dissolve high-purity plasmid DNA in **Citrate Buffer (10 mM, pH 4.0-4.5)**
    2. Gently mix until fully dissolved (target concentration: e.g., 1 mg/mL)
    3. ⚠️ **Avoid vigorous vortexing** - can fragment large plasmid DNA molecules
""")

with st.expander("Step 3: Nanoparticle Assembly via Rapid Mixing"):

    tab1, tab2 = st.tabs(["Method A: Manual Rapid Injection", "Method B: Microfluidic Mixing"])

    with tab1:
        st.markdown("""
        **Procedure:**
        1. Draw lipid-ethanol solution into syringe
        2. **Rapidly inject** into stirring aqueous pDNA solution
        3. Immediately shake or pipette vigorously for homogenous formation
        4. Incubate for **10 minutes** at room temperature for stabilization
        
        **Advantages:** Simple, low equipment cost  
        **Disadvantages:** Less control, higher batch-to-batch variability
        """)

    with tab2:
        st.markdown("""
        **Procedure:**
        1. Load phases into separate syringes on syringe pumps
        2. Set **Flow Rate Ratio (FRR)**: typically 3:1 (aqueous:ethanol)
        3. Set **Total Flow Rate (TFR)**: e.g., 12 mL/min
        4. Infuse through microfluidic chip for controlled mixing
        5. Discard first/last drops, collect main product
        
        **Advantages:** Superior control, narrow size distribution, high reproducibility  
        **Disadvantages:** Requires specialized equipment  
        **Recommended for:** Therapeutic development and regulatory applications
        """)

with st.expander("Step 4: Downstream Processing and Purification"):
    st.markdown("""
    1. **Dialysis**: Transfer to dialysis cassette (20-100 kDa MWCO)
    - Dialyze against **1x PBS (pH 7.4)** for ≥2 hours
    - Change buffer 1-2 times
    - Purpose: Remove ethanol + neutralize pH
    
    2. **Sterilization**: Filter through **0.22 µm sterile filter**
    - Mandatory for in vitro/in vivo applications
    
    3. **Concentration** (if needed): Use centrifugal filtration
    - Reach desired target concentration for dosing
    """)

# Section 4: Surface Modification
with st.expander("4. Post-Formulation Surface Modification for Targeted Delivery"):

    st.markdown("""
    Surface modification with targeting ligands enhances therapeutic potential by improving tissue specificity 
    and reducing off-target effects.
    """)

    with st.expander("4.1 Ligand Preparation and Conjugation"):
        st.markdown("""
        **Example: Dual-Targeted LNP for HER2+ Breast Cancer**
        1. Prepare LNPs with folate-conjugated PEGylated lipids
        2. Modify Herceptin (trastuzumab) antibody to introduce thiol groups (thiolation)
        3. Conjugate thiolated antibody to maleimide groups on PEG-lipid surface
        4. Result: Dual targeting via folate receptor and HER2 receptor
        """)

    with st.expander("4.2 Linkage Strategies"):
        linkage_data = {
            "Linkage Strategy": [
                "Avidin-Biotin Bridging",
            "Electrostatic Bonds",
            "Covalent - Disulfide Bonds",
            "Covalent - Maleimide-Thiol",
            "Covalent - DBCO-Azide (SPAAC)"
        ],
        "Key Characteristics": [
            "Very strong non-covalent interaction; time-consuming synthesis",
            "Suitable for charged NPs with oppositely charged ligands",
            "Stable in circulation, reversible in reducing intracellular environment",
            "Rapid, efficient, biocompatible; stable covalent bond",
            "Biorthogonal 'click chemistry'; rapid, non-toxic, highly stable"
        ]
        }
        st.table(pd.DataFrame(linkage_data))



# Section 5: Quality Control
with st.expander("5. Quality Control and Characterization"):

    st.markdown("""
    Robust QC ensures pDNA-LNPs meet quality specifications for intended applications and regulatory compliance.
    """)
    qc_data = {
        "Parameter": [
            "Size & Polydispersity Index (PDI)",
            "Surface Charge",
            "pDNA Encapsulation Efficiency",
            "Surface Ionization (pKa)",
            "Morphology"
        ],
        "Technique": [
            "Dynamic Light Scattering (DLS)",
            "Zeta Potential Measurement",
            "Quant-iT RiboGreen Assay",
            "TNS Assay",
            "Transmission Electron Microscopy (TEM)"
        ],
        "Description": [
            "Measures average hydrodynamic diameter and size distribution uniformity (PDI <0.2 = monodisperse)",
            "Determines electrical charge on surface; influences stability and cell membrane interaction",
            "Measures intact LNPs (free pDNA) vs. lysed LNPs (total pDNA) using Triton X-100",
            "Uses TNS probe to measure pKa of ionizable lipid; predicts endosomal escape ability",
            "Direct visualization to confirm size, spherical shape, and structural integrity"
        ]
    }
    st.table(pd.DataFrame(qc_data))


# Section 6: Safety and Application
with st.expander("6. Strategic Considerations for Application and Safety"):
    st.markdown("""
    **Problem**: pDNA-LNPs induce severe inflammation via cGAS-STING pathway activation
    **Solution**: Incorporate **Nitro-Oleic Acid (NOA)** - an endogenous STING-inhibiting lipid

    - **Optimal NOA:Total Lipid Ratio**: 0.2–0.8 mole ratio
    - **Effect**: Suppresses cytokine storm (IFN-β, IL-6)
    - **Result**: Prevents mortality in mice at high doses (1 mg/kg), transforming lethal formulations into viable ones

    ⚠️ **Critical Safety Component** for clinical translation
    """)

    with st.expander("6.2 Physical Methods for Enhanced Cellular Delivery"):
        method_col1, method_col2 = st.columns(2)

    with method_col1:
        st.markdown("""
            **Sonoporation**
            - Uses therapeutic ultrasound (1 MHz, 2 W·cm⁻²)
            - Stimulates co-administered microbubbles
            - Cavitation creates transient membrane pores
            - Direct physical route for LNP entry
            - **Application**: In vivo tissue-targeted delivery
            """)
    with method_col2:
        st.markdown("""
            **Electroporation**
            - Applies short, intense electric pulses
            - Transiently permeabilizes cell membrane
            - High-efficiency LNP uptake
            - **Application**: Ex vivo cell modification for cell-based therapies
            """)

    with st.expander("6.3 Storage and Handling"):
        st.markdown("""
        📦 **Storage**: 2-8°C (refrigerated)  
        ⏱️ **Stability**: Prevents degradation of lipids and pDNA payload  
        🧊 **Long-term**: Consider lyophilization for extended shelf life
        """)


# Section 7: Conclusion
with st.expander("7. Conclusion"):
    st.markdown("""
    Successful pDNA-LNP preparation requires:

    1. ✅ **Principled design** of core components
    2. ✅ **Controlled formulation** for desired physicochemical properties
    3. ✅ **Optional surface functionalization** for targeted delivery
    4. ✅ **Rigorous characterization** for quality and consistency
    5. ✅ **Integration of safety components** (e.g., NOA) to overcome inflammatory toxicity

    By addressing these formulation and safety challenges, pDNA-LNPs represent a **highly promising and 
    versatile platform** poised to deliver the next generation of advanced genetic medicines.
    """)


# --- 右侧/下侧：交互式计算器 ---
st.header("🧮 LNP Formulation Calculator")
st.info("Input your parameters below to generate the pipetting recipe. SM-102/DSPC/Chol/DMG-PEG2K default ratios used.")

# 1. 创建输入列
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Target Specs")
    pdna_mass_ug = st.number_input("Total pDNA required (μg)", value=100.0, step=10.0)
    np_ratio = st.number_input("N/P Ratio (Nitrogen/Phosphate)", value=6.0, step=0.5)
    frr = st.selectbox("Flow Rate Ratio (Aq:Eth)", options=[3, 1], index=0)

with col2:
    st.subheader("2. Molecular Weights (g/mol)")
    mw_ionizable = st.number_input("MW Ionizable Lipid", value=710.17)
    mw_chol = st.number_input("MW Cholesterol", value=386.65)
    mw_helper = st.number_input("MW Helper (DSPC)", value=790.15)
    mw_peg = st.number_input("MW PEG-Lipid", value=2507.64)
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