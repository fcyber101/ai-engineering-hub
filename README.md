# ai-engineering-hub
A collection of LLM-powered applications and projects

🌟 AI Engineering Hub
<div align="center">
https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white

https://img.shields.io/badge/Python-3.9%252B-3776AB?logo=python&logoColor=white
https://img.shields.io/badge/LangChain-0.1.0-1C3C3C?logo=langchain&logoColor=white
https://img.shields.io/badge/LangGraph-0.0.20-7C3AED
https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai&logoColor=white
https://img.shields.io/badge/Anthropic-Claude-CC5A4A?logo=anthropic&logoColor=white
https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B?logo=streamlit&logoColor=white
https://img.shields.io/badge/License-MIT-yellow
https://img.shields.io/badge/Contributions-Welcome-brightgreen

<h3>A curated collection of production-ready LLM applications built with RAG, AI Agents, Agentic Systems, MCP, and more</h3> <p> This repository features LLM apps that use models from <strong>OpenAI</strong>, <strong>Anthropic</strong>, <strong>Google</strong>, <strong>xAI</strong> and open-source models like <strong>Qwen</strong> or <strong>Llama</strong> that you can run locally on your computer. </p> <br> <!-- Multi-language support --> <p> <strong>English</strong> | <a href="#">Deutsch</a> | <a href="#">Español</a> | <a href="#">Français</a> | <a href="#">日本語</a> | <a href="#">한국어</a> | <a href="#">Português</a> | <a href="#">Русский</a> | <a href="#">中文</a> </p> <br>
<a href="#-featured-ai-projects">📂 Featured AI Projects</a> •
<a href="#-getting-started">🚀 Getting Started</a> •
<a href="#-why-ai-engineering-hub">🤔 Why AI Engineering Hub?</a> •
<a href="#-contributing">🤝 Contributing</a> •
<a href="#-thank-you">🙏 Thank You</a>

<br> <br>
<sub>Supported by</sub>


<a href="#"><img src="https://img.shields.io/badge/TinyFish-Sponsor-FF6B6B?style=for-the-badge&logo=fish&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/Tiger_Data_MCP-Sponsor-FF8800?style=for-the-badge&logo=tiger&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/Speechmatics-Sponsor-4A90E2?style=for-the-badge&logo=speechmatics&logoColor=white" /></a>


<a href="#"><sub>Become a Sponsor</sub></a>

</div>
🤔 Why AI Engineering Hub?
<div align="center">
💡 Discover	🔥 Explore	🎓 Learn
Discover practical and creative ways LLMs can be applied across different domains, from document analysis to intelligent agents and more.	Explore apps that combine LLMs from OpenAI, Anthropic, Gemini, and open-source alternatives with AI Agents, Agent Teams, MCP, and Agentic RAG.	Learn from well-documented projects and contribute to the growing open-source ecosystem of LLM-powered applications.
</div>
📂 Featured AI Projects
👨‍💼 Agentic RAG Assistant
Smart Q&A Assistant with intelligent routing, query refinement, hallucination checking, self-correction loops, and hybrid retrieval

<div align="center">
https://img.shields.io/badge/Status-Active-success
https://img.shields.io/badge/Difficulty-Advanced-red
https://img.shields.io/badge/LangGraph-%E2%9C%93-purple
https://img.shields.io/badge/Hybrid_Search-%E2%9C%93-blue
https://img.shields.io/badge/Self_Correction-%E2%9C%93-orange

</div>
A sophisticated question-answering system that goes beyond traditional RAG by incorporating intelligent agentic behaviors:

Feature	Description
🔀 Intelligent Routing	Dynamically routes queries to specialized agents based on intent analysis
🔍 Query Refinement	Self-improves queries through reflection and rewriting
✅ Hallucination Checking	Validates responses against source documents with faithfulness scoring
🔄 Self-Correction Loops	Automatically detects and fixes inadequate responses
📊 Hybrid Retrieval	Combines semantic, keyword, and knowledge graph search
View Project →

🚧 More Projects Coming Soon
<details> <summary><b>🔮 Planned Projects (Click to Expand)</b></summary> <br>
Project	Description	Status
🗣️ Voice RAG Agent	Voice-enabled Q&A with real-time transcription	Planned
🌐 MCP Browser Agent	Browser automation with Model Context Protocol	Planned
🤝 Multi-Agent Research Team	Collaborative research agents with handoffs	Planned
📄 Chat with PDF (RAG)	Document Q&A with hybrid search	Planned
💬 Stateful Chat with Memory	Conversational AI with persistent memory	Planned
</details>
🚀 Getting Started
Clone the repository
bash
git clone https://github.com/yourusername/ai-engineering-hub.git
Navigate to the desired project directory
bash
cd ai-engineering-hub/01-agentic-rag-assistant
Install the required dependencies
bash
pip install -r requirements.txt
Set up environment variables
bash
cp .env.example .env
# Edit .env with your API keys
Run the application
bash
streamlit run app.py
Follow the project-specific instructions in each project's README.md file to set up and run the app with all features.

📁 Repository Structure
text
ai-engineering-hub/
├── 📁 01-agentic-rag-assistant/     # Agentic RAG Assistant
│   ├── app.py                       # Main application
│   ├── requirements.txt             # Dependencies
│   ├── README.md                    # Project documentation
│   ├── .env.example                 # Environment variables
│   └── assets/                      # Screenshots & diagrams
│
├── 📁 02-*/                         # Coming soon
├── 📁 03-*/                         # Coming soon
├── 📁 assets/                       # Global assets
├── .gitignore
├── LICENSE
└── README.md                        # You are here
🛠️ Technology Stack
Category	Technologies
LLM Frameworks	LangChain, LangGraph, LlamaIndex
Models	GPT-4, Claude 3, Gemini Pro, Llama 3, Qwen
Vector Databases	Pinecone, Chroma, Weaviate, Qdrant
Embeddings	OpenAI, Cohere, HuggingFace
Frontend	Streamlit, Gradio, Chainlit
Monitoring	LangSmith, Arize
Deployment	Streamlit Cloud, Docker, AWS
🤝 Contributing
We welcome contributions! Here's how you can help:

📋 Contribution Guidelines
Fork the repository

Create a feature branch (git checkout -b feature/amazing-project)

Commit your changes (git commit -m 'Add amazing project')

Push to the branch (git push origin feature/amazing-project)

Open a Pull Request

✅ Checklist for New Projects
Self-contained directory with descriptive name

Comprehensive README with setup instructions

Working demo with clear setup steps

.env.example with all required variables

requirements.txt with pinned versions

Screenshots demonstrating functionality

📊 Repository Stats
<div align="center">
https://img.shields.io/github/stars/yourusername/ai-engineering-hub?style=social
https://img.shields.io/github/forks/yourusername/ai-engineering-hub?style=social
https://img.shields.io/github/watchers/yourusername/ai-engineering-hub?style=social

</div>
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Thank You, Community, for the Support!
<div align="center">
⭐ Star this repository if you find it useful! ⭐

<br> <br>
<sub>Built with ❤️ by AI Engineers for AI Engineers</sub>


<sub>Inspired by <a href="https://github.com/Shubhamsaboo/awesome-llm-apps">Awesome LLM Apps</a></sub>

</div>
📬 Connect With Me
<div align="center">
https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white

</div>
