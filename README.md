# Agentic Fraud Investigation Copilot

Portfolio project demonstrating how Agentic AI can augment fraud operations by assisting fraud analysts with transaction investigations, policy retrieval, explainable recommendations, and human-in-the-loop decision making.

This project was created as a portfolio project to demonstrate Product Management, Agentic AI architecture, Prompt Engineering, Retrieval-Augmented Generation (RAG), and Human-in-the-Loop (HITL) workflows for financial services.

---

## Features

- Agentic Fraud Investigation
- Retrieval-Augmented Generation (RAG)
- Explainable AI recommendations
- Human-in-the-Loop (HITL) workflow
- Policy-based decision support
- Streamlit dashboard
- Structured JSON responses
- Modular architecture

---

## Technology Stack

- Python 3.12
- Streamlit
- OpenAI API
- ChromaDB
- PyPDF
- Pandas
- Pydantic
- Python Dotenv

---

## Project Structure
agentic-fraud-investigation-copilot/

├── backend/
├── rag/
├── ui/
├── sample_data/
├── policies/
├── tests/
├── docs/
├── assets/
├── app.py
└── README.md


---

## Current Status

- [x] Product Requirements
- [x] Solution Architecture
- [x] Engineering Specifications
- [x] Prompt Engineering
- [x] Sample Investigation Cases
- [x] Policy Knowledge Base
- [ ] Backend Implementation
- [ ] RAG Implementation
- [ ] Streamlit UI
- [ ] Integration Testing

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/bsrikiran/agentic-fraud-investigation-copilot
cd agentic-fraud-investigation-copilot

Create a virtual environment
python -m venv .venv
Activate the virtual environment

Windows

.venv\Scripts\activate

macOS / Linux

source .venv/bin/activate
Install dependencies
pip install -r requirements.txt
Configure environment variables

Create a .env file in the project root.

OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1
LOG_LEVEL=INFO
Run the application
streamlit run app.py
Roadmap
Backend AI Investigation Agent
Policy Knowledge Service (RAG)
Streamlit Dashboard
Human Review Workflow
Evaluation Framework
Multi-Agent Architecture (Future)
License

This project is intended for educational and portfolio purposes.

## 🚀 Production Deployment
To pull and execute the official stable release, check out the target tag:
```bash
git checkout v1.0
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 rag_ingest.py
streamlit run app.py
```
