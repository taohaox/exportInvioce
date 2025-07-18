# 商业发票一键导出系统

## 项目简介
本项目为一套基于 Flask（后端）+ HTML/JS（前端）的商业发票自动生成系统，支持智能识别收货信息、动态填写商品明细、一键导出 Word 发票文档。适用于出口贸易、跨境电商等场景。

## 主要功能
- 智能识别收货信息（AI接口，自动提取联系人、地址、电话、邮编）
- 商品明细动态增删、自动统计件数与总货值
- 一键导出标准 Word 发票（.docx）
- 前后端分离，支持跨域
- 适配本地与服务器部署，前端自动适配后端地址

## 目录结构
```
├── app.py           # Word生成主逻辑
├── server.py        # Flask后端服务，含AI识别接口
├── demo_ai.py       # AI接口调用示例
├── index.html       # 前端页面
├── requirements.txt # Python依赖
└── README.md        # 项目说明
```

## 环境依赖
- Python 3.8+
- Flask
- flask-cors
- python-docx
- openai（兼容阿里云百炼API）

安装依赖：
```bash
pip install -r requirements.txt
```

## AI接口配置
- 需注册阿里云百炼平台并获取 API Key。
- 设置环境变量 `DASHSCOPE_API_KEY`，或在 `server.py`/`demo_ai.py` 里直接填写。

## 启动后端
```bash
python server.py
```
默认监听 5001 端口。

## 启动前端
直接用浏览器打开 `index.html` 即可。
- 本地开发：建议用 VSCode Live Server 或 Python SimpleHTTPServer 运行静态页面。
- 服务器部署：将 `index.html` 放到 Nginx/Apache/wwwroot 等静态目录。

## 常见问题
- **导出报错/文件被占用**：已修复，确保 Flask 用 after_this_request 删除临时文件。
- **AI接口异常**：请检查 API Key 配置与网络连通性。
- **跨域问题**：已全局支持 CORS。
- **前后端地址适配**：前端自动用 window.location.origin，无需手动配置。

## 联系方式
如有问题或定制需求，请联系开发者。
