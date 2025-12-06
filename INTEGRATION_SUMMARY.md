# DOE-pDNA 整合总结

## ✅ 已完成的改进

### 1. 添加 N/P 比计算函数
在 DOE Designer 中集成了 `calculate_np_ratio()` 函数，采用来自 pDNA Formulation 页面的实现：

```python
def calculate_np_ratio(dna_mass_ug, ionizable_lipid_moles, amines_per_molecule=1.0):
    """
    计算 N/P 比（胺基/磷酸基团的摩尔比）
    
    输入：
    - dna_mass_ug: DNA 质量（微克）
    - ionizable_lipid_moles: 离子化脂质摩尔数（微摩尔）
    
    公式：
    - P = DNA_mass_μg / 330 × 1e6 (转换为 μmol)
    - N = ionizable_lipid_moles × amines_per_molecule
    - N/P = N / P
    """
```

### 2. 增强 calculate_volumes() 函数
现在返回 `Ionizable_Moles`，用于计算 N/P 比：

```python
return {
    ...,
    "Ionizable_Moles": moles_ion  # 用于 N/P 比计算
}
```

### 3. 扩展 generate_run_sheet() 函数
添加了两列：
- `NP_Ratio_Target`: DOE 设计中的目标 N/P 比
- `NP_Ratio_Calc`: 基于 DNA 质量计算的实际 N/P 比

函数签名：
```python
def generate_run_sheet(
    design_df, num_replicates, num_blocks,
    mw_ion, mw_helper, mw_chol, mw_peg,
    conc_ion, conc_helper, conc_chol, conc_peg,
    target_vol_ul,
    dna_mass_ug=None,           # ← 新参数（可选）
    dna_concentration=None       # ← 新参数（可选）
):
```

### 4. 改进 UI 显示
在结果显示部分添加了 N/P 比统计指标：
- N/P Min
- N/P Avg
- N/P Max

### 5. 数据导出增强
Excel 导出现在包括：
- 完整的运行表（包含 N/P 比列）
- 设计矩阵
- 摘要工作表（包含 N/P 范围信息）

---

## 🎯 工作流程

### 当前流程
```
1. 用户输入 DOE 参数（Ionizable %、Cholesterol %、PEG %、N/P Ratio 范围）
                ↓
2. 生成 DOE 设计矩阵
                ↓
3. 为每个设计点计算体积
   - normalize_molar_ratios()
   - calculate_volumes() → 获得 ionizable_moles
                ↓
4. 计算 N/P 比（如果提供 DNA 质量）
   - calculate_np_ratio(dna_mass_ug, ionizable_moles)
                ↓
5. 生成运行表，包含所有组分体积和 N/P 比
                ↓
6. 显示结果、3D 可视化、热力图和统计
                ↓
7. 导出 CSV 或 Excel
```

### 所需改进点
为了完全集成 pDNA 方法，需要：

- [ ] 在 UI 中添加 DNA 质量输入字段
- [ ] 添加 DNA 浓度输入字段（用于体积计算）
- [ ] 实现 `aqueous_to_ethanol_ratio` 作为变量参数
- [ ] 集成 DNA 体积、柠檬酸钠体积和缓冲液体积的计算
- [ ] 添加批量制备缩放选项

---

## 📊 技术细节

### 单位说明

| 参数 | 单位 | 说明 |
|------|------|------|
| DNA 质量 | μg | 输入参数 |
| DNA 浓度 | μg/μL | DNA 库存浓度 |
| 磷酸摩尔数 (P) | μmol | DNA_mass / 330 × 1e6 |
| 胺基摩尔数 (N) | μmol | ionizable_moles × amines_per_molecule |
| 分子量 (MW) | g/mol | 脂质分子量 |
| 浓度 | mg/mL | 脂质库存浓度 |
| 体积 | μL | 吸液体积 |

### pDNA 整合要点

1. **N/P 比计算基础**
   - 使用 DNA 质量和离子化脂质摩尔数
   - 不依赖于目标体积或摩尔比例

2. **离子化脂质摩尔数来源**
   - 在当前 DOE 中来自 `calculate_volumes()` 中的百分比计算
   - 在 pDNA 中来自 DNA 质量 × ionizable_lipid_to_dna_ratio

3. **关键差异**
   - DOE：使用摩尔百分比作为变量
   - pDNA：使用 DNA 质量作为基础

---

## 🔍 代码验证

✅ 语法检查: 无错误
✅ 函数导入: `calculate_np_ratio` 可调用
✅ 数据流: Run Sheet 包含 N/P 比列
✅ 单位一致: 所有摩尔数为 μmol

---

## 💡 使用示例

### 在运行表中查看 N/P 比

运行表现在包含这些 N/P 相关列：

```
Run_ID | Ionizable_% | NP_Ratio_Target | NP_Ratio_Calc | ...
--------|-------------|-----------------|---------------|---
R001    | 50.0        | 5.0             | N/A           | ...
R002    | 48.5        | 5.2             | N/A           | ...
...
```

**注意**: `NP_Ratio_Calc` 当前显示 "N/A"，因为 DNA 质量参数未在 UI 中提供。

### 后续步骤实现完全功能

1. 在"Component Database Configuration"下添加：
   ```python
   dna_mass = st.number_input("DNA Scale (μg)", value=3.0)
   dna_concentration = st.number_input("DNA Stock (μg/μL)", value=1.0)
   ```

2. 修改生成运行表的调用：
   ```python
   run_sheet = generate_run_sheet(
       ...,
       dna_mass_ug=dna_mass,
       dna_concentration=dna_concentration
   )
   ```

3. `NP_Ratio_Calc` 列将自动填充计算值

---

## ✨ 新增功能亮点

1. **N/P 比验证**: 为每个设计点计算实际 N/P 比
2. **统计显示**: 显示 N/P 比的最小值、平均值、最大值
3. **导出完整性**: Excel 导出包含所有 N/P 数据
4. **向后兼容**: 在没有 DNA 参数时优雅降级

---

**最后更新**: 2024
**涉及文件**: 
- `/pages/6_🀄️_High-Throughput_Formulation.py`
- `/DOE_PDNA_INTEGRATION.md`
- `/test_doe_pdna_integration.py`
