import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FinancialPredictor:
    def __init__(self):
        self.models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(
                n_estimators=200, 
                max_depth=15, 
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=150,
                max_depth=6,
                learning_rate=0.05,
                random_state=42
            )
        }
        
        self.trained_models = {}
    
    def create_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        创建时间序列特征
        """
        df = data.copy()
        
        # 收益率特征
        df['Returns'] = df['Close'].pct_change()
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # 移动平均线
        for window in [5, 10, 20, 50]:
            df[f'MA_{window}'] = df['Close'].rolling(window=window).mean()
            df[f'MA_Ratio_{window}'] = df['Close'] / df[f'MA_{window}']
        
        # RSI
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        # MACD
        df['MACD'], df['Signal'], df['MACD_Hist'] = self._calculate_macd(df['Close'])
        
        # 波动率
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        df['High_Low_Range'] = (df['High'] - df['Low']) / df['Close']
        
        # 滞后特征
        for lag in range(1, 6):
            df[f'Returns_Lag_{lag}'] = df['Returns'].shift(lag)
        
        # 时间特征
        df['Day_of_Week'] = df['Date'].dt.dayofweek
        df['Month'] = df['Date'].dt.month
        
        df = df.dropna()
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple:
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    
    def train(self, data: pd.DataFrame, model_type: str = 'random_forest') -> Dict:
        if model_type not in self.models:
            return {'error': f'不支持的模型类型: {model_type}'}
        
        df = self.create_features(data)
        
        if len(df) < 100:
            return {'error': '数据不足，至少需要100条有效记录'}
        
        # 使用收益率作为目标变量
        exclude_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'OpenInt', 'Returns', 'Log_Returns']
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols]
        y = df['Returns'].shift(-1).dropna()
        X = X.loc[y.index]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = self.models[model_type]
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        metrics = {
            'mse': float(mean_squared_error(y_test, y_pred)),
            'mae': float(mean_absolute_error(y_test, y_pred)),
            'r2': float(r2_score(y_test, y_pred)),
            'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred)))
        }
        
        feature_importance = {}
        if hasattr(model, 'feature_importances_'):
            importance = dict(zip(feature_cols, model.feature_importances_))
            sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]
            feature_importance = dict(sorted_importance)
        
        self.trained_models[model_type] = {
            'model': model,
            'scaler': scaler,
            'feature_cols': feature_cols,
            'last_data': df.iloc[-1:].copy(),
            'last_price': df['Close'].iloc[-1],
            'last_date': df['Date'].iloc[-1]
        }
        
        return {
            'metrics': metrics,
            'feature_importance': feature_importance,
            'train_size': len(X_train),
            'test_size': len(X_test),
            'model_type': model_type
        }
    
    def predict(self, data: pd.DataFrame, model_type: str = 'random_forest', days: int = 30) -> Dict:
        try:
            if model_type not in self.trained_models:
                train_result = self.train(data, model_type)
                if 'error' in train_result:
                    return train_result
            
            if model_type not in self.trained_models:
                return {'error': f'模型 {model_type} 训练失败'}
            
            model_info = self.trained_models[model_type]
            model = model_info['model']
            scaler = model_info['scaler']
            feature_cols = model_info['feature_cols']
            
            if model is None:
                return {'error': f'模型 {model_type} 未正确初始化'}
        
            df = self.create_features(data)
            
            if len(df) == 0:
                return {'error': '无法创建足够的特征'}
            
            predictions = []
            last_price = df['Close'].iloc[-1]
            current_price = last_price
            current_date = df['Date'].iloc[-1]
            last_features = df.iloc[-1:][feature_cols]
            
            returns_std = df['Returns'].std() if len(df) > 0 else 0.01
            
            for day in range(1, days + 1):
                X_pred = last_features.values
                X_pred_scaled = scaler.transform(X_pred)
                predicted_return = model.predict(X_pred_scaled)[0]
                
                predicted_price = current_price * (1 + predicted_return)
                
                uncertainty = returns_std * np.sqrt(day) * current_price
                upper_bound = predicted_price + uncertainty
                lower_bound = predicted_price - uncertainty
                
                next_date = current_date + timedelta(days=1)
                while next_date.weekday() >= 5:
                    next_date += timedelta(days=1)
                
                predictions.append({
                    'date': next_date.strftime('%Y-%m-%d'),
                    'predicted_price': float(predicted_price),
                    'predicted_return': float(predicted_return * 100),
                    'upper_bound': float(upper_bound),
                    'lower_bound': float(lower_bound),
                    'day': day
                })
                
                current_price = predicted_price
                current_date = next_date
                
                last_features = self._update_features(last_features, df, predicted_price, next_date)
            
            total_return = ((predictions[-1]['predicted_price'] / last_price) - 1) * 100
            trend = '上涨' if total_return > 0 else '下跌'
            
            return {
                'predictions': predictions,
                'trend': trend,
                'total_return': float(total_return),
                'confidence_level': 0.95,
                'last_price': float(last_price),
                'model_type': model_type,
                'days_predicted': days,
                'returns_std': float(returns_std)
            }
        except Exception as e:
            return {'error': f'预测失败: {str(e)}'}
    
    def _update_features(self, last_features: pd.DataFrame, original_df: pd.DataFrame, 
                         predicted_price: float, next_date: datetime) -> pd.DataFrame:
        new_features = last_features.copy()
        
        # 更新移动平均线（简化处理）
        for window in [5, 10, 20, 50]:
            ma_col = f'MA_{window}'
            ma_ratio_col = f'MA_Ratio_{window}'
            if ma_col in new_features.columns:
                old_ma = new_features[ma_col].values[0]
                new_ma = old_ma + (predicted_price - old_ma) / window
                new_features[ma_col] = new_ma
                new_features[ma_ratio_col] = predicted_price / new_ma
        
        # 更新RSI（使用之前的RSI值进行平滑）
        if 'RSI' in new_features.columns:
            old_rsi = new_features['RSI'].values[0]
            new_features['RSI'] = old_rsi * 0.8 + 50 * 0.2
        
        # 更新MACD相关
        if 'MACD' in new_features.columns:
            new_features['MACD'] = new_features['MACD'].values[0] * 0.9
            new_features['Signal'] = new_features['Signal'].values[0] * 0.9
            new_features['MACD_Hist'] = new_features['MACD_Hist'].values[0] * 0.9
        
        # 更新波动率
        if 'Volatility' in new_features.columns:
            new_features['Volatility'] = original_df['Returns'].std()
        
        if 'High_Low_Range' in new_features.columns:
            new_features['High_Low_Range'] = 0.02
        
        # 更新滞后收益率
        for lag in range(4, 0, -1):
            prev_lag = f'Returns_Lag_{lag}'
            next_lag = f'Returns_Lag_{lag + 1}'
            if prev_lag in new_features.columns and next_lag in new_features.columns:
                new_features[next_lag] = new_features[prev_lag].values[0]
        
        if 'Returns_Lag_1' in new_features.columns:
            prev_price = original_df['Close'].iloc[-1]
            new_features['Returns_Lag_1'] = (predicted_price - prev_price) / prev_price
        
        # 更新时间特征
        new_features['Day_of_Week'] = next_date.dayofweek
        new_features['Month'] = next_date.month
        
        return new_features
    
    def predict_ensemble(self, data: pd.DataFrame, days: int = 30) -> Dict:
        results = {}
        
        for model_type in ['random_forest', 'gradient_boosting']:
            try:
                result = self.predict(data, model_type, days)
                if 'predictions' in result:
                    results[model_type] = result
            except Exception as e:
                print(f"Model {model_type} failed: {e}")
        
        if not results:
            return {'error': '所有模型预测失败'}
        
        ensemble_predictions = []
        n_models = len(results)
        
        for i in range(days):
            avg_price = sum(r['predictions'][i]['predicted_price'] for r in results.values()) / n_models
            avg_upper = sum(r['predictions'][i]['upper_bound'] for r in results.values()) / n_models
            avg_lower = sum(r['predictions'][i]['lower_bound'] for r in results.values()) / n_models
            
            ensemble_predictions.append({
                'date': results['random_forest']['predictions'][i]['date'],
                'predicted_price': float(avg_price),
                'upper_bound': float(avg_upper),
                'lower_bound': float(avg_lower),
                'day': i + 1
            })
        
        last_price = results['random_forest']['last_price']
        total_return = ((ensemble_predictions[-1]['predicted_price'] / last_price) - 1) * 100
        trend = '上涨' if total_return > 0 else '下跌'
        
        return {
            'predictions': ensemble_predictions,
            'trend': trend,
            'total_return': float(total_return),
            'confidence_level': 0.95,
            'last_price': float(last_price),
            'model_count': n_models,
            'models_used': list(results.keys()),
            'individual_results': results
        }
    
    def compare_models(self, data: pd.DataFrame) -> Dict:
        comparison = {}
        
        for model_type in ['linear', 'random_forest', 'gradient_boosting']:
            try:
                train_result = self.train(data, model_type)
                if 'metrics' in train_result:
                    comparison[model_type] = train_result
            except Exception as e:
                comparison[model_type] = {'error': str(e)}
        
        return comparison
    
    def backtest(self, data: pd.DataFrame, model_type: str = 'random_forest', test_days: int = 180) -> Dict:
        if len(data) < test_days * 2:
            return {'error': '数据不足'}
        
        train_data = data.iloc[:-test_days]
        test_data = data.iloc[-test_days:]
        
        train_result = self.train(train_data, model_type)
        if 'error' in train_result:
            return train_result
        
        predictions = []
        actual_prices = []
        dates = []
        
        current_data = train_data.copy()
        
        for i in range(min(test_days, len(test_data))):
            pred_result = self.predict(current_data, model_type, days=1)
            
            if 'predictions' in pred_result:
                predictions.append(pred_result['predictions'][0]['predicted_price'])
                actual_prices.append(test_data['Close'].iloc[i])
                dates.append(test_data['Date'].iloc[i])
                
                current_data = pd.concat([current_data, test_data.iloc[[i]]])
        
        if len(predictions) > 0:
            predictions_array = np.array(predictions)
            actual_array = np.array(actual_prices)
            
            mse = mean_squared_error(actual_array, predictions_array)
            mae = mean_absolute_error(actual_array, predictions_array)
            rmse = np.sqrt(mse)
            r2 = r2_score(actual_array, predictions_array)
            
            actual_returns = np.diff(actual_array)
            pred_returns = np.diff(predictions_array)
            direction_correct = np.sum(np.sign(actual_returns) == np.sign(pred_returns))
            direction_accuracy = direction_correct / len(actual_returns) if len(actual_returns) > 0 else 0
            
            return {
                'mse': float(mse),
                'mae': float(mae),
                'rmse': float(rmse),
                'r2': float(r2),
                'direction_accuracy': float(direction_accuracy),
                'test_days': len(predictions),
                'model_type': model_type,
                'predictions': [{'date': str(d), 'predicted': float(p), 'actual': float(a)}
                               for d, p, a in zip(dates, predictions, actual_prices)]
            }
        else:
            return {'error': '回测失败'}
