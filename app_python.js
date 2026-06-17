// 根据环境自动选择API地址
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api'
    : '/api';

let currentData = null;
let allCategories = null;
let retryCount = 0;
const MAX_RETRIES = 3;

// 图表描述信息
const chartDescriptions = {
    kline: {
        title: 'K线图（蜡烛图）',
        description: 'K线图是金融领域最常用的图表类型，展示股票价格的四个关键数据点：开盘价、收盘价、最高价和最低价。',
        features: [
            '绿色K线表示收盘价高于开盘价（上涨）',
            '红色K线表示收盘价低于开盘价（下跌）',
            '下方柱状图展示对应日期的交易量',
            '通过K线实体大小和影线长度判断买卖力量对比',
            '支持缩放、平移、悬停查看详细数据'
        ]
    },
    line: {
        title: '价格走势图（折线图）',
        description: '折线图展示股票价格随时间的变化趋势，帮助用户识别长期和短期的价格变动模式。',
        features: [
            '蓝色区域展示收盘价走势，填充效果增强视觉层次',
            '橙色线条展示开盘价走势',
            '通过两条线的交叉关系判断价格趋势',
            '适合观察价格的连续变化和趋势方向',
            '支持时间范围选择和数据筛选'
        ]
    },
    bar: {
        title: '交易量柱状图',
        description: '柱状图展示最近50个交易日的交易量变化，颜色根据当日涨跌自动调整。',
        features: [
            '绿色柱子表示当日收盘价高于开盘价（上涨日）',
            '红色柱子表示当日收盘价低于开盘价（下跌日）',
            '柱子高度代表交易量大小',
            '通过交易量变化判断市场活跃度',
            '交易量与价格波动通常存在相关性'
        ]
    },
    area: {
        title: '价格区间面积图',
        description: '面积图展示每日的最高价和最低价区间，直观反映市场波动性。',
        features: [
            '红色线条表示每日最高价',
            '蓝色线条表示每日最低价',
            '阴影区域表示价格波动区间',
            '区间宽度变化反映市场波动性变化',
            '区间扩大表明市场波动加剧'
        ]
    },
    scatter: {
        title: '交易量与价格散点图',
        description: '散点图展示交易量与收盘价的关系，颜色表示当日收益率。',
        features: [
            'X轴表示交易量，Y轴表示收盘价',
            '颜色从红色到绿色表示收益率从负到正',
            '通过散点分布判断交易量与价格的关系',
            '可识别异常交易量和价格波动',
            '支持悬停查看具体数据点信息'
        ]
    },
    heatmap: {
        title: '相关性热力图',
        description: '热力图展示不同价格指标之间的相关性系数，帮助理解指标间的关联程度。',
        features: [
            '红色表示正相关，蓝色表示负相关',
            '颜色深浅表示相关性强度',
            '数值范围从-1到1，绝对值越大相关性越强',
            '对角线数值为1（自身相关）',
            '可快速识别高度相关的指标组合'
        ]
    },
    boxplot: {
        title: '月度收盘价箱线图',
        description: '箱线图展示各月份收盘价的统计分布，识别季节性规律和异常值。',
        features: [
            '箱子表示四分位数范围（25%-75%）',
            '中间线表示中位数',
            '须线表示数据范围（排除异常值）',
            '圆点表示异常值',
            '可识别各月份的价格波动特征'
        ]
    },
    pie: {
        title: '月度交易量占比饼图',
        description: '饼图展示最近8个月交易量的占比情况，直观比较各月交易活跃度。',
        features: [
            '每个扇形代表一个月的交易量',
            '扇形大小表示交易量占比',
            '显示百分比标签',
            '环形设计增强视觉效果',
            '可快速识别交易量最大的月份'
        ]
    },
    technical: {
        title: '技术指标分析',
        description: '综合展示移动平均线、涨跌幅和交易量，辅助技术分析决策。',
        features: [
            '上方：收盘价和移动平均线（MA20）',
            '中间：每日涨跌幅（绿色涨红色跌）',
            '下方：交易量变化趋势',
            '三条图表共享X轴时间轴',
            '通过多指标综合判断市场趋势'
        ]
    },
    distribution: {
        title: '价格与交易量分布',
        description: '双直方图展示收盘价和交易量的分布情况，了解数据的统计特征。',
        features: [
            '左侧：收盘价分布直方图',
            '右侧：交易量分布直方图',
            '通过分布形状判断数据特征',
            '可识别价格和交易量的集中区域',
            '辅助理解数据的偏态和峰态'
        ]
    },
    returns: {
        title: '收益率分布分析',
        description: '展示收益率的直方图和Q-Q图，检验收益率是否符合正态分布。',
        features: [
            '左侧：收益率直方图',
            '右侧：收益率Q-Q图（分位数-分位数图）',
            'Q-Q图中点越接近对角线，数据越接近正态分布',
            '可识别收益率的尖峰厚尾特征',
            '辅助选择合适的统计模型'
        ]
    }
};

// 更新图表描述
function updateChartDescription(chartType) {
    const desc = chartDescriptions[chartType];
    if (!desc) return;

    const descElement = document.getElementById('chartDescription');
    let html = `<h4>${desc.title}</h4>`;
    html += `<p>${desc.description}</p>`;
    html += '<ul>';
    desc.features.forEach(feature => {
        html += `<li>${feature}</li>`;
    });
    html += '</ul>';
    descElement.innerHTML = html;
}

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    retryCount = 0;
    return await fetchWithRetry(`${API_BASE}${endpoint}`, options);
}

async function fetchWithRetry(url, options, retries = MAX_RETRIES) {
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.success && result.error) {
            throw new Error(result.error);
        }
        
        return result;
    } catch (error) {
        if (retries > 0 && (error.message.includes('Failed to fetch') || 
                           error.message.includes('NetworkError') ||
                           error.message.includes('net::ERR_'))) {
            retryCount++;
            console.log(`网络错误，${retryCount}/${MAX_RETRIES} 次重试...`);
            await new Promise(resolve => setTimeout(resolve, 2000 * retryCount));
            return fetchWithRetry(url, options, retries - 1);
        }
        
        console.error('API请求错误:', error);
        alert(`数据加载失败: ${error.message}\n请刷新页面重试`);
        return null;
    }
}

async function loadSources() {
    const result = await apiRequest('/data/sources', 'GET');
    
    if (result && result.success) {
        allCategories = result.categories;
    }
}

async function loadCategory() {
    const categorySelector = document.getElementById('categorySelector');
    const dataSelector = document.getElementById('dataSelector');
    const category = categorySelector.value;
    
    dataSelector.innerHTML = '<option value="">选择数据源</option>';
    
    if (!category || !allCategories) {
        return;
    }
    
    const categoryData = allCategories[category];
    if (categoryData && categoryData.items) {
        categoryData.items.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.name;
            dataSelector.appendChild(option);
        });
    }
}

async function loadData() {
    const selector = document.getElementById('dataSelector');
    const source = selector.value;
    
    if (!source) {
        clearAllCharts();
        resetStats();
        return;
    }
    
    const result = await apiRequest('/data/load', 'POST', { source });
    
    if (result && result.success) {
        await updateStatistics();
        await updateChart();
        
        const rangeResult = await apiRequest(`/data/range?symbol=${source}`);
        if (rangeResult && rangeResult.success) {
            document.getElementById('startDate').value = rangeResult.start_date;
            document.getElementById('endDate').value = rangeResult.end_date;
            document.getElementById('dateRangeInfo').textContent = `(最早: ${rangeResult.earliest_date})`;
        }
        
        document.getElementById('predictionSection').style.display = 'none';
        document.getElementById('analysisSection').style.display = 'none';
    }
}

async function updateStatistics() {
    const result = await apiRequest('/data/statistics');
    
    if (result && result.success) {
        const stats = result.statistics;
        document.getElementById('statCount').textContent = stats.count.toLocaleString();
        document.getElementById('statAvgClose').textContent = stats.avg_close.toFixed(2);
        document.getElementById('statMaxClose').textContent = stats.max_close.toFixed(2);
        document.getElementById('statMinClose').textContent = stats.min_close.toFixed(2);
        document.getElementById('statAvgVolume').textContent = (stats.avg_volume / 1000000).toFixed(2) + 'M';
        document.getElementById('statVolatility').textContent = (stats.volatility * 100).toFixed(2) + '%';
    }
}

function resetStats() {
    document.getElementById('statCount').textContent = '0';
    document.getElementById('statAvgClose').textContent = '0';
    document.getElementById('statMaxClose').textContent = '0';
    document.getElementById('statMinClose').textContent = '0';
    document.getElementById('statAvgVolume').textContent = '0';
    document.getElementById('statVolatility').textContent = '0';
}

async function updateChart() {
    const chartType = getChartType();
    const result = await apiRequest(`/visualize/${chartType}`, 'POST');

    if (result && result.success) {
        const chartContainer = document.getElementById('mainChart');
        chartContainer.innerHTML = '';

        try {
            const figData = JSON.parse(result.chart_json);
            Plotly.newPlot('mainChart', figData.data, figData.layout);
            // 更新图表描述
            updateChartDescription(chartType);
        } catch (error) {
            console.error('图表渲染失败:', error);
            chartContainer.innerHTML = '<p>图表渲染失败</p>';
        }
    }
}

function getChartType() {
    const radios = document.querySelectorAll('input[name="chartType"]');
    for (const radio of radios) {
        if (radio.checked) return radio.value;
    }
    return 'kline';
}

async function filterData() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const selector = document.getElementById('dataSelector');
    const source = selector.value;
    
    if (!source) {
        alert('请先选择股票');
        return;
    }
    
    if (!startDate || !endDate) {
        alert('请选择开始和结束日期');
        return;
    }
    
    const result = await apiRequest('/data/load', 'POST', {
        source,
        start_date: startDate,
        end_date: endDate
    });
    
    if (result && result.success) {
        await updateStatistics();
        await updateChart();
    }
}

async function uploadData() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('请选择文件');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE}/data/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('数据上传成功！');
            await updateStatistics();
            await updateChart();
        } else {
            alert(`上传失败: ${result.error}`);
        }
    } catch (error) {
        alert(`错误: ${error.message}`);
    }
}

async function exportData() {
    try {
        const response = await fetch(`${API_BASE}/data/export`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `financial_data_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            const result = await response.json();
            alert(`导出失败: ${result.error}`);
        }
    } catch (error) {
        alert(`错误: ${error.message}`);
    }
}

async function runPrediction() {
    const days = parseInt(document.getElementById('predictDays').value) || 30;
    const model = document.getElementById('modelSelector').value;
    
    const result = await apiRequest('/predict', 'POST', {
        days,
        model
    });
    
    if (result && result.success) {
        displayPrediction(result.prediction);
    }
}

function displayPrediction(prediction) {
    if (!prediction || !prediction.predictions || prediction.predictions.length === 0) {
        alert('预测结果无效');
        return;
    }

    const section = document.getElementById('predictionSection');
    section.style.display = 'block';

    document.getElementById('predTrend').textContent = prediction.trend || '未知';
    document.getElementById('predTotalReturn').textContent = (prediction.total_return || 0).toFixed(2) + '%';
    document.getElementById('predLastPrice').textContent = (prediction.last_price || 0).toFixed(2);
    document.getElementById('predDays').textContent = prediction.predictions.length;
    document.getElementById('predConfidence').textContent = ((prediction.confidence_level || 0.95) * 100).toFixed(0) + '%';

    const dates = prediction.predictions.map(p => String(p.date));
    const prices = prediction.predictions.map(p => Number(p.predicted_price));
    const upper = prediction.predictions.map(p => Number(p.upper_bound));
    const lower = prediction.predictions.map(p => Number(p.lower_bound));

    const trace1 = {
        x: dates,
        y: prices,
        type: 'scatter',
        mode: 'lines+markers',
        name: '预测价格',
        line: { color: '#00d2ff', width: 2 }
    };

    const trace2 = {
        x: dates,
        y: upper,
        type: 'scatter',
        mode: 'lines',
        name: '上限',
        line: { color: '#e74c3c', width: 1, dash: 'dash' }
    };

    const trace3 = {
        x: dates,
        y: lower,
        type: 'scatter',
        mode: 'lines',
        name: '下限',
        line: { color: '#e74c3c', width: 1, dash: 'dash' },
        fill: 'tonexty',
        fillcolor: 'rgba(231, 76, 60, 0.1)'
    };

    const layout = {
        title: '价格预测',
        template: 'plotly_dark',
        height: 500,
        xaxis: { title: '日期' },
        yaxis: { title: '价格' }
    };

    Plotly.newPlot('predictionChart', [trace1, trace2, trace3], layout);

    // 更新预测结果描述
    const descElement = document.getElementById('predictionDescription');
    const trendText = prediction.trend === '上涨' ? '上升趋势' : (prediction.trend === '下跌' ? '下降趋势' : '震荡趋势');
    let html = `<h4>📈 机器学习价格预测分析</h4>`;
    html += `<p>基于历史数据和技术指标，使用机器学习模型对未来${prediction.predictions.length}个交易日的股票价格进行预测。</p>`;
    html += '<ul>';
    html += `<li><strong>预测趋势：</strong>${trendText}，预计总收益率为${(prediction.total_return || 0).toFixed(2)}%</li>`;
    html += `<li><strong>当前价格：</strong>${(prediction.last_price || 0).toFixed(2)}，作为预测起点</li>`;
    html += `<li><strong>置信区间：</strong>红色虚线表示预测的上下限，实际价格有${((prediction.confidence_level || 0.95) * 100).toFixed(0)}%的概率落在该区间内</li>`;
    html += `<li><strong>蓝色实线：</strong>表示模型预测的价格走势</li>`;
    html += `<li><strong>阴影区域：</strong>表示价格的不确定性范围，区间越宽表示预测不确定性越大</li>`;
    html += '<li><strong>注意事项：</strong>预测仅供参考，不构成投资建议，金融市场受多种因素影响</li>';
    html += '</ul>';
    descElement.innerHTML = html;
}

async function compareModels() {
    const result = await apiRequest('/predict/compare', 'POST');
    
    if (result && result.success) {
        displayModelComparison(result.comparison);
    }
}

function displayModelComparison(comparison) {
    const section = document.getElementById('analysisSection');
    section.style.display = 'block';

    const models = Object.keys(comparison);
    const metrics = ['mse', 'mae', 'r2', 'rmse'];

    // 创建模型对比图表
    const displayMetrics = ['r2', 'mse', 'mae', 'rmse'];
    const metricNames = { 'r2': 'R²', 'mse': 'MSE', 'mae': 'MAE', 'rmse': 'RMSE' };
    const colors = ['#10b981', '#ef4444', '#f59e0b', '#3b82f6'];

    const traces = displayMetrics.map((metric, index) => {
        const values = models.map(model => comparison[model].metrics ? comparison[model].metrics[metric] : null);
        return {
            x: models,
            y: values,
            type: 'bar',
            name: metricNames[metric],
            marker: { color: colors[index] }
        };
    });

    const layout = {
        title: '模型性能对比',
        xaxis: { title: '模型', tickangle: -45 },
        yaxis: { title: '指标值' },
        barmode: 'group',
        showlegend: true,
        height: 400,
        margin: { t: 50, b: 80 }
    };

    Plotly.newPlot('analysisChart', traces, layout);

    // 创建表格
    let html = '<table class="comparison-table"><thead><tr><th>模型</th>';
    metrics.forEach(m => html += `<th>${m.toUpperCase()}</th>`);
    html += '</tr></thead><tbody>';

    models.forEach(model => {
        html += `<tr><td>${model}</td>`;
        if (comparison[model].metrics) {
            metrics.forEach(m => {
                const value = comparison[model].metrics[m];
                html += `<td>${value.toFixed(4)}</td>`;
            });
        } else {
            html += '<td colspan="4">-</td>';
        }
        html += '</tr>';
    });

    html += '</tbody></table>';
    document.getElementById('analysisTable').innerHTML = html;

    // 更新模型对比描述
    const descElement = document.getElementById('analysisDescription');
    let descHtml = `<h4>🤖 机器学习模型性能对比</h4>`;
    descHtml += '<p>对比三种机器学习模型在测试集上的表现，评估模型的预测准确性和稳定性。</p>';
    descHtml += '<ul>';
    descHtml += '<li><strong>R²（决定系数）：</strong>值越接近1，模型解释能力越强，绿色柱子表示</li>';
    descHtml += '<li><strong>MSE（均方误差）：</strong>值越小，预测误差越小，红色柱子表示</li>';
    descHtml += '<li><strong>MAE（平均绝对误差）：</strong>值越小，预测越准确，黄色柱子表示</li>';
    descHtml += '<li><strong>RMSE（均方根误差）：</strong>值越小，预测越稳定，蓝色柱子表示</li>';
    descHtml += '<li><strong>随机森林：</strong>集成学习方法，抗过拟合能力强，适合复杂非线性关系</li>';
    descHtml += '<li><strong>梯度提升：</strong>逐步优化模型，预测精度高，但训练时间较长</li>';
    descHtml += '<li><strong>线性回归：</strong>简单快速，适合线性关系，但对非线性数据拟合能力有限</li>';
    descHtml += '</ul>';
    descElement.innerHTML = descHtml;
}

async function showIndicators() {
    const result = await apiRequest('/analysis/indicators');
    
    if (result && result.success) {
        displayIndicators(result.indicators);
    }
}

function displayIndicators(indicators) {
    const section = document.getElementById('analysisSection');
    section.style.display = 'block';
    document.getElementById('analysisTable').innerHTML = '';

    const trace1 = {
        y: indicators.ma_20,
        type: 'scatter',
        mode: 'lines',
        name: 'MA20',
        line: { color: '#00d2ff' }
    };

    const trace2 = {
        y: indicators.ma_50,
        type: 'scatter',
        mode: 'lines',
        name: 'MA50',
        line: { color: '#f39c12' }
    };

    const trace3 = {
        y: indicators.rsi,
        type: 'scatter',
        mode: 'lines',
        name: 'RSI',
        line: { color: '#e74c3c' }
    };

    const layout = {
        title: '技术指标',
        template: 'plotly_dark',
        height: 400
    };

    Plotly.newPlot('analysisChart', [trace1, trace2, trace3], layout);

    // 更新技术指标描述
    const descElement = document.getElementById('analysisDescription');
    let descHtml = `<h4>📊 技术指标分析</h4>`;
    descHtml += '<p>展示常用的技术分析指标，辅助判断市场趋势和买卖时机。</p>';
    descHtml += '<ul>';
    descHtml += '<li><strong>MA20（20日移动平均线）：</strong>蓝色线条，反映短期价格趋势，价格突破MA20通常视为买入信号</li>';
    descHtml += '<li><strong>MA50（50日移动平均线）：</strong>橙色线条，反映中期价格趋势，MA20上穿MA50形成金叉为看涨信号</li>';
    descHtml += '<li><strong>RSI（相对强弱指标）：</strong>红色线条，取值范围0-100，超过70为超买区，低于30为超卖区</li>';
    descHtml += '<li><strong>金叉信号：</strong>短期均线上穿长期均线，预示上涨趋势</li>';
    descHtml += '<li><strong>死叉信号：</strong>短期均线下穿长期均线，预示下跌趋势</li>';
    descHtml += '<li><strong>使用建议：</strong>结合多个指标综合判断，单一指标可能产生误判</li>';
    descHtml += '</ul>';
    descElement.innerHTML = descHtml;
}

async function showCorrelation() {
    const result = await apiRequest('/analysis/correlation');
    
    if (result && result.success) {
        displayCorrelation(result.correlation);
    }
}

function displayCorrelation(correlation) {
    const section = document.getElementById('analysisSection');
    section.style.display = 'block';
    document.getElementById('analysisTable').innerHTML = '';

    const cols = Object.keys(correlation);
    const z = cols.map(col => cols.map(row => correlation[col][row]));

    const trace = {
        z: z,
        x: cols,
        y: cols,
        type: 'heatmap',
        colorscale: 'RdBu',
        zmid: 0
    };

    const layout = {
        title: '相关性矩阵',
        template: 'plotly_dark',
        height: 500
    };

    Plotly.newPlot('analysisChart', [trace], layout);

    // 更新相关性分析描述
    const descElement = document.getElementById('analysisDescription');
    let descHtml = `<h4>🔗 相关性分析</h4>`;
    descHtml += '<p>展示不同价格指标之间的相关性系数，帮助理解指标间的关联程度。</p>';
    descHtml += '<ul>';
    descHtml += '<li><strong>红色区域：</strong>表示正相关（系数>0），指标同向变化</li>';
    descHtml += '<li><strong>蓝色区域：</strong>表示负相关（系数<0），指标反向变化</li>';
    descHtml += '<li><strong>颜色深浅：</strong>表示相关性强度，颜色越深相关性越强</li>';
    descHtml += '<li><strong>数值范围：</strong>从-1到1，绝对值越大相关性越强</li>';
    descHtml += '<li><strong>对角线：</strong>数值为1，表示指标自身完全相关</li>';
    descHtml += '<li><strong>应用场景：</strong>识别高度相关的指标，避免特征冗余，优化模型输入</li>';
    descHtml += '</ul>';
    descElement.innerHTML = descHtml;
}

async function showMonthly() {
    const result = await apiRequest('/analysis/monthly');
    
    if (result && result.success) {
        displayMonthly(result.monthly);
    }
}

function displayMonthly(monthly) {
    const section = document.getElementById('analysisSection');
    section.style.display = 'block';
    document.getElementById('analysisChart').innerHTML = '';

    let html = '<table class="data-table"><thead><tr><th>月份</th><th>开盘</th><th>收盘</th><th>最高</th><th>最低</th><th>收益率(%)</th></tr></thead><tbody>';

    monthly.forEach(m => {
        html += `<tr>
            <td>${m.YearMonth}</td>
            <td>${m.Open.toFixed(2)}</td>
            <td>${m.Close.toFixed(2)}</td>
            <td>${m.High.toFixed(2)}</td>
            <td>${m.Low.toFixed(2)}</td>
            <td>${m.Return.toFixed(2)}</td>
        </tr>`;
    });

    html += '</tbody></table>';
    document.getElementById('analysisTable').innerHTML = html;

    // 更新月度汇总描述
    const descElement = document.getElementById('analysisDescription');
    let descHtml = `<h4>📅 月度数据汇总</h4>`;
    descHtml += '<p>按月份汇总股票价格和收益率数据，识别季节性规律和长期趋势。</p>';
    descHtml += '<ul>';
    descHtml += '<li><strong>月份：</strong>数据所属的年月</li>';
    descHtml += '<li><strong>开盘/收盘：</strong>该月第一个和最后一个交易日的价格</li>';
    descHtml += '<li><strong>最高/最低：</strong>该月内的最高价和最低价</li>';
    descHtml += '<li><strong>收益率：</strong>该月价格涨跌幅度，正数表示上涨</li>';
    descHtml += '<li><strong>季节性分析：</strong>通过比较不同月份的表现，识别季节性规律</li>';
    descHtml += '<li><strong>趋势判断：</strong>连续多月上涨或下跌反映长期趋势</li>';
    descHtml += '</ul>';
    descElement.innerHTML = descHtml;
}

async function showOutliers() {
    const result = await apiRequest('/analysis/outliers');
    
    if (result && result.success) {
        displayOutliers(result.outliers);
    }
}

function displayOutliers(outliers) {
    const section = document.getElementById('analysisSection');
    section.style.display = 'block';
    document.getElementById('analysisChart').innerHTML = '';

    if (outliers.length === 0) {
        document.getElementById('analysisTable').innerHTML = '<p>未检测到异常值</p>';
        const descElement = document.getElementById('analysisDescription');
        let descHtml = `<h4>🔍 异常值检测</h4>`;
        descHtml += '<p>基于Z-score方法检测数据中的异常值。</p>';
        descHtml += '<ul>';
        descHtml += '<li><strong>检测方法：</strong>使用Z-score统计方法，识别偏离均值超过3个标准差的数据点</li>';
        descHtml += '<li><strong>检测结果：</strong>当前数据未检测到异常值，数据质量良好</li>';
        descHtml += '<li><strong>异常值影响：</strong>异常值可能影响模型训练和预测准确性</li>';
        descHtml += '<li><strong>处理建议：</strong>如发现异常值，可考虑剔除或进行平滑处理</li>';
        descHtml += '</ul>';
        descElement.innerHTML = descHtml;
        return;
    }

    let html = '<table class="data-table"><thead><tr><th>日期</th><th>开盘</th><th>收盘</th><th>最高</th><th>最低</th><th>交易量</th></tr></thead><tbody>';

    outliers.forEach(o => {
        html += `<tr>
            <td>${o.Date}</td>
            <td>${o.Open.toFixed(2)}</td>
            <td>${o.Close.toFixed(2)}</td>
            <td>${o.High.toFixed(2)}</td>
            <td>${o.Low.toFixed(2)}</td>
            <td>${o.Volume.toLocaleString()}</td>
        </tr>`;
    });

    html += '</tbody></table>';
    document.getElementById('analysisTable').innerHTML = html;

    // 更新异常值检测描述
    const descElement = document.getElementById('analysisDescription');
    let descHtml = `<h4>🔍 异常值检测</h4>`;
    descHtml += '<p>基于Z-score方法检测数据中的异常值，识别可能的数据质量问题。</p>';
    descHtml += '<ul>';
    descHtml += '<li><strong>检测方法：</strong>使用Z-score统计方法，识别偏离均值超过3个标准差的数据点</li>';
    descHtml += `<li><strong>检测数量：</strong>共检测到${outliers.length}个异常值</li>`;
    descHtml += '<li><strong>异常值特征：</strong>价格或交易量显著偏离正常范围</li>';
    descHtml += '<li><strong>可能原因：</strong>市场突发事件、数据错误、特殊交易日等</li>';
    descHtml += '<li><strong>处理建议：</strong>检查数据准确性，确认是否为真实异常，考虑剔除或平滑处理</li>';
    descHtml += '<li><strong>影响分析：</strong>异常值可能影响统计分析和模型预测的准确性</li>';
    descHtml += '</ul>';
    descElement.innerHTML = descHtml;
}

function clearAllCharts() {
    document.getElementById('mainChart').innerHTML = '';
    document.getElementById('predictionChart').innerHTML = '';
    document.getElementById('analysisChart').innerHTML = '';
    document.getElementById('analysisTable').innerHTML = '';
}

document.querySelectorAll('input[name="chartType"]').forEach(radio => {
    radio.addEventListener('change', updateChart);
});

window.addEventListener('resize', () => {
    Plotly.Plots.resize('mainChart');
    Plotly.Plots.resize('predictionChart');
    Plotly.Plots.resize('analysisChart');
});

document.addEventListener('DOMContentLoaded', async () => {
    await loadSources();
});