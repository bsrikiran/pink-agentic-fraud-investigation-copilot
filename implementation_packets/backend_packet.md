Backend Implementation Packet
Give the next LLM this prompt.
 
Project Overview
Project: Agentic Fraud Investigation Copilot
This project demonstrates an enterprise-style Agentic AI solution for fraud operations.
The application assists fraud analysts by:
•	Investigating suspicious transactions 
•	Retrieving supporting fraud policies (future RAG integration) 
•	Generating explainable recommendations 
•	Supporting Human-in-the-Loop (HITL) decision making 
•	Returning structured JSON for downstream UI components 
This implementation request is only for the backend module.
Do not implement the UI or RAG modules.
 
Scope
Implement only files inside:
backend/
Do not modify any other folders.
 
Existing Project Assets
The project already contains:
backend/prompts.py
with the following prompts:
•	SYSTEM_PROMPT_V1 
•	INVESTIGATION_PROMPT_V1 
•	RAG_INSTRUCTIONS_PROMPT_V1 
•	JSON_OUTPUT_PROMPT_V1 
•	HUMAN_REVIEW_PROMPT_V1 
•	EVALUATION_PROMPT_V1 
Use these prompts.
Do not rewrite them.
 
The project also contains:
sample_data/
including:
•	fraud_investigation_cases.json 
•	fraud_investigation_cases.csv 
Use these for testing.
 
The project also contains:
policies/
with ten policy PDF documents.
The backend should accept policy text as input but must not implement PDF loading or vector search. That belongs to the RAG module.
 
Backend Responsibilities
Implement:
•	OpenAI client 
•	Investigation workflow 
•	Prompt orchestration 
•	JSON validation 
•	Configuration 
•	Error handling 
•	Logging 
 
Inputs
The backend receives:
•	Transaction case 
•	Customer profile 
•	Customer history 
•	Policy context (string) 
 
Output
Return structured JSON exactly matching the agreed schema.
 
Engineering Constraints
Follow:
•	Chapter 3 Integration Contract
•	Chapter 4 Backend Engineering Specification
•	Chapter 9 Chapter 9 Code Standards & Project Structure
 
Folder Ownership
Implement only:
backend/
Expected files:
backend/

config.py

investigator.py

llm_client.py

models.py

utils.py
Do not modify:
rag/

ui/

sample_data/

policies/
 
Coding Standards
Requirements:
•	Python 3.12 
•	Type hints 
•	Docstrings 
•	Logging 
•	Pydantic models 
•	Modular functions 
•	PEP 8 
•	No hardcoded API keys 
•	Read configuration from .env 
 
Deliverables
Generate complete production-quality code for:
•	config.py 
•	llm_client.py 
•	investigator.py 
•	models.py 
•	utils.py 
The generated code should run after the user provides an OpenAI API key.
Do not generate Streamlit code.
Do not generate RAG code.
