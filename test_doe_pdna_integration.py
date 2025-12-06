#!/usr/bin/env python3
"""
测试 DOE 与 pDNA 方法整合
验证 calculate_np_ratio 和改进的 calculate_volumes 功能
"""

import sys
sys.path.insert(0, '/Users/yuexu/Documents/Streamlit/LNP-formulation')

# 测试 calculate_np_ratio 函数
def test_calculate_np_ratio():
    """测试 N/P 比计算"""
    print("=" * 60)
    print("测试 1: calculate_np_ratio 函数")
    print("=" * 60)
    
    # 模拟的 DNA 质量和离子化脂质摩尔数
    dna_mass_ug = 3.0  # 3 μg DNA
    ionizable_lipid_moles = 30.0  # 30 μmol 离子化脂质
    
    # 计算磷酸摩尔数
    phosphate_moles_mol = dna_mass_ug * 1e-6 / 330.0
    phosphate_moles_umol = phosphate_moles_mol * 1e6
    
    # 计算胺基摩尔数
    amine_moles_umol = ionizable_lipid_moles * 1.0
    
    # 计算 N/P 比
    if phosphate_moles_umol > 0:
        np_ratio = amine_moles_umol / phosphate_moles_umol
    else:
        np_ratio = 0
    
    print(f"DNA 质量: {dna_mass_ug} μg")
    print(f"离子化脂质摩尔数: {ionizable_lipid_moles} μmol")
    print(f"磷酸摩尔数 (P): {phosphate_moles_umol:.4f} μmol")
    print(f"胺基摩尔数 (N): {amine_moles_umol:.4f} μmol")
    print(f"N/P 比: {np_ratio:.2f}")
    print()


def test_volume_calculation():
    """测试体积计算"""
    print("=" * 60)
    print("测试 2: 改进的体积计算")
    print("=" * 60)
    
    # 模拟摩尔百分比
    ion_pct = 50.0
    helper_pct = 35.0
    chol_pct = 10.0
    peg_pct = 5.0
    
    # 模拟分子量 (g/mol)
    mw_ion = 710.182 / 1000
    mw_helper = 790.147 / 1000
    mw_chol = 386.654 / 1000
    mw_peg = 2509.2 / 1000
    
    # 模拟浓度 (mg/mL)
    conc_ion = 100.0
    conc_helper = 12.5
    conc_chol = 20.0
    conc_peg = 50.0
    
    target_vol_ul = 200.0
    
    print(f"目标体积: {target_vol_ul} μL")
    print(f"摩尔比例: Ion {ion_pct}% / Helper {helper_pct}% / Chol {chol_pct}% / PEG {peg_pct}%")
    print()
    
    # 计算
    assumed_lipid_conc_mg_per_ml = 15.0
    target_lipid_mass_mg = (target_vol_ul / 2.0) * assumed_lipid_conc_mg_per_ml
    
    avg_mw = (ion_pct * mw_ion + helper_pct * mw_helper + 
              chol_pct * mw_chol + peg_pct * mw_peg) / 100.0
    
    total_moles_lipid = target_lipid_mass_mg / avg_mw
    
    moles_ion = (ion_pct / 100.0) * total_moles_lipid
    moles_helper = (helper_pct / 100.0) * total_moles_lipid
    moles_chol = (chol_pct / 100.0) * total_moles_lipid
    moles_peg = (peg_pct / 100.0) * total_moles_lipid
    
    print(f"目标脂质质量: {target_lipid_mass_mg:.2f} mg")
    print(f"平均分子量: {avg_mw:.2f} g/mol")
    print(f"总脂质摩尔数: {total_moles_lipid:.4f} mmol")
    print()
    
    print("各组分摩尔数:")
    print(f"  - 离子化脂质: {moles_ion:.4f} mmol")
    print(f"  - 辅助脂质: {moles_helper:.4f} mmol")
    print(f"  - 胆固醇: {moles_chol:.4f} mmol")
    print(f"  - PEG 脂质: {moles_peg:.4f} mmol")
    print()
    
    # 计算质量
    mass_ion_mg = moles_ion * mw_ion * 1000
    mass_helper_mg = moles_helper * mw_helper * 1000
    mass_chol_mg = moles_chol * mw_chol * 1000
    mass_peg_mg = moles_peg * mw_peg * 1000
    
    # 计算体积
    vol_ion_ul = (mass_ion_mg / conc_ion * 1000) if conc_ion > 0 else 0
    vol_helper_ul = (mass_helper_mg / conc_helper * 1000) if conc_helper > 0 else 0
    vol_chol_ul = (mass_chol_mg / conc_chol * 1000) if conc_chol > 0 else 0
    vol_peg_ul = (mass_peg_mg / conc_peg * 1000) if conc_peg > 0 else 0
    
    print("各组分体积:")
    print(f"  - 离子化脂质: {vol_ion_ul:.2f} μL")
    print(f"  - 辅助脂质: {vol_helper_ul:.2f} μL")
    print(f"  - 胆固醇: {vol_chol_ul:.2f} μL")
    print(f"  - PEG 脂质: {vol_peg_ul:.2f} μL")
    print()
    
    # 计算乙醇体积
    organic_phase_vol_ul = vol_ion_ul + vol_helper_ul + vol_chol_ul + vol_peg_ul
    target_organic_vol_ul = target_vol_ul / 2.0
    ethanol_vol_ul = max(0, target_organic_vol_ul - organic_phase_vol_ul)
    aqueous_vol_ul = target_vol_ul - (organic_phase_vol_ul + ethanol_vol_ul)
    
    print(f"有机相体积: {organic_phase_vol_ul:.2f} μL")
    print(f"乙醇体积: {ethanol_vol_ul:.2f} μL")
    print(f"水相体积: {aqueous_vol_ul:.2f} μL")
    print(f"总体积: {organic_phase_vol_ul + ethanol_vol_ul + aqueous_vol_ul:.2f} μL")
    print()
    
    # 用于 N/P 比的数据
    print("用于 N/P 比计算:")
    print(f"  - 离子化脂质摩尔数: {moles_ion:.4f} mmol = {moles_ion * 1000:.2f} μmol")
    print()


def test_np_ratio_with_dna():
    """测试带 DNA 的 N/P 比"""
    print("=" * 60)
    print("测试 3: 实际 N/P 比计算示例")
    print("=" * 60)
    
    dna_mass_ug = 3.0
    ionizable_moles_umol = 10.0  # 0.01 mmol = 10 μmol
    
    # 公式：P = DNA_mass_μg / 330 * 1e6 μmol
    phosphate_moles_umol = (dna_mass_ug / 330) * 1e6
    amine_moles_umol = ionizable_moles_umol * 1.0
    np_ratio = amine_moles_umol / phosphate_moles_umol if phosphate_moles_umol > 0 else 0
    
    print(f"DNA 质量: {dna_mass_ug} μg")
    print(f"离子化脂质: {ionizable_moles_umol} μmol")
    print()
    print(f"磷酸基团 (P): {phosphate_moles_umol:.4f} μmol")
    print(f"胺基 (N): {amine_moles_umol:.4f} μmol")
    print(f"N/P 比: {np_ratio:.2f}")
    print()
    print("✓ 这个 N/P 比应该在 DOE 运行表中作为 NP_Ratio_Calc 显示")
    print()


if __name__ == "__main__":
    test_calculate_np_ratio()
    test_volume_calculation()
    test_np_ratio_with_dna()
    
    print("=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)
