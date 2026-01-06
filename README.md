# 教科书阅读助手 - Textbook Reading Assistant

<div align="center">

📚 基于 DeepSeek V3 的智能教科书阅读助手 | AI-Powered Textbook Reading Assistant

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

## 📖 项目简介

教科书阅读助手是一个基于 Web 的智能学习工具，帮助学生更好地阅读和理解教科书内容。通过集成 DeepSeek V3 API，本应用提供：

- 📤 **文件上传**：支持 PDF 和图片格式
- 🔍 **文本提取**：自动从 PDF 和图片中提取文本
- 📑 **章节识别**：智能识别教科书章节结构
- 🤖 **AI 总结**：生成详细的章节学习总结
- 💬 **智能问答**：基于章节内容的智能问答系统
- 💾 **内容保存**：导出 Markdown 格式的学习笔记

## ✨ 主要功能

### 1. 文件处理
- ✅ 支持 PDF、JPG、PNG 格式
- ✅ 单文件最大 50MB
- ✅ 拖拽上传界面
- ✅ OCR 文字识别（图片）
- ✅ PDF 文本提取

### 2. 章节分析
- ✅ 自动识别章节结构
- ✅ 支持多种章节格式（中文、英文、数字编号）
- ✅ 生成章节目录树
- ✅ 可视化章节导航

### 3. AI 智能总结
使用 DeepSeek V3 为每个章节生成：
- 📝 主要内容概述
- 🔑 关键概念列表
- ⭐ 重点知识点
- 💡 难点解析
- 📚 学习建议

### 4. 智能问答
- ✅ 针对特定章节提问
- ✅ 基于内容的准确回答
- ✅ 支持上下文对话
- ✅ 对话历史记录

## 🚀 快速开始

### 环境要求

- Python 3.9 或更高版本
- pip 包管理器
- Tesseract OCR（用于图片文字识别，可选）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/1252759303liu-alt/Dick-Sir.git
cd Dick-Sir
```

2. **安装 Python 依赖**
```bash
cd backend
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 DeepSeek API Key
# DEEPSEEK_API_KEY=your_api_key_here
```

4. **（可选）安装 Tesseract OCR**

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
下载并安装：https://github.com/UB-Mannheim/tesseract/wiki

5. **启动应用**

**方法一：使用快速启动脚本（推荐）**

Linux/macOS:
```bash
./start.sh
```

Windows:
```cmd
start.bat
```

**方法二：手动启动**
```bash
cd backend
python app.py
```

6. **访问应用**

打开浏览器访问：http://localhost:8000

## 📚 使用指南

### 1️⃣ 上传教科书

1. 点击上传区域或拖拽文件
2. 选择 PDF 或图片文件
3. 等待文件上传和文本提取

### 2️⃣ 浏览章节

1. 上传成功后，系统自动分析章节结构
2. 在左侧目录中查看识别的章节
3. 点击章节标题查看内容

### 3️⃣ 生成 AI 总结

1. 选择要总结的章节
2. 切换到"总结"视图
3. 点击"生成 AI 总结"按钮
4. 等待 AI 生成详细总结

### 4️⃣ 智能问答

1. 在问答区域输入问题
2. （可选）选择特定章节
3. 点击"提问"按钮
4. 查看 AI 回答

## ⚠️ 安全提醒

**🔐 永远不要将 API Key 提交到代码仓库！**

### API Key 安全指南

1. ✅ 复制 `.env.example` 为 `.env`
2. ✅ 在 `.env` 中填入真实 API Key
3. ✅ `.env` 文件已在 `.gitignore` 中，不会被上传
4. ❌ 不要在代码中硬编码 API Key
5. ❌ 不要在公共场所分享 API Key

### 如果 API Key 泄露

如果不慎泄露 API Key，请立即：

1. 访问 https://platform.deepseek.com
2. 删除泄露的 Key
3. 生成新的 Key
4. 更新 `.env` 文件

## 🛠️ 技术架构

### 后端技术栈
- **FastAPI** - 现代 Python Web 框架
- **pdfplumber** - PDF 文本提取
- **PyPDF2** - PDF 处理（备选）
- **pytesseract** - OCR 文字识别
- **Pillow** - 图片处理
- **requests** - HTTP 请求
- **python-dotenv** - 环境变量管理

### 前端技术栈
- **HTML5 + CSS3 + JavaScript**
- **Bootstrap 5** - UI 组件库
- **Bootstrap Icons** - 图标
- **Marked.js** - Markdown 渲染

### AI 服务
- **DeepSeek V3** - 大语言模型
- **API Endpoint**: https://api.deepseek.com/v1

## 📁 项目结构

```
Dick-Sir/
├── backend/                   # 后端代码
│   ├── app.py                # FastAPI 主应用
│   ├── config.py             # 配置管理
│   ├── requirements.txt      # Python 依赖
│   ├── .env.example         # 环境变量模板
│   ├── services/            # 业务服务
│   │   ├── pdf_service.py   # PDF 处理
│   │   ├── ocr_service.py   # OCR 识别
│   │   ├── ai_service.py    # AI 服务
│   │   └── chapter_service.py # 章节识别
│   └── utils/               # 工具函数
│       └── text_processor.py # 文本处理
├── frontend/                 # 前端代码
│   ├── index.html           # 主页面
│   ├── css/
│   │   └── style.css        # 样式文件
│   └── js/
│       ├── app.js           # 主逻辑
│       └── upload.js        # 上传功能
├── uploads/                  # 上传文件存储
├── outputs/                  # 总结输出存储
├── .gitignore               # Git 忽略配置
└── README.md                # 项目文档
```

## 🔧 API 端点

### 文件上传
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (PDF/Image)
```

### 章节分析
```
POST /api/analyze-chapters
Content-Type: application/x-www-form-urlencoded
Body: text=<extracted_text>
```

### 生成总结
```
POST /api/summarize-chapter
Content-Type: application/x-www-form-urlencoded
Body: chapter_text=<text>&chapter_title=<title>
```

### 智能问答
```
POST /api/ask-question
Content-Type: application/x-www-form-urlencoded
Body: question=<question>&context=<context>&chapter_title=<title>
```

### 获取总结列表
```
GET /api/summaries
```

### 下载总结
```
GET /api/summary/{filename}
```

## 📊 性能指标

- ✅ PDF 处理：支持 100 页以内，处理时间 < 30秒
- ✅ OCR 识别：单张图片处理时间 < 5秒
- ✅ AI 总结：生成时间 < 60秒
- ✅ 文件上传：支持最大 50MB

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 常见问题

### Q: 如何获取 DeepSeek API Key？
**A:** 访问 https://platform.deepseek.com 注册账号并创建 API Key。

### Q: Tesseract OCR 必须安装吗？
**A:** 如果只使用 PDF 功能，不需要安装。图片 OCR 功能需要 Tesseract。

### Q: 支持哪些语言？
**A:** 目前主要支持中文和英文教科书。

### Q: API 调用失败怎么办？
**A:** 检查：
1. API Key 是否正确配置
2. 网络连接是否正常
3. API 额度是否充足

### Q: 上传文件后没有反应？
**A:** 检查：
1. 文件格式是否支持
2. 文件大小是否超过 50MB
3. 浏览器控制台是否有错误信息

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供强大的 AI 能力
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Bootstrap](https://getbootstrap.com/) - 优秀的 UI 组件库
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - 开源 OCR 引擎

## 📧 联系方式

如有问题或建议，欢迎通过 Issue 反馈。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个 Star！⭐**

Made with ❤️ by [1252759303liu-alt](https://github.com/1252759303liu-alt)

</div>
