import streamlit as st
import math

st.set_page_config(page_title="N/P Ratio", page_icon="💡", layout="wide")

st.title("N/P Ratio: What it is and how to calculate it")

# Try to display the figure if present in common locations
try:
	import os
	possible_paths = [
		os.path.join(os.getcwd(), "N_P_Ratio.png"),
		os.path.join(os.getcwd(), "Data", "N_P_Ratio.png"),
		os.path.join(os.path.dirname(__file__), "N_P_Ratio.png"),
	]
	img_path = next((p for p in possible_paths if os.path.exists(p)), None)
	if img_path:
		col1, col2, col3 = st.columns([1, 2, 1])
		with col2:
			st.image(img_path, caption="N/P Ratio schematic", use_container_width=True)
except Exception:
	pass

st.markdown(
	"""
	The N/P ratio is the molar ratio of cationic nitrogen groups (N) from your
	transfection reagent or ionizable lipid to the anionic phosphate groups (P) on
	nucleic acids (DNA/RNA). It quantifies charge balance and is commonly used
	to tune complexation and formulation.
	"""
)

st.markdown("## Basic Formula")
st.latex(r"\text{N/P} = \frac{\text{mol N}}{\text{mol P}}")
st.markdown("""
Where:
- **mol N** is the number of moles of protonatable nitrogen from the reagent in the transfection mixture
- **mol P** is the number of moles of anionic phosphate from the nucleic acid in the transfection mixture
""")

st.markdown("## Calculating mol P")
st.latex(r"\text{mol P} \approx 3 \times 10^{-9} \text{ mol/µg} \times \text{mass of nucleic acid (µg)}")
st.markdown("""
(This relationship derives from the average molecular weight of a nucleic acid being ~330 g/mol per base, 
with 1 mole of P per 1 mole of base.)

For double-stranded DNA (dsDNA):
""")
st.latex(r"\text{mol P} \approx \frac{\text{DNA mass (µg)} \times 10^{-6}}{330 \text{ g/mol}}")
st.markdown("""
- Average mass per base pair ≈ 660 g/mol
- Each base pair contributes 2 phosphate groups (one per strand)
""")

st.markdown("## Calculating mol N")
st.markdown("""
Ascertaining the amount of **mol N** requires knowledge of the molecular weight 
and chemical structure of your transfection reagent. You will need:

1. **Molecular weight of your transfection reagent** (µg / mol transfection reagent)
2. **Number of moles of protonatable nitrogen per mole of transfection reagent** (mol N / mol transfection reagent)

With this information:
""")
st.latex(r"\text{mol N} = \frac{\text{mass of transfection reagent (µg)}}{\text{molecular weight (µg/mol)}} \times \frac{\text{mol N}}{\text{mol transfection reagent}}")

st.divider()
st.header("Quick Calculator")

with st.form("np_calc"):
	st.subheader("Inputs")
	col1, col2 = st.columns(2)
	with col1:
		dna_mass_default = 10.0
		dna_mass_ug = st.number_input(
			"DNA mass (µg)", value=dna_mass_default, min_value=0.0, step=0.5, help="Mass of dsDNA used in the mixture."
		)
		ds_dna = st.checkbox("Use dsDNA approximation (P = mass/330)", value=True)
		bp_length = st.number_input(
			"Optional: plasmid length (bp)", value=0, min_value=0,
			help="If provided, shows alternative calculation using base pairs."
		)
	with col2:
		stock_conc_default = 100.0
		amines_per_molecule_default = 1.0
		add_volume_default = 50.0
		stock_conc_mM = st.number_input(
			"Ionizable lipid stock (mM)", value=stock_conc_default, min_value=0.0, step=10.0,
			help="Molar concentration of the ionizable lipid stock solution."
		)
		stock_amine_per_molecule = st.number_input(
			"Tertiary amines per molecule", value=amines_per_molecule_default, min_value=0.0, step=0.5,
			help="Effective number of protonatable tertiary nitrogens per lipid (often ~1 for many ionizable lipids)."
		)
		add_volume_uL = st.number_input(
			"Volume added (µL)", value=add_volume_default, min_value=0.0, step=1.0,
			help="Volume of the ionizable lipid stock added to the mixture."
		)

	submitted = st.form_submit_button("Calculate N/P")

if submitted:
	# Convert inputs to moles
	dna_mass_g = dna_mass_ug * 1e-6

	# Phosphate moles from dsDNA mass approximation: P ≈ mass / 330 g/mol
	P_mol = dna_mass_g / 330.0 if ds_dna else None

	# Optional alternative using base pairs: moles of BP = mass/660; phosphates = 2 * moles_BP
	P_alt_mol = (dna_mass_g / 660.0) * 2 if bp_length and bp_length > 0 else None

	# N moles from stock concentration and volume
	# stock_conc_mM (mmol/L) * volume (µL -> L) => mmol; convert to mol; multiply by amines per molecule
	N_mol = (stock_conc_mM * 1e-3) * (add_volume_uL * 1e-6) * stock_amine_per_molecule

	st.subheader("Results")

	results = {}
	if ds_dna and P_mol is not None and P_mol > 0:
		np_ratio = N_mol / P_mol if P_mol > 0 else math.nan
		st.metric("N/P (dsDNA mass method)", f"{np_ratio:.3f}")
		st.caption(f"P (moles) ≈ {P_mol:.3e}; N (moles) = {N_mol:.3e}")
		results.update({"method": "dsDNA mass", "N (mol)": N_mol, "P (mol)": P_mol, "N/P": np_ratio})
	else:
		# Ensure np_ratio is defined and handle None P formatting for the caption
		np_ratio = math.nan
		P_str = f"{P_mol:.3e}" if (P_mol is not None and P_mol != 0) else "N/A"
		st.caption(f"P (moles) ≈ {P_str}; N (moles) = {N_mol:.3e}")
		results.update({"method": "dsDNA mass", "N (mol)": N_mol, "P (mol)": P_mol, "N/P": np_ratio})
		st.warning("Provide DNA mass and enable dsDNA approximation to compute P via mass/330.")

	if P_alt_mol:
		np_ratio_alt = N_mol / P_alt_mol if P_alt_mol > 0 else math.nan
		st.metric("N/P (bp-based alternative)", f"{np_ratio_alt:.3f}")
		st.caption(f"P_alt (moles) ≈ {P_alt_mol:.3e}; N (moles) = {N_mol:.3e}")
		results.setdefault("method", "bp-based")
		results.update({"N (mol)": N_mol, "P (mol)": P_alt_mol, "N/P": np_ratio_alt})

	# Export buttons if we have results
	if results:
		import pandas as pd
		df_out = pd.DataFrame({k: [v] for k, v in results.items()})
		st.download_button(
			"Download CSV",
			data=df_out.to_csv(index=False),
			file_name="np_ratio_results.csv",
			mime="text/csv",
		)
		try:
			from io import BytesIO
			import openpyxl  # noqa: F401
			bio = BytesIO()
			with pd.ExcelWriter(bio, engine="openpyxl") as writer:
				df_out.to_excel(writer, index=False, sheet_name="N_P")
			bio.seek(0)
			st.download_button(
				"Download Excel",
				data=bio.read(),
				file_name="np_ratio_results.xlsx",
				mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
			)
		except Exception as e:
			st.caption(f"Excel export unavailable: {e}")

st.divider()
st.header("Target N/P → Required Volume")

with st.form("np_target"):
	colA, colB = st.columns(2)
	with colA:
		dna_mass_ug_t = st.number_input("DNA mass (µg)", value=10.0, min_value=0.0, step=0.5, key="dna_mass_t")
		ds_dna_t = st.checkbox("Use dsDNA approximation (P = mass/330)", value=True, key="ds_dna_t")
		target_np = st.number_input("Target N/P", value=5.0, min_value=0.0, step=0.5)
	with colB:
		stock_conc_mM_t = st.number_input("Ionizable stock (mM)", value=100.0, min_value=0.0, step=10.0, key="stock_conc_t")
		amines_per_molecule_t = st.number_input("Amines per molecule", value=1.0, min_value=0.0, step=0.5, key="amines_t")

	submitted_t = st.form_submit_button("Calculate required volume (µL)")

if submitted_t:
	dna_mass_g_t = dna_mass_ug_t * 1e-6
	P_mol_t = dna_mass_g_t / 330.0 if ds_dna_t else None
	if not P_mol_t or P_mol_t <= 0 or stock_conc_mM_t <= 0 or amines_per_molecule_t <= 0:
		st.error("Please provide positive values for DNA mass, stock concentration, and amines per molecule.")
	else:
		# target_np = N/P ⇒ N = target_np * P
		N_needed_mol = target_np * P_mol_t
		# N_needed_mol = C(mol/L) * V(L) * amines ⇒ V = N / (C * amines)
		V_L = N_needed_mol / ((stock_conc_mM_t * 1e-3) * amines_per_molecule_t)
		V_uL = V_L * 1e6
		st.metric("Required volume (µL)", f"{V_uL:.2f}")
		st.caption(
			f"For target N/P={target_np:.2f}: P={P_mol_t:.3e} mol, N (tertiary amines) needed={N_needed_mol:.3e} mol, volume={V_uL:.2f} µL"
		)
		# Export a single-row table for this calculation
		import pandas as pd
		df_req = pd.DataFrame({
			"Target N/P": [target_np],
			"DNA mass (µg)": [dna_mass_ug_t],
			"P (mol)": [P_mol_t],
			"Stock (mM)": [stock_conc_mM_t],
			"Amines per molecule": [amines_per_molecule_t],
			"Required volume (µL)": [V_uL],
		})
		st.download_button("Download volume CSV", df_req.to_csv(index=False), file_name="np_required_volume.csv", mime="text/csv")

st.divider()
st.info(
	"Assumptions: dsDNA mass uses 660 g/mol per base pair and 2 phosphates per bp (P ≈ mass/330). "
	"For other nucleic acids or reagents, adjust the amines per molecule and the mass-to-phosphate mapping accordingly."
)

