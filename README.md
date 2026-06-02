# 金融数据可视化分析平台

一个基于 **Python Flask** 的金融数据可视化分析平台，展示如何使用 **Plotly** 进行交互式金融数据可视化。数据通过 **yfinance** 从 Yahoo Finance 实时获取，无需本地数据文件。

**在线演示**: https://finviz-platform.onrender.com

---

## 📋 项目概述

本项目是一个金融数据可视化课程作业，主要展示：

- **数据获取**：使用 yfinance 从 Yahoo Finance 实时获取股票/ETF历史数据
- **数据处理**：使用 pandas 进行数据清洗、筛选和分析
- **可视化展示**：使用 Plotly 实现 11 种交互式图表
- **后端架构**：Flask RESTful API 提供数据接口
- **前端交互**：原生 JavaScript + Plotly.js 实现动态交互

### 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Flask** | Web 后端框架 | 3.0.0 |
| **pandas** | 数据处理分析 | 2.2.1 |
| **NumPy** | 数值计算 | 1.26.2 |
| **yfinance** | Yahoo Finance 数据获取 | ≥0.2.36 |
| **Plotly** | 交互式可视化 | 5.18.0 |
| **Matplotlib** | 传统图表渲染 | 3.8.2 |
| **Seaborn** | 统计图表美化 | 0.13.0 |
| **scikit-learn** | 机器学习预测 | 1.3.2 |
| **SciPy** | 科学计算统计 | 1.11.4 |
| **Flask-CORS** | 跨域资源共享 | 4.0.0 |
| **Gunicorn** | 生产环境 WSGI 服务器 | ≥21.2.0 |

---

## 📊 数据获取技术详解

### 1. 数据源

项目使用 **yfinance** 库从 Yahoo Finance 获取实时股票数据，无需本地存储数据文件。

### 2. 核心代码实现

**数据处理器** (`data_processor.py`)：

```python
class FinancialDataProcessor:
    def load_from_yfinance(self, symbol: str, period: str = "5y") -> pd.DataFrame:
        """从 Yahoo Finance 加载股票数据"""
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        # 重置索引，将日期从索引变为列
        df = df.reset_index()
        # 移除时区信息，避免跨时区问题
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        # 只保留必要的6列
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df[required_columns]
        # 按日期排序
        df = df.sort_values('Date').reset_index(drop=True)
        
        self.data = df
        self.filtered_data = df.copy()
        return self.data
```

### 3. 数据结构

获取的数据包含 **6 个核心字段**：

| 字段 | 数据类型 | 说明 | 示例 |
|------|---------|------|------|
| **Date** | datetime64 | 交易日期（无时区） | 2024-01-15 |
| **Open** | float64 | 开盘价（美元） | 185.32 |
| **High** | float64 | 最高价（美元） | 187.50 |
| **Low** | float64 | 最低价（美元） | 184.20 |
| **Close** | float64 | 收盘价（美元） | 186.75 |
| **Volume** | int64 | 成交量（股） | 52,341,200 |

### 4. 支持的数据周期

| 参数 | 说明 | 数据条数（约） |
|------|------|---------------|
| `1d` | 最近1天 | 1 |
| `5d` | 最近5天 | 5 |
| `1mo` | 最近1个月 | 22 |
| `3mo` | 最近3个月 | 66 |
| `6mo` | 最近6个月 | 132 |
| `1y` | 最近1年 | 252 |
| `2y` | 最近2年 | 504 |
| `5y` | 最近5年（默认） | 1260 |
| `10y` | 最近10年 | 2520 |
| `max` | 全部历史数据 | 依股票上市时间 |

### 5. 支持的股票/ETF

**ETF基金（25只）**：
- 宽基指数：SPY（标普500）、QQQ（纳斯达克100）、VTI（整体股市）、IVV（标普500）
- 行业ETF：XLE（能源）、XLF（金融）、XLV（医疗）、XLK（科技）、XLY（非必需消费）、XLP（必需消费）、XLI（工业）
- 主题ETF：SMH（半导体）、SOXX（费城半导体）、VGT（信息技术）
- 债券黄金：GLD（黄金）、BND（债券）
- 国际市场：VEA（发达市场）、VWO（新兴市场）、EFA、EEM、IWM

**个股（45只）**：
- 科技巨头：AAPL、MSFT、GOOGL、GOOG、AMZN、TSLA、META、NVDA、AMD、NFLX
- 中国概念股：BABA、JD、PDD、BIDU
- 金融银行：JPM、BAC、C、WFC、GS、MS、V、MA
- 其他：PFE、KO、PEP、NKE、UPS 等

---

## 📈 可视化技术实现

### 1. 可视化架构

项目使用 **Plotly** 作为主要可视化库，其优势包括：

- **交互性强**：支持缩放、平移、悬停提示
- **无需刷新**：动态更新图表
- **多图表支持**：支持超过 40 种图表类型
- **导出方便**：支持 PNG、SVG、PDF 等格式

### 2. 11种图表类型详解

#### 2.1 K线图（Candlestick Chart）

**用途**：展示股票的开盘价、收盘价、最高价、最低价

**核心代码**：
```python
def plot_kline(self, data: pd.DataFrame, title: str = "K线图") -> str:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, row_heights=[0.7, 0.3])
    
    # K线主体
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#00da3c',  # 上涨绿色
        decreasing_line_color='#ec0000'   # 下跌红色
    ), row=1, col=1)
    
    # 成交量副图
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], 
                         marker_color='#3a7bd5', opacity=0.7), row=2, col=1)
    
    return fig.to_json(engine='json')
```

**视觉效果**：
- 上方面板：K线图，红涨绿跌
- 下方面板：成交量柱状图

---

#### 2.2 折线图（Line Chart）

**用途**：展示价格趋势，支持多条线叠加

**核心代码**：
```python
def plot_line_chart(self, data: pd.DataFrame, title: str = "价格走势图") -> str:
    fig = go.Figure()
    
    # 收盘价线
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name='收盘价',
        line=dict(color='#00d2ff', width=2),
        fill='tozeroy',  # 填充到零轴
        fillcolor='rgba(0, 210, 255, 0.2)'
    ))
    
    # 开盘价线
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Open'],
        mode='lines',
        name='开盘价',
        line=dict(color='#f39c12', width=2),
        fill='tonexty',
        fillcolor='rgba(243, 156, 18, 0.1)'
    ))
    
    return fig.to_json(engine='json')
```

---

#### 2.3 柱状图（Bar Chart）

**用途**：展示交易量分布

**核心代码**：
```python
def plot_bar_chart(self, data: pd.DataFrame, title: str = "交易量柱状图") -> str:
    recent_data = data.tail(50)  # 只显示最近50天
    
    fig = go.Figure()
    colors = ['#00da3c' if recent_data.iloc[i]['Close'] >= recent_data.iloc[i]['Open'] 
              else '#ec0000' for i in range(len(recent_data))]
    
    fig.add_trace(go.Bar(
        x=recent_data['Date'],
        y=recent_data['Volume'],
        marker_color=colors,
        opacity=0.8
    ))
    
    return fig.to_json(engine='json')
```

---

#### 2.4 面积图（Area Chart）

**用途**：展示价格区间面积

**核心代码**：
```python
def plot_area_chart(self, data: pd.DataFrame, title: str = "面积图") -> str:
    fig = go.Figure()
    
    # 高价区域
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['High'],
        mode='lines',
        name='最高价',
        line=dict(color='#00da3c'),
        fill=None
    ))
    
    # 低价区域（填充）
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Low'],
        mode='lines',
        name='最低价',
        line=dict(color='#ec0000'),
        fill='tonexty',
        fillcolor='rgba(236, 0, 0, 0.3)'
    ))
    
    return fig.to_json(engine='json')
```

---

#### 2.5 散点图（Scatter Plot）

**用途**：展示涨跌幅分布

**核心代码**：
```python
def plot_scatter(self, data: pd.DataFrame, title: str = "散点图") -> str:
    # 计算日收益率
    data['Returns'] = data['Close'].pct_change() * 100
    
    fig = px.scatter(
        data,
        x='Date',
        y='Returns',
        color='Returns',
        color_continuous_scale='RdYlGn',  # 红跌绿涨
        title=title
    )
    
    return fig.to_json(engine='json')
```

---

#### 2.6 热力图（Heatmap）

**用途**：展示价格相关性

**核心代码**：
```python
def plot_heatmap(self, data: pd.DataFrame, title: str = "相关性热力图") -> str:
    # 计算各列相关性矩阵
    corr_matrix = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        text=corr_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10}
    ))
    
    return fig.to_json(engine='json')
```

---

#### 2.7 箱线图（Box Plot）

**用途**：展示月度价格分布

**核心代码**：
```python
def plot_boxplot(self, data: pd.DataFrame, title: str = "箱线图") -> str:
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    
    fig = go.Figure()
    for month in range(1, 13):
        month_data = data[data['Month'] == month]['Close']
        if len(month_data) > 0:
            fig.add_trace(go.Box(
                y=month_data,
                name=f'{month}月',
                boxpoints='outliers'
            ))
    
    return fig.to_json(engine='json')
```

---

#### 2.8 饼图（Pie Chart）

**用途**：展示年度涨跌天数比例

**核心代码**：
```python
def plot_pie_chart(self, data: pd.DataFrame, title: str = "饼图") -> str:
    data['Up'] = (data['Close'] > data['Open']).astype(int)
    up_days = data['Up'].sum()
    down_days = len(data) - up_days
    
    fig = go.Figure(data=[go.Pie(
        labels=['上涨天数', '下跌天数'],
        values=[up_days, down_days],
        hole=0.6,  # 环形图
        marker=dict(colors=['#00da3c', '#ec0000'])
    )])
    
    return fig.to_json(engine='json')
```

---

#### 2.9 技术指标图（Technical Indicators）

**用途**：展示均线和技术指标

**核心代码**：
```python
def plot_technical_indicators(self, data: pd.DataFrame, ma_window: int = 20) -> str:
    # 计算移动平均线
    data['MA'] = data['Close'].rolling(window=ma_window).mean()
    
    fig = make_subplots(rows=3, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.05,
                       row_heights=[0.5, 0.25, 0.25])
    
    # 价格和均线
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], 
                             name='收盘价', line=dict(color='blue')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MA'], 
                             name=f'MA{ma_window}', line=dict(color='orange')),
                  row=1, col=1)
    
    # MACD
    data['EMA12'] = data['Close'].ewm(span=12).mean()
    data['EMA26'] = data['Close'].ewm(span=26).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], 
                             name='MACD', line=dict(color='purple')),
                  row=2, col=1)
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    fig.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], 
                             name='RSI', line=dict(color='green')),
                  row=3, col=1)
    
    return fig.to_json(engine='json')
```

---

#### 2.10 分布直方图（Distribution Histogram）

**用途**：展示价格分布

**核心代码**：
```python
def plot_distribution(self, data: pd.DataFrame, title: str = "价格分布") -> str:
    fig = make_subplots(rows=1, cols=2)
    
    # 收盘价分布
    fig.add_trace(go.Histogram(
        x=data['Close'],
        name='收盘价分布',
        marker_color='#3a7bd5',
        opacity=0.75
    ), row=1, col=1)
    
    # 成交量分布
    fig.add_trace(go.Histogram(
        x=data['Volume'],
        name='成交量分布',
        marker_color='#f39c12',
        opacity=0.75
    ), row=1, col=2)
    
    return fig.to_json(engine='json')
```

---

#### 2.11 收益率分布图（Returns Distribution）

**用途**：展示收益率分布和正态性检验

**核心代码**：
```python
def plot_returns_distribution(self, data: pd.DataFrame, title: str = "收益率分布") -> str:
    data['Returns'] = data['Close'].pct_change() * 100
    returns = data['Returns'].dropna()
    
    fig = make_subplots(rows=1, cols=2)
    
    # 收益率直方图
    fig.add_trace(go.Histogram(
        x=returns,
        name='日收益率',
        marker_color='#00da3c' if returns.mean() > 0 else '#ec0000',
        opacity=0.75
    ), row=1, col=1)
    
    # Q-Q图（正态性检验）
    from scipy import stats
    sorted_returns = np.sort(returns)
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(returns)))
    
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sorted_returns,
        mode='markers',
        name='Q-Q图',
        marker=dict(color='#3a7bd5')
    ), row=1, col=2)
    
    return fig.to_json(engine='json')
```

---

## 🔌 API 接口设计

项目提供 18 个 RESTful API 接口：

### 数据接口

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/data/sources` | GET | 获取所有股票/ETF列表 | 无 |
| `/api/data/load` | POST | 加载股票数据 | source, start_date?, end_date? |
| `/api/data/statistics` | GET | 获取统计数据 | 无 |
| `/api/data/filter` | POST | 按日期筛选数据 | start_date, end_date |
| `/api/data/range` | GET | 获取数据日期范围 | symbol |
| `/api/data/raw` | GET | 获取原始数据 | limit（默认100） |
| `/api/data/upload` | POST | 上传本地CSV数据 | file |
| `/api/data/export` | GET | 导出筛选后的数据 | 无 |

### 可视化接口

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/visualize/kline` | POST | K线图 | 无 |
| `/api/visualize/line` | POST | 折线图 | 无 |
| `/api/visualize/bar` | POST | 柱状图 | 无 |
| `/api/visualize/area` | POST | 面积图 | 无 |
| `/api/visualize/scatter` | POST | 散点图 | 无 |
| `/api/visualize/heatmap` | POST | 热力图 | 无 |
| `/api/visualize/boxplot` | POST | 箱线图 | 无 |
| `/api/visualize/pie` | POST | 饼图 | 无 |
| `/api/visualize/technical` | POST | 技术指标图 | 无 |
| `/api/visualize/distribution` | POST | 分布直方图 | 无 |
| `/api/visualize/returns` | POST | 收益率分布图 | 无 |

### 示例响应

**加载数据** (`/api/data/load`)：
```json
{
  "success": true,
  "count": 1260,
  "date_range": {
    "start": "2021-06-02",
    "end": "2026-06-02"
  }
}
```

**获取K线图** (`/api/visualize/kline`)：
```json
{
  "success": true,
  "chart": {
    "data": [...],
    "layout": {...}
  }
}
```

---

## 📁 项目目录结构

```
finviz-platform/
├── app.py                      # Flask 应用主入口
├── data_processor.py           # 数据处理模块
├── visualizer.py               # 可视化图表生成模块
├── predictor.py                # 机器学习预测模块
├── requirements.txt             # Python 依赖清单
├── README.md                    # 项目说明文档
├── DEPLOYMENT.md               # 部署指南
├── index_python.html           # 前端主页面
├── style.css                   # 样式表
├── app_python.js               # 前端 JavaScript
└── .gitignore                  # Git 忽略配置
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/finviz-platform.git
cd finviz-platform

# 安装依赖
pip install -r requirements.txt
```

### 运行项目

```bash
# 本地运行
python app.py

# 访问 http://localhost:5000
```

### 部署到 Render（免费）

1. 将代码推送到 GitHub
2. 登录 [Render](https://render.com)
3. 点击 **New → Web Service**
4. 连接 GitHub 仓库
5. 配置构建命令：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. 点击 **Create Web Service**
7. 等待部署完成（约2-3分钟）

---

## 💡 使用指南

### 1. 选择数据源

- 在左侧面板的「数据源分类」中选择 **ETF基金** 或 **个股**
- 在「选择数据源」中选择具体的股票代码

### 2. 选择可视化类型

提供 11 种可视化图表：

- **K线图**：显示OHLC价格和成交量
- **折线图**：显示价格走势
- **柱状图**：显示交易量分布
- **面积图**：显示价格区间
- **散点图**：显示涨跌幅分布
- **热力图**：显示数据相关性
- **箱线图**：显示月度分布
- **饼图**：显示涨跌比例
- **技术指标**：显示MA、MACD、RSI
- **分布图**：显示价格分布
- **收益率**：显示收益率分布和正态性

### 3. 时间筛选

- 选择开始和结束日期
- 点击「应用筛选」获取指定时间段的数据
- 系统会显示该股票的最早可获取日期

---

## 📊 功能特点

### 数据获取

- ✅ 实时从 Yahoo Finance 获取数据
- ✅ 支持47只预定义股票/ETF
- ✅ 支持自定义日期范围
- ✅ 显示股票最早上市日期

### 可视化展示

- ✅ 11种交互式图表
- ✅ 深色主题设计
- ✅ 缩放、平移、悬停交互
- ✅ 响应式布局

### 技术实现

- ✅ RESTful API 设计
- ✅ CORS 跨域支持
- ✅ 数据缓存机制
- ✅ 错误处理完善

---

## 🛠️ 技术细节

### 数据处理流程

```
1. 用户选择股票/ETF
   ↓
2. 前端发送 POST /api/data/load 请求
   ↓
3. 后端调用 yfinance 获取数据
   ↓
4. 数据处理：重置索引、时区处理、列筛选、排序
   ↓
5. 返回成功响应和日期范围
   ↓
6. 前端更新图表和统计信息
```

### 可视化生成流程

```
1. 用户选择图表类型
   ↓
2. 前端发送 POST /api/visualize/{chart_type} 请求
   ↓
3. 后端从缓存读取数据
   ↓
4. 使用 Plotly 生成图表
   ↓
5. 返回 JSON 格式的图表数据
   ↓
6. 前端使用 Plotly.js 渲染图表
```

### 数据缓存机制

- 数据加载后存储在服务器内存
- 筛选操作直接使用缓存数据
- 无需重复请求 Yahoo Finance

---

## ⚠️ 注意事项

1. **网络要求**：需要稳定的网络连接才能获取 Yahoo Finance 数据
2. **请求限制**：Yahoo Finance 可能有请求频率限制，避免频繁刷新
3. **数据延迟**：数据可能有15-20分钟的延迟
4. **历史数据**：部分股票的历史数据可能不完整

---

## 📝 License

MIT License

---

## 🙏 致谢

- [Yahoo Finance](https://finance.yahoo.com/) - 提供股票数据
- [Plotly](https://plotly.com/) - 提供交互式可视化
- [yfinance](https://github.com/ranaroussi/yfinance) - Python 数据获取库

---

**课程作业项目 - Python 数据可视化技术**
