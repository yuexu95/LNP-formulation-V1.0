# 修复：DOE 设计中的负数 Helper Lipid 问题

## 问题描述

在 High-Throughput DOE Designer (页面 6) 中，生成 DOE 设计后，某些设计点中 **Helper Lipid 的百分比显示为负数**（如 -1%）。

### 问题现象
```
Run 8: Ionizable=55% + Cholesterol=43.5% + PEG=2.5% → Helper=-1% ❌
```

## 根本原因

**DOE 设计的独立参数假设与脂质比例的 100% 约束条件冲突**

### 约束条件
所有脂质的摩尔百分比必须相加等于 100%：
```
Ionizable% + Helper% + Cholesterol% + PEG% = 100%
```

### DOE 参数范围（默认）
- Ionizable: 45% ~ 55%
- Cholesterol: 33.5% ~ 43.5%
- PEG: 0.5% ~ 2.5%
- Helper: **自动计算** (100% 减去其他三个)

### 冲突情况
当所有参数**同时取最大值**时：
```
55% + 43.5% + 2.5% = 101% > 100%
Helper = 100% - 101% = -1% ❌
```

## 解决方案

### 实现方式

添加了新的过滤函数 `filter_valid_design_points()`，在 DOE 生成后立即过滤无效的设计点：

```python
def filter_valid_design_points(design_df, min_helper_pct=0.5):
    """
    过滤 DOE 设计点以确保所有摩尔比例有效。
    
    有效条件：
    Ionizable + Cholesterol + PEG + Helper = 100%
    且 Helper >= min_helper_pct (默认 0.5%)
    """
    valid_mask = (
        design_df["Ionizable_%"] + 
        design_df["Cholesterol_%"] + 
        design_df["PEG_%"]
    ) <= (100.0 - min_helper_pct)
    
    filtered_df = design_df[valid_mask].reset_index(drop=True)
    
    if len(design_df) - len(filtered_df) > 0:
        st.warning(f"⚠️ {n_removed} 个设计点被移除...")
    
    return filtered_df
```

### 执行流程
1. **生成 DOE 设计** → 所有设计点
2. **过滤无效点** → 只保留 Ionizable% + Cholesterol% + PEG% ≤ 99.5% 的点
3. **检查有效性** → 如果无有效点，显示错误并要求调整参数范围
4. **生成运行表** → 使用过滤后的有效设计点

## 实际效果

### 示例（2-Level Factorial）
```
过滤前：8 个设计点
过滤后：7 个设计点
移除：1 个无效点（Ion=55% + Chol=43.5% + PEG=2.5%）

保留的所有设计点都有有效的 Helper% 值 (≥ 0.5%) ✓
```

### 用户提示
当过滤发生时，用户会看到警告信息：
```
⚠️ Design Space Constraint: 1 of 8 design points removed because 
Ionizable + Cholesterol + PEG > 100%. Remaining valid points: 7
```

## 参数范围建议

为了获得最多的设计点，建议参数范围满足以下条件：

### 最大值之和 ≤ 99.5%
```
Ionizable_Max + Cholesterol_Max + PEG_Max ≤ 99.5%
```

### 推荐的参数范围
| 参数 | 最小值 | 最大值 | 说明 |
|------|--------|--------|------|
| Ionizable% | 45.0 | 55.0 | 最大和 = 45+43.5+2.5 = 91% ✓ |
| Cholesterol% | 33.5 | 43.5 | 最大和 = 55+43.5+2.5 = 101% ✗ 会被过滤 |
| PEG% | 0.5 | 2.5 | 最大和 = 55+33.5+2.5 = 91% ✓ |

### 改进的参数范围（无损失）
```
Ionizable: 45% → 50%      (最大和 = 50+38+2.5 = 90.5%)
Cholesterol: 35% → 40%    (最大和 = 50+40+2.5 = 92.5%)
PEG: 1% → 2.5%           (最大和 = 50+40+2.5 = 92.5%)
```

## 代码位置

**文件**: `/pages/6_🀄️_High-Throughput_Formulation.py`

**修改内容**:
1. **Line 274-321**: 添加 `filter_valid_design_points()` 函数
2. **Line 667-668**: 在 DOE 生成后调用过滤函数
3. **Line 670-677**: 添加有效性检查和错误处理

## 测试验证

✓ 默认参数范围内的 2-Level Factorial 设计：8 个点 → 过滤后 7 个点
✓ 所有保留的设计点的 Helper% ≥ 0.5%
✓ 无语法错误，已验证

## 后续改进建议

1. **智能范围建议**：根据用户输入的范围，自动计算并建议调整
2. **可视化显示**：在设计空间可视化中用不同颜色标记被过滤的点
3. **详细日志**：显示被过滤的具体设计点及其原因
4. **Alternative Design**: 提供基于约束的设计方法（如 Mixture Design）

## 相关问题

- **Issue**: 为什么 DOE 之后会出现 Helper Lipid 为-1 的情况
- **Root Cause**: 参数范围冲突导致摩尔比例无法相加到 100%
- **Status**: ✅ 已修复
- **Fix Date**: 2025-12-08
