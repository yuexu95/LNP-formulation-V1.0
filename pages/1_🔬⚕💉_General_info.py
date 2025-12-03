import streamlit as st

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
