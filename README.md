# 金融数据可视化分析平台

基于 Python Flask + Plotly 构建的金融时间序列数据可视化分析平台，支持数据导入、多样化图表展示、统计分析和机器学习预测。

---

## 📁 项目结构

```
finalsummary/
├── app.py                 # Flask后端API服务（核心）
├── data_processor.py      # 数据处理模块
├── visualizer.py          # 可视化模块(Plotly)
├── predictor.py           # 机器学习预测模块
├── requirements.txt       # Python依赖清单
├── index_python.html      # 前端页面
├── app_python.js          # 前端JavaScript逻辑
├── style.css              # 样式文件
└── Data/                  # 金融数据源目录
    ├── ETFs/              # ETF基金数据 (1344个文件)
    └── Stocks/            # 个股数据 (7195个文件)
```

---

## 📸 界面预览

以下是平台的主要功能界面截图：

![平台界面预览](image/README/1780403497096.png)

---

## 📊 数据结构

### 数据文件格式

所有数据文件为 CSV 格式，包含以下字段：

| 字段 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| Date | datetime | 交易日期 | 2005-02-25 |
| Open | float | 开盘价 | 104.77 |
| High | float | 最高价 | 106.00 |
| Low | float | 最低价 | 104.68 |
| Close | float | 收盘价 | 105.79 |
| Volume | int | 交易量 | 70221808 |
| OpenInt | int | 未平仓合约数 | 0 |

### 数据统计

| 分类 | 文件数量 | 时间范围 | 数据量 |
|------|----------|----------|--------|
| ETF基金 | 1344 | 1999-2017 | ~500万条 |
| 个股 | 7195 | 1999-2017 | ~3000万条 |
| **总计** | **8539** | 1999-2017 | **~3500万条** |

### 示例数据 (`Data/ETFs/spy.us.txt`)

```csv
Date,Open,High,Low,Close,Volume,OpenInt
2005-02-25,104.77,106.0,104.68,105.79,70221808,0
2005-02-28,105.55,105.68,104.56,105.08,79695344,0
2005-03-01,105.45,105.78,104.43,105.45,55081752,0
```

---

## 🛠️ 技术栈

### 后端技术

| 技术 | 版本 | 用途 | 核心功能 |
|------|------|------|----------|
| Python | 3.8+ | 编程语言 | 核心业务逻辑 |
| Flask | 2.0+ | Web框架 | RESTful API服务 |
| Flask-CORS | 3.0+ | 跨域支持 | 前端跨域请求 |
| pandas | 1.4+ | 数据处理 | 数据清洗、转换、分析 |
| numpy | 1.22+ | 数值计算 | 矩阵运算、统计分析 |
| scikit-learn | 1.0+ | 机器学习 | 预测模型训练 |
| plotly | 5.6+ | 可视化库 | 交互式图表生成 |

### 前端技术

| 技术 | 用途 | 核心功能 |
|------|------|----------|
| HTML5 | 页面结构 | 布局与组件定义 |
| CSS3 | 样式设计 | 响应式布局、深色主题 |
| JavaScript ES6+ | 交互逻辑 | API调用、图表渲染、用户交互 |
| Plotly.js | 图表渲染 | 交互式可视化展示 |

---

## 🎯 功能特性

### 1. 数据导入与管理
- ✅ 自动扫描数据源目录（ETFs/Stocks分类）
- ✅ 分类展示（ETF基金/个股）
- ✅ 文件上传支持（CSV格式）
- ✅ 数据导出功能（JSON/CSV）

### 2. 多样化可视化图表

| 图表类型 | 说明 | 数据维度 | 技术实现 |
|----------|------|----------|----------|
| 📈 **K线图** | 蜡烛图展示OHLC数据 | Date, Open, High, Low, Close, Volume | Plotly Candlestick + Bar |
| 📉 **折线图** | 收盘价/开盘价趋势 | Date, Open, Close | Plotly Scatter(fill) |
| 📊 **柱状图** | 交易量展示（近期50条） | Date, Volume, Close-Open | Plotly Bar(颜色映射) |
| 📋 **面积图** | 最高价/最低价区间 | Date, High, Low | Plotly Scatter(tonexty) |
| 🔵 **散点图** | 交易量vs收盘价相关性 | Volume, Close, 涨跌幅 | Plotly Express |
| 🗺️ **热力图** | 特征相关性矩阵 | Open, High, Low, Close, Volume | Plotly Heatmap |
| 📦 **箱线图** | 月度价格分布 | Month, Close | Plotly Box |
| 🥧 **饼图** | 月度交易量占比 | Month, Volume | Plotly Pie(donut) |
| 📈 **技术指标** | MA/收益率/交易量综合 | Date, Close, MA, Returns, Volume | Plotly Subplots(3行) |
| 📊 **分布直方图** | 价格与交易量分布 | Close, Volume | Plotly Histogram(双栏) |
| 📊 **收益率分布** | 收益率直方图+Q-Q图 | Returns | Plotly Histogram + Scatter |

### 3. 统计分析
- ✅ 数据条数统计
- ✅ 平均收盘价
- ✅ 最高/最低收盘价
- ✅ 平均交易量
- ✅ 波动率计算

### 4. 时间筛选
- ✅ 开始/结束日期选择
- ✅ 实时数据过滤
- ✅ 日期格式验证（YYYY-MM-DD）

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
- Conda 环境（推荐）
- Windows 10/11

### 安装步骤

1. **进入项目目录**
```bash
cd e:\visualization\finalsummary
```

2. **创建并激活虚拟环境**
```bash
conda create -n vis python=3.8
conda activate vis
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

## 🌐 API接口说明

### 数据源管理

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/data/sources` | GET | 获取所有数据源分类 | 无 |
| `/api/data/load` | POST | 加载指定数据源 | `source`: 数据源ID |
| `/api/data/range` | GET | 获取数据日期范围 | 无 |
| `/api/data/filter` | POST | 按日期筛选数据 | `start_date`, `end_date` |
| `/api/data/statistics` | GET | 获取统计指标 | 无 |
| `/api/data/upload` | POST | 上传数据文件 | `file`: 文件对象 |
| `/api/data/export` | GET | 导出数据 | `format`: json/csv |

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
| `/api/visualize/tech` | POST | 技术指标图 | JSON(Plotly) |
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
  -d '{"start_date": "2010-01-01", "end_date": "2010-12-31"}'
```

**生成K线图**
```bash
curl -X POST http://localhost:5000/api/visualize/kline \
  -H "Content-Type: application/json" \
  -d '{}'
```

**执行预测**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"days": 30, "model": "ensemble"}'
```

---

## 📈 可视化技术实现详解

### 1. 可视化架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    可视化架构                               │
├─────────────────────────────────────────────────────────────┤
│  前端 (Plotly.js)                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 图表渲染层: Plotly.newPlot()                        │    │
│  │ 交互层: 缩放、平移、悬停提示、图例切换               │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓ JSON                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 后端 (Flask + Plotly Python)                        │    │
│  │ 图表生成层: FinancialVisualizer类                   │    │
│  │ 数据处理层: FinancialDataProcessor类                │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓ CSV                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 数据源: Data/ETFs/*.us.txt, Data/Stocks/*.us.txt   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2. 核心可视化类设计

#### 2.1 FinancialVisualizer 类结构

```python
class FinancialVisualizer:
    def __init__(self):
        plt.style.use('dark_background')  # 深色主题
        sns.set_palette("husl")           # 颜色方案
    
    def _to_list(self, data):
        # 将pandas Series转换为Python列表（解决JSON序列化问题）
        if hasattr(data, 'tolist'):
            return data.tolist()
        return data
    
    def _fig_to_base64(self, fig) -> str:
        # 将matplotlib图转换为Base64（备用方案）
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
```

### 3. 图表实现详解

#### 3.1 K线图 (Candlestick Chart)

**技术原理**: 使用 Plotly 的 `go.Candlestick` 组件，结合 `make_subplots` 实现双图联动（K线+交易量）。

```python
def plot_kline(self, data: pd.DataFrame, title: str = "K线图") -> str:
    # 创建子图布局：2行1列，共享X轴
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.03, 
        row_heights=[0.7, 0.3]  # K线占70%，交易量占30%
    )
    
    # 添加K线图（第一行）
    fig.add_trace(go.Candlestick(
        x=self._to_list(data['Date']),
        open=self._to_list(data['Open']),
        high=self._to_list(data['High']),
        low=self._to_list(data['Low']),
        close=self._to_list(data['Close']),
        name='K线',
        increasing_line_color='#00da3c',   # 上涨绿色
        decreasing_line_color='#ec0000'    # 下跌红色
    ), row=1, col=1)
    
    # 添加交易量柱状图（第二行）
    fig.add_trace(go.Bar(
        x=self._to_list(data['Date']),
        y=self._to_list(data['Volume']),
        name='交易量',
        marker_color='#3a7bd5',
        opacity=0.7
    ), row=2, col=1)
    
    # 布局配置
    fig.update_layout(
        title=title,
        template='plotly_dark',      # 深色主题
        xaxis_rangeslider_visible=False,  # 隐藏底部滑块
        height=800
    )
    
    return fig.to_json(engine='json', pretty=False)
```

**关键技术点**:
- `shared_xaxes=True`: X轴联动，缩放时两张图同步
- `vertical_spacing`: 子图间距控制
- `_to_list()`: pandas数据转换，确保JSON序列化成功
- 颜色语义: 绿色上涨、红色下跌（符合A股习惯）

#### 3.2 折线图 (Line Chart)

**技术原理**: 使用 `go.Scatter` 的 `fill` 参数实现面积填充效果。

```python
def plot_line_chart(self, data: pd.DataFrame, title: str = "价格走势图") -> str:
    fig = go.Figure()
    
    # 收盘价（底部填充）
    fig.add_trace(go.Scatter(
        x=self._to_list(data['Date']),
        y=self._to_list(data['Close']),
        mode='lines',
        name='收盘价',
        line=dict(color='#00d2ff', width=2),
        fill='tozeroy',                # 填充到Y轴0点
        fillcolor='rgba(0, 210, 255, 0.2)'  # 半透明填充
    ))
    
    # 开盘价（填充到收盘价）
    fig.add_trace(go.Scatter(
        x=self._to_list(data['Date']),
        y=self._to_list(data['Open']),
        mode='lines',
        name='开盘价',
        line=dict(color='#f39c12', width=2),
        fill='tonexty',                # 填充到上一个trace
        fillcolor='rgba(243, 156, 18, 0.1)'
    ))
    
    fig.update_layout(title=title, template='plotly_dark', height=500)
    return fig.to_json(engine='json', pretty=False)
```

**关键技术点**:
- `fill='tozeroy'`: 从曲线填充到Y轴底部
- `fill='tonexty'`: 填充到上一条曲线
- `fillcolor`: 使用RGBA颜色，支持透明度

#### 3.3 柱状图 (Bar Chart)

**技术原理**: 根据涨跌方向动态设置柱体颜色。

```python
def plot_bar_chart(self, data: pd.DataFrame, title: str = "交易量柱状图") -> str:
    recent_data = data.tail(50)  # 取最近50条数据
    
    # 根据收盘价与开盘价比较设置颜色
    colors = [
        '#00da3c' if recent_data['Close'].iloc[i] >= recent_data['Open'].iloc[i] 
        else '#ec0000' 
        for i in range(len(recent_data))
    ]
    
    fig.add_trace(go.Bar(
        x=self._to_list(recent_data['Date']),
        y=self._to_list(recent_data['Volume']),
        marker_color=colors,  # 动态颜色
        opacity=0.8
    ))
    ...
```

**关键技术点**:
- 数据截取: 使用 `tail(50)` 只显示近期数据
- 颜色映射: 涨绿跌红的视觉编码

#### 3.4 热力图 (Heatmap)

**技术原理**: 计算特征相关性矩阵，使用颜色编码相关系数。

```python
def plot_heatmap(self, data: pd.DataFrame, title: str = "相关性热力图") -> str:
    # 选择数值型列
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    corr_matrix = data[numeric_cols].corr()  # 计算皮尔逊相关系数
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',    # 红-白-蓝配色
        zmid=0,               # 0为中心（白色）
        text=corr_matrix.values.round(2),  # 显示相关系数值
        texttemplate='%{text}',
        colorbar=dict(title="相关系数")
    ))
    ...
```

**关键技术点**:
- `pandas.corr()`: 计算皮尔逊相关系数
- `colorscale='RdBu'`: 红色表示负相关，蓝色表示正相关
- `zmid=0`: 零相关显示为白色

#### 3.5 技术指标图 (Technical Indicators)

**技术原理**: 多子图布局，同时展示价格、收益率和交易量。

```python
def plot_technical_indicators(self, data: pd.DataFrame, ma_window: int = 20) -> str:
    # 3行1列布局
    fig = make_subplots(
        rows=3, cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.05, 
        row_heights=[0.5, 0.25, 0.25]
    )
    
    # 计算技术指标
    data['MA'] = data['Close'].rolling(window=ma_window).mean()  # 移动平均线
    data['Returns'] = data['Close'].pct_change() * 100          # 涨跌幅
    
    # 第1行：价格与MA
    fig.add_trace(go.Scatter(x=..., y=..., name='收盘价'), row=1, col=1)
    fig.add_trace(go.Scatter(x=..., y=..., name=f'MA{ma_window}', 
                             line=dict(dash='dash')), row=1, col=1)
    
    # 第2行：涨跌幅柱状图
    colors = ['#00da3c' if r >= 0 else '#ec0000' for r in data['Returns']]
    fig.add_trace(go.Bar(x=..., y=..., marker_color=colors), row=2, col=1)
    
    # 第3行：交易量
    fig.add_trace(go.Scatter(x=..., y=..., fill='tozeroy'), row=3, col=1)
    ...
```

**关键技术点**:
- `rolling().mean()`: 计算移动平均线
- `pct_change()`: 计算涨跌幅
- 多行联动: 共享X轴，便于分析多维度关系

#### 3.6 收益率分布图 (Returns Distribution)

**技术原理**: 结合直方图和Q-Q图，分析收益率分布特征。

```python
def plot_returns_distribution(self, data: pd.DataFrame, title: str = "收益率分布") -> str:
    returns = data['Close'].pct_change().dropna() * 100
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=('收益率直方图', '收益率Q-Q图'))
    
    # 直方图
    fig.add_trace(go.Histogram(x=self._to_list(returns), nbinsx=50), row=1, col=1)
    
    # Q-Q图（正态性检验）
    from scipy import stats
    sorted_returns = np.sort(returns)
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(sorted_returns)))
    sample_quantiles = np.percentile(sorted_returns, np.linspace(1, 99, len(sorted_returns)))
    
    fig.add_trace(go.Scatter(x=theoretical_quantiles, y=sample_quantiles, mode='markers'), 
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=theoretical_quantiles, y=theoretical_quantiles, 
                             line=dict(dash='dash')), row=1, col=2)
    ...
```

**关键技术点**:
- `scipy.stats.norm.ppf()`: 计算理论正态分布分位数
- Q-Q图: 用于检验数据是否服从正态分布
- 如果点接近对角线，说明数据近似正态分布

### 4. 前端图表渲染流程

```javascript
async function updateChart() {
    const chartType = getChartType();  // 获取用户选择的图表类型
    
    // 调用后端API获取图表数据
    const result = await apiRequest(`/visualize/${chartType}`, 'POST');
    
    if (result?.success) {
        // 将JSON字符串解析为Plotly配置对象
        const figData = JSON.parse(result.chart_json);
        
        // 使用Plotly.js渲染图表
        Plotly.newPlot('mainChart', figData.data, figData.layout, {
            responsive: true,
            displayModeBar: true  // 显示工具栏（缩放、下载等）
        });
    }
}
```

**前端交互特性**:
- ✅ 响应式布局
- ✅ 缩放/平移
- ✅ 悬停提示
- ✅ 图例切换
- ✅ 图表下载（PNG/SVG/PDF）

### 5. 图表渲染性能优化

| 优化策略 | 实现方式 | 效果 |
|----------|----------|------|
| 数据截断 | 柱状图只取最近50条 | 减少数据量 |
| 异步加载 | AJAX异步请求 | 不阻塞UI |
| JSON序列化 | `to_json(pretty=False)` | 减少传输体积 |
| 共享X轴 | `shared_xaxes=True` | 减少渲染计算 |
| WebGL加速 | Plotly内置 | 提升渲染速度 |

---

## 📊 数据处理流程

### 数据加载流程

```
用户选择数据源 → load_data() → 数据验证 → 日期转换 → 存储到全局变量
    ↓
用户选择日期范围 → filter_by_date() → 日期验证 → 筛选数据 → 更新filtered_data
    ↓
用户选择图表类型 → plot_xxx() → 生成图表JSON → 返回前端渲染
```

### 数据验证机制

```python
def load_data(self, file_path: str) -> pd.DataFrame:
    # 1. 文件读取
    self.data = pd.read_csv(file_path)
    
    # 2. 空文件检查
    if self.data.empty or len(self.data.columns) == 0:
        raise ValueError('文件内容为空或无法解析')
    
    # 3. 必要列检查
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    missing_cols = [col for col in required_columns if col not in self.data.columns]
    if missing_cols:
        raise ValueError(f'缺少必要的列: {", ".join(missing_cols)}')
    
    # 4. 日期格式转换
    self.data['Date'] = pd.to_datetime(self.data['Date'])
    self.filtered_data = self.data.copy()
    
    return self.data
```

### 日期筛选验证

```python
def filter_by_date(self, start_date: str, end_date: str) -> pd.DataFrame:
    import re
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    # 格式验证
    if not re.match(date_pattern, start_date):
        raise ValueError(f'开始日期格式错误，应为YYYY-MM-DD: {start_date}')
    
    # 年份验证
    start_year = int(start_date[:4])
    if start_year < 1900:
        raise ValueError('日期年份必须大于等于1900')
    
    # 日期范围验证
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    if start > end:
        raise ValueError('开始日期不能大于结束日期')
    
    # 执行筛选
    self.filtered_data = self.data[
        (self.data['Date'] >= start) & 
        (self.data['Date'] <= end)
    ]
    return self.filtered_data
```

---

## 🤖 机器学习预测实现

### 预测模型架构

```python
class FinancialPredictor:
    def __init__(self):
        self.data = None
        self.models = {}
    
    def _create_features(self, data):
        """创建预测特征"""
        features = pd.DataFrame()
        features['Open'] = data['Open']
        features['High'] = data['High']
        features['Low'] = data['Low']
        features['Volume'] = data['Volume']
        features['MA5'] = data['Close'].rolling(5).mean()
        features['MA20'] = data['Close'].rolling(20).mean()
        features['Returns'] = data['Close'].pct_change()
        return features.dropna()
    
    def predict_ensemble(self, days: int = 30) -> Dict:
        """集成模型预测"""
        features = self._create_features(self.data)
        
        # 多模型训练
        models = {
            'linear': LinearRegression(),
            'rf': RandomForestRegressor(n_estimators=100),
            'gb': GradientBoostingRegressor(n_estimators=100)
        }
        
        predictions = {}
        for name, model in models.items():
            model.fit(features[:-1], self.data['Close'].iloc[1:])
            predictions[name] = self._predict_future(model, features, days)
        
        # 集成预测（取平均）
        ensemble_pred = np.mean(list(predictions.values()), axis=0)
        
        return {
            'ensemble': ensemble_pred.tolist(),
            'individual': predictions,
            'confidence_interval': self._calculate_confidence(ensemble_pred)
        }
```

### 预测API响应格式

```json
{
  "success": true,
  "predictions": {
    "ensemble": [105.2, 105.8, 106.3, ...],
    "individual": {
      "linear": [104.9, 105.5, 106.1, ...],
      "rf": [105.3, 105.9, 106.5, ...],
      "gb": [105.4, 106.0, 106.4, ...]
    },
    "confidence_interval": {
      "lower": [103.2, 103.8, 104.3, ...],
      "upper": [107.2, 107.8, 108.3, ...]
    },
    "dates": ["2024-01-01", "2024-01-02", "2024-01-03", ...]
  }
}
```

---

## 🔒 安全特性

| 安全措施 | 实现位置 | 说明 |
|----------|----------|------|
| 文件大小限制 | `data_processor.py` | < 50字节拒绝加载 |
| 文件类型验证 | `app.py` | 仅支持 .txt/.csv |
| 日期格式验证 | `data_processor.py` | YYYY-MM-DD格式检查 |
| 年份范围限制 | `data_processor.py` | 年份 >= 1900 |
| SQL注入防护 | Flask | 参数化请求处理 |
| CORS跨域控制 | `app.py` | 配置允许的来源 |
| 异常处理 | 全局 | 统一错误响应格式 |

---

## 📝 配置说明

### 数据源配置 (`app.py`)

```python
DATA_DIR = 'Data'  # 数据源目录（相对于app.py的路径）

# 股票中文名称映射（用于前端显示）
STOCK_NAMES = {
    'spy': '标普500ETF',
    'qqq': '纳斯达克100ETF',
    'aapl': '苹果公司',
    'msft': '微软公司',
    # ... 更多映射
}
```

### 图表主题配置 (`visualizer.py`)

```python
def __init__(self):
    plt.style.use('dark_background')  # matplotlib深色主题
    sns.set_palette("husl")           # seaborn颜色方案
    # Plotly图表默认使用 'plotly_dark' 模板
```

---

## 🐛 常见问题与解决方案

| 问题 | 错误信息 | 原因 | 解决方案 |
|------|----------|------|----------|
| 日期筛选报错 | `Out of bounds nanosecond timestamp` | 日期格式不正确或年份过小 | 确保使用 YYYY-MM-DD 格式，年份 >= 1900 |
| 图表不显示 | 控制台无错误 | Plotly JSON格式问题 | 使用 `fig.to_json(engine='json')` |
| 空文件报错 | `文件内容为空或无法解析` | 文件大小 < 50字节 | 检查数据源文件是否有效 |
| 中文显示乱码 | 前端文字乱码 | 编码问题 | 确保所有文件使用 UTF-8 编码 |
| API 500错误 | `No columns to parse from file` | 文件格式不正确 | 检查CSV文件是否有正确的表头 |

---

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**项目版本**: v1.0  
**最后更新**: 2024年  
**作者**: Financial Data Analysis Team  
**联系邮箱**: support@example.com
