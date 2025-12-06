# 🀄 LNP-Flow 快速参考卡

## 🚀 快速启动

```bash
# 激活环境
source venv312_new/bin/activate

# 启动应用
streamlit run "👋Homepage.py"

# 访问: http://localhost:8501
```

---

## 📖 6个页面导览

| # | 页面 | 功能 | 用途 |
|---|------|------|------|
| 1 | 🔬 General Info | LNP教育资源 | 学习基础知识 |
| 2 | 🧬 pDNA Formulation | 单个配方计算 | 验证配方 |
| 3 | 〰️ mRNA Formulation | mRNA指导 | mRNA项目 |
| 4 | 📚 References | 50+文献 | 查找论文 |
| 5 | 🧐 Methods | 完整SOP | 实验协议 |
| 6 | 🀄 DOE Designer | 高通量设计 | 批量实验规划 |

---

## 🀄 DOE Designer (Page 6) - 核心功能

### 7种设计类型

| 设计 | 运行数 | 用途 | 特点 |
|------|--------|------|------|
| 2-Level Factorial | 32 | 探索 | 全面，最多运行 |
| 3-Level Factorial | 243 | 详细探索 | 最全面，最多运行 |
| Fractional Factorial | ~16 | 快速筛选 | 高效，假设交互小 |
| Plackett-Burman | 12 | 初始筛选 | 超高效，仅12运行 |
| Box-Behnken | ~26 | 优化 | 中等，响应曲面 |
| Central Composite | ~30 | 完整优化 | 完整，二次模型 |
| Mixture Design | 可变 | 比例优化 | 特定，混合专用 |

### 3个3D图表

```
图1: 摩尔比空间 (3D)        图2: 工艺参数空间 (3D)      图3: 体积分布 (3D)
Ion% vs Chol% vs PEG%      TFR vs FRR vs Ion%         IonVol vs HelperVol vs PEGVol
↓                          ↓                          ↓
理解配方约束               理解工艺交互               理解移液需求
```

### 2个2D热力图

```
热力图1: 总体积                    热力图2: 辅助脂质体积
Ion% vs 总流速                     胆固醇% vs 流速比
↓                                  ↓
体积优化                           体积平衡
```

---

## 📊 工作流步骤

### 步骤1️⃣: 配置
- 侧边栏 → 设置分子量 (MW) 和浓度
- 侧边栏 → 设置N/P比目标

### 步骤2️⃣: 设计选择
- Tab1: 选择DOE方法
- Tab1: 设置摩尔比范围 (Ion%, Chol%, PEG%)
- Tab1: 设置工艺参数 (TFR, FRR)
- Tab1: 设置体积和重复

### 步骤3️⃣: 生成
- 点击绿色按钮 "🚀 Generate DOE Design"
- 等待设计生成 (<2秒)

### 步骤4️⃣: 查看
- 查看设计矩阵表
- 查看运行表预览
- 查看3D可视化
- 查看热力图

### 步骤5️⃣: 导出
- 下载 CSV (LIMS导入)
- 下载 Excel (完整分析)

---

## 🧮 关键计算

### 摩尔比标准化
```
输入: Ion=45%, Chol=35%, PEG=2%
处理: Helper = 100% - 45% - 35% - 2% = 18%
输出: (45%, 18%, 35%, 2%) → 和 = 100% ✓
```

### 体积计算
```
摩尔% (45%) 
   ↓ 用MW计算 (平均MW = 加权平均)
摩尔数 
   ↓ 用MW转换 (moles × MW)
质量 (mg) 
   ↓ 用浓度转换 (mass / concentration)
体积 (µL)
```

### N/P比
```
N/P = 胺基数 / 磷酸基数
P ≈ DNA质量(µg) / 330 g/mol
N = 来自离子脂质的胺基总数
```

---

## 📁 文件映射

### 应用文件
```
pages/
├── 1_🔬_General_info.py (2000行, 教育资源)
├── 2_🧬_pDNA_formulation.py (650行, 单配方)
├── 3_〰️_mRNA_formulation.py (300行, mRNA指导)
├── 4_📚_References.py (1300行, 50+文献)
├── 5_🧐_Methods.py (600行, 完整SOP)
└── 6_🀄️_High-Throughput_Formulation.py (830行, DOE工具)
```

### 文档文件
```
├── DOE_FEATURES.md (功能列表)
├── DOE_USER_GUIDE.md (用户指南)
├── 3D_VISUALIZATION_GUIDE.md (3D说明)
├── PROJECT_COMPLETION.md (完成清单)
└── README.md (项目说明)
```

---

## 🎨 颜色与缩放

### Plotly色标
- **Viridis**: 摩尔比 (紫-绿-黄)
- **Plasma**: 工艺参数 (紫-橙-黄)
- **Turbo**: 体积 (蓝-绿-黄-红)
- **RdYlBu_r**: 热力图 (蓝-黄-红)

### 图表尺寸
- 3D图表: 600px高度
- 热力图: 400px高度
- 响应式宽度

---

## ⚙️ 参数范围 (默认值)

### 摩尔比 (%)
```
离子脂质:    40-50%
胆固醇:      35-45%
PEG脂质:     1-3%
辅助脂质:    自动计算 (必须≥0%)
```

### 工艺参数
```
总流速 (TFR):      8-15 mL/min
流速比 (FRR):      2-4 (水:乙醇)
```

### 体积
```
目标体积:          200 µL (可调)
```

---

## 💾 导出格式

### CSV结构
```
Block,Run_ID,Experiment,Replicate,Ionizable_%,Helper_%,Cholesterol_%,
PEG_%,TFR_mL_min,FRR,Ionizable_Vol_uL,Helper_Vol_uL,Chol_Vol_uL,
PEG_Vol_uL,Ethanol_Vol_uL,Buffer_Vol_uL,Total_Vol_uL,Timestamp,Notes
```

### Excel工作表
1. **Run Sheet**: 完整移液指令
2. **Design Matrix**: 因子设置
3. **Summary**: 元数据

---

## 🔧 组件数据库 (可修改)

| 成分 | 默认MW | 默认Conc |
|------|--------|----------|
| 离子脂质 | 710.182 | 100 mg/mL |
| 辅助脂质 | 790.147 | 12.5 mg/mL |
| 胆固醇 | 386.654 | 20 mg/mL |
| PEG脂质 | 2509.2 | 50 mg/mL |

---

## 📈 质量检查清单

- [ ] 摩尔比总和 = 100%
- [ ] 没有负的Helper %
- [ ] 最小 < 最大 (所有参数)
- [ ] 目标体积 > 0
- [ ] 设计点数量合理

---

## 🚨 常见问题

**Q: 3D图不显示?**
A: 更新浏览器或尝试 Chrome/Firefox

**Q: 设计生成太慢?**
A: 尝试 Plackett-Burman 或 Fractional Factorial

**Q: 体积看起来不对?**
A: 检查组件MW和浓度是否正确

**Q: 导出后如何使用?**
A: 用CSV导入LIMS或液体处理系统

---

## 🎯 最佳实践

1. **筛选阶段**: 用 Plackett-Burman (12 runs)
2. **优化阶段**: 用 Box-Behnken (26 runs)
3. **验证阶段**: 用 2-3 replicates
4. **参数范围**: 基于先验知识确定
5. **导出格式**: 优先用 Excel (完整信息)

---

## 📞 技术支持

### 依赖检查
```bash
source venv312_new/bin/activate
pip list | grep -E "streamlit|pandas|plotly"
```

### 日志查看
- 检查浏览器开发者工具 (F12)
- 查看Streamlit终端输出
- 保存错误信息用于调试

---

## 🌐 浏览器兼容性

✅ Chrome 90+  
✅ Firefox 88+  
✅ Safari 14+  
✅ Edge 90+  
❌ IE 11 (不支持)

---

## 📚 进阶应用

### 自定义工作流
1. 保存常用参数范围
2. 批量生成多个设计
3. 比较不同设计方法
4. 跟踪实验结果

### 集成选项
1. LIMS系统连接
2. 液体处理系统接口
3. 数据分析平台整合
4. 实验室信息系统

---

## 🎉 您现在拥有

✅ 完整的LNP设计工具  
✅ 7种DOE方法  
✅ 3个3D可视化  
✅ 自动体积计算  
✅ 多格式导出  
✅ 详细文档  
✅ 生产就绪代码  

**立即开始设计您的LNP配方！**

---

Quick Reference v1.0  
Updated: December 6, 2025  
Status: ✅ Ready
