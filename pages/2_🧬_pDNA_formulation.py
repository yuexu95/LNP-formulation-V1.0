
import streamlit as st
import pandas as pd
import textwrap


# Set the layout to wide
st.set_page_config(layout="wide")
st. title ("pDNA LNP formulation calculator")

def calculate_np_ratio(dna_mass_ug, ionizable_lipid_moles, amines_per_molecule=1.0):
    """
    Calculates the N/P ratio for pDNA formulation.
    
    Parameters:
    - dna_mass_ug: Mass of DNA in micrograms
    - ionizable_lipid_moles: Moles of ionizable lipid (μmol)
    - amines_per_molecule: Number of ionizable tertiary amine groups per lipid molecule (default=1.0)
    
    Returns:
    - N/P ratio: Molar ratio of amine groups (N) to phosphate groups (P)
    
    Notes:
    - For double-stranded DNA (dsDNA): average MW per base pair ≈ 660 g/mol
    - Each base pair contributes 2 phosphate groups (one per strand)
    - Therefore: P (μmol) = DNA mass (μg) / 330
    """
    # Convert DNA mass from μg to g, then calculate moles of phosphate groups
    dna_mass_g = dna_mass_ug * 1e-6
    phosphate_moles_mol = dna_mass_g / 330.0  # moles in mol (dsDNA: 2 phosphates per bp, MW ~660/bp)
    phosphate_moles_umol = phosphate_moles_mol * 1e6  # convert to μmol
    
    # Calculate moles of tertiary amine groups (N)
    amine_moles_umol = ionizable_lipid_moles * amines_per_molecule
    
    # Calculate N/P ratio
    if phosphate_moles_umol > 0:
        np_ratio = amine_moles_umol / phosphate_moles_umol
    else:
        np_ratio = 0
    
    return np_ratio, amine_moles_umol, phosphate_moles_umol

def make_lnp_formulation(dna_scale, dna_stock_concentration, ionizable_lipid_to_dna_ratio, aqueous_to_ethanol_ratio, ionizable_lipid_mw, helper_lipid_mw, cholesterol_mw, pegdmg2000_mw, ionizable_lipid_concentration, helper_lipid_concentration, cholesterol_concentration, pegdmg2000_concentration, ionizable_lipid_ratio, helper_lipid_ratio, cholesterol_ratio, pegdmg2000_ratio):
    """
    Calculates the composition and prepares a pDNA LNP formulation.

    Returns:
    A DataFrame containing the calculated values for the LNP composition and preparation.
    """ 
    # Calculate moles of ionizable lipid using the correct formula
    ionizable_lipid_moles = (dna_scale * ionizable_lipid_to_dna_ratio) / ionizable_lipid_mw
    
    # Calculate moles of each lipid based on their molar ratios
    helper_lipid_moles = ionizable_lipid_moles * helper_lipid_ratio / ionizable_lipid_ratio
    cholesterol_moles = ionizable_lipid_moles * cholesterol_ratio / ionizable_lipid_ratio
    pegdmg2000_moles = ionizable_lipid_moles * pegdmg2000_ratio / ionizable_lipid_ratio

    # Calculate mass of each lipid
    ionizable_lipid_mass = ionizable_lipid_moles * ionizable_lipid_mw
    helper_lipid_mass = helper_lipid_moles * helper_lipid_mw
    cholesterol_mass = cholesterol_moles * cholesterol_mw
    pegdmg2000_mass = pegdmg2000_moles * pegdmg2000_mw

    # Calculate final LNP volume
    final_lnp_volume = dna_scale / 0.1
    
    # Calculate ethanol phase volume
    ionizable_lipid_volume = ionizable_lipid_mass / ionizable_lipid_concentration
    helper_lipid_volume = helper_lipid_mass / helper_lipid_concentration
    cholesterol_volume = cholesterol_mass / cholesterol_concentration
    pegdmg2000_volume = pegdmg2000_mass / pegdmg2000_concentration
    ethanol = final_lnp_volume / (aqueous_to_ethanol_ratio + 1) - ionizable_lipid_volume - helper_lipid_volume - cholesterol_volume - pegdmg2000_volume
    ethanol_phase_volume = ionizable_lipid_volume + helper_lipid_volume + cholesterol_volume + pegdmg2000_volume + ethanol

    # Calculate aqueous phase volume
    aqueous_phase_volume = final_lnp_volume * (aqueous_to_ethanol_ratio / (aqueous_to_ethanol_ratio + 1))
    dna_volume = dna_scale / dna_stock_concentration
    citrate_volume = 0.1 * aqueous_phase_volume
    water_volume = aqueous_phase_volume - dna_volume - citrate_volume

    # Create DataFrame for the results
    data = {
        'Component': ['Ionizable Lipid', 'Helper Lipid', 'Cholesterol', 'PEG-DMG2000', 'Ethanol', 'DNA', 'Citrate', 'Water'],
        'Volume (μL)': [ionizable_lipid_volume, helper_lipid_volume, cholesterol_volume, pegdmg2000_volume, ethanol, dna_volume, citrate_volume, water_volume]
    }

    df = pd.DataFrame(data)
    
    volumes = {
        "Ionizable Lipid": ionizable_lipid_volume,
        "helper_lipid_volume": helper_lipid_volume,
        "cholesterol_volume": cholesterol_volume,
        "pegdmg2000_volume": pegdmg2000_volume,
        "ethanol": ethanol,
        "ethanol_phase_volume": ethanol_phase_volume,
        "dna_volume": dna_volume,
        "citrate_volume": citrate_volume,
        "water_volume": water_volume,
        "aqueous_volume": aqueous_phase_volume,
        "ionizable_lipid_moles": ionizable_lipid_moles
    }

    return df, volumes

def prepare_bulk_lnp_volumes(volumes, times):
    """
    Prepares the volumes for any times the LNP with extra.

    Returns:
    A DataFrame containing the bulk volumes.
    """
    bulk_volumes = {
        "Component": ['Ionizable Lipid', "Helper Lipid", "Cholesterol", "PEG-DMG2000", "Ethanol", "DNA", "Citrate", "Water"],
        "Volume (μL)": [
            volumes["Ionizable Lipid"] * times * 1.5,
            volumes["helper_lipid_volume"] * times * 1.5,
            volumes["cholesterol_volume"] * times * 1.5,
            volumes["pegdmg2000_volume"] * times * 1.5,
            volumes["ethanol"] * times * 1.5,
            volumes["dna_volume"] * times * 1.2,
            volumes["citrate_volume"] * times * 1.2,
            volumes["water_volume"] * times * 1.2,
        ]
    } 
    bulk_df = pd.DataFrame(bulk_volumes)
    return bulk_df

def main():

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dna_scale = st.number_input("DNA Scale (μg)", min_value=0.0, step=1.0, value=3.0)
    with col2:
        dna_stock_concentration = st.number_input("DNA Stock (μg/μL)", min_value=0.0, step=0.1, value=1.0)
    with col3:
        ionizable_lipid_to_dna_ratio = st.number_input("Ionizable Lipid to DNA Ratio", min_value=0.0, max_value=100.0, step=0.1, value=10.0)
    with col4:
        aqueous_to_ethanol_ratio = st.number_input("Aqueous to Ethanol Ratio", min_value=0.0, step=0.1, value=3.0)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        ionizable_lipid_mw = st.number_input("Ionizable Lipid Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=710.182)
    with col6:
        helper_lipid_mw = st.number_input("Helper Lipid Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=790.147)
    with col7:
        cholesterol_mw = st.number_input("Cholesterol Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=386.654)
    with col8:
        pegdmg2000_mw = st.number_input("PEG-DMG2000 Molecular Weight (μg/μmol)", min_value=0.0, step=1.0, value=2509.2)

    col9, col10, col11, col12 = st.columns(4)
    with col9:
        ionizable_lipid_concentration = st.number_input("Ionizable Lipid Concentration (μg/μL)", min_value=0.0, step=1.0, value=20.0)
    with col10:
        helper_lipid_concentration = st.number_input("Helper Lipid Concentration (μg/μL)", min_value=0.0, step=1.0, value=5.0)
    with col11:
        cholesterol_concentration = st.number_input("Cholesterol Concentration (μg/μL)", min_value=0.0, step=1.0, value=10.0)
    with col12:
        pegdmg2000_concentration = st.number_input("PEG-DMG2000 Concentration (μg/μL)", min_value=0.0, step=1.0, value=2.0)
    
    col13, col14, col15, col16 = st.columns(4)
    with col13:
        ionizable_lipid_ratio = st.number_input("Ionizable Lipid Molar Ratio (%)", min_value=0.0, step=1.0, value=50.0)
    with col14:
        helper_lipid_ratio = st.number_input("Helper Lipid Molar Ratio (%)", min_value=0.0, step=1.0, value=10.0)
    with col15:
        cholesterol_ratio = st.number_input("Cholesterol Molar Ratio (%)", min_value=0.0, step=0.5, value=38.5)
    with col16:
        pegdmg2000_ratio = st.number_input("PEG-DMG2000 Molar Ratio (%)", min_value=0.0, step=0.1, value=1.5)
    
    col17, col18 = st. columns(2)
    with col17:
        bulk_times = st.number_input("Bulk Preparation Times", min_value=1, step=1, value=1)
    with col18:
        amines_per_molecule = st.number_input("Amines per Ionizable Lipid Molecule", min_value=0.0, step=0.1, value=1.0, help="Number of ionizable amine groups per lipid molecule for N/P calculation")
    
    formulation_name = st.text_input("Formulation Name (for record keeping)", value="", placeholder="Enter a name for this formulation")
    
    if "result_df" not in st.session_state:
        st.session_state.result_df = None
        st.session_state.volumes = None
        st.session_state.checkboxes_col2 = {}
        st.session_state.checkboxes_col4 = {}
    
    if "history_records" not in st.session_state:
        st.session_state.history_records = []

    if st.button("Calculate"):
        result_df, volumes = make_lnp_formulation(
            dna_scale, dna_stock_concentration, ionizable_lipid_to_dna_ratio, aqueous_to_ethanol_ratio,
            ionizable_lipid_mw, helper_lipid_mw, cholesterol_mw, pegdmg2000_mw, ionizable_lipid_concentration,
            helper_lipid_concentration, cholesterol_concentration, pegdmg2000_concentration, ionizable_lipid_ratio,
            helper_lipid_ratio, cholesterol_ratio, pegdmg2000_ratio
        )
        st.session_state.result_df = result_df
        st.session_state.volumes = volumes
        # 初始化复选框状态
        st.session_state.checkboxes_col2 = {index: False for index in result_df.index}
        st.session_state.checkboxes_col4 = {index: False for index in result_df.index}
        
        # Calculate N/P ratio
        np_ratio, n_moles, p_moles = calculate_np_ratio(
            dna_scale, 
            volumes["ionizable_lipid_moles"],
            amines_per_molecule
        )
        
        # Save to history
        record = {
            "Formulation Name": formulation_name if formulation_name else "Unnamed",
            "Ionizable Lipid (μL)": f"{volumes['Ionizable Lipid']:.2f}",
            "Helper Lipid (μL)": f"{volumes['helper_lipid_volume']:.2f}",
            "Cholesterol (μL)": f"{volumes['cholesterol_volume']:.2f}",
            "PEG-DMG2000 (μL)": f"{volumes['pegdmg2000_volume']:.2f}",
            "Ethanol (μL)": f"{volumes['ethanol']:.2f}",
            "DNA (μL)": f"{volumes['dna_volume']:.2f}",
            "Citrate (μL)": f"{volumes['citrate_volume']:.2f}",
            "Water (μL)": f"{volumes['water_volume']:.2f}",
            "N/P Ratio": f"{np_ratio:.3f}",
        }
        st.session_state.history_records.append(record)
        st.success(f"✅ Formulation '{record['Formulation Name']}' saved!")

    # Display formulation history (moved to top)
    if len(st.session_state.history_records) > 0:
        st.header('Formulation History', divider='rainbow')
        history_df = pd.DataFrame(st.session_state.history_records)
        st.dataframe(history_df, use_container_width=True)
        
        # Add CSV export button and clear history option
        col_download, col_clear = st.columns(2)
        with col_download:
            csv_data = history_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="formulation_history.csv",
                mime="text/csv"
            )
        with col_clear:
            if st.button("🗑️ Clear History"):
                st.session_state.history_records = []
                st.rerun()

    if st.session_state.result_df is not None:
        # Calculate and display N/P ratio
        np_ratio, n_moles, p_moles = calculate_np_ratio(
            dna_scale, 
            st.session_state.volumes["ionizable_lipid_moles"],
            amines_per_molecule
        )
        
        st.header('N/P Ratio Analysis', divider='rainbow')
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("N/P Ratio", f"{np_ratio:.3f}")
        with metric_col2:
            st.metric("N (tertiary amine groups, μmol)", f"{n_moles:.4f}")
        with metric_col3:
            st.metric("P (phosphate groups, μmol)", f"{p_moles:.4f}")
        
        st.caption(f"📌 N/P ratio represents the molar ratio of cationic tertiary amine groups to anionic phosphate groups. For dsDNA: P = DNA mass (μg) / 330")

if __name__ == "__main__":
    main()
