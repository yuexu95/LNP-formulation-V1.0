# 🚀 Streamlit 云部署 - 依赖项修复

## 📌 问题诊断

**错误**: `ModuleNotFoundError: No module named 'plotly'`

**原因**: `requirements.txt` 中缺少 `plotly` 和 `openpyxl` 包

**影响页面**: 
- `pages/6_🀄️_High-Throughput_Formulation.py` (第 4 行)
- 其他使用 Plotly 的页面

---

## ✅ 修复方案

### 已添加的依赖项

```
plotly==6.5.0      # 3D 可视化、交互式图表
openpyxl==3.1.5    # Excel 文件导出
```

### requirements.txt 更新

添加到 `requirements.txt`:
```
plotly==6.5.0
openpyxl==3.1.5
```

---

## 🔍 验证

| 包名 | 版本 | 用途 | 状态 |
|------|------|------|------|
| plotly | 6.5.0 | 3D 散点图、热力图 | ✅ 已添加 |
| openpyxl | 3.1.5 | Excel 工作簿操作 | ✅ 已添加 |
| pandas | 2.3.3 | 数据处理 | ✅ 已有 |
| numpy | 2.3.5 | 数值计算 | ✅ 已有 |
| streamlit | 1.51.0 | Web 框架 | ✅ 已有 |

---

## 🚀 部署步骤

1. **更新 requirements.txt**
   ```bash
   git add requirements.txt
   git commit -m "Add plotly and openpyxl dependencies"
   git push
   ```

2. **重新部署 Streamlit Cloud**
   - Streamlit Cloud 会自动检测 `requirements.txt` 变化
   - 自动重新安装依赖项
   - 应用将自动重启

3. **验证部署**
   - 打开应用
   - 导航到 DOE Designer (页面 6)
   - 检查 3D 图表和 Excel 导出功能

---

## 📝 完整依赖列表

所有必需的包现已完整列出：

```
✅ 数据处理: pandas, numpy
✅ 可视化: plotly, altair, pydeck
✅ Web 框架: streamlit
✅ 文件操作: openpyxl, pillow
✅ 数据验证: jsonschema
✅ 工具库: requests, urllib3, six
✅ 其他: 支持库
```

---

## 🔧 本地测试

在本地验证所有依赖项：

```bash
# 激活虚拟环境
source venv312_new/bin/activate

# 安装依赖项
pip install -r requirements.txt

# 运行应用
streamlit run Homepage.py
```

---

## ✨ 功能验证

修复后可用的功能：

- ✅ 3D 设计空间可视化
- ✅ 热力图显示
- ✅ Excel 导出功能
- ✅ CSV 导出功能
- ✅ N/P 比统计显示
- ✅ 所有交互式图表

---

## 📞 故障排除

### 如果仍然出现错误

1. **检查 requirements.txt**
   ```bash
   cat requirements.txt | grep -E "plotly|openpyxl"
   ```
   应该显示:
   ```
   openpyxl==3.1.5
   plotly==6.5.0
   ```

2. **Streamlit Cloud 强制重新部署**
   - 在 Streamlit Cloud 中进入"Settings"
   - 点击"Advanced settings"
   - 选择"Reboot app"

3. **清空缓存**
   - 按 `R` 键（在 Streamlit 应用中）
   - 或清空浏览器缓存

---

## 📊 部署清单

- [x] 添加 `plotly==6.5.0`
- [x] 添加 `openpyxl==3.1.5`
- [x] 更新 `requirements.txt`
- [x] 验证所有导入
- [x] 文档记录

---

## 🎯 下一步

1. **提交更改**
   ```bash
   git add requirements.txt
   git commit -m "Fix: Add missing plotly and openpyxl dependencies"
   git push
   ```

2. **监控部署**
   - 检查 Streamlit Cloud 日志
   - 验证应用启动成功

3. **测试功能**
   - 打开 DOE Designer
   - 生成设计并检查所有功能

---

**状态**: ✅ **已修复**  
**修改文件**: `requirements.txt`  
**添加包**: plotly, openpyxl  
**部署**: 手动（通过 git push）

