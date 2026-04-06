<div align="center">
  
[![EN](https://img.shields.io/badge/EN-English-blue)](README.md)
[![DE](https://img.shields.io/badge/DE-Deutsch-black)](README.de.md)
[![RU](https://img.shields.io/badge/RU-Русский-orange)](README.ru.md)
[![ZH](https://img.shields.io/badge/ZH-中文-yellow)](README.zh.md)

</div>



### 👨‍💼 1. 代理型RAG助手
[![Demo Video](https://img.shields.io/badge/📺-Watch%20Demo-red)](assets/project_1.gif) [![Live App](https://img.shields.io/badge/🤗-Try%20Now-yellow)](https://huggingface.co/spaces/fcyber/agentic_rag)

#### 智能问答助手，具备智能路由、查询优化、幻觉检测和自我修正循环功能。

<div align="center">

![状态](https://img.shields.io/badge/状态-活跃中-success)
![难度](https://img.shields.io/badge/难度-高级-red)
![LangGraph](https://img.shields.io/badge/LangGraph-%E2%9C%93-purple)
![混合搜索](https://img.shields.io/badge/混合搜索-%E2%9C%93-blue)
![自我修正](https://img.shields.io/badge/自我修正-%E2%9C%93-orange)

</div>

| 功能 | 描述 |
| :--- | :--- |
| **🔀 智能路由** | 基于意图分析，动态地将查询路由到专门的智能体。 |
| **🔍 查询优化** | 通过反思和重写来自我改进查询。 |
| **✅ 幻觉检测** | 通过忠实度评分，根据源文档验证响应。 |
| **🔄 自我修正** | 自动检测并修复不充分的响应。 |
| **📊 混合检索** | 结合语义搜索、关键词搜索和知识图谱搜索。 |

---

<div align="center">

![Agentischer RAG-Workflow](assets/workflow.JPG)

</div>

---


## 🚀 快速开始

### 🎯 快速启动比较（更新版）

| 方法 | 命令 | 时间 | 需要 |
|--------|---------|------|---------|
| **Python** | `pip install -r requirements.txt && python app.py` | 2-5分钟 | Python 3.9+ |
| **Docker** | `docker-compose up -d` | 30秒 | Docker + Compose |
| **Hugging Face** | [![Hugging Face](https://img.shields.io/badge/🤗%20Live%20Demo-FFD21E?style=flat-square)](https://huggingface.co/spaces/fcyber/agentic_rag) | 1秒 | 网页浏览器 |

### 📦 选项1：Python（本地设置）


1. **克隆代码库**
```bash
git clone [https://github.com/fcyber/ai-engineering-hub.git](https://github.com/fcyber/ai-engineering-hub.git)
```

2. **导航到所需项目目录**
```bash
cd ai-engineering-hub/01-agentic-rag-assistant
```

3. **安装所需的依赖项**
```bash
pip install -r requirements.txt && python app.py
```

#### 请遵循每个项目`README.md`文件中的特定项目说明来设置和运行应用。

• • •

### 🐳 选项2：Docker Compose（推荐）
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/fcyber/agentic-rag-assistant)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)


1. **克隆代码库**
```bash
git clone https://github.com/fcyber/ai-engineering-hub.git
```

2. **导航到所需项目目录**
```bash
cd ai-engineering-hub/01-agentic-rag-assistant
```

3. **设置环境变量**
```bash
cp .env.example .env
# 使用您的API密钥编辑.env文件 GROQ_API_KEY
```

4. **使用Docker Compose运行**
```bash
docker-compose up -d
```

5. **查看日志（可选）**
```bash
docker-compose logs -f
```

6. **在浏览器中打开**
```bash
http://localhost:7860
```

7. **停止容器**
```bash
docker-compose down
```

**就这样！** 项目包含预配置的`Dockerfile`和`docker-compose.yml` — 无需额外设置。

• • •

### 🤗 选项3：Hugging Face Spaces

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-FFD21E?style=for-the-badge)](https://huggingface.co/spaces/fcyber/)

```bash
# 无需安装！点击上面的徽章尝试在线演示。
# 或者克隆并在本地运行：
pip install huggingface-hub
huggingface-cli download fcyber/agentic-rag-assistant
python app.py  # Gradio应用通过python运行

```

