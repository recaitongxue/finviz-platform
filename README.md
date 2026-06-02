# 金融数据可视化分析平台

基于 Python Flask + Plotly 构建的金融时间序列数据可视化分析平台，支持**实时数据获取**、多样化图表展示、统计分析和机器学习预测。

---

## 📁 项目结构

```
finviz-platform/
├── app.py                 # Flask后端API服务（核心）
├── data_processor.py      # 数据处理模块（支持yfinance）
├── visualizer.py          # 可视化模块(Plotly)
├── predictor.py           # 机器学习预测模块
├── requirements.txt       # Python依赖清单
├── index_python.html      # 前端页面
├── app_python.js          # 前端JavaScript逻辑
├── style.css              # 样式文件
└── Data/                  # 预留数据目录（可选本地数据）
    └── .gitkeep           # Git占位文件
```

---

## ✨ 主要更新

### 🔥 新增功能
- ✅ **实时数据获取** - 使用 yfinance 从 Yahoo Finance 实时获取股票数据
- ✅ **无需本地数据文件** - 不再依赖庞大的 CSV 数据文件
- ✅ **支持 47+ 只股票/ETF** - 预定义热门股票和指数基金

### 🗑️ 移除依赖
- 不再需要 `Data/ETFs/` 和 `Data/Stocks/` 目录
- 数据文件无需上传到 GitHub

---

## 📸 界面预览

以下是平台的主要功能界面截图：

![平台界面预览](image/README/1780403497096.png)

---

## 📊 数据来源

### 实时数据获取

平台使用 **yfinance** 库从 Yahoo Finance 获取实时股票数据：

| 数据类型 | 来源 | 更新频率 |
|----------|------|----------|
| 股票价格 | Yahoo Finance | 实时 |
| ETF数据 | Yahoo Finance | 实时 |
| 技术指标 | 本地计算 | 实时 |

### 支持的股票/ETF

**ETF基金**：SPY(标普500)、QQQ(纳斯达克100)、XLE(能源)、XLF(金融)、XLV(医疗)等 24 只

**个股**：AAPL(苹果)、MSFT(微软)、TSLA(特斯拉)、NVDA(英伟达)、GOOGL(谷歌)等 23 只

---

## 🛠️ 技术栈

### 后端技术

| 技术 | 版本 | 用途 | 核心功能 |
|------|------|------|----------|
| Python | 3.8+ | 编程语言 | 核心业务逻辑 |
| Flask | 3.0+ | Web框架 | RESTful API服务 |
| Flask-CORS | 4.0+ | 跨域支持 | 前端跨域请求 |
| pandas | 2.1+ | 数据处理 | 数据清洗、转换、分析 |
| numpy | 1.26+ | 数值计算 | 矩阵运算、统计分析 |
| scikit-learn | 1.3+ | 机器学习 | 预测模型训练 |
| plotly | 5.18+ | 可视化库 | 交互式图表生成 |
| **yfinance** | 0.2+ | 数据获取 | 从Yahoo Finance获取实时数据 |

### 前端技术

| 技术 | 用途 | 核心功能 |
|------|------|----------|
| HTML5 | 页面结构 | 布局与组件定义 |
| CSS3 | 样式设计 | 响应式布局、深色主题 |
| JavaScript ES6+ | 交互逻辑 | API调用、图表渲染、用户交互 |
| Plotly.js | 图表渲染 | 交互式可视化展示 |

---

## 🎯 功能特性

### 1. 实时数据获取
- ✅ 从 Yahoo Finance 实时获取股票数据
- ✅ 支持 47+ 只预定义股票/ETF
- ✅ 自动分类展示（ETF基金/个股）

### 2. 多样化可视化图表

| 图表类型 | 说明 | 数据维度 |
|----------|------|----------|
| 📈 **K线图** | 蜡烛图展示OHLC数据 | Date, Open, High, Low, Close, Volume |
| 📉 **折线图** | 收盘价/开盘价趋势 | Date, Open, Close |
| 📊 **柱状图** | 交易量展示 | Date, Volume |
| 📋 **面积图** | 最高价/最低价区间 | Date, High, Low |
| 🔵 **散点图** | 交易量vs收盘价相关性 | Volume, Close |
| 🗺️ **热力图** | 特征相关性矩阵 | Open, High, Low, Close, Volume |
| 📦 **箱线图** | 月度价格分布 | Month, Close |
| 🥧 **饼图** | 月度交易量占比 | Month, Volume |
| 📈 **技术指标** | MA/收益率/交易量综合 | Date, Close, MA, Returns |
| 📊 **分布直方图** | 价格与交易量分布 | Close, Volume |
| 📊 **收益率分布** | 收益率直方图+Q-Q图 | Returns |

### 3. 统计分析
- ✅ 数据条数统计
- ✅ 平均收盘价
- ✅ 最高/最低收盘价
- ✅ 平均交易量
- ✅ 波动率计算

### 4. 时间筛选
- ✅ 开始/结束日期选择
- ✅ 实时数据过滤

### 5. 机器学习预测
- ✅ 线性回归预测
- ✅ 随机森林预测
- ✅ 梯度提升预测
- ✅ 集成模型预测
- ✅ 置信区间估计

---

## 🔧 安装与运行

### 环境要求
- Python 3.8+
- Windows 10/11 或 Linux/Mac

### 安装步骤

1. **进入项目目录**
```bash
cd finviz-platform
```

2. **创建并激活虚拟环境**
```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **启动服务**
```bash
python app.py
```

5. **访问应用**
打开浏览器访问：http://localhost:5000

---

## 🚀 部署到云端

### 推荐平台

| 平台 | 免费额度 | 适合项目 |
|------|---------|---------|
| **Render** | 750小时/月 | Flask 后端 ✅ |
| **Railway** | $5/月 | Flask 后端 ✅ |
| **Vercel** | 无限 | 纯前端 |

### 部署步骤（Render为例）

1. **推送到 GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/finviz-platform.git
git push -u origin main
```

2. **连接 Render**
- 访问 https://render.com
- 新建 Web Service
- 选择 GitHub 仓库
- 配置：
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app`

3. **启动服务**
- Render 会自动构建并部署
- 获取访问 URL

---

## 🌐 API接口说明

### 数据源管理

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/data/sources` | GET | 获取所有数据源分类 | 无 |
| `/api/data/load` | POST | 加载指定数据源 | `source`: 股票代码（如 spy, aapl） |
| `/api/data/range` | GET | 获取数据日期范围 | 无 |
| `/api/data/filter` | POST | 按日期筛选数据 | `start_date`, `end_date` |
| `/api/data/statistics` | GET | 获取统计指标 | 无 |

### 可视化接口

| 接口 | 方法 | 说明 | 返回格式 |
|------|------|------|----------|
| `/api/visualize/kline` | POST | K线图 | JSON(Plotly) |
| `/api/visualize/line` | POST | 折线图 | JSON(Plotly) |
| `/api/visualize/bar` | POST | 柱状图 | JSON(Plotly) |
| `/api/visualize/area` | POST | 面积图 | JSON(Plotly) |
| `/api/visualize/scatter` | POST | 散点图 | JSON(Plotly) |
| `/api/visualize/heatmap` | POST | 热力图 | JSON(Plotly) |
| `/api/visualize/boxplot` | POST | 箱线图 | JSON(Plotly) |
| `/api/visualize/pie` | POST | 饼图 | JSON(Plotly) |
| `/api/visualize/technical` | POST | 技术指标图 | JSON(Plotly) |
| `/api/visualize/distribution` | POST | 分布直方图 | JSON(Plotly) |
| `/api/visualize/returns` | POST | 收益率分布图 | JSON(Plotly) |

### 预测接口

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/predict` | POST | 执行预测 | `days`: 预测天数, `model`: 模型类型 |

### 请求示例

**加载数据源**
```bash
curl -X POST http://localhost:5000/api/data/load \
  -H "Content-Type: application/json" \
  -d '{"source": "spy"}'
```

**日期筛选**
```bash
curl -X POST http://localhost:5000/api/data/filter \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2021-01-01", "end_date": "2026-06-01"}'
```

**生成K线图**
```bash
curl -X POST http://localhost:5000/api/visualize/kline
```

**执行预测**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"days": 30, "model": "ensemble"}'
```

---

## 📈 可视化技术实现

### 核心架构

```
┌─────────────────────────────────────────────────────┐
│                    系统架构                          │
├─────────────────────────────────────────────────────┤
│  前端 (Plotly.js)                                  │
│  ┌─────────────────────────────────────────────┐    │
│  │ 图表渲染层: Plotly.newPlot()                │    │
│  │ 交互层: 缩放、平移、悬停提示、图例切换       │    │
│  └─────────────────────────────────────────────┘    │
│                          ↓ JSON                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ 后端 (Flask + Plotly Python)                │    │
│  │ 图表生成层: FinancialVisualizer类           │    │
│  │ 数据处理层: FinancialDataProcessor类        │    │
│  └─────────────────────────────────────────────┘    │
│                          ↓ API                       │
│  ┌─────────────────────────────────────────────┐    │
│  │ 数据源: Yahoo Finance (yfinance)            │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### 数据加载流程

```
用户选择股票 → API请求 → yfinance获取数据 → 数据处理 → 返回前端
     ↓
用户选择图表类型 → API请求 → 生成图表JSON → 返回前端渲染
```

---

## 🔒 安全特性

| 安全措施 | 说明 |
|----------|------|
| 数据验证 | 验证股票代码有效性 |
| 异常处理 | 统一错误响应格式 |
| CORS跨域控制 | 配置允许的来源 |
| 请求参数检查 | 验证日期格式等 |

---

## 📝 配置说明

### 股票名称映射 (`app.py`)

```python
STOCK_NAMES = {
    'spy': '标普500ETF',
    'qqq': '纳斯达克100ETF',
    'aapl': '苹果公司',
    # ... 更多映射
}
```

### 添加新股票

只需在 `STOCK_NAMES` 字典中添加新的股票代码和中文名称即可。

---

## 🐛 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 数据加载失败 | 网络问题或股票代码错误 | 检查网络连接，确认股票代码正确 |
| 图表不显示 | Plotly JSON格式问题 | 检查浏览器控制台错误 |
| API请求失败 | 服务器未启动 | 确保 Flask 服务正在运行 |
| yfinance安装失败 | 网络问题 | 使用国内PyPI镜像或检查网络 |

---

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**项目版本**: v2.0 (支持 yfinance)  
**最后更新**: 2026年  
**作者**: Financial Data Analysis Team