# 金融数据可视化分析平台
## Python可视化技术课程答辩

**项目名称**: finviz-platform  
**在线演示**: https://finviz-platform.onrender.com  
**课程**: Python数据可视化技术

---

# 目录

1. 项目概述
2. 数据获取技术
3. 数据处理流程
4. 可视化技术实现
5. 11种图表详解
6. 技术架构设计
7. 功能演示
8. 总结与展望

---

# 一、项目概述

## 1.1 项目背景

本项目是一个**金融数据可视化分析平台**，旨在展示Python数据可视化技术在金融领域的应用。

**核心目标**：
- 掌握数据获取技术（yfinance）
- 理解数据处理流程（pandas）
- 实现多种可视化图表（Plotly）
- 构建完整的Web应用（Flask）

---

## 1.2 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Flask** | Web后端框架 | 3.0.0 |
| **yfinance** | Yahoo Finance数据获取 | ≥0.2.36 |
| **pandas** | 数据处理分析 | 2.2.1 |
| **NumPy** | 数值计算 | 1.26.2 |
| **Plotly** | 交互式可视化 | 5.18.0 |
| **Matplotlib** | 传统图表渲染 | 3.8.2 |
| **Seaborn** | 统计图表美化 | 0.13.0 |
| **scikit-learn** | 机器学习预测 | 1.3.2 |

---

## 1.3 项目特点

✅ **实时数据获取** - 无需本地数据文件  
✅ **11种可视化图表** - 覆盖主流图表类型  
✅ **交互式展示** - 缩放、平移、悬停提示  
✅ **RESTful API** - 18个数据接口  
✅ **深色主题设计** - 专业金融风格  
✅ **免费云端部署** - Render平台托管

---

# 二、数据获取技术

## 2.1 数据源选择

**为什么选择 Yahoo Finance？**

1. **免费开放** - 无需API Key，无请求限制
2. **数据全面** - 覆盖全球70+主要股票/ETF
3. **历史数据** - 支持从上市日至今的完整数据
4. **实时更新** - 数据延迟仅15-20分钟
5. **Python支持** - yfinance库封装完善

---

## 2.2 yfinance库介绍

**yfinance** 是Yahoo Finance的Python封装库：

```python
import yfinance as yf

# 创建股票对象
ticker = yf.Ticker('SPY')

# 获取历史数据
df = ticker.history(period='5y')

# 获取公司信息
info = ticker.info
```

**支持的时间周期**：
- `1d`, `5d`, `1mo`, `3mo`, `6mo`
- `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

---

## 2.3 数据获取核心代码

**实际代码实现** (`data_processor.py`)：

```python
def load_from_yfinance(self, symbol: str, period: str = "5y") -> pd.DataFrame:
    """从Yahoo Finance加载股票数据"""
    
    # 1. 创建Ticker对象
    ticker = yf.Ticker(symbol)
    
    # 2. 获取历史数据
    df = ticker.history(period=period)
    
    # 3. 数据处理（见下一节）
    ...
    
    return df
```

---

## 2.4 获取的数据结构

**返回的DataFrame包含6个核心字段**：

| 字段 | 数据类型 | 说明 | 示例值 |
|------|---------|------|--------|
| **Date** | datetime64 | 交易日期 | 2024-01-15 |
| **Open** | float64 | 开盘价（美元） | 185.32 |
| **High** | float64 | 最高价（美元） | 187.50 |
| **Low** | float64 | 最低价（美元） | 184.20 |
| **Close** | float64 | 收盘价（美元） | 186.75 |
| **Volume** | int64 | 成交量（股） | 52,341,200 |

**这是标准的OHLCV数据格式**

---

## 2.5 支持的股票/ETF

**ETF基金（25只）**：
- 宽基指数：SPY、QQQ、VTI、IVV、IWM
- 行业ETF：XLE、XLF、XLV、XLK、XLY、XLP、XLI
- 主题ETF：SMH、SOXX、VGT
- 债券黄金：GLD、BND、TLT

**个股（45只）**：
- 科技巨头：AAPL、MSFT、GOOGL、AMZN、TSLA、META、NVDA
- 中国概念：BABA、JD、PDD、BIDU
- 金融银行：JPM、BAC、GS、V、MA

---

# 三、数据处理流程

## 3.1 数据处理的重要性

**原始数据存在的问题**：

1. ❌ **日期带时区** - 导致跨时区比较错误
2. ❌ **列名不统一** - yfinance返回9列，我们只需要6列
3. ❌ **日期作为索引** - 不方便后续处理
4. ❌ **未排序** - 可能存在日期混乱

**必须进行标准化处理**

---

## 3.2 数据处理核心代码

**实际代码实现** (`data_processor.py`)：

```python
def load_from_yfinance(self, symbol: str, period: str = "5y"):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    
    # 1. 重置索引（将Date从索引变为列）
    df = df.reset_index()
    
    # 2. 移除时区信息
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    
    # 3. 只保留必要的6列
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df[required_columns]
    
    # 4. 按日期排序
    df = df.sort_values('Date')
    df = df.reset_index(drop=True)
    
    return df
```

---

## 3.3 数据处理流程图

```
yfinance获取原始数据
        ↓
   重置索引（reset_index）
        ↓
   移除时区（tz_localize(None))
        ↓
   列筛选（只保留6列）
        ↓
   日期排序（sort_values）
        ↓
   重置行号（reset_index）
        ↓
   存储到内存（self.data）
```

---

## 3.4 按日期范围获取数据

**支持自定义日期范围**：

```python
def load_from_yfinance_by_date(self, symbol: str, 
                                start_date: str, end_date: str):
    """按日期范围获取数据"""
    
    # 日期验证
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # 获取指定范围数据
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)
    
    # 同样的数据处理流程
    ...
    
    return df
```

**示例**：获取SPY从2000年到今天的数据 → 返回6537条记录

---

# 四、可视化技术实现

## 4.1 为什么选择Plotly？

**Plotly的优势**：

| 特性 | Matplotlib | Plotly |
|------|-----------|--------|
| **交互性** | ❌ 静态图片 | ✅ 缩放、平移、悬停 |
| **Web支持** | ❌ 需转换 | ✅ 直接嵌入HTML |
| **图表数量** | ~20种 | ~40+种 |
| **美观度** | 需配置 | 默认美观 |
| **导出格式** | PNG、PDF | PNG、SVG、PDF、HTML |

**金融数据需要交互式展示**

---

## 4.2 Plotly核心组件

**项目使用的Plotly模块**：

```python
import plotly.graph_objects as go    # 核心图表对象
import plotly.express as px          # 快速图表生成
from plotly.subplots import make_subplots  # 子图布局
```

**核心对象**：
- `go.Figure()` - 图表容器
- `go.Scatter()` - 折线图、散点图
- `go.Bar()` - 柱状图
- `go.Candlestick()` - K线图
- `go.Heatmap()` - 热力图
- `go.Box()` - 箱线图
- `go.Pie()` - 饼图
- `go.Histogram()` - 直方图

---

## 4.3 可视化类设计

**实际代码架构** (`visualizer.py`)：

```python
class FinancialVisualizer:
    def __init__(self):
        # 设置深色主题
        plt.style.use('dark_background')
        sns.set_palette("husl")
    
    # 11种图表方法
    def plot_kline(self, data): ...        # K线图
    def plot_line_chart(self, data): ...   # 折线图
    def plot_bar_chart(self, data): ...    # 柱状图
    def plot_area_chart(self, data): ...   # 面积图
    def plot_scatter(self, data): ...      # 散点图
    def plot_heatmap(self, data): ...      # 热力图
    def plot_boxplot(self, data): ...      # 箱线图
    def plot_pie_chart(self, data): ...    # 饼图
    def plot_technical_indicators(self, data): ...  # 技术指标
    def plot_distribution(self, data): ...          # 分布图
    def plot_returns_distribution(self, data): ...  # 收益率
```

---

## 4.4 图表生成流程

```
用户选择图表类型
        ↓
前端发送POST请求 → /api/visualize/{chart_type}
        ↓
后端读取缓存数据
        ↓
调用对应的可视化方法
        ↓
Plotly生成图表对象
        ↓
转换为JSON格式（fig.to_json()）
        ↓
返回给前端
        ↓
前端Plotly.js渲染图表
```

---

# 五、11种图表详解

## 5.1 K线图（Candlestick Chart）

**用途**：展示股票的开盘、收盘、最高、最低价

**核心代码**：

```python
def plot_kline(self, data: pd.DataFrame):
    # 创建双面板布局
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True,
                        row_heights=[0.7, 0.3])
    
    # K线主体（上方70%）
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#00da3c',  # 上涨绿色
        decreasing_line_color='#ec0000'   # 下跌红色
    ), row=1, col=1)
    
    # 成交量副图（下方30%）
    fig.add_trace(go.Bar(
        x=data['Date'],
        y=data['Volume'],
        marker_color='#3a7bd5'
    ), row=2, col=1)
    
    return fig.to_json()
```

---

## 5.2 K线图技术要点

**关键技术**：

1. **双面板布局** - `make_subplots(rows=2, cols=1)`
   - 上方：K线图（70%高度）
   - 下方：成交量（30%高度）

2. **共享X轴** - `shared_xaxes=True`
   - 缩放时两个面板同步

3. **颜色编码** - 红涨绿跌（中国习惯）
   - `increasing_line_color='#00da3c'`
   - `decreasing_line_color='#ec0000'`

4. **隐藏范围滑块** - `xaxis_rangeslider_visible=False`

---

## 5.3 折线图（Line Chart）

**用途**：展示价格趋势变化

**核心代码**：

```python
def plot_line_chart(self, data: pd.DataFrame):
    fig = go.Figure()
    
    # 收盘价线（带填充）
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name='收盘价',
        line=dict(color='#00d2ff', width=2),
        fill='tozeroy',  # 填充到零轴
        fillcolor='rgba(0, 210, 255, 0.2)'
    ))
    
    # 开盘价线（填充到前一条线）
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Open'],
        mode='lines',
        name='开盘价',
        line=dict(color='#f39c12', width=2),
        fill='tonexty',
        fillcolor='rgba(243, 156, 18, 0.1)'
    ))
    
    return fig.to_json()
```

---

## 5.4 折线图技术要点

**关键技术**：

1. **填充效果** - `fill` 参数
   - `tozeroy` - 填充到Y轴零点
   - `tonexty` - 填充到上一条线

2. **渐变效果** - 使用RGBA颜色
   - `rgba(0, 210, 255, 0.2)` - 20%透明度

3. **线条样式** - `line=dict(width=2)`
   - 可设置宽度、颜色、形状

4. **多线叠加** - 多次调用 `add_trace`

---

## 5.5 柱状图（Bar Chart）

**用途**：展示交易量分布

**核心代码**：

```python
def plot_bar_chart(self, data: pd.DataFrame):
    # 只显示最近50天
    recent_data = data.tail(50)
    
    # 根据涨跌设置颜色
    colors = ['#00da3c' if recent_data['Close'].iloc[i] >= 
              recent_data['Open'].iloc[i] 
              else '#ec0000' 
              for i in range(len(recent_data))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=recent_data['Date'],
        y=recent_data['Volume'],
        marker_color=colors,  # 动态颜色
        opacity=0.8
    ))
    
    return fig.to_json()
```

---

## 5.6 面积图（Area Chart）

**用途**：展示价格波动区间

**核心代码**：

```python
def plot_area_chart(self, data: pd.DataFrame):
    fig = go.Figure()
    
    # 最高价线
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['High'],
        mode='lines',
        line=dict(color='#e74c3c'),
        fill=None
    ))
    
    # 最低价线（填充到最高价）
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Low'],
        mode='lines',
        line=dict(color='#3498db'),
        fill='tonexty',  # 填充到上一条线
        fillcolor='rgba(52, 152, 219, 0.2)'
    ))
    
    return fig.to_json()
```

---

## 5.7 散点图（Scatter Plot）

**用途**：展示成交量与价格的关系

**核心代码**：

```python
def plot_scatter(self, data: pd.DataFrame):
    # 计算涨跌幅作为颜色映射
    returns = data['Close'].pct_change().fillna(0)
    
    fig = px.scatter(
        data,
        x='Volume',      # X轴：成交量
        y='Close',       # Y轴：收盘价
        color=returns,   # 颜色：涨跌幅
        color_continuous_scale='RdYlGn',  # 红跌绿涨
        template='plotly_dark'
    )
    
    return fig.to_json()
```

**技术要点**：
- 使用 `plotly.express` 快速生成
- `color_continuous_scale` 设置颜色渐变

---

## 5.8 热力图（Heatmap）

**用途**：展示数据相关性矩阵

**核心代码**：

```python
def plot_heatmap(self, data: pd.DataFrame):
    # 计算相关性矩阵
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    corr_matrix = data[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,       # 矩阵值
        x=corr_matrix.columns,      # X轴标签
        y=corr_matrix.columns,      # Y轴标签
        colorscale='RdBu',          # 红-蓝配色
        zmid=0,                     # 中点为0
        text=corr_matrix.values.round(2),  # 显示数值
        texttemplate='%{text}',     # 文本模板
    ))
    
    return fig.to_json()
```

---

## 5.9 箱线图（Box Plot）

**用途**：展示月度价格分布和异常值

**核心代码**：

```python
def plot_boxplot(self, data: pd.DataFrame):
    # 添加月份列
    data['Month'] = data['Date'].dt.month
    
    fig = go.Figure()
    
    # 为每个月份创建一个箱线图
    for month in range(1, 13):
        month_data = data[data['Month'] == month]['Close']
        fig.add_trace(go.Box(
            y=month_data,
            name=f'{month}月',
            boxpoints='outliers'  # 显示异常值
        ))
    
    return fig.to_json()
```

---

## 5.10 饼图（Pie Chart）

**用途**：展示月度成交量占比

**核心代码**：

```python
def plot_pie_chart(self, data: pd.DataFrame):
    # 按月份汇总成交量
    data['Month'] = data['Date'].dt.to_period('M')
    monthly_volume = data.groupby('Month')['Volume'].sum().tail(8)
    
    fig = go.Figure(data=[go.Pie(
        labels=[str(m) for m in monthly_volume.index],
        values=monthly_volume.values,
        hole=0.3,  # 环形图（中心空洞30%）
        textinfo='label+percent'
    ))
    
    return fig.to_json()
```

---

## 5.11 技术指标图（Technical Indicators）

**用途**：展示MA、MACD、RSI等技术指标

**核心代码**：

```python
def plot_technical_indicators(self, data: pd.DataFrame):
    # 三面板布局
    fig = make_subplots(rows=3, cols=1,
                        row_heights=[0.5, 0.25, 0.25])
    
    # 计算移动平均线
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    # 计算MACD
    data['EMA12'] = data['Close'].ewm(span=12).mean()
    data['EMA26'] = data['Close'].ewm(span=26).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    
    # 计算RSI
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # 添加三条轨迹...
    return fig.to_json()
```

---

## 5.12 分布直方图（Distribution）

**用途**：展示价格和成交量分布

**核心代码**：

```python
def plot_distribution(self, data: pd.DataFrame):
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
        marker_color='#f39c12'
    ), row=1, col=2)
    
    return fig.to_json()
```

---

## 5.13 收益率分布图

**用途**：展示收益率分布和正态性检验

**核心代码**：

```python
def plot_returns_distribution(self, data: pd.DataFrame):
    # 计算日收益率
    data['Returns'] = data['Close'].pct_change() * 100
    returns = data['Returns'].dropna()
    
    fig = make_subplots(rows=1, cols=2)
    
    # 收益率直方图
    fig.add_trace(go.Histogram(x=returns), row=1, col=1)
    
    # Q-Q图（正态性检验）
    from scipy import stats
    theoretical_q = stats.norm.ppf(np.linspace(0.01, 0.99, len(returns)))
    sorted_returns = np.sort(returns)
    
    fig.add_trace(go.Scatter(
        x=theoretical_q,
        y=sorted_returns,
        mode='markers'
    ), row=1, col=2)
    
    return fig.to_json()
```

---

# 六、技术架构设计

## 6.1 整体架构

```
┌─────────────────────────────────────────┐
│           前端（浏览器）                  │
│  ┌─────────────────────────────────┐    │
│  │  index_python.html              │    │
│  │  app_python.js                  │    │
│  │  Plotly.js（图表渲染）           │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
                    ↕ HTTP/JSON
┌─────────────────────────────────────────┐
│           后端（Flask服务器）             │
│  ┌─────────────────────────────────┐    │
│  │  app.py（18个API接口）           │    │
│  │  data_processor.py              │    │
│  │  visualizer.py                  │    │
│  │  predictor.py                   │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
                    ↕ yfinance API
┌─────────────────────────────────────────┐
│        Yahoo Finance数据源               │
└─────────────────────────────────────────┘
```

---

## 6.2 API接口设计

**18个RESTful API接口**：

| 类别 | 接口数量 | 主要功能 |
|------|---------|---------|
| **数据接口** | 8个 | 加载、筛选、统计、导出 |
| **可视化接口** | 11个 | 11种图表生成 |
| **预测接口** | 4个 | 训练、预测、对比、回测 |
| **分析接口** | 4个 | 指标、相关性、月度、异常值 |

---

## 6.3 核心API示例

**数据加载接口** (`/api/data/load`)：

```python
@app.route('/api/data/load', methods=['POST'])
def load_data():
    data_source = request.json.get('source', 'spy')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    
    if start_date and end_date:
        data = processor.load_from_yfinance_by_date(
            data_source, start_date, end_date)
    else:
        data = processor.load_from_yfinance(data_source, '5y')
    
    return jsonify({
        'success': True,
        'count': len(data),
        'date_range': {...}
    })
```

---

## 6.4 可视化接口路由

**动态路由设计**：

```python
@app.route('/api/visualize/<chart_type>', methods=['POST'])
def visualize(chart_type):
    data = processor.filtered_data
    
    # 图表方法映射
    chart_methods = {
        'kline': visualizer.plot_kline,
        'line': visualizer.plot_line_chart,
        'bar': visualizer.plot_bar_chart,
        'area': visualizer.plot_area_chart,
        'scatter': visualizer.plot_scatter,
        'heatmap': visualizer.plot_heatmap,
        'boxplot': visualizer.plot_boxplot,
        'pie': visualizer.plot_pie_chart,
        'technical': visualizer.plot_technical_indicators,
        'distribution': visualizer.plot_distribution,
        'returns': visualizer.plot_returns_distribution
    }
    
    chart_json = chart_methods[chart_type](data)
    return jsonify({'success': True, 'chart_json': chart_json})
```

---

## 6.5 前端交互流程

**JavaScript核心代码** (`app_python.js`)：

```javascript
// 1. 加载股票数据
async function loadData() {
    const result = await apiRequest('/data/load', 'POST', {
        source: 'spy',
        start_date: '2000-01-01',
        end_date: '2026-06-02'
    });
    
    if (result.success) {
        updateStatistics();
        updateChart();
    }
}

// 2. 更新图表
async function updateChart() {
    const chartType = getSelectedChartType();
    const result = await apiRequest(`/visualize/${chartType}`, 'POST');
    
    if (result.success) {
        const chartData = JSON.parse(result.chart_json);
        Plotly.newPlot('chartContainer', chartData.data, 
                       chartData.layout);
    }
}
```

---

# 七、功能演示

## 7.1 主要功能

**1. 数据源选择**
- ETF基金分类（25只）
- 个股分类（45只）
- 支持自定义上传CSV

**2. 时间筛选**
- 显示股票最早上市日期
- 支持自定义日期范围
- 直接获取指定时间段数据

**3. 11种可视化图表**
- 一键切换图表类型
- 实时交互（缩放、平移）
- 悬停显示详细数据

---

## 7.2 实际演示

**在线演示地址**: https://finviz-platform.onrender.com

**演示步骤**：
1. 选择「ETF基金」分类
2. 选择「SPY - 标普500ETF」
3. 系统显示最早日期：1993-01-29
4. 选择日期范围：2000-06-02 到 2026-06-02
5. 点击「应用筛选」
6. 切换不同图表类型查看

---

## 7.3 性能数据

**实际测试结果**：

| 操作 | 数据量 | 响应时间 |
|------|--------|---------|
| 加载5年数据 | 1260条 | ~2秒 |
| 加载26年数据 | 6537条 | ~3秒 |
| 切换图表类型 | - | <0.5秒 |
| 日期筛选 | - | <0.1秒 |

**数据缓存机制**：
- 数据加载后存储在内存
- 切换图表无需重新获取
- 筛选操作直接使用缓存

---

# 八、总结与展望

## 8.1 项目总结

**技术收获**：

1. ✅ **数据获取** - 掌握yfinance库的使用
2. ✅ **数据处理** - 理解pandas的数据清洗流程
3. ✅ **可视化** - 学会11种Plotly图表的实现
4. ✅ **Web开发** - 构建完整的Flask RESTful API
5. ✅ **前后端交互** - 实现异步数据请求和图表渲染
6. ✅ **云端部署** - 成功部署到Render平台

---

## 8.2 可视化技术要点

**核心可视化技术**：

| 技术 | 应用场景 |
|------|---------|
| `make_subplots` | 多面板布局（K线图、技术指标） |
| `go.Candlestick` | 金融K线图专用组件 |
| `fill参数` | 折线图、面积图的填充效果 |
| `color_continuous_scale` | 散点图的颜色映射 |
| `go.Heatmap` | 相关性矩阵可视化 |
| `go.Box` | 统计分布和异常值检测 |
| `rolling/ewm` | 移动平均线和技术指标计算 |

---

## 8.3 项目亮点

1. **真实数据** - 从Yahoo Finance实时获取，无需本地存储
2. **完整流程** - 从数据获取到可视化展示的完整链路
3. **交互体验** - Plotly提供的专业交互功能
4. **代码规范** - 模块化设计，类封装，RESTful API
5. **免费部署** - Render平台免费托管，可公开访问

---

## 8.4 未来展望

**可扩展方向**：

1. 📊 **更多图表** - 添加3D图表、地理图表
2. 🤖 **AI预测** - 集成深度学习模型
3. 📱 **移动端** - 开发响应式移动版本
4. 🔔 **实时推送** - WebSocket实时数据更新
5. 📈 **更多数据源** - 支持A股、港股数据
6. 💾 **数据持久化** - 添加数据库存储

---

## 8.5 致谢

**感谢以下开源项目**：

- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance数据获取
- [Plotly](https://plotly.com/) - 交互式可视化库
- [Flask](https://flask.palletsprojects.com/) - Web框架
- [pandas](https://pandas.pydata.org/) - 数据处理
- [Render](https://render.com/) - 免费云托管平台

---

# 谢谢！

**项目地址**: https://github.com/yourusername/finviz-platform  
**在线演示**: https://finviz-platform.onrender.com

**欢迎提问！**