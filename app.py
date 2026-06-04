from flask import Flask, request, jsonify, render_template_string, send_file, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json
import time

from data_processor import FinancialDataProcessor
from visualizer import FinancialVisualizer
from predictor import FinancialPredictor

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

processor = FinancialDataProcessor()
visualizer = FinancialVisualizer()
predictor = FinancialPredictor()

# 数据缓存
data_cache = {}
CACHE_DURATION = 300  # 5分钟缓存

STOCK_NAMES = {
    'spy': '标普500ETF', 'qqq': '纳斯达克100ETF',
    'aapl': '苹果公司', 'msft': '微软公司', 'amzn': '亚马逊', 'googl': '谷歌', 'fb': 'Meta(Facebook)',
    'tsla': '特斯拉', 'nvda': '英伟达', 'jpm': '摩根大通', 'v': '维萨卡', 'jnj': '强生', 'wmt': '沃尔玛',
    'pg': '宝洁', 'ma': '万事达', 'unh': '联合健康', 'hd': '家得宝', 'dis': '迪士尼', 'bac': '美国银行',
    'xom': '埃克森美孚', 'cvx': '雪佛龙', 'pfe': '辉瑞', 'abbv': '艾伯维', 'ko': '可口可乐', 'pep': '百事可乐',
    'nke': '耐克', 'vz': '威瑞森', 'intel': '英特尔', 'crm': 'Salesforce', 'adbe': 'Adobe', 'csco': '思科',
    'acn': '埃森哲', 'txn': '德州仪器', 'qcom': '高通', 'avgo': '博通', 'dhr': '丹纳赫', 'ups': '联合包裹',
    'gs': '高盛', 'axp': '美国运通', 'mcd': '麦当劳', 'amd': '超微半导体', 'now': 'ServiceNow', 'jd': '京东',
    'pdd': '拼多多', 'bidu': '百度', 'baba': '阿里巴巴', 'aadr': '金瑞主题投资ETF', 'smh': '半导体ETF',
    'soxx': '费城半导体ETF', 'xle': '能源ETF', 'xlf': '金融ETF', 'xlv': '医疗保健ETF', 'xly': '非必需消费品ETF',
    'xlp': '必需消费品ETF', 'xli': '工业ETF', 'xlk': '科技ETF', 'vgt': 'Vanguard信息技术ETF', 'vti': 'Vanguard整体股市ETF',
    'voo': 'Vanguard标普500ETF', 'iwm': 'iShares罗素2000ETF', 'gld': 'SPDR黄金ETF', 'dia': 'SPDR道琼斯ETF',
    'iwr': 'iShares中型股ETF', 'ief': 'iShares中期国债ETF', 'tlt': 'iShares长期国债ETF',
    'agg': 'iShares核心美国债券ETF', 'lqd': 'iShares投资级债券ETF', 'hyg': 'iShares高收益债券ETF',
}

ETF_SYMBOLS = ['spy', 'qqq', 'aadr', 'smh', 'soxx', 'xle', 'xlf', 'xlv', 'xly', 'xlp', 'xli', 'xlk', 'vgt', 'vti', 'voo', 'iwm', 'gld', 'dia', 'iwr', 'ief', 'tlt', 'agg', 'lqd', 'hyg']


@app.route('/')
def index():
    with open('index_python.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/api/data/sources', methods=['GET'])
def get_sources():
    try:
        etfs = []
        stocks = []
        
        for key in sorted(STOCK_NAMES.keys()):
            name = STOCK_NAMES[key]
            if key in ETF_SYMBOLS:
                etfs.append({'id': key, 'name': name})
            else:
                stocks.append({'id': key, 'name': name})
        
        return jsonify({
            'success': True,
            'categories': {
                'etfs': {
                    'name': 'ETF基金',
                    'count': len(etfs),
                    'items': etfs
                },
                'stocks': {
                    'name': '个股',
                    'count': len(stocks),
                    'items': stocks
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/load', methods=['POST'])
def load_data():
    try:
        data_source = request.json.get('source', 'spy').lower()
        
        if data_source not in STOCK_NAMES:
            return jsonify({'error': '无效的数据源'}), 400
        
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        
        # 生成缓存键
        cache_key = f"{data_source}_{start_date}_{end_date}"
        
        # 检查缓存
        if cache_key in data_cache:
            cached_data, cached_time = data_cache[cache_key]
            if time.time() - cached_time < CACHE_DURATION:
                print(f"使用缓存数据: {cache_key}")
                return jsonify({
                    'success': True,
                    'count': len(cached_data),
                    'date_range': {
                        'start': cached_data['Date'].min().strftime('%Y-%m-%d'),
                        'end': cached_data['Date'].max().strftime('%Y-%m-%d')
                    },
                    'cached': True
                })
        
        # 带重试的数据加载
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if start_date and end_date:
                    data = processor.load_from_yfinance_by_date(data_source.upper(), start_date, end_date)
                else:
                    data = processor.load_from_yfinance(data_source.upper(), '5y')
                
                # 保存到缓存
                data_cache[cache_key] = (data, time.time())
                
                return jsonify({
                    'success': True,
                    'count': len(data),
                    'date_range': {
                        'start': data['Date'].min().strftime('%Y-%m-%d'),
                        'end': data['Date'].max().strftime('%Y-%m-%d')
                    }
                })
            except Exception as e:
                last_error = e
                print(f"数据加载失败，第 {attempt + 1} 次重试: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # 等待2秒后重试
                    continue
        
        raise last_error or Exception("数据加载失败")
        
    except ImportError:
        return jsonify({'error': 'yfinance 未安装，请运行: pip install yfinance'}), 500
    except Exception as e:
        return jsonify({'error': f'数据加载失败: {str(e)}'}), 500


@app.route('/api/data/statistics', methods=['GET'])
def get_statistics():
    try:
        stats = processor.get_statistics()
        return jsonify({'success': True, 'statistics': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/filter', methods=['POST'])
def filter_data():
    try:
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': '缺少日期参数'}), 400
        
        filtered_data = processor.filter_by_date(start_date, end_date)
        
        return jsonify({
            'success': True,
            'count': len(filtered_data),
            'statistics': processor.get_statistics()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/range', methods=['GET'])
def get_date_range():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or data.empty:
            return jsonify({'error': '未加载数据'}), 400
        
        return jsonify({
            'success': True,
            'start_date': data['Date'].min().strftime('%Y-%m-%d'),
            'end_date': data['Date'].max().strftime('%Y-%m-%d'),
            'earliest_date': processor.get_earliest_date(request.args.get('symbol', 'SPY'))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/raw', methods=['GET'])
def get_raw_data():
    try:
        limit = request.args.get('limit', 100, type=int)
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None:
            return jsonify({'error': '未加载数据'}), 400
        
        data_sample = data.tail(limit).to_dict('records')
        
        for record in data_sample:
            if 'Date' in record:
                record['Date'] = record['Date'].strftime('%Y-%m-%d')
        
        return jsonify({'success': True, 'data': data_sample})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualize/<chart_type>', methods=['POST'])
def visualize(chart_type):
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) == 0:
            return jsonify({'error': '未加载数据'}), 400
        
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
        
        if chart_type not in chart_methods:
            return jsonify({'error': '不支持的图表类型'}), 400
        
        chart_json = chart_methods[chart_type](data)
        
        return jsonify({'success': True, 'chart_json': chart_json})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) < 100:
            return jsonify({'error': '数据不足，至少需要100条记录'}), 400
        
        days = request.json.get('days', 30)
        model_type = request.json.get('model', 'ensemble')
        
        if days < 1 or days > 100:
            return jsonify({'error': '预测天数必须在1-100之间'}), 400
        
        if model_type == 'ensemble':
            result = predictor.predict_ensemble(data, days)
        else:
            result = predictor.predict(data, model_type, days)
        
        return jsonify({'success': True, 'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/train', methods=['POST'])
def train_model():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) < 100:
            return jsonify({'error': '数据不足'}), 400
        
        model_type = request.json.get('model', 'random_forest')
        
        result = predictor.train(data, model_type)
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/compare', methods=['POST'])
def compare_models():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) < 100:
            return jsonify({'error': '数据不足，至少需要100条记录'}), 400
        
        comparison = predictor.compare_models(data)
        
        return jsonify({'success': True, 'comparison': comparison})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/backtest', methods=['POST'])
def backtest():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) < 200:
            return jsonify({'error': '数据不足，至少需要200条记录用于回测'}), 400
        
        model_type = request.json.get('model', 'random_forest')
        test_days = request.json.get('test_days', 365)
        
        if test_days < 30 or test_days > len(data) // 2:
            return jsonify({'error': f'回测天数必须在30-{len(data)//2}之间'}), 400
        
        result = predictor.backtest(data, model_type, test_days)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({'success': True, 'backtest': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/indicators', methods=['GET'])
def get_indicators():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) == 0:
            return jsonify({'error': '未加载数据'}), 400
        
        ma_20 = processor.calculate_moving_average(20)
        ma_50 = processor.calculate_moving_average(50)
        rsi = processor.calculate_rsi()
        sma, upper_band, lower_band = processor.calculate_bollinger_bands()
        
        indicators = {
            'ma_20': ma_20.tail(30).tolist(),
            'ma_50': ma_50.tail(30).tolist(),
            'rsi': rsi.tail(30).tolist(),
            'upper_band': upper_band.tail(30).tolist(),
            'lower_band': lower_band.tail(30).tolist(),
            'sma': sma.tail(30).tolist()
        }
        
        return jsonify({'success': True, 'indicators': indicators})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/correlation', methods=['GET'])
def get_correlation():
    try:
        correlation = processor.get_correlation_matrix()
        return jsonify({'success': True, 'correlation': correlation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/monthly', methods=['GET'])
def get_monthly_summary():
    try:
        monthly = processor.get_monthly_summary()
        
        monthly['YearMonth'] = monthly['YearMonth'].astype(str)
        monthly_data = monthly.tail(12).to_dict('records')
        
        return jsonify({'success': True, 'monthly': monthly_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/outliers', methods=['GET'])
def get_outliers():
    try:
        threshold = request.args.get('threshold', 3.0, type=float)
        outliers = processor.detect_outliers(threshold)
        
        if len(outliers) == 0:
            return jsonify({'success': True, 'outliers': []})
        
        # 处理日期列，确保转换为字符串
        if 'Date' in outliers.columns:
            outliers['Date'] = outliers['Date'].apply(lambda x: str(x) if hasattr(x, 'strftime') else str(x))
        
        outliers_data = outliers.to_dict('records')
        
        return jsonify({'success': True, 'outliers': outliers_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/upload', methods=['POST'])
def upload_data():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not file.filename.endswith(('.txt', '.csv')):
            return jsonify({'error': '只支持.txt或.csv文件'}), 400
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            file.save(f.name)
            temp_path = f.name
        
        data = processor.load_data(temp_path)
        
        os.unlink(temp_path)
        
        return jsonify({
            'success': True,
            'count': len(data),
            'date_range': {
                'start': data['Date'].min().strftime('%Y-%m-%d'),
                'end': data['Date'].max().strftime('%Y-%m-%d')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/export', methods=['GET'])
def export_data():
    try:
        data = processor.filtered_data if processor.filtered_data is not None else processor.data
        
        if data is None or len(data) == 0:
            return jsonify({'error': '无数据可导出'}), 400
        
        output_file = f'export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        data.to_csv(output_file, index=False)
        
        return send_file(output_file, as_attachment=True, download_name=output_file)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)