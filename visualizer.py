import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
from io import BytesIO
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')


class FinancialVisualizer:
    def __init__(self):
        plt.style.use('dark_background')
        sns.set_palette("husl")
    
    def _to_list(self, data):
        if hasattr(data, 'tolist'):
            return data.tolist()
        return data
    
    def _fig_to_base64(self, fig) -> str:
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_base64
    
    def plot_kline(self, data: pd.DataFrame, title: str = "K线图") -> str:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])
        
        fig.add_trace(go.Candlestick(
            x=self._to_list(data['Date']),
            open=self._to_list(data['Open']),
            high=self._to_list(data['High']),
            low=self._to_list(data['Low']),
            close=self._to_list(data['Close']),
            name='K线',
            increasing_line_color='#00da3c',
            decreasing_line_color='#ec0000'
        ), row=1, col=1)
        
        fig.add_trace(go.Bar(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Volume']),
            name='交易量',
            marker_color='#3a7bd5',
            opacity=0.7
        ), row=2, col=1)
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=800
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_line_chart(self, data: pd.DataFrame, title: str = "价格走势图") -> str:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Close']),
            mode='lines',
            name='收盘价',
            line=dict(color='#00d2ff', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 210, 255, 0.2)'
        ))
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Open']),
            mode='lines',
            name='开盘价',
            line=dict(color='#f39c12', width=2),
            fill='tonexty',
            fillcolor='rgba(243, 156, 18, 0.1)'
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=500
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_bar_chart(self, data: pd.DataFrame, title: str = "交易量柱状图") -> str:
        recent_data = data.tail(50)
        
        fig = go.Figure()
        
        colors = ['#00da3c' if recent_data['Close'].iloc[i] >= recent_data['Open'].iloc[i] 
                  else '#ec0000' for i in range(len(recent_data))]
        
        fig.add_trace(go.Bar(
            x=self._to_list(recent_data['Date']),
            y=self._to_list(recent_data['Volume']),
            name='交易量',
            marker_color=colors,
            opacity=0.8
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=400
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_area_chart(self, data: pd.DataFrame, title: str = "面积图") -> str:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['High']),
            mode='lines',
            name='最高价',
            line=dict(color='#e74c3c', width=1),
            fill=None
        ))
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Low']),
            mode='lines',
            name='最低价',
            line=dict(color='#3498db', width=1),
            fill='tonexty',
            fillcolor='rgba(52, 152, 219, 0.2)'
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=400
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_scatter(self, data: pd.DataFrame, title: str = "散点图") -> str:
        fig = px.scatter(
            data,
            x='Volume',
            y='Close',
            color=data['Close'].pct_change().fillna(0),
            color_continuous_scale='RdYlGn',
            title=title,
            template='plotly_dark'
        )
        
        fig.update_layout(height=500)
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_heatmap(self, data: pd.DataFrame, title: str = "相关性热力图") -> str:
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        corr_matrix = data[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="相关系数")
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=500
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_boxplot(self, data: pd.DataFrame, title: str = "箱线图") -> str:
        data['Month'] = data['Date'].dt.month
        monthly_data = data.groupby('Month')['Close'].apply(list)
        
        fig = go.Figure()
        
        for month in range(1, 13):
            if month in monthly_data.index:
                fig.add_trace(go.Box(
                    y=monthly_data[month],
                    name=f'{month}月',
                    boxpoints='outliers'
                ))
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=500
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_pie_chart(self, data: pd.DataFrame, title: str = "饼图") -> str:
        data['Month'] = data['Date'].dt.to_period('M')
        monthly_volume = data.groupby('Month')['Volume'].sum().tail(8)
        
        fig = go.Figure(data=[go.Pie(
            labels=[str(m) for m in monthly_volume.index],
            values=monthly_volume.values,
            hole=0.3,
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=500
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_technical_indicators(self, data: pd.DataFrame, ma_window: int = 20) -> str:
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                            vertical_spacing=0.05, row_heights=[0.5, 0.25, 0.25])
        
        data['MA'] = data['Close'].rolling(window=ma_window).mean()
        data['Returns'] = data['Close'].pct_change() * 100
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Close']),
            mode='lines',
            name='收盘价',
            line=dict(color='#00d2ff', width=2)
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['MA']),
            mode='lines',
            name=f'MA{ma_window}',
            line=dict(color='#f39c12', width=2, dash='dash')
        ), row=1, col=1)
        
        colors = ['#00da3c' if r >= 0 else '#ec0000' for r in data['Returns']]
        fig.add_trace(go.Bar(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Returns']),
            name='涨跌幅',
            marker_color=colors,
            opacity=0.7
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=self._to_list(data['Date']),
            y=self._to_list(data['Volume']),
            mode='lines',
            name='交易量',
            line=dict(color='#3a7bd5', width=1),
            fill='tozeroy'
        ), row=3, col=1)
        
        fig.update_layout(
            title='技术指标分析',
            template='plotly_dark',
            height=900
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_distribution(self, data: pd.DataFrame, title: str = "价格分布") -> str:
        fig = make_subplots(rows=1, cols=2, subplot_titles=('收盘价分布', '交易量分布'))
        
        fig.add_trace(go.Histogram(
            x=self._to_list(data['Close']),
            name='收盘价',
            nbinsx=30,
            marker_color='#00d2ff',
            opacity=0.7
        ), row=1, col=1)
        
        fig.add_trace(go.Histogram(
            x=self._to_list(data['Volume']),
            name='交易量',
            nbinsx=30,
            marker_color='#3a7bd5',
            opacity=0.7
        ), row=1, col=2)
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=400
        )
        
        return fig.to_json(engine='json', pretty=False)
    
    def plot_returns_distribution(self, data: pd.DataFrame, title: str = "收益率分布") -> str:
        returns = data['Close'].pct_change().dropna() * 100
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=('收益率直方图', '收益率Q-Q图'))
        
        fig.add_trace(go.Histogram(
            x=self._to_list(returns),
            name='收益率',
            nbinsx=50,
            marker_color='#f39c12',
            opacity=0.7
        ), row=1, col=1)
        
        from scipy import stats
        sorted_returns = np.sort(returns)
        theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(sorted_returns)))
        sample_quantiles = np.percentile(sorted_returns, np.linspace(1, 99, len(sorted_returns)))
        
        fig.add_trace(go.Scatter(
            x=self._to_list(theoretical_quantiles),
            y=self._to_list(sample_quantiles),
            mode='markers',
            name='Q-Q',
            marker=dict(color='#e74c3c', size=5)
        ), row=1, col=2)
        
        fig.add_trace(go.Scatter(
            x=self._to_list(theoretical_quantiles),
            y=self._to_list(theoretical_quantiles),
            mode='lines',
            name='理论线',
            line=dict(color='white', dash='dash')
        ), row=1, col=2)
        
        fig.update_layout(
            title=title,
            template='plotly_dark',
            height=400
        )
        
        return fig.to_json(engine='json', pretty=False)