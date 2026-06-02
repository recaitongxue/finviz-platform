# 金融数据可视化平台 - 部署指南

本文档详细介绍如何将本项目部署到线上服务器，包含多个免费平台的部署步骤。

---

## 目录

1. [部署前准备](#部署前准备)
2. [平台一：Render（推荐）](#平台一render推荐)
3. [平台二：Railway](#平台二railway)
4. [平台三：PythonAnywhere](#平台三pythonanywhere)
5. [平台四：Vercel（纯前端）](#平台四vercel纯前端)
6. [部署验证](#部署验证)
7. [常见问题](#常见问题)

---

## 一、部署前准备

### 1.1 代码准备

确保你的代码已推送到 GitHub：

```bash
# 初始化仓库（首次）
git init
git add .
git commit -m "Initial commit"
git branch -M main

# 添加远程仓库（替换为你的 GitHub 仓库地址）
git remote add origin https://github.com/your-username/finviz-platform.git
git push -u origin main
```

### 1.2 项目结构确认

确保项目包含以下核心文件：

```
finviz-platform/
├── app.py                 # Flask 入口文件
├── data_processor.py      # 数据处理模块
├── visualizer.py          # 可视化模块
├── predictor.py           # 预测模块
├── requirements.txt       # 依赖清单
├── index_python.html      # 前端页面
├── app_python.js          # 前端逻辑
└── style.css              # 样式文件
```

### 1.3 requirements.txt 内容

```txt
Flask>=3.0.0
Flask-CORS>=4.0.0
pandas>=2.1.0
numpy>=1.26.0
plotly>=5.18.0
yfinance>=0.2.0
scikit-learn>=1.3.0
gunicorn>=21.2.0  # 生产环境 WSGI 服务器
```

---

## 二、平台一：Render（推荐）

**优点**：免费额度充足（750小时/月）、部署简单、支持 Flask

### 2.1 注册账号

访问 [Render](https://render.com)，使用 GitHub 账号登录。

### 2.2 创建 Web Service

1. 点击 **New +** → **Web Service**
2. 选择 **Connect a repository**
3. 选择你的 GitHub 仓库 `finviz-platform`
4. 点击 **Connect**

### 2.3 配置部署参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| Name | finviz-platform | 项目名称 |
| Region | Oregon (US West) | 选择就近区域 |
| Branch | main | 部署分支 |
| Build Command | `pip install -r requirements.txt` | 安装依赖 |
| Start Command | `gunicorn app:app` | 启动命令 |
| Instance Type | Free | 选择免费套餐 |

### 2.4 环境变量（可选）

如果需要配置环境变量：
- 点击 **Advanced** → **Add Environment Variable**
- 添加 `FLASK_ENV=production`

### 2.5 部署

点击 **Create Web Service**，等待部署完成。

### 2.6 获取访问地址

部署成功后，你会获得一个类似这样的 URL：
`https://finviz-platform-xxxx.onrender.com`

---

## 三、平台二：Railway

**优点**：免费额度 $5/月、支持 Python、部署灵活

### 3.1 注册账号

访问 [Railway](https://railway.app)，使用 GitHub 账号登录。

### 3.2 创建项目

1. 点击 **Start a New Project**
2. 选择 **Deploy from GitHub repo**
3. 选择你的仓库 `finviz-platform`

### 3.3 配置服务

1. 进入项目后，点击 **Add Service** → **Empty Service**
2. 在 **Settings** 中：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 3.4 设置端口

Railway 会自动分配端口，但需要确保 Flask 监听正确端口：

修改 `app.py` 添加以下代码：

```python
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### 3.5 部署

点击 **Deploy**，等待构建完成。

---

## 四、平台三：PythonAnywhere

**优点**：专门针对 Python、免费版可用、配置简单

### 4.1 注册账号

访问 [PythonAnywhere](https://www.pythonanywhere.com)，注册免费账号。

### 4.2 上传代码

1. 进入 **Files** 页面
2. 点击 **Upload a file**，上传所有项目文件
3. 或者使用 Git 克隆：
   ```bash
   git clone https://github.com/your-username/finviz-platform.git
   ```

### 4.3 创建虚拟环境

1. 进入 **Consoles** → **Bash**
2. 创建虚拟环境：
   ```bash
   cd finviz-platform
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 4.4 配置 WSGI

1. 进入 **Web** 页面
2. 点击 **Add a new web app**
3. 选择 **Flask** → **Python 3.8**
4. 修改 WSGI 配置文件：
   ```python
   import sys
   path = '/home/your-username/finviz-platform'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

### 4.5 启动服务

点击 **Reload your-username.pythonanywhere.com**

访问地址：`https://your-username.pythonanywhere.com`

---

## 五、平台四：Vercel（纯前端）

**注意**：此方案仅部署前端静态文件，无法使用后端 API。适合仅展示前端页面的场景。

### 5.1 注册账号

访问 [Vercel](https://vercel.com)，使用 GitHub 账号登录。

### 5.2 部署

1. 点击 **New Project**
2. 选择你的仓库 `finviz-platform`
3. 配置：
   - **Framework**: Other
   - **Build Command**: 留空
   - **Output Directory**: 留空

### 5.3 部署完成

Vercel 会自动部署静态文件。

---

## 六、部署验证

### 6.1 基础测试

部署成功后，访问你的网站，验证以下功能：

1. ✅ 页面正常加载
2. ✅ 选择股票后数据能正常加载
3. ✅ K线图能正常显示
4. ✅ 其他图表能正常生成

### 6.2 API 测试

使用 curl 或 Postman 测试 API：

```bash
# 测试数据源列表
curl https://your-domain.com/api/data/sources

# 测试数据加载
curl -X POST https://your-domain.com/api/data/load \
  -H "Content-Type: application/json" \
  -d '{"source": "spy"}'

# 测试 K线图生成
curl -X POST https://your-domain.com/api/visualize/kline
```

### 6.3 预期响应

**成功响应**：
```json
{
  "success": true,
  "message": "数据加载成功",
  "data": {...}
}
```

**图表响应**：
```json
{
  "success": true,
  "chart_json": "{...}"
}
```

---

## 七、常见问题

### 7.1 部署失败

**可能原因**：
- 依赖安装失败 → 检查 `requirements.txt`
- 启动命令错误 → 确认使用 `gunicorn app:app`
- 端口未正确配置 → 使用环境变量 `PORT`

### 7.2 数据加载失败

**可能原因**：
- 网络问题 → 检查服务器网络连接
- yfinance 库问题 → 确认已安装最新版本
- 股票代码错误 → 使用正确的股票代码

### 7.3 图表不显示

**可能原因**：
- Plotly JSON 格式错误 → 检查后端日志
- 前端解析错误 → 检查浏览器控制台
- CORS 问题 → 确认 Flask-CORS 已正确配置

### 7.4 内存/资源限制

**解决方案**：
- 免费版有资源限制，高峰期可能暂停服务
- 考虑升级到付费版本
- 优化代码，减少内存使用

### 7.5 部署命令参考

```bash
# 安装依赖
pip install -r requirements.txt

# 开发环境运行
python app.py

# 生产环境运行
gunicorn --workers=4 --bind=0.0.0.0:5000 app:app
```

---

## 附录：部署对比

| 平台 | 免费额度 | 适合场景 | 稳定性 |
|------|----------|----------|--------|
| Render | 750小时/月 | Flask 后端 | ⭐⭐⭐⭐⭐ |
| Railway | $5/月 | Flask 后端 | ⭐⭐⭐⭐ |
| PythonAnywhere | 1个免费应用 | Python 专属 | ⭐⭐⭐⭐ |
| Vercel | 无限 | 纯前端 | ⭐⭐⭐⭐⭐ |

---

**推荐选择**：如果需要完整功能（后端 API + 前端），推荐使用 **Render**；如果仅需前端展示，使用 **Vercel**。