import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🧪 DNA-Component Interaction Validation Tool")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_gradient_volumes(
    dna_amount_ug,
    component_mw,
    component_stock_conc_ug_ul,
    w_w_ratios,
    dna_stock_conc_ug_ul=1.0
):
    """
    Calculate volumes for DNA-component binding gradient experiments (w/w ratio).
    
    Parameters:
    - dna_amount_ug: Amount of DNA per sample (μg)
    - component_mw: Molecular weight of component (Da)
    - component_stock_conc_ug_ul: Component stock concentration (μg/μL)
    - w_w_ratios: List of weight-to-weight ratios (e.g., [1, 2, 3, ...])
    - dna_stock_conc_ug_ul: DNA stock concentration (μg/μL), default 1.0
    
    Returns:
    - DataFrame with calculated volumes and masses
    """
    
    results = []
    dna_volume = dna_amount_ug / dna_stock_conc_ug_ul
    
    for ratio in w_w_ratios:
        # Component mass = DNA mass × ratio
        component_mass_ug = dna_amount_ug * ratio
        
        # Component volume from stock
        component_volume = component_mass_ug / component_stock_conc_ug_ul
        
        # Molar amounts
        dna_moles_nmol = dna_amount_ug * 1000 / 330  # 330 Da per nucleotide
        component_moles_nmol = component_mass_ug * 1000 / component_mw
        
        # Molar ratio
        molar_ratio = component_moles_nmol / dna_moles_nmol if dna_moles_nmol > 0 else 0
        
        results.append({
            "w/w Ratio": f"{ratio}:1",
            "Component (μg)": f"{component_mass_ug:.2f}",
            "Component (μL)": f"{component_volume:.2f}",
            "DNA (μg)": f"{dna_amount_ug:.2f}",
            "DNA (μL)": f"{dna_volume:.2f}",
            "Component Moles (nmol)": f"{component_moles_nmol:.3f}",
            "DNA Moles (nmol)": f"{dna_moles_nmol:.3f}",
            "Molar Ratio": f"{molar_ratio:.3f}",
            "Total Volume (μL)": f"{component_volume + dna_volume:.2f}",
        })
    
    return pd.DataFrame(results)

def calculate_binding_metrics(
    dna_amount_ug,
    component_amount_ug,
    component_mw,
    expected_binding_sites=None
):
    """
    Calculate binding metrics for DNA-component interaction.
    
    Parameters:
    - dna_amount_ug: DNA mass (μg)
    - component_amount_ug: Component mass (μg)
    - component_mw: Component molecular weight (Da)
    - expected_binding_sites: Expected number of binding sites per component (optional)
    
    Returns:
    - Dictionary with binding metrics
    """
    
    # Molar amounts
    dna_moles = dna_amount_ug * 1000 / 330  # nmol, assuming 330 Da per bp
    component_moles = component_amount_ug * 1000 / component_mw  # nmol
    
    # Weight ratio
    w_w_ratio = component_amount_ug / dna_amount_ug
    
    # Molar ratio
    molar_ratio = component_moles / dna_moles if dna_moles > 0 else 0
    
    metrics = {
        "DNA Amount (μg)": dna_amount_ug,
        "Component Amount (μg)": component_amount_ug,
        "Weight Ratio (w/w)": f"{w_w_ratio:.2f}:1",
        "DNA Moles (nmol)": f"{dna_moles:.3f}",
        "Component Moles (nmol)": f"{component_moles:.3f}",
        "Molar Ratio": f"{molar_ratio:.3f}",
    }
    
    if expected_binding_sites and component_moles > 0:
        binding_capacity = (dna_amount_ug / component_mw) * expected_binding_sites
        metrics["Expected Binding Capacity (μg)"] = f"{binding_capacity:.2f}"
        if component_amount_ug > 0:
            binding_saturation = (component_amount_ug / binding_capacity) * 100 if binding_capacity > 0 else 0
            metrics["Binding Saturation (%)"] = f"{binding_saturation:.1f}%"
    
    return metrics

def generate_visualization_data(w_w_ratios):
    """Generate data for visualization of gradient series."""
    return {
        "Ratio": w_w_ratios,
        "Component Mass (×DNA mass)": w_w_ratios,
    }

# ============================================================================
# PAGE TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["🧪 Gradient Experiment Design", "📊 Binding Analysis", "🧬 Multi-step LNP with Compounds", "🔬 NLS Peptide for pDNA Delivery"])

# ============================================================================
# TAB 1: GRADIENT EXPERIMENT DESIGN
# ============================================================================

with tab1:
    st.header("🧪 DNA-Component Gradient Experiment Design")
    st.info("💡 Design gradient mixing experiments to validate component-DNA interactions. This tool calculates precise volumes for w/w ratio experiments ranging from 1:1 to 10:1.")
    
    # Initialize session state
    if "gradient_results" not in st.session_state:
        st.session_state.gradient_results = None
    if "gradient_history" not in st.session_state:
        st.session_state.gradient_history = []
    
    # ========== Experiment Parameters ==========
    st.subheader("📋 Experiment Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        exp_name = st.text_input(
            "Experiment Name",
            value="",
            placeholder="e.g., Peptide-DNA Binding",
            key="exp_name"
        )
    with col2:
        component_name = st.text_input(
            "Component Name",
            value="Additional Component",
            placeholder="e.g., Targeting Peptide",
            key="comp_name"
        )
    with col3:
        dna_type = st.selectbox(
            "DNA Type",
            ["dsDNA (plasmid)", "dsDNA (linear)", "ssDNA", "oligonucleotide"],
            key="dna_type"
        )
    with col4:
        dna_length_bp = st.number_input(
            "DNA Length (bp)",
            min_value=20,
            step=100,
            value=5000,
            key="dna_length",
            help="For MW calculation if needed"
        )
    
    # ========== DNA Parameters ==========
    st.markdown("### 🧬 DNA Setup")
    col5, col6, col7 = st.columns(3)
    with col5:
        dna_amount = st.number_input(
            "DNA Amount per Sample (μg)",
            min_value=0.1,
            step=0.5,
            value=5.0,
            key="dna_amount",
            help="Amount of DNA used in each mixture"
        )
    with col6:
        dna_stock = st.number_input(
            "DNA Stock Concentration (μg/μL)",
            min_value=0.1,
            step=0.1,
            value=1.0,
            key="dna_stock",
            help="Concentration of your DNA stock solution"
        )
    with col7:
        dna_buffer = st.selectbox(
            "DNA Buffer",
            ["TE", "PBS", "Citrate", "Custom"],
            key="dna_buffer"
        )
    
    # ========== Component Parameters ==========
    st.markdown("### 🧪 Component Setup")
    col8, col9, col10 = st.columns(3)
    with col8:
        comp_stock = st.number_input(
            "Component Stock Concentration (mg/ml)",
            min_value=0.1,
            step=0.1,
            value=10.0,
            key="comp_stock",
            help="Concentration of your component stock (1 mg/ml = 1 μg/μL)"
        )
    with col9:
        comp_mw = st.number_input(
            "Component Molecular Weight (Da)",
            min_value=50.0,
            step=50.0,
            value=500.0,
            key="comp_mw",
            help="MW for molar ratio calculation"
        )
    with col10:
        comp_solvent = st.selectbox(
            "Component Solvent",
            ["Ethanol", "Water", "PBS", "DMSO", "Other"],
            key="comp_solvent"
        )
    
    # ========== Ratio Range ==========
    st.markdown("### 📊 w/w Ratio Range")
    col11, col12, col13 = st.columns(3)
    with col11:
        ratio_start = st.number_input(
            "Start Ratio",
            min_value=0.1,
            step=0.1,
            value=1.0,
            key="ratio_start"
        )
    with col12:
        ratio_end = st.number_input(
            "End Ratio",
            min_value=0.1,
            step=0.1,
            value=10.0,
            key="ratio_end"
        )
    with col13:
        ratio_step = st.number_input(
            "Step Size",
            min_value=0.1,
            step=0.1,
            value=1.0,
            key="ratio_step"
        )
    
    # Generate ratio list
    ratios = np.arange(ratio_start, ratio_end + ratio_step, ratio_step)
    ratios = np.round(ratios, 1).tolist()
    st.info(f"📌 **Gradient Series:** {len(ratios)} samples - Ratios: {', '.join([f'{r}:1' for r in ratios])}")
    st.caption("💡 **Unit Note:** Component stock concentration in **mg/ml** (1 mg/ml = 1 μg/μL)")
    
    # ========== Calculate ==========
    if st.button("📊 Calculate Gradient Volumes", key="calc_gradient", use_container_width=True):
        try:
            gradient_df = calculate_gradient_volumes(
                dna_amount,
                comp_mw,
                comp_stock,
                ratios,
                dna_stock
            )
            st.session_state.gradient_results = gradient_df
            
            # Add to history
            history_record = {
                "Experiment": exp_name if exp_name else "Unnamed",
                "Component": component_name,
                "DNA Type": dna_type,
                "DNA (μg)": dna_amount,
                "Component MW": comp_mw,
                "Ratios": f"{len(ratios)} samples ({ratio_start}:1 - {ratio_end}:1)",
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.gradient_history.append(history_record)
            
            st.success("✅ Gradient volumes calculated successfully!")
        except Exception as e:
            st.error(f"❌ Error calculating gradient: {str(e)}")
    
    # ========== Results Display ==========
    if st.session_state.gradient_results is not None:
        st.markdown("---")
        st.subheader("📋 Gradient Composition Table")
        
        # Display results
        st.dataframe(st.session_state.gradient_results, use_container_width=True)
        
        # ========== Visualization ==========
        st.subheader("📈 Gradient Visualization")
        
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Extract numeric values for plotting
            ratios_numeric = [float(str(r).split(':')[0]) for r in st.session_state.gradient_results['w/w Ratio']]
            comp_volumes = pd.to_numeric(st.session_state.gradient_results['Component (μL)'], errors='coerce')
            dna_volume = float(st.session_state.gradient_results['DNA (μL)'].iloc[0])
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(ratios_numeric, comp_volumes, 'o-', label='Component Volume', linewidth=2, markersize=8, color='#1f77b4')
            ax.axhline(y=dna_volume, color='#ff7f0e', linestyle='--', label=f'DNA Volume ({dna_volume:.2f} μL)', linewidth=2)
            ax.set_xlabel('w/w Ratio (Component:DNA)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Volume (μL)', fontsize=12, fontweight='bold')
            ax.set_title('Component Volume vs w/w Ratio', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
            st.pyplot(fig)
        
        with col_viz2:
            # Molar ratio visualization
            molar_ratios = pd.to_numeric(st.session_state.gradient_results['Molar Ratio'], errors='coerce')
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(range(len(ratios_numeric)), molar_ratios, color='#2ca02c', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Sample Index', fontsize=12, fontweight='bold')
            ax.set_ylabel('Molar Ratio (Component:DNA)', fontsize=12, fontweight='bold')
            ax.set_title('Molar Ratio Distribution', fontsize=14, fontweight='bold')
            ax.set_xticks(range(len(ratios_numeric)))
            ax.set_xticklabels([f'{r}:1' for r in ratios_numeric], rotation=45)
            ax.grid(True, alpha=0.3, axis='y')
            st.pyplot(fig)
        
        # ========== Export Options ==========
        st.subheader("📥 Export Results")
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            csv_data = st.session_state.gradient_results.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv_data,
                file_name=f"gradient_volumes_{exp_name or 'experiment'}.csv",
                mime="text/csv",
                key="download_gradient"
            )
        
        with col_exp2:
            # Generate protocol text
            protocol = f"""DNA-Component Interaction Gradient Protocol
Experiment: {exp_name or 'Unnamed'}
Component: {component_name}
DNA Type: {dna_type}
Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}

DNA Setup:
- Amount per sample: {dna_amount} μg
- Stock concentration: {dna_stock} μg/μL
- Buffer: {dna_buffer}

Component Setup:
- Molecular weight: {comp_mw} Da
- Stock concentration: {comp_stock} μg/μL
- Solvent: {comp_solvent}

Gradient Series ({len(ratios)} samples):
"""
            for idx, row in st.session_state.gradient_results.iterrows():
                protocol += f"\nSample {idx+1} ({row['w/w Ratio']}):\n"
                protocol += f"  - Component: {row['Component (μL)']} μL ({row['Component (μg)']} μg)\n"
                protocol += f"  - DNA: {row['DNA (μL)']} μL ({row['DNA (μg)']} μg)\n"
                protocol += f"  - Molar ratio: {row['Molar Ratio']}\n"
            
            st.download_button(
                "📄 Download Protocol",
                protocol,
                file_name=f"protocol_{exp_name or 'experiment'}.txt",
                mime="text/plain",
                key="download_protocol"
            )
        
        with col_exp3:
            if st.button("🗑️ Clear Results", key="clear_gradient"):
                st.session_state.gradient_results = None
                st.rerun()

# ============================================================================
# TAB 2: BINDING ANALYSIS
# ============================================================================

with tab2:
    st.header("📊 DNA-Component Binding Analysis")
    st.info("💡 Analyze binding metrics and predict interaction patterns for your DNA-component experiments.")
    
    if "binding_analysis" not in st.session_state:
        st.session_state.binding_analysis = []
    
    # ========== Quick Analysis ==========
    st.subheader("⚡ Quick Binding Analysis")
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        b_dna_amount = st.number_input(
            "DNA Amount (μg)",
            min_value=0.1,
            step=0.5,
            value=5.0,
            key="b_dna_amount"
        )
    with col_b2:
        b_comp_amount = st.number_input(
            "Component Amount (μg)",
            min_value=0.1,
            step=0.5,
            value=5.0,
            key="b_comp_amount"
        )
    with col_b3:
        b_comp_mw = st.number_input(
            "Component MW (Da)",
            min_value=50.0,
            step=50.0,
            value=500.0,
            key="b_comp_mw"
        )
    with col_b4:
        b_binding_sites = st.number_input(
            "Binding Sites per Component",
            min_value=0,
            step=1,
            value=0,
            key="b_binding_sites",
            help="Optional: if known, leave 0 if unknown"
        )
    
    if st.button("🔍 Analyze Binding", key="analyze_binding", use_container_width=True):
        metrics = calculate_binding_metrics(
            b_dna_amount,
            b_comp_amount,
            b_comp_mw,
            b_binding_sites if b_binding_sites > 0 else None
        )
        
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.markdown("### Basic Metrics")
            for key, value in list(metrics.items())[:4]:
                st.metric(key.replace(" (μg)", ""), value)
        
        with col_m2:
            st.markdown("### Molar Analysis")
            for key, value in list(metrics.items())[4:]:
                st.metric(key.replace(" (nmol)", ""), value)
        
        # Store analysis
        analysis_record = {
            "DNA (μg)": b_dna_amount,
            "Component (μg)": b_comp_amount,
            "MW": b_comp_mw,
            "w/w Ratio": f"{(b_comp_amount/b_dna_amount):.2f}:1",
            "Molar Ratio": metrics.get("Molar Ratio", "N/A"),
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.binding_analysis.append(analysis_record)
    
    # ========== Analysis History ==========
    st.markdown("---")
    st.subheader("📋 Analysis History")
    
    if len(st.session_state.binding_analysis) > 0:
        analysis_df = pd.DataFrame(st.session_state.binding_analysis)
        st.dataframe(analysis_df, use_container_width=True)
        
        if st.button("🗑️ Clear Analysis History", key="clear_analysis"):
            st.session_state.binding_analysis = []
            st.rerun()
    else:
        st.info("No analysis records yet. Perform an analysis to see results here.")
    
    # ========== Binding Model Information ==========
    st.markdown("---")
    with st.expander("📚 Binding Model Reference"):
        st.markdown("""
        ### Key Binding Concepts:
        
        **1. Weight-to-Weight (w/w) Ratio**
        - Simple mass ratio between component and DNA
        - Formula: w/w = Component mass / DNA mass
        - Easy to prepare and reproduce experimentally
        
        **2. Molar Ratio**
        - Ratio based on moles of molecules
        - Formula: Molar ratio = (Component mass / MW) / (DNA mass / 330 Da)
        - More relevant for binding kinetics
        - 330 Da = average molecular weight per base pair
        
        **3. Binding Saturation**
        - Percentage of binding sites occupied by component
        - Indicates if DNA is saturated with component
        - >100% suggests excess component beyond saturation
        
        **4. Typical Binding Experiments**
        - **Electrophoretic Mobility Shift (EMSA):** Test w/w 1:1 to 10:1
        - **Fluorescence Titration:** Gradual component addition
        - **Isothermal Titration (ITC):** Precise thermodynamic measurements
        - **Surface Plasmon Resonance (SPR):** Real-time binding kinetics
        
        **5. Gradient Design Recommendations**
        - Start with 1:1 w/w ratio (1 part component per 1 part DNA)
        - Increase to 10:1 to find saturation point
        - Use 0.5:1 or 2:1 step size for finer resolution
        - Include a DNA-only control (0:1 ratio)
        """)

# ============================================================================
# EXPERIMENT HISTORY & SUMMARY
# ============================================================================

st.markdown("---")
st.subheader("📚 Experiment History Summary")

if len(st.session_state.gradient_history) > 0:
    history_df = pd.DataFrame(st.session_state.gradient_history)
    st.dataframe(history_df, use_container_width=True)
    
    if st.button("📥 Export Experiment History", key="export_history"):
        csv_history = history_df.to_csv(index=False)
        st.download_button(
            "Download History CSV",
            csv_history,
            file_name="experiment_history.csv",
            mime="text/csv",
            key="download_history"
        )
else:
    st.info("💡 No experiments designed yet. Start by designing a gradient experiment in the first tab.")

# ============================================================================
# TIPS & BEST PRACTICES
# ============================================================================

with st.expander("💡 Best Practices for DNA-Component Interaction Validation"):
    st.markdown("""
    ### Experimental Design Tips:
    
    **1. Sample Preparation**
    - Prepare component and DNA stocks separately
    - Use fresh stocks to avoid degradation
    - Mix component and DNA at room temperature unless protein involved
    - Allow sufficient incubation time (5-30 minutes depending on interaction)
    
    **2. Gradient Design Optimization**
    - Include DNA-only control (0:1 ratio)
    - Use regular increments (0.5:1, 1:1, 2:1, etc.)
    - For weak interactions: use finer steps (0.2:1 increments)
    - For strong interactions: use larger steps (5:1 increments)
    
    **3. Common w/w Ratios for Different Components**
    - **Peptides:** 1:1 to 5:1 (typically saturate at 2-3:1)
    - **Small molecules:** 5:1 to 20:1 (often need high ratios)
    - **Polymers:** 0.1:1 to 1:1 (saturation at low ratios)
    - **Proteins:** 1:1 to 10:1 (depends on protein size)
    
    **4. Detection Methods**
    - **EMSA:** Visualize DNA binding/complex formation
    - **Fluorescence:** Use fluorescent DNA or component labels
    - **Turbidity:** Monitor precipitation/aggregation
    - **DLS:** Check particle size changes
    - **Zeta Potential:** Monitor charge changes
    
    **5. Data Interpretation**
    - Plot signal vs. w/w ratio to find saturation point
    - Calculate EC50 (50% saturation concentration)
    - Assess stoichiometry from molar ratios
    - Check for cooperative binding patterns
    
    **6. Quality Control**
    - Verify DNA intactness (gel electrophoresis)
    - Check component purity
    - Validate stock concentrations
    - Run duplicates for reproducibility
    """)

# ============================================================================
# TAB 3: MULTI-STEP LNP FORMULATION WITH NLS
# ============================================================================

with tab3:
    st.header("🧬 Multi-step LNP Formulation with Custom DNA-Binding Compound")
    st.info("💡 Design LNP formulations where a custom compound (peptide, protein, polymer, etc.) is pre-complexed with DNA before mixing with lipid components. Adjust molecular weight and ratio for your specific compound.")
    
    # Initialize session state
    if "compound_results" not in st.session_state:
        st.session_state.compound_results = None
    if "compound_history" not in st.session_state:
        st.session_state.compound_history = []
    
    # ========== Preset Compounds ==========
    st.subheader("⚡ Quick Preset Selection")
    
    # Define preset compounds with their properties
    preset_compounds = {
        "Custom": {"mw": 500.0, "conc": 10.0, "solvent": "Water"},
        "Protamine Sulfate (Full)": {"mw": 4150.0, "conc": 10.0, "solvent": "Water", "info": "MW ≈ 4.15 kDa, 49 amino acids, typical stock 10-50 mg/ml"},
        "Low Molecular Weight Protamine (LMWP)": {"mw": 1880.18, "conc": 10.0, "solvent": "Water", "info": "MW = 1880.18 Da, 14 amino acids, CPP, solubility ≥100 mg/ml"},
        "Poly-L-Lysine (PLL) 10kDa": {"mw": 10000.0, "conc": 10.0, "solvent": "Water", "info": "Common DNA binding polymer, typical stock 10-50 mg/ml"},
        "Poly-L-Arginine 5kDa": {"mw": 5000.0, "conc": 10.0, "solvent": "Water", "info": "Positively charged polymer, typical stock 10-50 mg/ml"},
        "Histone H1": {"mw": 21000.0, "conc": 10.0, "solvent": "Water", "info": "DNA-binding protein, typical stock 5-20 mg/ml"},
        "Spermidine": {"mw": 145.24, "conc": 100.0, "solvent": "Water", "info": "Small DNA condensing agent, very soluble"},
        "Spermine": {"mw": 202.34, "conc": 100.0, "solvent": "Water", "info": "Polyamine DNA condensing agent, very soluble"},
    }
    
    col_preset1, col_preset2 = st.columns([3, 1])
    with col_preset1:
        preset_select = st.selectbox(
            "Select a Preset Compound",
            list(preset_compounds.keys()),
            key="preset_compound",
            help="Choose from common DNA-binding compounds or select 'Custom' to enter your own values"
        )
    with col_preset2:
        if preset_select in preset_compounds:
            preset_data = preset_compounds[preset_select]
            if "info" in preset_data:
                st.caption(f"📝 {preset_data['info']}")
    
    # Auto-apply preset values when selected (no button needed)
    if preset_select != "Custom":
        preset_data = preset_compounds[preset_select]
        st.session_state.current_preset_mw = preset_data["mw"]
        st.session_state.current_preset_conc = preset_data["conc"]
        st.session_state.current_preset_solvent = preset_data["solvent"]
    else:
        st.session_state.current_preset_mw = 500.0
        st.session_state.current_preset_conc = 10.0
        st.session_state.current_preset_solvent = "Water"
    
    # ========== Step 1: DNA-Compound Complex Formation ==========
    st.subheader("📋 Step 1: DNA-Compound Complex Formation")
    st.markdown("**Protocol:** Mix DNA solution with your compound at specified w/w ratio, incubate at room temperature")
    
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        comp_exp_name = st.text_input(
            "Experiment Name",
            value="",
            placeholder="e.g., Peptide-DNA-LNP",
            key="comp_exp_name"
        )
    with col_p2:
        comp_dna_amount = st.number_input(
            "DNA Amount (μg)",
            min_value=1.0,
            step=1.0,
            value=10.0,
            key="comp_dna_amount",
            help="Total DNA used per LNP batch"
        )
    with col_p3:
        comp_dna_stock = st.number_input(
            "DNA Stock (μg/μL)",
            min_value=0.1,
            step=0.1,
            value=1.0,
            key="comp_dna_stock"
        )
    with col_p4:
        comp_dna_buffer = st.selectbox(
            "DNA Buffer",
            ["TE", "PBS", "Citrate", "Water"],
            key="comp_dna_buffer"
        )
    
    # Custom compound parameters
    st.markdown("**Custom DNA-Binding Compound Parameters**")
    col_p5, col_p6, col_p7, col_p8 = st.columns(4)
    with col_p5:
        compound_name = st.text_input(
            "Compound Name",
            value=preset_select if preset_select != "Custom" else "Custom Compound",
            placeholder="e.g., Protamine, Peptide, Polymer",
            key="compound_name"
        )
    with col_p6:
        default_mw = st.session_state.get("current_preset_mw", 500.0)
        compound_mw = st.number_input(
            "Compound Molecular Weight (Da)",
            min_value=50.0,
            step=50.0,
            value=default_mw,
            key="compound_mw",
            help="Molecular weight of your compound in Daltons (Da)"
        )
    with col_p7:
        default_conc = st.session_state.get("current_preset_conc", 10.0)
        compound_stock_conc = st.number_input(
            "Compound Stock (mg/ml)",
            min_value=0.1,
            step=0.5,
            value=default_conc,
            key="compound_stock_conc",
            help="Stock concentration of your compound (mg/ml = μg/μL)"
        )
    with col_p8:
        default_solvent = st.session_state.get("current_preset_solvent", "Water")
        solvent_options = ["Water", "PBS", "Ethanol", "DMSO", "Other"]
        default_index = solvent_options.index(default_solvent) if default_solvent in solvent_options else 0
        compound_solvent = st.selectbox(
            "Compound Solvent",
            solvent_options,
            index=default_index,
            key="compound_solvent"
        )
    
    col_p9, col_p10, col_p11 = st.columns(3)
    with col_p9:
        compound_w_w_ratio = st.number_input(
            f"{compound_name}:DNA w/w Ratio",
            min_value=0.1,
            step=0.1,
            value=1.0,
            key="compound_w_w_ratio",
            help="Weight ratio of compound to DNA"
        )
    with col_p10:
        compound_incubation = st.number_input(
            "Incubation Time (min)",
            min_value=1,
            step=1,
            value=10,
            key="compound_incubation",
            help="Complex formation incubation time"
        )
    with col_p11:
        compound_temp = st.selectbox(
            "Incubation Temperature",
            ["Room Temperature (RT)", "4°C", "37°C", "Custom"],
            key="compound_temp"
        )
    
    # Calculate DNA-Compound complex
    comp_dna_volume = comp_dna_amount / comp_dna_stock
    compound_amount = comp_dna_amount * compound_w_w_ratio
    compound_volume = compound_amount / compound_stock_conc
    comp_dna_complex_volume = comp_dna_volume + compound_volume
    
    with st.expander("📊 DNA-Compound Complex Summary"):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("DNA Volume", f"{comp_dna_volume:.2f} μL")
            st.metric(f"{compound_name} Amount", f"{compound_amount:.2f} μg")
            st.metric(f"{compound_name} Volume", f"{compound_volume:.2f} μL")
        with col_s2:
            st.metric("Total Complex Volume", f"{comp_dna_complex_volume:.2f} μL")
            # Calculate molar ratio
            dna_moles = comp_dna_amount * 1000 / 330  # nmol
            compound_moles = compound_amount * 1000 / compound_mw  # nmol
            molar_ratio = compound_moles / dna_moles if dna_moles > 0 else 0
            st.metric(f"Molar Ratio ({compound_name}:DNA)", f"{molar_ratio:.3f}")
    
    # ========== Step 2: Lipid Formulation ==========
    st.markdown("---")
    st.subheader("📋 Step 2: Lipid Formulation Parameters")
    st.markdown(f"**After DNA-{compound_name} complex formation, add the lipid components. The complex solution acts as the aqueous phase.**")
    
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    with col_l1:
        ion_lipid_mw = st.number_input(
            "Ionizable Lipid MW (Da)",
            min_value=100.0,
            step=1.0,
            value=710.182,
            key="prot_ion_mw",
            help="SM-102 MW = 710.182"
        )
    with col_l2:
        helper_lipid_mw = st.number_input(
            "Helper Lipid MW (Da)",
            min_value=100.0,
            step=1.0,
            value=790.147,
            key="prot_helper_mw",
            help="DSPC MW = 790.147"
        )
    with col_l3:
        chol_mw = st.number_input(
            "Cholesterol MW (Da)",
            min_value=100.0,
            step=1.0,
            value=386.654,
            key="prot_chol_mw"
        )
    with col_l4:
        peg_mw = st.number_input(
            "PEG-DMG2000 MW (Da)",
            min_value=1000.0,
            step=1.0,
            value=2509.2,
            key="prot_peg_mw"
        )
    
    col_l5, col_l6, col_l7, col_l8 = st.columns(4)
    with col_l5:
        ion_stock_conc = st.number_input(
            "Ionizable Lipid Conc (mg/ml)",
            min_value=0.1,
            step=1.0,
            value=40.0,
            key="prot_ion_conc"
        )
    with col_l6:
        helper_stock_conc = st.number_input(
            "Helper Lipid Conc (mg/ml)",
            min_value=0.1,
            step=1.0,
            value=10.0,
            key="prot_helper_conc"
        )
    with col_l7:
        chol_stock_conc = st.number_input(
            "Cholesterol Conc (mg/ml)",
            min_value=0.1,
            step=1.0,
            value=10.0,
            key="prot_chol_conc"
        )
    with col_l8:
        peg_stock_conc = st.number_input(
            "PEG-DMG2000 Conc (mg/ml)",
            min_value=0.1,
            step=1.0,
            value=10.0,
            key="prot_peg_conc"
        )
    
    col_l9, col_l10, col_l11, col_l12 = st.columns(4)
    with col_l9:
        ion_ratio = st.number_input(
            "Ionizable Lipid %",
            min_value=0.0,
            step=1.0,
            value=50.0,
            key="prot_ion_ratio"
        )
    with col_l10:
        helper_ratio = st.number_input(
            "Helper Lipid %",
            min_value=0.0,
            step=1.0,
            value=10.0,
            key="prot_helper_ratio"
        )
    with col_l11:
        chol_ratio = st.number_input(
            "Cholesterol %",
            min_value=0.0,
            step=0.1,
            value=38.5,
            key="prot_chol_ratio"
        )
    with col_l12:
        peg_ratio = st.number_input(
            "PEG-DMG2000 %",
            min_value=0.0,
            step=0.1,
            value=1.5,
            key="prot_peg_ratio"
        )
    
    col_l13, col_l14 = st.columns(2)
    with col_l13:
        aq_eth_ratio = st.number_input(
            "Aqueous to Ethanol Ratio",
            min_value=0.5,
            step=0.1,
            value=3.0,
            key="prot_aq_eth_ratio",
            help="Ratio of aqueous phase (DNA-Protamine complex) to ethanol phase"
        )
    with col_l14:
        final_lnp_volume_target = st.number_input(
            "Target Final LNP Volume (μL)",
            min_value=10.0,
            step=10.0,
            value=200.0,
            key="prot_final_volume",
            help="Desired final LNP volume"
        )
    
    # ========== Calculate Multi-step LNP ==========
    if st.button("🧬 Calculate Multi-step LNP Formulation", key="calc_protamine", use_container_width=True):
        try:
            # Calculate lipid phase volumes
            ethanol_phase_volume = final_lnp_volume_target / (aq_eth_ratio + 1)
            aqueous_phase_volume = final_lnp_volume_target * aq_eth_ratio / (aq_eth_ratio + 1)
            
            # Calculate ionizable lipid amount needed
            ion_lipid_mass_needed = (ethanol_phase_volume * 0.1) / (ion_stock_conc / 1000)  # rough estimate
            
            # More accurate calculation based on ratio
            total_lipid_molar_percent = ion_ratio + helper_ratio + chol_ratio + peg_ratio
            
            if total_lipid_molar_percent != 100:
                st.warning(f"⚠️ Warning: Lipid molar % sum = {total_lipid_molar_percent}% (should be 100%)")
            
            # Simplified calculation: assume target concentration of lipids in ethanol
            # Let's use a standard approach: calculate based on DNA-to-ionizable-lipid ratio
            n_p_ratio = 6  # Standard N/P ratio for Protamine-DNA-LNP
            
            dna_moles = prot_dna_amount * 1000 / 330  # nmol
            ion_lipid_moles = dna_moles / n_p_ratio
            ion_lipid_mass = ion_lipid_moles * ion_lipid_mw / 1000  # μg
            
            # Calculate other lipid amounts based on ratios
            helper_lipid_mass = ion_lipid_mass * helper_ratio / ion_ratio
            chol_mass = ion_lipid_mass * chol_ratio / ion_ratio
            peg_mass = ion_lipid_mass * peg_ratio / ion_ratio
            
            # Calculate volumes
            ion_lipid_vol = ion_lipid_mass / (ion_stock_conc / 1000)
            helper_lipid_vol = helper_lipid_mass / (helper_stock_conc / 1000)
            chol_vol = chol_mass / (chol_stock_conc / 1000)
            peg_vol = peg_mass / (peg_stock_conc / 1000)
            
            # Ethanol volume
            ethanol_vol = ethanol_phase_volume - ion_lipid_vol - helper_lipid_vol - chol_vol - peg_vol
            
            # Aqueous phase components
            citrate_volume = 0.1 * aqueous_phase_volume
            water_volume = aqueous_phase_volume - prot_dna_complex_volume - citrate_volume
            
            # Create results dataframe
            results_data = {
                'Component': [
                    'DNA (in buffer)',
                    f'{compound_name}',
                    'Ionizable Lipid (in EtOH)',
                    'Helper Lipid (in EtOH)',
                    'Cholesterol (in EtOH)',
                    'PEG-DMG2000 (in EtOH)',
                    'Ethanol',
                    'Citrate Buffer',
                    'Water'
                ],
                'Volume (μL)': [
                    comp_dna_volume,
                    compound_volume,
                    ion_lipid_vol,
                    helper_lipid_vol,
                    chol_vol,
                    peg_vol,
                    max(0, ethanol_vol),
                    citrate_volume,
                    max(0, water_volume)
                ],
                'Mass (μg)': [
                    comp_dna_amount,
                    compound_amount,
                    ion_lipid_mass,
                    helper_lipid_mass,
                    chol_mass,
                    peg_mass,
                    '-',
                    '-',
                    '-'
                ]
            }
            
            results_df = pd.DataFrame(results_data)
            st.session_state.compound_results = results_df
            
            # Add to history
            history_record = {
                "Experiment": comp_exp_name if comp_exp_name else "Unnamed",
                "Compound": compound_name,
                "DNA (μg)": comp_dna_amount,
                f"{compound_name}:DNA w/w": f"{compound_w_w_ratio:.2f}:1",
                "Total LNP (μL)": f"{final_lnp_volume_target:.2f}",
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.compound_history.append(history_record)
            
            st.success(f"✅ Multi-step {compound_name}-DNA-LNP formulation calculated!")
            
        except Exception as e:
            st.error(f"❌ Error calculating formulation: {str(e)}")
    
    # ========== Display Results ==========
    if st.session_state.compound_results is not None:
        st.markdown("---")
        st.subheader("📊 Formulation Composition")
        
        tab_comp, tab_protocol = st.tabs(["Composition", "Protocol"])
        
        with tab_comp:
            st.dataframe(st.session_state.compound_results, use_container_width=True)
            
            # Summary metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Total Volume", f"{final_lnp_volume_target:.2f} μL")
            with col_m2:
                st.metric(f"DNA-{compound_name} Complex", f"{comp_dna_complex_volume:.2f} μL")
            with col_m3:
                dna_moles = comp_dna_amount * 1000 / 330
                compound_moles = compound_amount * 1000 / compound_mw
                st.metric(f"Molar Ratio ({compound_name}:DNA)", f"{compound_moles/dna_moles:.3f}")
            with col_m4:
                st.metric("Lipid Phase %", f"{(final_lnp_volume_target - comp_dna_complex_volume) / final_lnp_volume_target * 100:.1f}%")
        
        with tab_protocol:
            st.markdown(f"""
            ### 📋 Experimental Protocol: Multi-step LNP with {compound_name}
            
            **Step 1: Complex Formation**
            """)
            
            step1_text = f"""
1. Prepare DNA solution: {comp_dna_amount:.2f} μg DNA in {comp_dna_buffer}
   - Volume: {comp_dna_volume:.2f} μL (from {comp_dna_stock:.1f} μg/μL stock)

2. Prepare {compound_name} solution: {compound_amount:.2f} μg
   - Volume: {compound_volume:.2f} μL (from {compound_stock_conc:.1f} mg/ml stock)
   - w/w ratio to DNA: {compound_w_w_ratio:.2f}:1

3. Mix DNA and {compound_name} solutions
   - Add {compound_name} to DNA slowly with mixing
   - Total volume: {comp_dna_complex_volume:.2f} μL

4. Incubate at {compound_temp} for {compound_incubation} minutes
   - This allows DNA-{compound_name} complex formation
            """
            st.text(step1_text)
            
            st.markdown("**Step 2: Lipid Mixing (Rapid)**")
            step2_text = f"""
1. Prepare ethanol phase (in one tube):
   - Ionizable Lipid: {results_df[results_df['Component']=='Ionizable Lipid (in EtOH)']['Volume (μL)'].values[0]:.2f} μL
   - Helper Lipid: {results_df[results_df['Component']=='Helper Lipid (in EtOH)']['Volume (μL)'].values[0]:.2f} μL
   - Cholesterol: {results_df[results_df['Component']=='Cholesterol (in EtOH)']['Volume (μL)'].values[0]:.2f} μL
   - PEG-DMG2000: {results_df[results_df['Component']=='PEG-DMG2000 (in EtOH)']['Volume (μL)'].values[0]:.2f} μL
   - Ethanol: {max(0, results_df[results_df['Component']=='Ethanol']['Volume (μL)'].values[0]):.2f} μL

2. Prepare aqueous phase (in another tube):
   - DNA-{compound_name} complex: {comp_dna_complex_volume:.2f} μL
   - Citrate buffer: {results_df[results_df['Component']=='Citrate Buffer']['Volume (μL)'].values[0]:.2f} μL
   - Water: {max(0, results_df[results_df['Component']=='Water']['Volume (μL)'].values[0]):.2f} μL

3. Mix ethanol phase into aqueous phase rapidly (1:3 or 3:1 flow rate)
   - Use syringe or microfluidic mixer for better control
   - Mix for 10-30 seconds

4. Optional dialysis or buffer exchange
   - Remove ethanol over 2-4 hours
   - Replace buffer with desired storage buffer
            """
            st.text(step2_text)
            
            st.markdown("**Step 3: Characterization (Optional)**")
            st.markdown(f"""
- **Size (DLS):** Measure average diameter and polydispersity
- **Zeta Potential:** Expected to be affected by {compound_name} charge
- **Encapsulation Efficiency:** Measure free vs. encapsulated DNA
- **Stability:** Test at 4°C and room temperature
            """)
        
        # Download options
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            csv_data = st.session_state.compound_results.to_csv(index=False)
            st.download_button(
                "📥 Download Formulation (CSV)",
                csv_data,
                file_name=f"{compound_name.lower()}_lnp_{comp_exp_name or 'formulation'}.csv",
                mime="text/csv",
                key="download_compound"
            )
        with col_d2:
            if st.button("🗑️ Clear Results", key="clear_compound"):
                st.session_state.compound_results = None
                st.rerun()
    
    # ========== History ==========
    if len(st.session_state.compound_history) > 0:
        st.markdown("---")
        st.subheader("📋 Formulation History")
        history_df = pd.DataFrame(st.session_state.compound_history)
        st.dataframe(history_df, use_container_width=True)
        
        if st.button("🗑️ Clear History", key="clear_comp_history"):
            st.session_state.compound_history = []
            st.rerun()
    
    # ========== Best Practices ==========
    with st.expander(f"💡 Best Practices for {compound_name}-DNA-Lipid LNPs"):
        st.markdown(f"""
        ### Advantages of {compound_name}-DNA-LNP:
        - **DNA interaction:** {compound_name} interacts with and modifies DNA structure
        - **Cellular uptake:** {compound_name} may improve cellular uptake properties
        - **Improved formulation:** Pre-complexation may enhance complex stability
        - **Tunable properties:** Adjust w/w ratio to optimize performance
        
        ### Key Optimization Parameters:
        
        **1. Compound:DNA Ratio (w/w)**
        - Typical range: 0.5:1 to 10:1 (depends on compound type and MW)
        - Lower ratios: Minimal structural changes to DNA
        - Higher ratios: Greater modification of DNA properties
        - Start with 1:1 and adjust based on experimental results
        
        **2. Incubation Time**
        - Minimum: 5 minutes (complex formation)
        - Standard: 10-15 minutes (complete complexation)
        - Can extend to 30+ minutes depending on compound-DNA interaction
        
        **3. Buffer Conditions**
        - Use appropriate pH for your compound (usually physiological: 6.5-8.0)
        - Match ionic strength to prevent aggregation
        - Consider compound solubility (aqueous vs. organic solvents)
        
        **4. Mixing Ratios**
        - Keep aqueous:ethanol ratio at 3:1 (or optimize for your compound)
        - Rapid mixing essential for LNP formation
        - Consider solvent compatibility between compound and lipids
        
        **5. Troubleshooting**
        - **Large particles:** Adjust compound:DNA ratio or incubation time
        - **Low encapsulation:** Optimize pH, buffer, or incubation conditions
        - **Aggregation:** Adjust concentration or ionic strength
        - **Poor transfection:** Optimize lipid composition or compound ratio
        
        ### Quality Control:
        - Size: 50-300 nm (depends on compound and formulation)
        - PDI: < 0.3 (monodisperse preferred)
        - Zeta potential: Varies by compound (adjust for charge)
        - Encapsulation: > 70-80% for optimal delivery
        
        ### Compound-Specific Considerations:
        - **Peptides/Proteins:** May require specific pH and ionic strength
        - **Polymers:** Consider chain length effects on DNA binding
        - **Small molecules:** May require higher concentrations for effects
        - **Charged compounds:** Will affect final LNP charge and biodistribution
        """)

# ============================================================================
# TAB 4: NLS PEPTIDE OPTIMIZATION FOR pDNA DELIVERY
# ============================================================================

with tab4:
    st.header("🔬 NLS Peptide Strategy for pDNA Nuclear Delivery")
    st.info("💡 Design optimized NLS (Nuclear Localization Signal) peptide strategies to enhance pDNA delivery into the nucleus. NLS peptides overcome the nuclear pore barrier, significantly improving gene expression efficiency.")
    
    # Initialize session state
    if "nls_results" not in st.session_state:
        st.session_state.nls_results = None
    if "nls_history" not in st.session_state:
        st.session_state.nls_history = []
    
    # ========== How NLS Works ==========
    with st.expander("📚 How NLS Peptides Enhance pDNA Delivery", expanded=False):
        st.markdown("""
        ### 🎯 Key Mechanisms
        
        **1. Signal Recognition**
        - NLS peptides mimic natural nuclear import signals
        - Bind to importin proteins (importin-α/β complex)
        - Direct the delivery system toward the nucleus
        
        **2. Nuclear Transport**
        - The importin complex carries the NLS-pDNA cargo through the nuclear pore complex (NPC)
        - Bypasses the ~125 nm size limit of the NPC
        - Critical advantage for non-viral gene delivery
        
        **3. Gene Expression**
        - Overcomes the major barrier preventing nuclear access
        - Enables efficient transcription of pDNA in the nucleus
        - Dramatically improves transfection efficiency
        
        ### 🔄 Delivery Strategies
        
        **Conjugation Approaches:**
        - Direct NLS attachment to pDNA via chemical linkage
        - NLS conjugation to delivery vehicles (LNPs, liposomes, nanoparticles)
        - Cell-penetrating peptides (CPPs) combined with NLS
        
        **Fusion Protein Strategy:**
        - Create chimeric proteins combining NLS + DNA-binding domains
        - Form nanocomplexes with pDNA
        - Enhanced nuclear uptake and protection
        
        **Bipartite NLS:**
        - Two-part NLS sequences (e.g., Ku70(2)-NLS)
        - Potentially higher efficiency than monopartite NLS
        - Improved binding to importin-α
        """)
    
    # ========== NLS Sequences Database ==========
    st.subheader("📋 Step 1: Select or Define NLS Sequence")
    
    # Define NLS sequences
    nls_database = {
        "SV40 Monopartite": {
            "sequence": "PKKKRKV",
            "type": "Monopartite",
            "pattern": "Pro-Lys-Lys-Lys-Arg-Lys-Val",
            "origin": "SV40 T-antigen",
            "efficiency": "High",
            "mw": 945.19,
            "notes": "Classic, well-characterized monopartite NLS"
        },
        "c-myc Monopartite": {
            "sequence": "PAAKRVKLD",
            "type": "Monopartite",
            "pattern": "Pro-Ala-Ala-Lys-Arg-Val-Lys-Leu-Asp",
            "origin": "c-myc protein",
            "efficiency": "High",
            "mw": 1041.27,
            "notes": "Strong monopartite signal"
        },
        "Nucleoplasmin Bipartite": {
            "sequence": "KRXR(5)LQFXKRX",
            "type": "Bipartite",
            "pattern": "Lys-Arg-X(5)-Leu-Gln-Phe-X-Lys-Arg-X",
            "origin": "Nucleoplasmin",
            "efficiency": "High",
            "mw": 1308.53,
            "notes": "Bipartite pattern with spacer region"
        },
        "Ku70 Bipartite": {
            "sequence": "KRXR(6)LXXKR",
            "type": "Bipartite",
            "pattern": "Lys-Arg-X(6)-Leu-X(2)-Lys-Arg",
            "origin": "Ku70 protein",
            "efficiency": "Very High",
            "mw": 1445.78,
            "notes": "Enhanced efficiency, Ku70(2)-NLS"
        },
        "Influenza NP Bipartite": {
            "sequence": "KRTEDMLKRKR",
            "type": "Bipartite",
            "pattern": "Lys-Arg-Thr-Glu-Asp-Met-Leu-Lys-Arg-Lys-Arg",
            "origin": "Influenza nucleoprotein",
            "efficiency": "High",
            "mw": 1457.75,
            "notes": "Natural bipartite NLS"
        },
        "Histone H2B": {
            "sequence": "KRSR",
            "type": "Monopartite",
            "pattern": "Lys-Arg-Ser-Arg",
            "origin": "Histone H2B",
            "efficiency": "Medium",
            "mw": 575.36,
            "notes": "Minimal NLS sequence"
        },
        "Synthetic Optimal": {
            "sequence": "KKKRKV",
            "type": "Monopartite",
            "pattern": "Lys-Lys-Lys-Arg-Lys-Val",
            "origin": "Synthetic",
            "efficiency": "High",
            "mw": 863.15,
            "notes": "Optimized synthetic variant"
        },
        "Custom": {
            "sequence": "CUSTOM",
            "type": "Custom",
            "pattern": "User defined",
            "origin": "User input",
            "efficiency": "Variable",
            "mw": 0,
            "notes": "Enter your own NLS sequence"
        }
    }
    
    col_nls1, col_nls2 = st.columns([2, 1])
    with col_nls1:
        nls_select = st.selectbox(
            "Select NLS Sequence",
            list(nls_database.keys()),
            key="nls_select",
            help="Choose from well-characterized NLS sequences or define custom"
        )
    
    # Display NLS information
    if nls_select in nls_database:
        nls_data = nls_database[nls_select]
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Sequence", nls_data["sequence"])
            st.metric("Type", nls_data["type"])
        with col_info2:
            st.metric("Efficiency", nls_data["efficiency"])
            st.caption(f"📝 {nls_data['notes']}")
    
    # If custom, allow user input
    if nls_select == "Custom":
        custom_nls_seq = st.text_input(
            "Enter Custom NLS Sequence",
            value="KKKRKV",
            placeholder="e.g., KKKRKV (single letter amino acid code)",
            key="custom_nls_seq",
            help="Use single letter amino acid codes"
        )
        custom_nls_mw = st.number_input(
            "NLS Molecular Weight (Da)",
            min_value=100.0,
            step=50.0,
            value=863.15,
            key="custom_nls_mw"
        )
    else:
        custom_nls_seq = nls_data["sequence"]
        custom_nls_mw = nls_data["mw"]
    
    # ========== pDNA and Delivery System Parameters ==========
    st.markdown("---")
    st.subheader("📋 Step 2: pDNA and NLS-Delivery System Design")
    
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        pdna_size_kb = st.number_input(
            "pDNA Size (kb)",
            min_value=1,
            step=1,
            value=5,
            key="pdna_size",
            help="Plasmid DNA size in kilobases"
        )
    with col_d2:
        pdna_amount = st.number_input(
            "pDNA Amount (μg)",
            min_value=0.1,
            step=0.5,
            value=10.0,
            key="pdna_amount_nls"
        )
    with col_d3:
        nls_copies_per_pdna = st.number_input(
            "NLS Copies per pDNA",
            min_value=1,
            step=1,
            value=5,
            key="nls_copies",
            help="Number of NLS sequences attached to each pDNA molecule"
        )
    with col_d4:
        delivery_system = st.selectbox(
            "Delivery System",
            ["LNP", "Liposome", "Nanoparticle", "Polymer Complex", "Protein Complex"],
            key="delivery_system",
            help="Choose the delivery vehicle for NLS-pDNA"
        )
    
    col_d5, col_d6, col_d7 = st.columns(3)
    with col_d5:
        nls_attachment_method = st.selectbox(
            "NLS Attachment Method",
            ["Chemical Conjugation", "Fusion Protein", "Electrostatic Complex", "Covalent Linker"],
            key="nls_attachment"
        )
    with col_d6:
        importin_binding_efficiency = st.slider(
            "Expected Importin Binding Efficiency (%)",
            min_value=10,
            max_value=100,
            value=80,
            step=5,
            key="importin_efficiency",
            help="Estimated % of NLS-pDNA complex recognized by importin proteins"
        )
    with col_d7:
        nuclear_penetration_efficiency = st.slider(
            "Nuclear Pore Penetration Rate (%)",
            min_value=10,
            max_value=100,
            value=70,
            step=5,
            key="npc_penetration",
            help="Estimated % of importin-bound complex successfully crossing NPC"
        )
    
    # ========== Calculate NLS-Delivery Parameters ==========
    st.markdown("---")
    st.subheader("📊 Step 3: Optimization & Analysis")
    
    if st.button("🧪 Calculate NLS-pDNA Delivery Parameters", key="calc_nls", use_container_width=True):
        try:
            # Calculate key parameters
            pdna_mw = pdna_size_kb * 1000 * 330  # approx MW in Da (330 Da per bp)
            total_nls_per_sample = nls_copies_per_pdna * pdna_amount / pdna_mw * 1e9  # rough estimate
            
            # Calculate efficiency metrics
            importin_bound = (pdna_amount * importin_binding_efficiency) / 100
            nuclear_entry = (importin_bound * nuclear_penetration_efficiency) / 100
            overall_efficiency = (importin_binding_efficiency * nuclear_penetration_efficiency) / 10000
            
            # Create results
            results_dict = {
                "Parameter": [
                    "pDNA Size",
                    "pDNA Amount",
                    "pDNA Molecular Weight (approx)",
                    "NLS Sequence",
                    "NLS Type",
                    "NLS Copies per pDNA",
                    "Delivery System",
                    "Attachment Method",
                    "Importin Recognition (%)",
                    "Nuclear Pore Crossing (%)",
                    "Overall Nuclear Delivery Efficiency (%)",
                    "Expected Nuclear Entry (μg)"
                ],
                "Value": [
                    f"{pdna_size_kb} kb",
                    f"{pdna_amount:.2f} μg",
                    f"{pdna_mw:.0f} Da",
                    custom_nls_seq,
                    nls_data["type"] if nls_select != "Custom" else "Custom",
                    f"{nls_copies_per_pdna} copies",
                    delivery_system,
                    nls_attachment_method,
                    f"{importin_binding_efficiency}%",
                    f"{nuclear_penetration_efficiency}%",
                    f"{overall_efficiency:.1f}%",
                    f"{nuclear_entry:.2f} μg"
                ]
            }
            
            results_df = pd.DataFrame(results_dict)
            st.session_state.nls_results = results_df
            
            # Add to history
            history_record = {
                "NLS": nls_select,
                "Sequence": custom_nls_seq,
                "pDNA (kb)": pdna_size_kb,
                "pDNA (μg)": f"{pdna_amount:.2f}",
                "Delivery System": delivery_system,
                "Overall Efficiency (%)": f"{overall_efficiency:.1f}%",
                "Nuclear Entry (μg)": f"{nuclear_entry:.2f}",
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.nls_history.append(history_record)
            
            st.success(f"✅ NLS optimization for {delivery_system} delivery calculated!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # ========== Display Results ==========
    if st.session_state.nls_results is not None:
        st.markdown("---")
        st.subheader("📊 NLS-pDNA Delivery Profile")
        
        # Results table
        st.dataframe(st.session_state.nls_results, use_container_width=True)
        
        # Key metrics visualization
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)
        with col_v1:
            st.metric("Overall Efficiency", f"{overall_efficiency:.1f}%")
        with col_v2:
            st.metric("Expected Nuclear Entry", f"{nuclear_entry:.2f} μg")
        with col_v3:
            st.metric("Importin Recognition", f"{importin_binding_efficiency}%")
        with col_v4:
            st.metric("NPC Crossing Rate", f"{nuclear_penetration_efficiency}%")
        
        # Optimization recommendations
        st.markdown("---")
        st.subheader("💡 Optimization Recommendations")
        
        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            st.markdown("**Factors to Enhance Nuclear Delivery:**")
            st.markdown(f"""
            - **Current Overall Efficiency: {overall_efficiency:.1f}%**
            
            1. **Increase NLS Copies**: Currently {nls_copies_per_pdna} copies
               - Recommend: Try 8-12 copies per pDNA
               - Effect: More importin binding sites
            
            2. **Optimize Attachment Method**:
               - Current: {nls_attachment_method}
               - Best for efficiency: Bipartite NLS + Fusion Protein
            
            3. **Choose Bipartite NLS**:
               - Current type: {nls_data.get('type', 'Custom')}
               - Recommended: Ku70 or Nucleoplasmin bipartite
               - Benefit: 10-20% higher efficiency
            """)
        
        with col_rec2:
            st.markdown("**System-Specific Strategies:**")
            if delivery_system == "LNP":
                st.markdown("""
                - Add helper lipids with positive charge
                - Incorporate ionizable lipids for buffering
                - Consider D-lin-MC3-DMA or SM-102 variants
                - Target NPC proteins via surface modification
                """)
            elif delivery_system == "Liposome":
                st.markdown("""
                - Use cationic lipids for NLS charge neutralization
                - Optimize liposome:pDNA w/w ratio
                - Consider fusogenic liposomes
                - Add nuclear localization enhancers
                """)
            elif delivery_system == "Polymer Complex":
                st.markdown("""
                - Use low MW PEI (1-10 kDa) for reduced toxicity
                - Combine with protamine for condensation
                - Add CPPs (TAT peptide) for cell penetration
                - Consider multi-functional polymers
                """)
            else:
                st.markdown("""
                - Optimize protein-DNA binding stoichiometry
                - Use pH-responsive fusion proteins
                - Consider enzymatically cleavable linkers
                - Validate importin-α specificity
                """)
        
        # Download options
        st.markdown("---")
        col_down1, col_down2 = st.columns(2)
        with col_down1:
            csv_data = st.session_state.nls_results.to_csv(index=False)
            st.download_button(
                "📥 Download Results (CSV)",
                csv_data,
                file_name=f"nls_optimization_{nls_select}.csv",
                mime="text/csv",
                key="download_nls"
            )
        with col_down2:
            if st.button("🗑️ Clear Results", key="clear_nls"):
                st.session_state.nls_results = None
                st.rerun()
    
    # ========== History ==========
    if len(st.session_state.nls_history) > 0:
        st.markdown("---")
        st.subheader("📋 Optimization History")
        history_df = pd.DataFrame(st.session_state.nls_history)
        st.dataframe(history_df, use_container_width=True)
        
        if st.button("🗑️ Clear History", key="clear_nls_history"):
            st.session_state.nls_history = []
            st.rerun()
    
    # ========== Best Practices & Strategies ==========
    with st.expander("🎯 NLS Peptide Engineering Best Practices", expanded=False):
        st.markdown("""
        ### 🔬 Selection Criteria for NLS Sequences
        
        **Monopartite NLS (Classic, Compact):**
        - Best for: Limited space, direct peptide conjugation
        - Examples: SV40, c-myc
        - Advantages: Simple, small (4-8 aa)
        - Disadvantages: May have lower efficiency than bipartite
        
        **Bipartite NLS (Enhanced, Natural):**
        - Best for: Maximum efficiency, complex assemblies
        - Examples: Nucleoplasmin, Ku70
        - Advantages: Higher importin-α binding affinity
        - Disadvantages: Larger, may interfere with DNA binding
        
        ### 🧪 Conjugation Strategies
        
        **1. Chemical Conjugation (Direct Attachment)**
        - Lysine-based cross-linking (EDC/NHS)
        - Thiol-based coupling (maleimide)
        - Photochemical cross-linking
        - **Pros**: Simple, direct control
        - **Cons**: May damage DNA or reduce binding
        
        **2. Fusion Protein Approach**
        - NLS + DNA-binding domain (DBD)
        - Expression as recombinant protein
        - Natural amino acid linkers
        - **Pros**: Better preserved activity, natural structure
        - **Cons**: More complex production, higher cost
        
        **3. Cell-Penetrating Peptide (CPP) + NLS**
        - TAT peptide + NLS sequences
        - Hybrid peptides combining CPP and NLS
        - Enables both cell entry and nuclear targeting
        - **Pros**: Dual function, synergistic effect
        - **Cons**: Larger molecular size
        
        **4. Multi-valent Presentation**
        - Dendrimers with multiple NLS copies
        - Scaffold proteins with NLS display
        - Nanoparticle-displayed NLS
        - **Pros**: Increased binding capacity
        - **Cons**: Size and complexity concerns
        
        ### 📊 Optimization Parameters
        
        **Number of NLS Copies:**
        - 1-3 copies: Basic targeting
        - 4-6 copies: Standard formulation
        - 7-12 copies: Enhanced efficiency
        - >12 copies: Risk of steric hindrance
        
        **Spacing/Linker Design:**
        - Flexible linkers (Gly/Ser-rich): Better accessibility
        - Rigid linkers: Better structural control
        - Cleavable linkers: Intracellular activation
        
        **Integration with Delivery Systems:**
        - LNPs: Surface display or internal modification
        - Liposomes: Cationic lipids for NLS neutralization
        - Polymers: NLS incorporation during synthesis
        - Proteins: Genetic fusion or chemical modification
        
        ### ✅ Quality Control & Validation
        
        1. **Sequence Verification**: Confirm NLS sequence by mass spec or sequencing
        2. **Importin Binding**: ELISA or SPR to verify importin-α recognition
        3. **Nuclear Localization**: Fluorescence microscopy with labeled NLS-pDNA
        4. **Transcription Activity**: RT-qPCR to measure gene expression
        5. **Cytotoxicity**: Cell viability assays for different concentrations
        
        ### 🎓 Key Considerations
        
        - **Bipartite NLS typically shows 2-10x better efficiency** than monopartite
        - **Multiple NLS copies improve targeting** but may reduce pDNA protection
        - **Attachment method significantly impacts delivery** (fusion proteins often outperform conjugation)
        - **System-specific optimization is crucial** (what works for LNPs may not work for polymers)
        - **Nuclear entry is only one barrier** - also optimize cell penetration and endosomal escape
        """)



