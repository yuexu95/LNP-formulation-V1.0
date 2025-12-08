import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import itertools
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="LNP-Flow: Professional DOE Designer", page_icon="🀄", layout="wide")

st.title("🀄 LNP-Flow: Professional DOE Designer")
st.markdown("""
Design, optimize, and generate lab-ready run sheets for multi-component LNP formulations using 
professional Design of Experiments (DOE) principles.
""")

st.markdown("---")

# ============================================================================
# SECTION 1: COMPONENT CONFIGURATION
# ============================================================================

st.header("🧪 Component Database Configuration")
st.subheader("Preset as Moderna SM-102 formulation")

with st.expander("📦 Lipid Components Configuration", expanded=True):
    st.subheader("Lipid Component Properties")
    
    lipid_col1, lipid_col2 = st.columns(2)
    
    with lipid_col1:
        st.markdown("#### Ionizable Lipid")
        mw_ionizable = st.number_input(
            "Ionizable Lipid MW (g/mol)",
            value=710.182,
            step=10.0,
            key="mw_ion"
        )
        conc_ionizable = st.number_input(
            "Ionizable Lipid Stock (mg/mL)",
            value=100.0,
            step=10.0,
            key="conc_ion",
            help="Stock concentration in mg/mL"
        )
        
        st.markdown("#### Helper Lipid")
        mw_helper = st.number_input(
            "Helper Lipid MW (g/mol)",
            value=790.147,
            step=10.0,
            key="mw_helper"
        )
        conc_helper = st.number_input(
            "Helper Lipid Stock (mg/mL)",
            value=12.5,
            step=1.0,
            key="conc_helper",
            help="Stock concentration in mg/mL"
        )
    
    with lipid_col2:
        st.markdown("#### Cholesterol")
        mw_chol = st.number_input(
            "Cholesterol MW (g/mol)",
            value=386.654,
            step=5.0,
            key="mw_chol"
        )
        conc_chol = st.number_input(
            "Cholesterol Stock (mg/mL)",
            value=20.0,
            step=1.0,
            key="conc_chol",
            help="Stock concentration in mg/mL"
        )
        
        st.markdown("#### PEG-Lipid")
        mw_peg = st.number_input(
            "PEG-Lipid MW (g/mol)",
            value=2509.2,
            step=50.0,
            key="mw_peg"
        )
        conc_peg = st.number_input(
            "PEG-Lipid Stock (mg/mL)",
            value=50.0,
            step=5.0,
            key="conc_peg",
            help="Stock concentration in mg/mL"
        )
    
    st.markdown("---")
    
    st.subheader("DNA Parameters (for N/P Ratio Calculation)")
    dna_col1, dna_col2 = st.columns(2)
    
    with dna_col1:
        dna_mass_ug = st.number_input(
            "DNA Mass (μg)",
            value=1.0,
            step=0.1,
            key="dna_mass_ug",
            help="Amount of DNA in formulation"
        )
    
    with dna_col2:
        dna_concentration = st.number_input(
            "DNA Concentration (mg/mL)",
            value=0.56,
            step=0.01,
            key="dna_conc",
            help="Stock concentration of DNA solution (= μg/μL)"
        )

st.markdown("---")

# ============================================================================
# SECTION 2: DOE DESIGN SELECTION
# ============================================================================

st.header("⚙️ DOE Configuration")

with st.container():
    col_design, col_params = st.columns([1, 1])
    
    with col_design:
        st.subheader("Design Type")
        design_type = st.radio(
            "Select DOE Method:",
            options=[
                "Full Factorial (2-Level)",
                "Full Factorial (3-Level)",
                "Fractional Factorial",
                "Plackett-Burman",
                "Box-Behnken",
                "Central Composite",
                "Mixture Design"
            ],
            help="Choose DOE strategy based on your objectives"
        )
    
    with col_params:
        st.subheader("Experiment Parameters")
        num_replicates = st.number_input(
            "Number of Replicates",
            value=1,
            min_value=1,
            max_value=5
        )
        num_blocks = st.number_input(
            "Number of Blocks",
            value=1,
            min_value=1,
            max_value=4,
            help="Divide experiments into blocks for different runs/days"
        )

    st.markdown("---")

    # Variable Ranges
    st.subheader("📊 Variable Ranges")
    st.caption("Helper Lipid % is auto-calculated to reach 100%")

    ratio_cols = st.columns(4)
    
    with ratio_cols[0]:
        st.markdown("**Ionizable Lipid**")
        ion_min = st.number_input("Min %", value=45.0, step=1.0, key="ion_min")
        ion_max = st.number_input("Max %", value=55.0, step=1.0, key="ion_max")

    with ratio_cols[1]:
        st.markdown("**Cholesterol**")
        chol_min = st.number_input("Min %", value=33.5, step=1.0, key="chol_min")
        chol_max = st.number_input("Max %", value=43.5, step=1.0, key="chol_max")

    with ratio_cols[2]:
        st.markdown("**PEG-Lipid**")
        peg_min = st.number_input("Min %", value=0.5, step=0.1, key="peg_min")
        peg_max = st.number_input("Max %", value=2.5, step=0.1, key="peg_max")

    with ratio_cols[3]:
        st.markdown("**N/P Ratio**")
        np_min = st.number_input("Min", value=3.0, step=0.5, key="np_min")
        np_max = st.number_input("Max", value=9.0, step=0.5, key="np_max")

    st.markdown("---")
    
    st.subheader("📊 Response Variable")
    response_type = st.selectbox(
        "Select Response Measure:",
        options=[
            "Bioluminescence Intensity",
            "Fluorescence Intensity"
        ],
        help="Choose the measurement type for experimental responses"
    )
    
    st.markdown("---")
    
    st.markdown("**📋 Design Information**")
    
    design_info = {
        "Full Factorial (2-Level)": "Tests all combinations of high/low levels (2^n runs). Best for initial exploration.",
        "Full Factorial (3-Level)": "Tests 3 levels per factor (3^n runs). More detailed mapping of design space.",
        "Fractional Factorial": "Reduced subset of full factorial. More efficient for many factors.",
        "Plackett-Burman": "Screening design for many factors in few runs. Typically 12-20 runs.",
        "Box-Behnken": "Response surface design with center and face points. Fewer runs than full factorial.",
        "Central Composite": "Full factorial + axial + center points. Best for comprehensive response surface.",
        "Mixture Design": "Optimized for proportional components. Perfect for LNP ratios."
    }
    
    st.info(design_info.get(design_type, ""))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_molar_ratios(ionizable_pct, cholesterol_pct, peg_pct):
    """Normalize three components so that Ionizable + Cholesterol + PEG + Helper = 100%."""
    helper_pct = 100.0 - ionizable_pct - cholesterol_pct - peg_pct
    if helper_pct < 0:
        return None
    return ionizable_pct, helper_pct, cholesterol_pct, peg_pct


def generate_2level_factorial(ranges_dict):
    """Generate 2-level full factorial design."""
    design_points = list(itertools.product([-1, 1], repeat=len(ranges_dict)))
    factor_names = list(ranges_dict.keys())
    scaled_points = []
    
    for point in design_points:
        scaled_point = {}
        for i, factor in enumerate(factor_names):
            min_val, max_val = ranges_dict[factor]
            scaled_point[factor] = min_val + (point[i] + 1) / 2 * (max_val - min_val)
        scaled_points.append(scaled_point)
    
    return pd.DataFrame(scaled_points)


def generate_3level_factorial(ranges_dict):
    """Generate 3-level full factorial design."""
    factor_names = list(ranges_dict.keys())
    levels = {}
    
    for factor, (min_val, max_val) in ranges_dict.items():
        levels[factor] = [min_val, (min_val + max_val) / 2, max_val]
    
    all_combos = itertools.product(*[levels[f] for f in factor_names])
    design_data = [{factor_names[i]: val for i, val in enumerate(combo)} for combo in all_combos]
    
    return pd.DataFrame(design_data)


def generate_fractional_factorial(ranges_dict):
    """Generate fractional factorial (subset of 2^5)."""
    full_design = generate_2level_factorial(ranges_dict)
    fraction = min(16, len(full_design))
    return full_design.sample(n=fraction, random_state=42).reset_index(drop=True)


def generate_plackett_burman(ranges_dict):
    """Generate Plackett-Burman screening design."""
    n_factors = len(ranges_dict)
    factor_names = list(ranges_dict.keys())
    
    # Standard PB matrix for 12 runs, 11 factors (can handle 5 factors)
    pb_matrix = np.array([
        [1, 1, 1, 1, 1],
        [1, -1, 1, 1, -1],
        [1, 1, -1, 1, 1],
        [1, 1, 1, -1, -1],
        [-1, 1, 1, 1, -1],
        [-1, -1, 1, 1, 1],
        [-1, -1, -1, 1, 1],
        [-1, -1, -1, -1, -1],
        [-1, 1, -1, -1, 1],
        [-1, 1, 1, -1, 1],
        [1, -1, -1, -1, 1],
        [1, 1, -1, 1, 1],
    ])
    
    design_points = []
    for point in pb_matrix:
        scaled_point = {}
        for i, factor in enumerate(factor_names):
            min_val, max_val = ranges_dict[factor]
            scaled_point[factor] = min_val + (point[i] + 1) / 2 * (max_val - min_val)
        design_points.append(scaled_point)
    
    return pd.DataFrame(design_points)


def generate_box_behnken(ranges_dict):
    """Generate Box-Behnken design."""
    factor_names = list(ranges_dict.keys())
    center = [np.mean(ranges_dict[f]) for f in factor_names]
    design_points = [center.copy()]
    
    # Axial points
    for i, factor in enumerate(factor_names):
        for val in [ranges_dict[factor][0], ranges_dict[factor][1]]:
            point = center.copy()
            point[i] = val
            design_points.append(point)
    
    design_data = [{factor_names[i]: val for i, val in enumerate(point)} for point in design_points]
    return pd.DataFrame(design_data)


def generate_central_composite(ranges_dict):
    """Generate Central Composite Design."""
    factor_names = list(ranges_dict.keys())
    n_factors = len(factor_names)
    
    # Factorial part
    factorial_df = generate_2level_factorial(ranges_dict)
    design_points = [dict(row) for _, row in factorial_df.iterrows()]
    
    center = [np.mean(ranges_dict[f]) for f in factor_names]
    
    # Axial points
    alpha = np.sqrt(n_factors)
    for i, factor in enumerate(factor_names):
        for sign in [-1, 1]:
            point = center.copy()
            min_val, max_val = ranges_dict[factor]
            range_val = (max_val - min_val) / 2
            point[i] = center[i] + sign * alpha * range_val / 2
            design_points.append({factor_names[j]: point[j] for j in range(len(factor_names))})
    
    # Center point
    design_points.append({factor_names[i]: center[i] for i in range(len(factor_names))})
    
    return pd.DataFrame(design_points)


def generate_mixture_design(ranges_dict):
    """Generate Mixture Design (simplex lattice)."""
    factor_names = list(ranges_dict.keys())
    design_points = list(itertools.product([0, 0.5, 1], repeat=len(factor_names)))
    
    valid_points = []
    for point in design_points:
        total = sum(point)
        if total > 0:
            normalized = tuple(p / total for p in point)
            scaled = {}
            for i, factor in enumerate(factor_names):
                min_val, max_val = ranges_dict[factor]
                scaled[factor] = min_val + normalized[i] * (max_val - min_val)
            valid_points.append(scaled)
    
    return pd.DataFrame(valid_points)


def calculate_np_ratio(dna_mass_ug, ionizable_lipid_moles, amines_per_molecule=1.0):
    """Calculate N/P ratio using pDNA formulation methodology."""
    phosphate_moles_mol = dna_mass_ug * 1e-6 / 330.0
    phosphate_moles_umol = phosphate_moles_mol * 1e6
    amine_moles_umol = ionizable_lipid_moles * amines_per_molecule
    
    if phosphate_moles_umol > 0:
        np_ratio = amine_moles_umol / phosphate_moles_umol
    else:
        np_ratio = 0
    
    return np_ratio, amine_moles_umol, phosphate_moles_umol


def calculate_volumes(
    ionizable_pct, helper_pct, chol_pct, peg_pct,
    mw_ion, mw_helper, mw_chol, mw_peg,
    conc_ion, conc_helper, conc_chol, conc_peg,
    target_vol_ul,
    dna_mass_ug=None,
    dna_concentration=None
):
    """
    Convert molar percentages to pipetting volumes.
    
    Strategy: 
    1. Calculate target lipid mass based on DNA amount (total lipid:DNA = 15:1 mass ratio)
    2. Distribute this mass according to molar percentages
    3. Calculate volumes from masses using stock concentrations
    4. Calculate aqueous phase using 3:1 aqueous:organic ratio
    5. DNA volume from DNA mass and concentration
    
    Key formulation rules:
    - Total lipid mass = DNA mass × 15 (μg)
    - Aqueous phase (DNA + buffer) = Organic phase (lipids + ethanol) × 3
    - N/P ratio determined by ionizable lipid to DNA mass ratio
    
    Input units:
    - Percentages: molar %
    - MW: g/mol  
    - Concentrations: mg/mL (= μg/μL)
    - Target volume: μL
    - DNA mass: μg
    - DNA concentration: mg/mL (= μg/μL)
    """
    # Calculate target lipid mass based on DNA content
    # Standard formulation: 15 μg total lipids per 1 μg DNA
    if dna_mass_ug and dna_mass_ug > 0:
        target_lipid_mass_ug = dna_mass_ug * 15.0  # Total lipid mass in μg
        target_lipid_mass_mg = target_lipid_mass_ug / 1000.0  # Convert to mg for calculation
    else:
        target_lipid_mass_ug = 15.0  # Default: 15 μg total lipids (for 1 μg DNA)
        target_lipid_mass_mg = 0.015  # 0.015 mg
    
    # Calculate average molecular weight from molar percentages
    avg_mw = (ionizable_pct * mw_ion + helper_pct * mw_helper + 
              chol_pct * mw_chol + peg_pct * mw_peg) / 100.0
    
    # Total moles needed: mass / MW (mg / (g/mol) = mmol, converted to μmol for consistency)
    total_moles_mmol = target_lipid_mass_mg / avg_mw
    total_moles_umol = total_moles_mmol * 1000.0
    
    # Calculate moles for each component (in mmol)
    moles_ion_mmol = (ionizable_pct / 100.0) * total_moles_mmol
    moles_helper_mmol = (helper_pct / 100.0) * total_moles_mmol
    moles_chol_mmol = (chol_pct / 100.0) * total_moles_mmol
    moles_peg_mmol = (peg_pct / 100.0) * total_moles_mmol
    
    # Convert moles to mass: mmol × (g/mol) = mg
    mass_ion_mg = moles_ion_mmol * mw_ion
    mass_helper_mg = moles_helper_mmol * mw_helper
    mass_chol_mg = moles_chol_mmol * mw_chol
    mass_peg_mg = moles_peg_mmol * mw_peg
    
    # Convert mass to volume: mg / (mg/mL) = mL = 1000 × μL
    vol_ion_ul = (mass_ion_mg / conc_ion * 1000.0) if conc_ion > 0 else 0
    vol_helper_ul = (mass_helper_mg / conc_helper * 1000.0) if conc_helper > 0 else 0
    vol_chol_ul = (mass_chol_mg / conc_chol * 1000.0) if conc_chol > 0 else 0
    vol_peg_ul = (mass_peg_mg / conc_peg * 1000.0) if conc_peg > 0 else 0
    
    # Total lipid volume in organic phase
    total_lipid_vol_ul = vol_ion_ul + vol_helper_ul + vol_chol_ul + vol_peg_ul
    
    # Apply 3:1 aqueous to organic ratio
    # Aqueous (DNA + buffer) = Organic (lipids + ethanol) × 3
    # Organic phase = lipids + ethanol
    # First, calculate ethanol to make a reasonable organic phase
    
    # Target organic phase volume (we'll calculate from aqueous constraint)
    # For now, use a reasonable organic volume target based on lipid content
    # The ethanol fills the remaining space in organic phase
    
    # Calculate DNA volume if DNA parameters provided
    if dna_mass_ug and dna_concentration and dna_concentration > 0:
        dna_vol_ul = dna_mass_ug / dna_concentration  # μg / (μg/μL) = μL
    else:
        dna_vol_ul = 0
    
    # Using 3:1 ratio: aqueous = 3 × organic
    # aqueous = DNA + buffer
    # organic = lipids + ethanol
    # 
    # Let's say we want to minimize total volume while maintaining 3:1 ratio
    # organic = lipids + ethanol
    # aqueous = 3 × organic = DNA + buffer
    # 
    # If we set ethanol to fill organic to match the constraint:
    # We need: (DNA + buffer) = 3 × (lipids + ethanol)
    # Therefore: buffer = 3 × (lipids + ethanol) - DNA
    # 
    # Let's use a reasonable approach: set organic phase to be slightly larger than lipids
    # A common approach is to target a specific total volume or ratio
    
    # Method: Start with lipid volume, add ethanol to reach a target organic volume
    # Then calculate aqueous to maintain 3:1 ratio
    
    # Target: minimize volume while maintaining ratios
    # Minimum organic = total_lipid_vol_ul (no ethanol)
    # But typically we want some ethanol for mixing
    
    # Use a heuristic: make organic phase = lipids × 1.2 (add 20% ethanol)
    # Or use the table pattern: calculate from DNA volume
    
    # From table analysis: for 100 μg DNA with DNA vol 178.5 μL
    # organic = 59.9 μL, aqueous = 180 μL
    # Let's use: organic ≈ lipids + reasonable ethanol
    
    # Simple approach: Calculate organic to satisfy 3:1 with given DNA
    # aqueous = DNA + buffer
    # We want: aqueous = 3 × organic
    # So: DNA + buffer = 3 × (lipids + ethanol)
    # buffer = 3 × (lipids + ethanol) - DNA
    # ethanol = organic - lipids
    # 
    # We need to choose organic volume. Let's use a target based on formulation scale
    # For small scale (1 μg DNA): organic ≈ 0.5-1 μL
    # For large scale (100 μg DNA): organic ≈ 60 μL
    
    # Pattern from table: organic / DNA ≈ 60 / 178.5 ≈ 0.336
    # So: target_organic = dna_vol_ul × 0.336
    
    if dna_vol_ul > 0:
        # Use the ratio from experimental data
        target_organic_vol = dna_vol_ul * 0.336  # Empirical ratio from table
        ethanol_vol_ul = max(0, target_organic_vol - total_lipid_vol_ul)
    else:
        # Default: add some ethanol
        ethanol_vol_ul = total_lipid_vol_ul * 0.2  # 20% ethanol by volume
        target_organic_vol = total_lipid_vol_ul + ethanol_vol_ul
    
    # Calculate aqueous phase using 3:1 ratio
    actual_organic_vol = total_lipid_vol_ul + ethanol_vol_ul
    target_aqueous_vol = actual_organic_vol * 3.0
    
    # Buffer = aqueous - DNA
    buffer_vol_ul = max(0, target_aqueous_vol - dna_vol_ul)
    
    # Total volume
    total = total_lipid_vol_ul + ethanol_vol_ul + dna_vol_ul + buffer_vol_ul
    
    return {
        "Ionizable_Vol_uL": round(vol_ion_ul, 2),
        "Helper_Vol_uL": round(vol_helper_ul, 2),
        "Chol_Vol_uL": round(vol_chol_ul, 2),
        "PEG_Vol_uL": round(vol_peg_ul, 2),
        "Ethanol_Vol_uL": round(ethanol_vol_ul, 2),
        "DNA_Vol_uL": round(dna_vol_ul, 2),
        "Buffer_Vol_uL": round(buffer_vol_ul, 2),
        "Total_Vol_uL": round(total, 2),
        "Ionizable_Moles": total_moles_umol * (ionizable_pct / 100.0)  # Return ionizable moles in μmol for N/P calculation
    }


def generate_run_sheet(design_df, num_replicates, num_blocks, mw_ion, mw_helper, mw_chol, mw_peg,
                       conc_ion, conc_helper, conc_chol, conc_peg, target_vol_ul,
                       dna_mass_ug=None, dna_concentration=None):
    """Generate a complete run sheet with pipetting volumes and N/P ratios."""
    run_data = []
    run_number = 1
    
    for block in range(num_blocks):
        for idx, row in design_df.iterrows():
            ion_pct = row["Ionizable_%"]
            chol_pct = row["Cholesterol_%"]
            peg_pct = row["PEG_%"]
            np_ratio_target = row.get("NP_Ratio", None)
            
            normalized = normalize_molar_ratios(ion_pct, chol_pct, peg_pct)
            if normalized is None:
                continue
            
            ion_pct, helper_pct, chol_pct, peg_pct = normalized
            
            vol_dict = calculate_volumes(
                ion_pct, helper_pct, chol_pct, peg_pct,
                mw_ion, mw_helper, mw_chol, mw_peg,
                conc_ion, conc_helper, conc_chol, conc_peg,
                target_vol_ul,
                dna_mass_ug=dna_mass_ug,
                dna_concentration=dna_concentration
            )
            
            # Calculate N/P ratio if DNA parameters provided
            np_ratio_calc = None
            if dna_mass_ug and vol_dict["Ionizable_Moles"]:
                np_ratio_calc, _, _ = calculate_np_ratio(dna_mass_ug, vol_dict["Ionizable_Moles"], 1.0)
            
            for rep in range(num_replicates):
                run_data.append({
                    "Block": block + 1,
                    "Run_ID": f"R{run_number:03d}",
                    "Experiment": idx + 1,
                    "Replicate": rep + 1,
                    "Ionizable_%": round(ion_pct, 2),
                    "Helper_%": round(helper_pct, 2),
                    "Cholesterol_%": round(chol_pct, 2),
                    "PEG_%": round(peg_pct, 2),
                    "NP_Ratio_Target": np_ratio_target if np_ratio_target else "N/A",
                    "NP_Ratio_Calc": round(np_ratio_calc, 2) if np_ratio_calc else "N/A",
                    "Ionizable_Vol_uL": vol_dict["Ionizable_Vol_uL"],
                    "Helper_Vol_uL": vol_dict["Helper_Vol_uL"],
                    "Chol_Vol_uL": vol_dict["Chol_Vol_uL"],
                    "PEG_Vol_uL": vol_dict["PEG_Vol_uL"],
                    "Ethanol_Vol_uL": vol_dict["Ethanol_Vol_uL"],
                    "DNA_Vol_uL": vol_dict["DNA_Vol_uL"],
                    "Buffer_Vol_uL": vol_dict["Buffer_Vol_uL"],
                    "Total_Vol_uL": vol_dict["Total_Vol_uL"],
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Notes": ""
                })
                run_number += 1
    
    return pd.DataFrame(run_data)


# ============================================================================
# SECTION 3: GENERATE DESIGN
# ============================================================================

st.markdown("---")

if st.button("🚀 Generate DOE Design", type="primary", use_container_width=True):
    
    if ion_min >= ion_max or chol_min >= chol_max or peg_min >= peg_max or np_min >= np_max:
        st.error("❌ Min must be less than Max for all variable ranges.")
    else:
        with st.spinner("Generating DOE design..."):
            
            ranges = {
                "Ionizable_%": (ion_min, ion_max),
                "Cholesterol_%": (chol_min, chol_max),
                "PEG_%": (peg_min, peg_max),
                "NP_Ratio": (np_min, np_max)
            }
            
            try:
                if design_type == "Full Factorial (2-Level)":
                    design_df = generate_2level_factorial(ranges)
                elif design_type == "Full Factorial (3-Level)":
                    design_df = generate_3level_factorial(ranges)
                elif design_type == "Fractional Factorial":
                    design_df = generate_fractional_factorial(ranges)
                elif design_type == "Plackett-Burman":
                    design_df = generate_plackett_burman(ranges)
                elif design_type == "Box-Behnken":
                    design_df = generate_box_behnken(ranges)
                elif design_type == "Central Composite":
                    design_df = generate_central_composite(ranges)
                elif design_type == "Mixture Design":
                    design_df = generate_mixture_design(ranges)
                
                run_sheet = generate_run_sheet(
                    design_df, num_replicates, num_blocks,
                    mw_ionizable, mw_helper, mw_chol, mw_peg,
                    conc_ionizable, conc_helper, conc_chol, conc_peg,
                    target_vol_ul=200.0,
                    dna_mass_ug=dna_mass_ug,
                    dna_concentration=dna_concentration
                )
                
                st.session_state.design_df = design_df
                st.session_state.run_sheet = run_sheet
                st.session_state.design_type = design_type
                
                st.success(f"✅ {design_type} Design Generated: {len(design_df)} design points × {num_replicates} replicate(s) × {num_blocks} block(s) = {len(run_sheet)} total runs")
                
            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")

# ============================================================================
# SECTION 4: DISPLAY RESULTS
# ============================================================================

if "run_sheet" in st.session_state:
    run_sheet = st.session_state.run_sheet
    design_df = st.session_state.design_df
    design_type_used = st.session_state.design_type
    
    st.markdown("---")
    st.header("📋 Results Summary")
    
    sum_col1, sum_col2, sum_col3, sum_col4, sum_col5 = st.columns(5)
    
    with sum_col1:
        st.metric("Design Type", design_type_used.split("(")[0].strip())
    with sum_col2:
        st.metric("Design Points", len(design_df))
    with sum_col3:
        st.metric("Total Runs", len(run_sheet))
    with sum_col4:
        st.metric("Replicates", num_replicates)
    with sum_col5:
        st.metric("Response Type", response_type.split()[0])
    
    st.markdown("---")
    
    st.subheader("🔍 Design Matrix")
    
    design_display = design_df.copy()
    design_display["Helper_%"] = 100.0 - design_display["Ionizable_%"] - design_display["Cholesterol_%"] - design_display["PEG_%"]
    
    st.dataframe(
        design_display.round(2),
        use_container_width=True,
        height=300
    )
    
    st.markdown("---")
    
    st.subheader("🧪 Lab Run Sheet")
    
    if len(run_sheet) > 20:
        show_rows = st.slider("Show first N rows", min_value=5, max_value=len(run_sheet), value=10)
    else:
        show_rows = len(run_sheet)
    
    # Display run sheet with N/P ratio information highlighted
    run_sheet_display = run_sheet.head(show_rows).copy()
    
    # Highlight columns with N/P information if available
    st.dataframe(
        run_sheet_display,
        use_container_width=True,
        height=400
    )
    
    if len(run_sheet) > show_rows:
        st.info(f"📌 Showing first {show_rows} of {len(run_sheet)} runs. Download full sheet below.")
    
    # Show N/P Ratio summary if calculated
    if "NP_Ratio_Calc" in run_sheet.columns and run_sheet["NP_Ratio_Calc"].dtype != 'object':
        np_values = pd.to_numeric(run_sheet["NP_Ratio_Calc"], errors='coerce')
        np_values = np_values.dropna()
        if len(np_values) > 0:
            st.markdown("---")
            col_np1, col_np2, col_np3 = st.columns(3)
            with col_np1:
                st.metric("N/P Min", f"{np_values.min():.2f}")
            with col_np2:
                st.metric("N/P Avg", f"{np_values.mean():.2f}")
            with col_np3:
                st.metric("N/P Max", f"{np_values.max():.2f}")
    
    st.markdown("---")
    
    st.subheader("📊 Design Space Visualization")
    
    # 3D Molar Ratio Space: Ionizable vs Cholesterol vs PEG
    fig3d_molar = go.Figure(data=[go.Scatter3d(
        x=design_display["Ionizable_%"],
        y=design_display["Cholesterol_%"],
        z=design_display["PEG_%"],
        mode='markers',
        marker=dict(
            size=8,
            color=design_display["Helper_%"],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Helper %", x=1.1),
            line=dict(width=1, color='white'),
            opacity=0.9
        ),
        text=[f"Ion: {i:.1f}%<br>Chol: {c:.1f}%<br>PEG: {p:.1f}%<br>Helper: {h:.1f}%" 
              for i, c, p, h in zip(design_display["Ionizable_%"], 
                                   design_display["Cholesterol_%"],
                                   design_display["PEG_%"],
                                   design_display["Helper_%"])],
        hoverinfo='text',
        name='Design Points'
    )])
    
    fig3d_molar.update_layout(
        title="3D Molar Ratio Design Space",
        scene=dict(
            xaxis_title="Ionizable Lipid (%)",
            yaxis_title="Cholesterol (%)",
            zaxis_title="PEG-Lipid (%)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        height=600,
        hovermode='closest',
        showlegend=True
    )
    
    st.plotly_chart(fig3d_molar, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🔬 Response Surface Heatmap")
    
    # Heatmap: Helper Volume vs Ionizable% and Cholesterol%
    pivot_data = run_sheet.pivot_table(
        values='Helper_Vol_uL',
        index='Cholesterol_%',
        columns='Ionizable_%',
        aggfunc='mean'
    )
    
    fig_hm = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        colorbar=dict(title="Helper Vol (µL)")
    ))
    
    fig_hm.update_layout(
        title="Helper Volume: Ionizable% vs Cholesterol%",
        xaxis_title="Ionizable Lipid (%)",
        yaxis_title="Cholesterol (%)",
        height=400
    )
    
    st.plotly_chart(fig_hm, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("💾 Export & Download")
    
    csv_data = run_sheet.to_csv(index=False)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    col_csv, col_xlsx = st.columns(2)
    
    with col_csv:
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"LNP_RunSheet_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_xlsx:
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            run_sheet.to_excel(writer, sheet_name='Run Sheet', index=False)
            design_display.to_excel(writer, sheet_name='Design Matrix', index=False)
            
            summary_data = {
                "Parameter": ["Design Type", "Design Points", "Replicates", "Blocks", "Total Runs", 
                             "Response Type", "Generated", "Ionizable MW", "Helper MW", 
                             "Chol MW", "PEG MW", "N/P Ratio Range"],
                "Value": [design_type_used, len(design_df), num_replicates, num_blocks, len(run_sheet),
                         response_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         mw_ionizable, mw_helper, mw_chol, mw_peg, f"{np_min:.1f} - {np_max:.1f}"]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        excel_buffer.seek(0)
        st.download_button(
            label="📊 Download Excel",
            data=excel_buffer.getvalue(),
            file_name=f"LNP_RunSheet_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.subheader("📈 Experimental Statistics")
    
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.markdown("**Molar Ratio & N/P Coverage**")
        st.text(f"""Ion:    {design_display['Ionizable_%'].min():.1f} → {design_display['Ionizable_%'].max():.1f}%
Chol:   {design_display['Cholesterol_%'].min():.1f} → {design_display['Cholesterol_%'].max():.1f}%
PEG:    {design_display['PEG_%'].min():.1f} → {design_display['PEG_%'].max():.1f}%
Helper: {design_display['Helper_%'].min():.1f} → {design_display['Helper_%'].max():.1f}%
N/P:    {np_min:.1f} → {np_max:.1f}""")
    
    with stat_col2:
        st.markdown("**Volume Range (µL)**")
        st.text(f"""Ion:    {run_sheet['Ionizable_Vol_uL'].min():.1f} → {run_sheet['Ionizable_Vol_uL'].max():.1f}
Helper: {run_sheet['Helper_Vol_uL'].min():.1f} → {run_sheet['Helper_Vol_uL'].max():.1f}
Chol:   {run_sheet['Chol_Vol_uL'].min():.1f} → {run_sheet['Chol_Vol_uL'].max():.1f}
PEG:    {run_sheet['PEG_Vol_uL'].min():.1f} → {run_sheet['PEG_Vol_uL'].max():.1f}""")

else:
    st.info("👈 Configure your DOE parameters and click 'Generate DOE Design' to get started!")

st.markdown("---")

with st.expander("❓ Help & Documentation"):
    st.markdown("""
    ### LNP-Flow: Professional DOE Designer Guide
    
    #### Available DOE Designs
    
    **Full Factorial (2-Level)**: Tests all combinations of high/low levels (2^n runs)
    - Best for initial exploration of design space
    - Useful when you have limited prior knowledge
    
    **Full Factorial (3-Level)**: Tests combinations at 3 levels per factor (3^n runs)
    - More detailed mapping of design space
    - Better for identifying non-linear relationships
    
    **Fractional Factorial**: Reduced subset of full factorial (2^(n-1) or similar)
    - More efficient for many factors
    - Assumes some interactions are negligible
    
    **Plackett-Burman**: Screening design for 7+ factors
    - Typically 12-20 runs regardless of factor count
    - Best for identifying most important variables
    
    **Box-Behnken**: Response surface methodology design
    - Efficient for optimizing near a target
    - Includes center points for curvature detection
    - Fewer runs than full factorial
    
    **Central Composite**: Full factorial + axial + center points
    - Comprehensive response surface modeling
    - Best after initial screening phases
    
    **Mixture Design**: Optimized for proportional components
    - Perfect for LNP formulation ratios
    - Simplex lattice design
    
    #### Key Parameters
    - **Replicates**: Repeat each design point for statistical power
    - **Blocks**: Divide into separate runs (different days, equipment, etc.)
    
    #### Volume Calculations
    1. Molar % → Moles (weighted average MW)
    2. Moles → Mass (mg) using molecular weight
    3. Mass → Volume (µL) using stock concentration
    4. Final volume includes organic phase, ethanol, and aqueous buffer
    """)
