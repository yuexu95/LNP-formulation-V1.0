import streamlit as st
import pandas as pd

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