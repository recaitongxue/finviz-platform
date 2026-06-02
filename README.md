# 金融数据可视化技术

本项目是一个基于 Python 的金融数据可视化分析平台，展示如何使用 **Plotly** 进行交互式数据可视化，数据通过 **yfinance** 从 Yahoo Finance 实时获取。

---

## 一、项目概述

### 课程目标

- 掌握 Python 数据可视化技术（Plotly）
- 理解金融时间序列数据的获取与处理
- 实现多种图表类型的交互式展示

### 技术亮点

- ✅ 使用 yfinance 实时获取股票数据
- ✅ 基于 Plotly 实现 11 种交互式图表
- ✅ Flask 后端提供 RESTful API
- ✅ 深色主题可视化设计

---

## 二、数据获取技术

### 2.1 数据源

项目使用 **yfinance** 库从 Yahoo Finance 获取实时股票数据：

```python
import yfinance as yf

# 获取 SPY 股票数据（5年历史）
ticker = yf.Ticker('SPY')
df = ticker.history(period='5y')
```

### 2.2 获取的数据结构

获取的数据包含 **6 个核心字段**：

| 字段   | 类型       | 说明           |
| ------ | ---------- | -------------- |
| Date   | datetime64 | 日期（无时区） |
| Open   | float64    | 开盘价         |
| High   | float64    | 最高价         |
| Low    | float64    | 最低价         |
| Close  | float64    | 收盘价         |
| Volume | int64      | 交易量         |

### 2.3 数据处理流程

```
yfinance获取 → 重置索引 → 时区处理 → 列筛选 → 排序 → 存储
```

核心处理代码（`data_processor.py`）：

```python
def load_from_yfinance(self, symbol: str, period: str = "5y") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
  
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
  
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df[required_columns]
  
    df = df.sort_values('Date')
    df = df.reset_index(drop=True)
  
    return df
```

### 2.4 支持的股票/ETF

**ETF基金（24只）**：SPY、QQQ、XLE、XLF、XLV、XLK、XLP、XLY、XLI、XLU、VTI、VEA、VWO、BND、GLD、SLV、USO、UNG、EFA、EEM、IWM、MDY、DVY、SDY

**个股（23只）**：AAPL、MSFT、GOOGL、GOOG、AMZN、TSLA、META、NVDA、AMD、NFLX、BABA、JD、PDD、BIDU、TCEHY、JPM、BAC、C、WFC、GS、MS、V、MA

---

## 三、可视化技术实现

### 3.1 可视化库

项目主要使用 **Plotly** 进行交互式可视化，辅以 matplotlib 和 seaborn：

| 库                   | 用途         | 特点       |
| -------------------- | ------------ | ---------- |
| plotly.graph_objects | 核心图表对象 | 高度可定制 |
| plotly.express       | 快速图表生成 | 简洁API    |
| plotly.subplots      | 子图布局     | 多图组合   |
| matplotlib           | 备用渲染     | 传统绘图   |
| seaborn              | 统计图表     | 美观样式   |

### 3.2 图表类型及实现

#### 1. K线图（Candlestick Chart）

**技术实现**：使用 `plotly.graph_objects.Candlestick`

```python
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03)

fig.add_trace(go.Candlestick(
    x=data['Date'],
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    increasing_line_color='#00da3c',   # 上涨绿色
    decreasing_line_color='#ec0000'    # 下跌红色
), row=1, col=1)

fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Volume'],
    marker_color='#3a7bd5'
), row=2, col=1)
```

**功能特点**：双面板布局，上方显示 K线，下方显示交易量

#### 2. 折线图（Line Chart）

**技术实现**：使用 `plotly.graph_objects.Scatter`

```python
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Close'],
    mode='lines',
    line=dict(color='#00d2ff', width=2),
    fill='tozeroy',
    fillcolor='rgba(0, 210, 255, 0.2)'
))
```

**功能特点**：叠加开盘价和收盘价，带渐变填充效果

#### 3. 柱状图（Bar Chart）

**技术实现**：使用 `plotly.graph_objects.Bar`

```python
colors = ['#00da3c' if close >= open else '#ec0000' for ...]

fig.add_trace(go.Bar(
    x=data['Date'],
    y=data['Volume'],
    marker_color=colors,
    opacity=0.8
))
```

**功能特点**：根据涨跌动态着色，仅显示最近50条数据

#### 4. 面积图（Area Chart）

**技术实现**：使用 `plotly.graph_objects.Scatter` 的 `fill` 参数

```python
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['High'],
    mode='lines',
    fill=None
))
fig.add_trace(go.Scatter(
    x=data['Date'],
    y=data['Low'],
    mode='lines',
    fill='tonexty',
    fillcolor='rgba(52, 152, 219, 0.2)'
))
```

**功能特点**：展示最高价与最低价之间的区域

#### 5. 散点图（Scatter Plot）

**技术实现**：使用 `plotly.express.scatter`

```python
fig = px.scatter(
    data,
    x='Volume',
    y='Close',
    color=data['Close'].pct_change().fillna(0),
    color_continuous_scale='RdYlGn'
)
```

**功能特点**：颜色映射涨跌幅，展示交易量与收盘价的相关性

#### 6. 相关性热力图（Heatmap）

**技术实现**：使用 `plotly.graph_objects.Heatmap`

```python
corr_matrix = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()

fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}'
))
```

**功能特点**：展示5个数值字段之间的相关性

#### 7. 箱线图（Boxplot）

**技术实现**：使用 `plotly.graph_objects.Box`

```python
data['Month'] = data['Date'].dt.month
monthly_data = data.groupby('Month')['Close'].apply(list)

for month in range(1, 13):
    fig.add_trace(go.Box(
        y=monthly_data[month],
        name=f'{month}月',
        boxpoints='outliers'
    ))
```

**功能特点**：按月份分组，展示收盘价的分布特征

#### 8. 饼图（Pie Chart）

**技术实现**：使用 `plotly.graph_objects.Pie`

```python
data['Month'] = data['Date'].dt.to_period('M')
monthly_volume = data.groupby('Month')['Volume'].sum().tail(8)

fig = go.Figure(data=[go.Pie(
    labels=[str(m) for m in monthly_volume.index],
    values=monthly_volume.values,
    hole=0.3,
    textinfo='label+percent'
)])
```

**功能特点**：环形饼图，展示最近8个月交易量占比

#### 9. 技术指标分析图

**技术实现**：多面板子图布局

```python
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.5, 0.25, 0.25])

data['MA'] = data['Close'].rolling(window=20).mean()
data['Returns'] = data['Close'].pct_change() * 100

# 面板1：收盘价 + 均线
# 面板2：涨跌幅柱状图
# 面板3：交易量折线图
```

**功能特点**：三面板展示，包含均线、涨跌幅、交易量

#### 10. 分布直方图（Distribution）

**技术实现**：使用 `plotly.graph_objects.Histogram`

```python
fig = make_subplots(rows=1, cols=2, subplot_titles=('收盘价分布', '交易量分布'))

fig.add_trace(go.Histogram(
    x=data['Close'],
    nbinsx=30,
    marker_color='#00d2ff'
), row=1, col=1)
```

**功能特点**：双面板对比收盘价和交易量的分布

#### 11. 收益率分布图（Returns Distribution）

**技术实现**：结合直方图和 Q-Q 图

```python
returns = data['Close'].pct_change().dropna() * 100

# 直方图
fig.add_trace(go.Histogram(x=returns, nbinsx=50), row=1, col=1)

# Q-Q图（正态分布检验）
from scipy import stats
theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(returns)))
fig.add_trace(go.Scatter(x=theoretical_quantiles, y=sample_quantiles), row=1, col=2)
```

**功能特点**：检验收益率是否符合正态分布

### 3.3 可视化设计特点

| 设计要素   | 实现方式                       |
| ---------- | ------------------------------ |
| 主题风格   | plotly_dark 深色主题           |
| 配色方案   | 绿色上涨、红色下跌、蓝色中性   |
| 交互功能   | 缩放、平移、悬停提示、图例切换 |
| 响应式布局 | 自适应高度、子图间距优化       |

---

## 四、项目结构

```
finviz-platform/
├── app.py                 # Flask后端API（核心路由）
├── data_processor.py      # 数据处理模块（yfinance获取）
├── visualizer.py          # 可视化模块（Plotly图表生成）
├── predictor.py           # 机器学习预测模块（可选）
├── requirements.txt       # Python依赖清单
├── index_python.html      # 前端页面
├── app_python.js          # 前端交互逻辑
└── style.css              # 样式文件
```

### 4.1 核心文件说明

| 文件              | 功能            | 核心类/函数            |
| ----------------- | --------------- | ---------------------- |
| app.py            | RESTful API服务 | Flask路由定义          |
| data_processor.py | 数据获取与处理  | FinancialDataProcessor |
| visualizer.py     | 图表生成        | FinancialVisualizer    |
| predictor.py      | 预测模型        | Predictor              |

### 4.2 API接口

| 接口                       | 方法 | 说明               |
| -------------------------- | ---- | ------------------ |
| `/api/data/sources`      | GET  | 获取支持的股票列表 |
| `/api/data/load`         | POST | 加载股票数据       |
| `/api/data/filter`       | POST | 日期筛选           |
| `/api/data/statistics`   | GET  | 统计指标           |
| `/api/visualize/kline`   | POST | 生成K线图          |
| `/api/visualize/line`    | POST | 生成折线图         |
| `/api/visualize/heatmap` | POST | 生成热力图         |
| `/api/predict`           | POST | 执行预测           |

---

## 五、安装与运行

### 5.1 环境要求

- Python 3.8+
- 依赖库：见 `requirements.txt`

### 5.2 安装步骤

```bash
# 克隆项目
cd finviz-platform

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 访问应用
# 浏览器打开: http://localhost:5000
```

### 5.3 依赖清单

| 库           | 版本   | 用途     |
| ------------ | ------ | -------- |
| flask        | >=3.0  | Web框架  |
| flask-cors   | >=4.0  | 跨域支持 |
| pandas       | >=2.1  | 数据处理 |
| numpy        | >=1.26 | 数值计算 |
| plotly       | >=5.18 | 可视化   |
| yfinance     | >=0.2  | 数据获取 |
| scikit-learn | >=1.3  | 机器学习 |

---

## 六、可视化效果展示

### 6.1 K线图效果

K线图展示股票的开盘价、收盘价、最高价、最低价，配合交易量柱状图：

- 绿色实体：收盘价 ≥ 开盘价（上涨）
- 红色实体：收盘价 < 开盘价（下跌）
- 下方柱状图展示对应日期的交易量

### 6.2 技术指标图效果

三面板布局：

- 上：收盘价 + 20日均线
- 中：每日涨跌幅（百分比）
- 下：交易量趋势

### 6.3 相关性热力图效果

展示5个特征之间的皮尔逊相关系数：

- 红色：正相关
- 蓝色：负相关
- 颜色深浅表示相关程度

---

## 七、课程技术要点总结

### 7.1 数据获取技术

- 使用 yfinance 库访问 Yahoo Finance API
- 处理时区信息（tz_localize(None)）
- 数据清洗与标准化

### 7.2 可视化技术

- Plotly 的交互式图表特性
- 子图布局设计（make_subplots）
- 颜色映射与视觉编码
- 图表导出为 JSON 格式供前端渲染

### 7.3 Web技术

- Flask RESTful API 设计
- CORS 跨域配置
- JSON 数据传输


**技术栈**

：Python + Flask + Plotly + yfinance
