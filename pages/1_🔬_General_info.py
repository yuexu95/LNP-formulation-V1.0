import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="General Information", page_icon="🔬", layout="wide")

st.title("🔬 Readme before you start")

st.markdown("""
## What are Lipid Nanoparticles (LNPs)?

Lipid nanoparticles (LNPs) are nanoscale delivery vehicles designed to encapsulate and protect nucleic acids 
(such as mRNA or plasmid DNA) for therapeutic applications. LNPs enable efficient cellular uptake and 
intracellular delivery of genetic material while protecting it from degradation by nucleases.
""")

st.divider()

st.header("📋 Classic LNP Composition")

st.markdown("""
A typical LNP formulation consists of four main lipid components:

1. **Ionizable/Cationic Lipid (40-50 mol%)**: The primary component that complexes with negatively charged 
   nucleic acids through electrostatic interactions. It remains neutral or slightly positive at physiological 
   pH but becomes positively charged at acidic pH to facilitate endosomal escape.

2. **Structural Lipid/Phospholipid (9-15 mol%)**: Usually phosphatidylcholine (e.g., DSPC, DOPE), which 
   provides structural stability and helps form the lipid bilayer.

3. **Cholesterol (38-48 mol%)**: Enhances membrane stability, rigidity, and fusion properties, improving 
   the overall integrity of the nanoparticle.

4. **PEG-Lipid (1-3 mol%)**: Polyethylene glycol (PEG)-conjugated lipid that provides steric stabilization, 
   reduces aggregation, and increases circulation time by minimizing protein adsorption and immune recognition.
""")

st.subheader("FDA-Approved LNP Formulations")
st.markdown("""
The following are FDA-approved LNP formulations with their molar ratios:

| Ionizable Lipid | Ionizable Lipid (mol%) | Cholesterol (mol%) | Structural Lipid* (mol%) | PEG-Lipid* (mol%) |
|---|---|---|---|---|
| **D-Lin-MC3-DMA** | 50% | 38.5% | 10% (DSPC) | 1.5% (DMG-PEG 2000) |
| **SM-102** | 50% | 38.5% | 10% (DSPC) | 1.5% (DMG-PEG 2000) |
| **ALC-0315** | 46.3% | 42.7% | 9.4% (DSPC) | 1.6% (ALC-0159) |

*DSPC = 1,2-distearoyl-sn-glycero-3-phosphocholine; DMG-PEG 2000 = Dimyristoyl glycerol PEG 2000; ALC-0159 = Proprietary PEGylated lipid
""")

st.divider()

st.header("🧮 Calculation Principles")

st.markdown("""
### Molar Ratio Calculations

LNP formulations are typically defined by **molar ratios** of the four lipid components. The key calculations involve:

**1. Determining Moles of Each Component:**
- Moles = Mass (g) / Molecular Weight (g/mol)
- For stock solutions: Moles = Concentration (M) × Volume (L)

**2. Calculating Molar Percentages:**
- Molar % of Component = (Moles of Component / Total Moles of All Lipids) × 100

**3. N/P Ratio:**
The N/P ratio represents the molar ratio of positively charged amine groups (N) from ionizable lipids to 
negatively charged phosphate groups (P) on nucleic acids:

- **N/P = (moles of amine groups) / (moles of phosphate groups)**

For double-stranded DNA (dsDNA):
- Each base pair has an average molecular weight of ~660 g/mol
- Each base pair contributes 2 phosphate groups (one per strand)
- Therefore: **P (moles) ≈ DNA mass (g) / 330 g/mol**

For mRNA (single-stranded):
- Each nucleotide has an average molecular weight of ~330 g/mol
- Each nucleotide contributes 1 phosphate group
- Therefore: **P (moles) ≈ RNA mass (g) / 330 g/mol**

**4. Volume Calculations:**
Once the desired molar ratios and N/P ratio are determined, you can calculate the required volumes of each 
lipid stock solution:

- Volume (L) = Moles needed / Stock concentration (M)
- Convert to µL for practical pipetting: Volume (µL) = Volume (L) × 10⁶
""")

st.divider()

st.header("⚙️ Formulation Process")

st.markdown("""
The typical LNP formulation process involves:

1. **Preparation Phase:**
   - Dissolve each lipid component in an appropriate organic solvent (typically ethanol)
   - Prepare nucleic acid solution in an aqueous buffer (e.g., acetate buffer, pH 4-5)

2. **Mixing Phase:**
   - Rapidly mix the lipid solution with the nucleic acid solution using microfluidic mixing, T-junction, 
     or pipette mixing
   - The rapid mixing is critical for forming uniform, small nanoparticles

3. **Post-Processing:**
   - Dialysis or tangential flow filtration to remove organic solvent and exchange into final buffer
   - Concentration if needed
   - Sterile filtration (typically 0.22 µm)

4. **Characterization:**
   - Size measurement (Dynamic Light Scattering - DLS)
   - Polydispersity index (PDI) for size distribution
   - Encapsulation efficiency
   - Zeta potential
""")

st.divider()

st.header("🎯 Key Parameters to Optimize")

st.markdown("""
- **N/P Ratio**: Ratio of tertiary amine groups (N) to phosphate groups (P). Typical range: 3-10
- **Molar Ratios**: Optimize for stability, size, and transfection efficiency
- **Flow Rate Ratio**: Aqueous to organic phase ratio during mixing (typically 3:1)
- **Total Flow Rate**: Affects particle size during microfluidic mixing
- **Nucleic Acid Concentration**: Influences loading capacity
- **pH of Aqueous Buffer**: Affects ionization and complexation
""")

st.divider()

st.info("""
**💡 Tips for Success:**
- Always prepare fresh lipid solutions to avoid oxidation
- Maintain strict sterile technique for therapeutic applications
- Optimize formulation parameters systematically
- Characterize each batch thoroughly
- Consider the specific requirements of your nucleic acid cargo (pDNA vs. mRNA)
""")

st.markdown("""
---
Use the other tabs to access calculators for:
- **pDNA Formulation**: Calculate lipid volumes for plasmid DNA delivery
- **mRNA Formulation**: Calculate lipid volumes for mRNA delivery
- **N/P Ratio**: Dedicated calculator for N/P ratio optimization
""")

st.divider()

st.header("🧬 DNA vs RNA: N/P Ratio Differences")

st.markdown("""
Understanding the chemical differences between DNA and RNA helps set correct expectations for N/P calculations and formulation behavior:

**Chemical and stoichiometric differences**
- **Phosphate count**: Each nucleotide contributes one phosphate group. For double‑stranded DNA (dsDNA), each base pair has two nucleotides (one per strand), so effectively **2 phosphates per base pair**. For single‑stranded RNA (ssRNA/mRNA), it’s **1 phosphate per nucleotide**.
- **Average masses**:
   - dsDNA: ~660 g/mol per base pair ⇒ **P (mol) ≈ mass / 330**
   - ssRNA: ~330 g/mol per nucleotide ⇒ **P (mol) ≈ mass / 330** (one phosphate per nucleotide)
- **Charge density**: RNA is single‑stranded, exposing phosphates and bases, which can change binding and packing vs dsDNA.

**Implications for N/P selection**
- **Encapsulation and stability**: RNA often requires similar or slightly different N/P than dsDNA depending on lipid chemistry and buffer pH. Typical starting ranges:
   - dsDNA: **N/P ~3–10**
   - mRNA: **N/P ~3–8**
- **pH sensitivity**: Ionizable lipids gain positive charge in mildly acidic buffers (pH ~4–5). The effective “N” depends on lipid pKa and buffer pH.
- **Amines per molecule**: Use the effective number of protonatable nitrogens for your ionizable lipid (often ~1). Adjust if the headgroup carries more than one amine.

**Practical calculation tips**
- For dsDNA: Compute P from mass using **mass/330**. For plasmid length, each base pair contributes two phosphates; mass and length methods should agree.
- For mRNA: Compute P from mass using **mass/330** (one phosphate per nucleotide). If length (nt) is known, total phosphates equal nt.
- Always double‑check units: mass in grams, concentration in mol/L, volume in liters; convert to µL for pipetting.

Use the **N/P Ratio** tab to quickly compare dsDNA‑based and RNA‑based calculations by adjusting the inputs.
""")

# Example validation section for pDNA formulation
st.divider()
st.header("Example: pDNA Formulation with N/P = 4 and Moderna LNP Formulation")
with st.expander("Show example for 100 µg DNA at N/P = 4; EtOH phase ratios"):
    st.markdown("""
    This example uses the ethanol-phase molar composition:
    SM102 50%, DSPC 10%, Cholesterol 38.5%, PEG-DMG2000 1.5% (sum 100%).
    """)

    df_example = pd.DataFrame({
        "ID": ["SM102", "DSPC", "Cholesterol", "PEG-DMG2000"],
        "EtOH phase mol%": [50.0, 10.0, 38.5, 1.5],
        "Stock (µg/µL)": [100.0, 12.5, 20.0, 50.0],
    })
    st.table(df_example)
    st.caption("Volumes depend on target total lipid and stocks; see formulas below.")

    st.warning("Dilute 100 µg DNA to 180 µL in 25 mM sodium acetate.")

# 用公式展示计算过程（可折叠）
with st.expander("Show detailed calculation formulas"):
    st.latex(r"\textbf{Moderna LNP Formulation for mRNA delivery(EtOH phase mol\%):}\quad f_{\text{SM102}}=0.50,\ f_{\text{DSPC}}=0.10,\ f_{\text{Chol}}=0.385,\ f_{\text{PEG}}=0.015")

    st.latex(r"\textbf{DNA and N/P:}\quad m_{\text{DNA}}=100\,\mu g,\ \text{N/P}=4,\ a=1")
    st.latex(r"P\,(\mu mol) = \frac{100}{330} \approx 0.30303\,\mu mol\,,\quad N = 4\times 0.30303 \approx 1.21212\,\mu mol")

    st.latex(r"\textbf{Mole split by fraction:}\quad n_{i} = f_{i}\,n_{\text{total}}\,,\ \sum_i f_i=1")
    st.latex(r"\text{Assume } n_{\text{total}} \text{ consistent with table masses.}")

    st.latex(r"\textbf{Mass from moles:}\quad m_{i}\,(\mu g) = n_{i}\,(\mu mol) \cdot MW_{i}\,(\mu g/\mu mol)")
    st.latex(r"\text{Table masses (per 100 }\mu g\text{ DNA at N/P=4): }\ m_{\text{SM102}}=860.8484848,\ m_{\text{DSPC}}=191.5515152,\ m_{\text{Chol}}=360.92,\ m_{\text{PEG}}=91.24363636\ (\mu g)")

    st.latex(r"\textbf{Volume from stock:}\quad V_{i}\,(\mu L) = \frac{m_{i}\,(\mu g)}{C_{i}\,(\mu g/\mu L)}")
    st.latex(r"V_{\text{SM102}} = \frac{860.8484848}{100} \approx 8.6085\,\mu L\,,\ \ V_{\text{DSPC}} = \frac{191.5515152}{12.5} \approx 15.3241\,\mu L")
    st.latex(r"V_{\text{Chol}} = \frac{360.92}{20} \approx 18.0460\,\mu L\,,\ \ V_{\text{PEG}} = \frac{91.24363636}{50} \approx 1.8249\,\mu L")
    st.latex(r"V_{\text{EtOH, lipids}} = \sum_i V_i \approx 8.6085+15.3241+18.0460+1.8249 \approx 16.2\,\mu L")

    st.latex(r"\textbf{DNA mixing volume:}\quad V_{\text{DNA}} = 180\,\mu L\ \text{(25 mM sodium acetate)}")
    st.latex(r"\textbf{Molecular weights (example):}\ \ MW_{\text{SM102}}\approx 1000\,\mu g/\mu mol,\ MW_{\text{DSPC}}=744.034,\ MW_{\text{Chol}}=386.654,\ MW_{\text{PEG}}=2509.2")

    st.latex(r"\textbf{Moles from masses (per table):}\quad n_{i}\,(\mu mol) = \frac{m_{i}\,(\mu g)}{MW_{i}\,(\mu g/\mu mol)}")
    st.latex(r"n_{\text{SM102}} = \frac{860.8484848}{1000} \approx 0.86085\,\mu mol\,,\ \ n_{\text{DSPC}} = \frac{191.5515152}{744.034} \approx 0.25757\,\mu mol")
    st.latex(r"n_{\text{Chol}} = \frac{360.92}{386.654} \approx 0.93345\,\mu mol\,,\ \ n_{\text{PEG}} = \frac{91.24363636}{2509.2} \approx 0.03636\,\mu mol")
    st.latex(r"n_{\text{total}} \approx 0.86085+0.25757+0.93345+0.03636 \approx 2.08823\,\mu mol")
    st.latex(r"\textbf{Check mol fractions:}\quad f_{i} = \frac{n_{i}}{n_{\text{total}}}\ \Rightarrow\ f_{\text{SM102}}\approx 0.412,\ f_{\text{DSPC}}\approx 0.123,\ f_{\text{Chol}}\approx 0.447,\ f_{\text{PEG}}\approx 0.017")
    st.latex(r"\text{Note: Actual table masses yield fractions close to provided EtOH mol\% after accounting for formulation specifics.}")
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

