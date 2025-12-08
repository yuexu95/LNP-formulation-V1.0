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
    st.subheader("Lipid Component Properties - Molecular Weights")
    
    col_mw1, col_mw2, col_mw3, col_mw4 = st.columns(4)
    with col_mw1:
        mw_ionizable = st.number_input(
            "Ionizable Lipid MW (g/mol)",
            value=710.182,
            step=0.1,
            key="mw_ion"
        )
    with col_mw2:
        mw_helper = st.number_input(
            "Helper Lipid MW (g/mol)",
            value=790.147,
            step=0.1,
            key="mw_helper"
        )
    with col_mw3:
        mw_chol = st.number_input(
            "Cholesterol MW (g/mol)",
            value=386.654,
            step=0.1,
            key="mw_chol"
        )
    with col_mw4:
        mw_peg = st.number_input(
            "PEG-DMG2000 MW (g/mol)",
            value=2509.2,
            step=0.1,
            key="mw_peg"
        )
    
    st.subheader("Stock Concentrations (μg/μL)")
    col_conc1, col_conc2, col_conc3, col_conc4 = st.columns(4)
    with col_conc1:
        conc_ionizable = st.number_input(
            "Ionizable Lipid (μg/μL)",
            value=20.0,
            step=0.1,
            key="conc_ion"
        )
    with col_conc2:
        conc_helper = st.number_input(
            "Helper Lipid (μg/μL)",
            value=5.0,
            step=0.1,
            key="conc_helper"
        )
    with col_conc3:
        conc_chol = st.number_input(
            "Cholesterol (μg/μL)",
            value=10.0,
            step=0.1,
            key="conc_chol"
        )
    with col_conc4:
        conc_peg = st.number_input(
            "PEG-DMG2000 (μg/μL)",
            value=2.0,
            step=0.1,
            key="conc_peg"
        )
    
    st.subheader("DNA Parameters")
    dna_col1, dna_col2 = st.columns(2)
    
    with dna_col1:
        dna_mass_ug = st.number_input(
            "DNA Scale (μg)",
            value=3.0,
            step=0.1,
            key="dna_mass_ug",
            help="The minimum volume for pDNA-LNP should be 30 μL, otherwise pipetting errors may occur."
        )
    
    with dna_col2:
        dna_concentration = st.number_input(
            "DNA Stock Concentration (μg/μL)",
            value=1.0,
            step=0.01,
            key="dna_conc",
            help="DNA stock solution concentration"
        )

st.markdown("---")

st.subheader("Molar Ratios (%)")
col_ratio1, col_ratio2, col_ratio3, col_ratio4 = st.columns(4)
with col_ratio1:
    ionizable_lipid_ratio = st.number_input(
        "Ionizable Lipid (%)",
        value=50.0,
        step=0.1,
        key="ion_ratio"
    )
with col_ratio2:
    helper_lipid_ratio = st.number_input(
        "Helper Lipid (%)",
        value=10.0,
        step=0.1,
        key="helper_ratio"
    )
with col_ratio3:
    cholesterol_ratio = st.number_input(
        "Cholesterol (%)",
        value=38.5,
        step=0.1,
        key="chol_ratio"
    )
with col_ratio4:
    pegdmg2000_ratio = st.number_input(
        "PEG-DMG2000 (%)",
        value=1.5,
        step=0.1,
        key="peg_ratio"
    )

st.markdown("---")

st.subheader("Additional Parameters")
col_add1, col_add2, col_add3 = st.columns(3)
with col_add1:
    ionizable_lipid_to_dna_ratio = st.number_input(
        "Ionizable Lipid to DNA Ratio",
        value=5.0,
        step=0.1,
        key="ion_dna_ratio_param",
        help="μg ionizable lipid per μg DNA"
    )
with col_add2:
    aqueous_to_ethanol_ratio = st.number_input(
        "Aqueous to Ethanol Ratio",
        value=3.0,
        step=0.1,
        key="aqueous_ethanol_ratio",
        help="Volume ratio of aqueous to ethanol phase"
    )
with col_add3:
    amines_per_molecule = st.number_input(
        "Amines per Ionizable Lipid Molecule",
        value=1.0,
        step=0.1,
        key="amines_per_molecule",
        help="Number of ionizable amine groups per lipid"
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
        design_type = st.selectbox(
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

    # DOE Variable Ranges
    st.subheader("📊 DOE Variable Ranges")
    st.caption("Define the parameter space for DOE exploration")

    ratio_cols = st.columns(4)
    
    with ratio_cols[0]:
        st.markdown("**Ionizable Lipid %**")
        ion_min = st.number_input("Min %", value=45.0, step=1.0, key="ion_min")
        ion_max = st.number_input("Max %", value=55.0, step=1.0, key="ion_max")

    with ratio_cols[1]:
        st.markdown("**Cholesterol %**")
        chol_pct_min = st.number_input("Min %", value=33.5, step=1.0, key="chol_pct_min")
        chol_pct_max = st.number_input("Max %", value=43.5, step=1.0, key="chol_pct_max")

    with ratio_cols[2]:
        st.markdown("**PEG-DMG2000 %**")
        peg_min = st.number_input("Min %", value=0.5, step=0.1, key="peg_min")
        peg_max = st.number_input("Max %", value=2.5, step=0.1, key="peg_max")

    with ratio_cols[3]:
        st.markdown("**Ionizable:DNA (μg/μg)**")
        ion_dna_min = st.number_input("Min", value=5.0, step=0.5, key="ion_dna_min", help="Ionizable lipid mass per DNA mass")
        ion_dna_max = st.number_input("Max", value=15.0, step=0.5, key="ion_dna_max", help="Ionizable lipid mass per DNA mass")

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
    """
    Normalize three components so that Ionizable + Cholesterol + PEG + Helper = 100%.
    Returns None if the combination is invalid (would result in negative Helper %).
    """
    helper_pct = 100.0 - ionizable_pct - cholesterol_pct - peg_pct
    if helper_pct < 0:
        return None
    return ionizable_pct, helper_pct, cholesterol_pct, peg_pct


def filter_valid_design_points(design_df, min_helper_pct=0.5):
    """
    Filter DOE design points to ensure all molar ratios are valid.
    
    A valid combination requires:
    Ionizable + Cholesterol + PEG + Helper = 100%
    And Helper >= min_helper_pct (default 0.5%)
    
    This removes points where the sum of Ion + Chol + PEG > 100% - min_helper_pct
    """
    if not {"Ionizable_%", "Cholesterol_%", "PEG_%"}.issubset(design_df.columns):
        return design_df  # If not all columns present, return unchanged
    
    valid_mask = (
        design_df["Ionizable_%"] + 
        design_df["Cholesterol_%"] + 
        design_df["PEG_%"]
    ) <= (100.0 - min_helper_pct)
    
    filtered_df = design_df[valid_mask].reset_index(drop=True)
    
    # Report filtering results
    n_original = len(design_df)
    n_filtered = len(filtered_df)
    n_removed = n_original - n_filtered
    
    if n_removed > 0:
        st.warning(
            f"⚠️ **Design Space Constraint**: {n_removed} of {n_original} design points removed "
            f"because Ionizable + Cholesterol + PEG > 100%. "
            f"Remaining valid points: {n_filtered}"
        )
    
    return filtered_df


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
    """Generate fractional factorial (subset of 2-level design)."""
    full_design = generate_2level_factorial(ranges_dict)
    fraction = min(16, len(full_design))
    sampled = full_design.sample(n=fraction, random_state=42).reset_index(drop=True)
    return sampled


def generate_plackett_burman(ranges_dict):
    """Generate Plackett-Burman screening design."""
    n_factors = len(ranges_dict)
    factor_names = list(ranges_dict.keys())
    
    # Standard PB matrix for 12 runs, 11 factors (can handle 4 factors)
    pb_matrix = np.array([
        [1, 1, 1, 1],
        [1, -1, 1, -1],
        [1, 1, -1, 1],
        [1, 1, 1, -1],
        [-1, 1, 1, 1],
        [-1, -1, 1, 1],
        [-1, -1, -1, 1],
        [-1, -1, -1, -1],
        [-1, 1, -1, -1],
        [-1, 1, 1, -1],
        [1, -1, -1, -1],
        [1, 1, -1, 1],
    ])
    
    design_points = []
    for point in pb_matrix[:min(12, 2**(n_factors+1))]:
        scaled_point = {}
        for i, factor in enumerate(factor_names[:n_factors]):
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
    
    # Factorial part - use 2-level factorial
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
    dna_mass_ug=None,
    dna_concentration=None,
    ionizable_lipid_to_dna_ratio=10.0,
    aqueous_to_ethanol_ratio=3.0,
    ionizable_lipid_ratio=50.0,
    helper_lipid_ratio=10.0,
    cholesterol_ratio=38.5,
    pegdmg2000_ratio=1.5
):
    """
    Convert molar percentages to pipetting volumes using pDNA formulation logic.
    
    This function follows the pDNA formulation approach:
    1. Use ionizable_lipid_to_dna_ratio to calculate ionizable lipid moles
    2. Scale other lipids based on molar ratios
    3. Calculate volumes from masses and stock concentrations
    4. Apply 3:1 aqueous:organic ratio with citrate buffer
    
    Input units:
    - Percentages: molar %
    - MW: g/mol  
    - Concentrations: μg/μL (= mg/mL)
    - DNA mass: μg
    - DNA concentration: μg/μL (= mg/mL)
    - ionizable_lipid_to_dna_ratio: μg ionizable per μg DNA
    - aqueous_to_ethanol_ratio: volume ratio
    """
    # Calculate moles of ionizable lipid using the ionizable_lipid_to_dna_ratio
    ionizable_lipid_moles = (dna_mass_ug * ionizable_lipid_to_dna_ratio) / mw_ion
    
    # Calculate moles of each lipid based on their molar ratios
    helper_lipid_moles = ionizable_lipid_moles * helper_lipid_ratio / ionizable_lipid_ratio
    cholesterol_moles = ionizable_lipid_moles * cholesterol_ratio / ionizable_lipid_ratio
    pegdmg2000_moles = ionizable_lipid_moles * pegdmg2000_ratio / ionizable_lipid_ratio
    
    # Calculate mass of each lipid
    ionizable_lipid_mass = ionizable_lipid_moles * mw_ion
    helper_lipid_mass = helper_lipid_moles * mw_helper
    cholesterol_mass = cholesterol_moles * mw_chol
    pegdmg2000_mass = pegdmg2000_moles * mw_peg
    
    # Calculate final LNP volume
    final_lnp_volume = dna_mass_ug / 0.1
    
    # Calculate ethanol phase volume
    ionizable_lipid_volume = ionizable_lipid_mass / conc_ion
    helper_lipid_volume = helper_lipid_mass / conc_helper
    cholesterol_volume = cholesterol_mass / conc_chol
    pegdmg2000_volume = pegdmg2000_mass / conc_peg
    ethanol = final_lnp_volume / (aqueous_to_ethanol_ratio + 1) - ionizable_lipid_volume - helper_lipid_volume - cholesterol_volume - pegdmg2000_volume
    ethanol_phase_volume = ionizable_lipid_volume + helper_lipid_volume + cholesterol_volume + pegdmg2000_volume + ethanol
    
    # Calculate aqueous phase volume
    aqueous_phase_volume = final_lnp_volume * (aqueous_to_ethanol_ratio / (aqueous_to_ethanol_ratio + 1))
    dna_volume = dna_mass_ug / dna_concentration
    citrate_volume = 0.1 * aqueous_phase_volume
    water_volume = aqueous_phase_volume - dna_volume - citrate_volume
    
    # Calculate total volume
    total = ionizable_lipid_volume + helper_lipid_volume + cholesterol_volume + pegdmg2000_volume + ethanol + dna_volume + citrate_volume + water_volume
    
    return {
        "Ionizable_Vol_uL": round(ionizable_lipid_volume, 2),
        "Helper_Vol_uL": round(helper_lipid_volume, 2),
        "Chol_Vol_uL": round(cholesterol_volume, 2),
        "PEG_Vol_uL": round(pegdmg2000_volume, 2),
        "Ethanol_Vol_uL": round(ethanol, 2),
        "DNA_Vol_uL": round(dna_volume, 2),
        "Citrate_Vol_uL": round(citrate_volume, 2),
        "Water_Vol_uL": round(water_volume, 2),
        "Total_Vol_uL": round(total, 2),
        "Ionizable_Moles": ionizable_lipid_moles,  # Return ionizable moles for N/P calculation
        "Phosphate_Moles": dna_mass_ug * 1e-6 / 330.0 * 1e6  # phosphate moles in μmol
    }


def generate_run_sheet(design_df, num_replicates, num_blocks, mw_ion, mw_helper, mw_chol, mw_peg,
                       conc_ion, conc_helper, conc_chol, conc_peg,
                       dna_mass_ug=None, dna_concentration=None,
                       ionizable_lipid_to_dna_ratio=10.0,
                       aqueous_to_ethanol_ratio=3.0,
                       ionizable_lipid_ratio=50.0,
                       helper_lipid_ratio=10.0,
                       cholesterol_ratio=38.5,
                       pegdmg2000_ratio=1.5,
                       amines_per_molecule=1.0):
    """
    Generate a complete run sheet with pipetting volumes and N/P ratios.
    Uses pDNA formulation calculation logic.
    """
    run_data = []
    run_number = 1
    
    for block in range(num_blocks):
        for idx, row in design_df.iterrows():
            ion_pct = row["Ionizable_%"]
            chol_pct = row["Cholesterol_%"]
            peg_pct = row["PEG_%"]
            ion_dna_ratio_target = row.get("Ion_DNA_Ratio", None)
            
            normalized = normalize_molar_ratios(ion_pct, chol_pct, peg_pct)
            if normalized is None:
                continue
            
            ion_pct, helper_pct, chol_pct, peg_pct = normalized
            
            vol_dict = calculate_volumes(
                ion_pct, helper_pct, chol_pct, peg_pct,
                mw_ion, mw_helper, mw_chol, mw_peg,
                conc_ion, conc_helper, conc_chol, conc_peg,
                dna_mass_ug=dna_mass_ug,
                dna_concentration=dna_concentration,
                ionizable_lipid_to_dna_ratio=ionizable_lipid_to_dna_ratio,
                aqueous_to_ethanol_ratio=aqueous_to_ethanol_ratio,
                ionizable_lipid_ratio=ionizable_lipid_ratio,
                helper_lipid_ratio=helper_lipid_ratio,
                cholesterol_ratio=cholesterol_ratio,
                pegdmg2000_ratio=pegdmg2000_ratio
            )
            
            # Calculate N/P ratio
            ionizable_moles = vol_dict["Ionizable_Moles"]
            phosphate_moles = vol_dict["Phosphate_Moles"]
            amine_moles = ionizable_moles * amines_per_molecule
            
            np_ratio = amine_moles / phosphate_moles if phosphate_moles > 0 else 0
            
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
                    "Ion_DNA_Target": ion_dna_ratio_target if ion_dna_ratio_target else "N/A",
                    "NP_Ratio": round(np_ratio, 2),
                    "Ionizable_Vol_uL": vol_dict["Ionizable_Vol_uL"],
                    "Helper_Vol_uL": vol_dict["Helper_Vol_uL"],
                    "Chol_Vol_uL": vol_dict["Chol_Vol_uL"],
                    "PEG_Vol_uL": vol_dict["PEG_Vol_uL"],
                    "Ethanol_Vol_uL": vol_dict["Ethanol_Vol_uL"],
                    "DNA_Vol_uL": vol_dict["DNA_Vol_uL"],
                    "Citrate_Vol_uL": vol_dict["Citrate_Vol_uL"],
                    "Water_Vol_uL": vol_dict["Water_Vol_uL"],
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
    
    if ion_min >= ion_max or chol_pct_min >= chol_pct_max or peg_min >= peg_max or ion_dna_min >= ion_dna_max:
        st.error("❌ Min must be less than Max for all variable ranges.")
    else:
        with st.spinner("Generating DOE design..."):
            
            ranges = {
                "Ionizable_%": (ion_min, ion_max),
                "Cholesterol_%": (chol_pct_min, chol_pct_max),
                "PEG_%": (peg_min, peg_max),
                "Ion_DNA_Ratio": (ion_dna_min, ion_dna_max)
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
                
                # Filter invalid design points (where ratios sum > 100%)
                design_df = filter_valid_design_points(design_df, min_helper_pct=0.5)
                
                # Check if we have any valid points left
                if len(design_df) == 0:
                    st.error("❌ No valid design points found! The specified ratio ranges are too wide and conflict with the requirement that all ratios sum to 100%. Please adjust your ranges.")
                else:
                    run_sheet = generate_run_sheet(
                        design_df, num_replicates, num_blocks,
                        mw_ionizable, mw_helper, mw_chol, mw_peg,
                        conc_ionizable, conc_helper, conc_chol, conc_peg,
                        dna_mass_ug=dna_mass_ug,
                        dna_concentration=dna_concentration,
                        ionizable_lipid_to_dna_ratio=ionizable_lipid_to_dna_ratio,
                        aqueous_to_ethanol_ratio=aqueous_to_ethanol_ratio,
                        ionizable_lipid_ratio=ionizable_lipid_ratio,
                        helper_lipid_ratio=helper_lipid_ratio,
                        cholesterol_ratio=cholesterol_ratio,
                        pegdmg2000_ratio=pegdmg2000_ratio,
                        amines_per_molecule=amines_per_molecule
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
    if "NP_Ratio" in run_sheet.columns and run_sheet["NP_Ratio"].dtype != 'object':
        np_values = pd.to_numeric(run_sheet["NP_Ratio"], errors='coerce')
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
                             "Chol MW", "PEG MW", "Ion/DNA Ratio Range"],
                "Value": [design_type_used, len(design_df), num_replicates, num_blocks, len(run_sheet),
                         response_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         mw_ionizable, mw_helper, mw_chol, mw_peg, f"{ion_dna_min:.1f} - {ion_dna_max:.1f}"]
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
        st.markdown("**Molar Ratio & Ion/DNA Coverage**")
        st.text(f"""Ion:    {design_display['Ionizable_%'].min():.1f} → {design_display['Ionizable_%'].max():.1f}%
Chol:   {design_display['Cholesterol_%'].min():.1f} → {design_display['Cholesterol_%'].max():.1f}%
PEG:    {design_display['PEG_%'].min():.1f} → {design_display['PEG_%'].max():.1f}%
Helper: {design_display['Helper_%'].min():.1f} → {design_display['Helper_%'].max():.1f}%
Ion/DNA: {ion_dna_min:.1f} → {ion_dna_max:.1f}""")
    
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
