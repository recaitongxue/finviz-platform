const API_BASE = 'http://localhost:5000/api';

let currentData = null;
let allCategories = null;

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
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || '请求失败');
        }
        
        return result;
    } catch (error) {
        console.error('API请求错误:', error);
        alert(`错误: ${error.message}`);
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
        
        const rangeResult = await apiRequest('/data/range');
        if (rangeResult && rangeResult.success) {
            document.getElementById('startDate').value = rangeResult.start_date;
            document.getElementById('endDate').value = rangeResult.end_date;
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
    
    if (!startDate || !endDate) {
        alert('请选择开始和结束日期');
        return;
    }
    
    const result = await apiRequest('/data/filter', 'POST', {
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