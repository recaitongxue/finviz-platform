import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


class FinancialDataProcessor:
    def __init__(self):
        self.data = None
        self.filtered_data = None
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        self.data = pd.read_csv(file_path)
        
        if self.data.empty or len(self.data.columns) == 0:
            raise ValueError('文件内容为空或无法解析')
        
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_columns if col not in self.data.columns]
        if missing_cols:
            raise ValueError(f'缺少必要的列: {", ".join(missing_cols)}')
        
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data = self.data.sort_values('Date')
        self.data = self.data.reset_index(drop=True)
        self.filtered_data = self.data.copy()
        return self.data
    
    def load_from_yfinance(self, symbol: str, period: str = "5y") -> pd.DataFrame:
        if not YFINANCE_AVAILABLE:
            raise ImportError('yfinance 库未安装，请运行: pip install yfinance')
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        if df.empty:
            raise ValueError(f'无法获取 {symbol} 的数据')
        
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df[required_columns]
        
        df = df.sort_values('Date')
        df = df.reset_index(drop=True)
        
        self.data = df
        self.filtered_data = df.copy()
        return self.data
    
    def filter_by_date(self, start_date: str, end_date: str) -> pd.DataFrame:
        if self.data is None:
            return pd.DataFrame()
        
        import re
        
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date):
            raise ValueError(f'开始日期格式错误，应为YYYY-MM-DD: {start_date}')
        if not re.match(date_pattern, end_date):
            raise ValueError(f'结束日期格式错误，应为YYYY-MM-DD: {end_date}')
        
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        
        if start_year < 1900 or end_year < 1900:
            raise ValueError('日期年份必须大于等于1900')
        
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
        except Exception as e:
            raise ValueError(f'日期解析错误: {str(e)}')
        
        if start > end:
            raise ValueError('开始日期不能大于结束日期')
        
        self.filtered_data = self.data[
            (self.data['Date'] >= start) & 
            (self.data['Date'] <= end)
        ]
        return self.filtered_data
    
    def get_statistics(self) -> Dict:
        if self.filtered_data is None or len(self.filtered_data) == 0:
            return {
                'count': 0,
                'avg_close': 0,
                'max_close': 0,
                'min_close': 0,
                'avg_volume': 0,
                'volatility': 0
            }
        
        closes = self.filtered_data['Close']
        volumes = self.filtered_data['Volume']
        
        returns = closes.pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) if len(returns) > 0 else 0
        
        return {
            'count': len(self.filtered_data),
            'avg_close': float(closes.mean()),
            'max_close': float(closes.max()),
            'min_close': float(closes.min()),
            'avg_volume': float(volumes.mean()),
            'volatility': float(volatility)
        }
    
    def calculate_returns(self, period: int = 1) -> pd.Series:
        if self.filtered_data is None:
            return pd.Series()
        return self.filtered_data['Close'].pct_change(period).dropna()
    
    def calculate_moving_average(self, window: int = 20) -> pd.Series:
        if self.filtered_data is None:
            return pd.Series()
        return self.filtered_data['Close'].rolling(window=window).mean()
    
    def calculate_rsi(self, period: int = 14) -> pd.Series:
        if self.filtered_data is None or len(self.filtered_data) < period + 1:
            return pd.Series()
        
        delta = self.filtered_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_bollinger_bands(self, window: int = 20, num_std: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        if self.filtered_data is None:
            return pd.Series(), pd.Series(), pd.Series()
        
        sma = self.calculate_moving_average(window)
        std = self.filtered_data['Close'].rolling(window=window).std()
        
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        
        return sma, upper_band, lower_band
    
    def get_correlation_matrix(self) -> Dict:
        if self.filtered_data is None:
            return {}
        
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        corr_matrix = self.filtered_data[numeric_cols].corr()
        
        return corr_matrix.to_dict()
    
    def get_monthly_summary(self) -> pd.DataFrame:
        if self.filtered_data is None:
            return pd.DataFrame()
        
        self.filtered_data['YearMonth'] = self.filtered_data['Date'].dt.to_period('M')
        monthly = self.filtered_data.groupby('YearMonth').agg({
            'Close': ['first', 'last', 'max', 'min'],
            'Volume': 'sum'
        }).reset_index()
        
        monthly.columns = ['YearMonth', 'Open', 'Close', 'High', 'Low', 'Volume']
        monthly['Return'] = ((monthly['Close'] - monthly['Open']) / monthly['Open'] * 100)
        
        return monthly
    
    def detect_outliers(self, threshold: float = 3.0) -> pd.DataFrame:
        if self.filtered_data is None:
            return pd.DataFrame()
        
        closes = self.filtered_data['Close']
        mean = closes.mean()
        std = closes.std()
        
        z_scores = np.abs((closes - mean) / std)
        outliers = self.filtered_data[z_scores > threshold]
        
        return outliers