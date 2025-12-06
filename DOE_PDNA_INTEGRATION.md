# DOE 设计与 pDNA 方法整合文档

## 📋 概述

已将 pDNA Formulation 页面的计算方法整合到 DOE Designer 中，包括：
- N/P 比的计算和验证
- 改进的体积计算逻辑
- 更完善的运行表结构

## 🔄 主要改进

### 1. **N/P 比计算函数**

从 pDNA 页面采用 `calculate_np_ratio()` 函数：

```python
def calculate_np_ratio(dna_mass_ug, ionizable_lipid_moles, amines_per_molecule=1.0):
    """
    计算 N/P 比
    - N: 离子化脂质中胺基的摩尔数
    - P: DNA 中磷酸基团的摩尔数
    - 公式: P (μmol) = DNA_mass (μg) / 330
    """
```

**关键公式**：
- 磷酸基团摩尔数：`P = DNA_mass_μg × 1e-6 / 330.0 × 1e6 (μmol)`
- 胺基摩尔数：`N = ionizable_lipid_moles × amines_per_molecule`
- N/P 比：`N/P = N / P`

### 2. **改进的体积计算**

`calculate_volumes()` 函数现已返回离子化脂质摩尔数：

```python
return {
    "Ionizable_Vol_uL": round(vol_ion_ul, 2),
    "Helper_Vol_uL": round(vol_helper_ul, 2),
    "Chol_Vol_uL": round(vol_chol_ul, 2),
    "PEG_Vol_uL": round(vol_peg_ul, 2),
    "Ethanol_Vol_uL": round(ethanol_vol_ul, 2),
    "Buffer_Vol_uL": round(aqueous_vol_ul, 2),
    "Total_Vol_uL": round(total, 2),
    "Ionizable_Moles": moles_ion  # ← 新增，用于 N/P 计算
}
```

### 3. **运行表增强**

`generate_run_sheet()` 函数现包含：

| 列名 | 说明 | 备注 |
|------|------|------|
| Block | 实验块号 | 用于分组 |
| Run_ID | 运行编号 | R001, R002, ... |
| Experiment | 实验点编号 | DOE 设计中的点 |
| Replicate | 重复编号 | 1, 2, 3, ... |
| Ionizable_% | 离子化脂质摩尔% | DOE 变量 |
| Helper_% | 辅助脂质摩尔% | 计算值 |
| Cholesterol_% | 胆固醇摩尔% | DOE 变量 |
| PEG_% | PEG 脂质摩尔% | DOE 变量 |
| **NP_Ratio_Target** | 目标 N/P 比 | DOE 变量 |
| **NP_Ratio_Calc** | 计算得到的 N/P 比 | 基于 DNA 质量 |
| Ionizable_Vol_uL | 离子化脂质体积 | 吸液体积 |
| Helper_Vol_uL | 辅助脂质体积 | 吸液体积 |
| Chol_Vol_uL | 胆固醇体积 | 吸液体积 |
| PEG_Vol_uL | PEG 脂质体积 | 吸液体积 |
| Ethanol_Vol_uL | 乙醇体积 | 有机相 |
| Buffer_Vol_uL | 缓冲液体积 | 水相 |
| Total_Vol_uL | 总体积 | 质量检查 |
| Timestamp | 时间戳 | 记录生成时间 |
| Notes | 备注 | 用户添加 |

### 4. **UI 显示增强**

在结果显示部分添加了 N/P 比统计：

```
📊 N/P 比范围统计
├── N/P Min
├── N/P Avg
└── N/P Max
```

## 🔧 技术细节

### 计算流程

```
DOE 设计点 (Molar %)
    ↓
normalize_molar_ratios() 
    ↓
calculate_volumes()
    ├── 计算摩尔数
    ├── 计算质量
    └── 计算体积 + 返回 ionizable_moles
    ↓
calculate_np_ratio(dna_mass, ionizable_moles)
    ├── 计算磷酸基团 (P)
    ├── 计算胺基 (N)
    └── 计算 N/P 比
    ↓
运行表中存储所有数据
```

### DNA 参数处理

目前 `generate_run_sheet()` 接受可选参数：
- `dna_mass_ug`: DNA 质量 (μg)
- `dna_concentration`: DNA 浓度 (μg/μL)

**当前设置**：默认为 `None`（N/P 比显示为 "N/A"）

**未来扩展**：可在 UI 中添加输入框获取这些参数。

## 📊 数据导出

Excel 导出现包含三个工作表：

1. **Run Sheet** - 完整的运行表
2. **Design Matrix** - DOE 设计点
3. **Summary** - 实验摘要（包括 N/P 范围）

## 🎯 后续可能的改进

- [ ] 在 UI 中添加 DNA 质量输入参数
- [ ] 自动计算和显示 N/P 比
- [ ] 添加 N/P 比验证（例如，是否在目标范围内）
- [ ] 整合 pDNA 的 aqueous_to_ethanol 比参数
- [ ] 添加批量制备缩放 (1.5x 乙醇，1.2x 水相)
- [ ] 集成历史记录跟踪（如 pDNA 页面所做的）

## ✅ 验证信息

- **代码检查**: ✓ 无语法错误
- **函数签名**: ✓ 向后兼容
- **数据结构**: ✓ 支持 NP_Ratio 列
- **UI 显示**: ✓ 条件显示 N/P 统计

## 📝 使用示例

### 基本流程

1. 配置组件数据库（自动加载）
2. 设置 DOE 参数
3. 选择 N/P 比范围（如 3-9）
4. 生成 DOE 设计
5. 查看运行表中的 N/P 比列
6. 下载 CSV 或 Excel

### 注意事项

- N/P 比计算需要 DNA 质量参数（当前未在 UI 中提供）
- 体积计算仍使用固定的 assumed_lipid_conc_mg_per_ml = 15.0
- 可根据需要调整此参数以匹配您的实际库存浓度

---

**最后更新**: 2024 年
**集成来源**: pDNA Formulation 页面 (pages/2_🧬_pDNA_formulation.py)
