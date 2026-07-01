I think this is the most important document we'll create. This becomes the **"Project Constitution"**—the single document that any LLM or engineer can read to understand the project without the previous chat history.

I recommend saving it as:

```
docs/project_overview.md
```

or

```
Project Overview.docx
```

---

# Agentic Fraud Investigation Copilot

## Project Overview

**Version:** 1.0

**Status:** Architecture Complete | Backend Complete | RAG Pending | UI Pending

---

# 1. Project Purpose

The Agentic Fraud Investigation Copilot is an enterprise-style AI product prototype demonstrating how Agentic AI can augment fraud operations within a financial institution.

The project was designed to showcase Product Management, AI solution architecture, Prompt Engineering, Retrieval-Augmented Generation (RAG), Human-in-the-Loop (HITL), and modular software design.

The goal is **not** to build a production fraud detection system. Instead, the project demonstrates how a Product Manager or Technical Product Owner would design, coordinate, and deliver an AI-powered fraud investigation solution.

The project aligns with enterprise AI concepts including:

* Agentic AI
* Prompt Engineering
* Retrieval-Augmented Generation (RAG)
* Human-in-the-Loop (HITL)
* Explainable AI
* AI Evaluation (Evals)
* Modular AI Architecture

---

# 2. Business Problem

Fraud analysts often spend significant time gathering information from multiple systems before making a decision.

Typical investigations require analysts to:

* Review transaction details
* Compare customer spending history
* Evaluate device information
* Review merchant risk
* Search internal fraud policies
* Apply investigation procedures
* Document findings

The objective of this project is to demonstrate how an AI-powered Fraud Investigation Agent can reduce manual effort by assisting analysts with evidence gathering and recommendation generation while keeping the human analyst responsible for the final decision.

---

# 3. Project Objectives

The project demonstrates the following capabilities:

* AI-assisted fraud investigation
* Policy retrieval using RAG
* Explainable recommendations
* Structured JSON responses
* Human review workflow
* Modular architecture suitable for independent development teams

---

# 4. Solution Overview

The application is composed of three independent modules.

## Backend

Responsible for:

* Prompt orchestration
* OpenAI communication
* Fraud investigation workflow
* Structured JSON generation
* Configuration
* Logging
* Error handling

Current Status:

**Completed**

---

## RAG Module

Responsible for:

* Loading fraud policy documents
* Creating embeddings
* Managing ChromaDB
* Retrieving relevant policy content
* Returning policy context to the backend

Current Status:

**Pending**

---

## Streamlit UI

Responsible for:

* Case selection
* Investigation execution
* Displaying AI recommendations
* Human review
* Product metrics

Current Status:

**Pending**

---

# 5. High-Level Architecture

```text
                Fraud Analyst

                       │

                       ▼

         Fraud Investigation Agent

          ┌────────────┴────────────┐

          ▼                         ▼

Policy Knowledge Service       OpenAI GPT

          │

          ▼

       ChromaDB

          │

          ▼

   Fraud Policy Documents
```

The Fraud Investigation Agent orchestrates the investigation process.

The Policy Knowledge Service retrieves relevant policy information.

The LLM combines transaction data with policy context to generate explainable recommendations.

The fraud analyst remains the final decision maker.

---

# 6. Current Project Structure

```
agentic-fraud-investigation-copilot/

backend/
rag/
ui/
sample_data/
policies/
assets/
docs/
tests/
logs/

app.py
requirements.txt
README.md
.env
```

Each folder has a single responsibility.

---

# 7. Current Project Assets

The following assets have already been created.

## Documentation

Completed:

* Product Vision
* Architecture
* Integration Contract
* Backend Specification
* RAG Specification
* UI Specification
* Build Guide
* GitHub README
* Source Code Standards

---

## Prompt Library

The project contains six prompts.

Located in:

```
backend/prompts.py
```

Prompts include:

* SYSTEM_PROMPT_V1
* INVESTIGATION_PROMPT_V1
* RAG_INSTRUCTIONS_PROMPT_V1
* JSON_OUTPUT_PROMPT_V1
* HUMAN_REVIEW_PROMPT_V1
* EVALUATION_PROMPT_V1

These prompts should be reused by all future development.

---

## Sample Investigation Cases

Located in:

```
sample_data/
```

Files:

* fraud_investigation_cases.csv
* fraud_investigation_cases.json

Contains twelve investigation scenarios including:

* Legitimate transactions
* Card theft
* Account takeover
* Travel exception
* Friendly fraud
* Device change
* High-value purchases
* Elder financial abuse

---

## Policy Library

Located in:

```
policies/
```

Contains ten PDF documents.

Examples:

* Fraud Investigation Policy (FP-214)
* Customer Verification Policy (CV-102)
* High-Value Transaction Policy (HV-410)
* Device Intelligence Policy (DI-220)
* Travel Exception Policy (TE-118)

These documents will be indexed by the RAG module.

---

# 8. Backend Status

The backend implementation is complete.

Implemented features include:

* OpenAI API integration
* Prompt orchestration
* Configuration management
* Logging
* JSON validation
* Investigation workflow

The backend returns structured investigation results including:

* Fraud score
* Risk level
* Confidence
* Recommendation
* Fraud indicators
* Reasoning
* Policy references
* Investigation summary

The backend has been successfully validated through smoke testing.

---

# 9. Module Responsibilities

## Backend Team

Owns:

```
backend/
```

Responsibilities:

* AI investigation
* Prompt execution
* OpenAI integration

Must not implement:

* UI
* RAG

---

## RAG Team

Owns:

```
rag/
```

Responsibilities:

* PDF loading
* Embeddings
* ChromaDB
* Policy retrieval

Must not implement:

* OpenAI chat completions
* Fraud investigation
* Streamlit

---

## UI Team

Owns:

```
ui/
```

Responsibilities:

* Streamlit dashboard
* Case selection
* Results visualization
* Human review

Must not implement:

* Prompt engineering
* OpenAI API
* ChromaDB

---

# 10. Integration Contract

The modules communicate through stable interfaces.

Backend Input:

* Investigation case
* Customer profile
* Customer history
* Policy context (string)

Backend Output:

Structured JSON containing investigation results.

The UI consumes only the backend output.

The RAG module supplies only policy context.

Modules should not call each other's internal functions directly.

---

# 11. Technology Stack

Language:

Python 3.12

Libraries:

* Streamlit
* OpenAI
* ChromaDB
* PyPDF
* Pandas
* Pydantic
* Python Dotenv

---

# 12. Current Development Status

| Module                | Status     |
| --------------------- | ---------- |
| Architecture          | ✅ Complete |
| Documentation         | ✅ Complete |
| Prompt Engineering    | ✅ Complete |
| Investigation Dataset | ✅ Complete |
| Policy Library        | ✅ Complete |
| Backend               | ✅ Complete |
| RAG                   | ⏳ Pending  |
| Streamlit UI          | ⏳ Pending  |
| Integration Testing   | ⏳ Pending  |

---

# 13. Future Work

Remaining implementation tasks include:

* Build the Policy Knowledge Service (RAG)
* Build the Streamlit user interface
* Integrate backend and RAG
* Integrate backend and UI
* Perform end-to-end testing
* Record demonstration video

The current backend should not require architectural changes during these phases.

---

# 14. Guidance for Future LLM Sessions

This document is intended to provide sufficient project context for future ChatGPT sessions or other LLMs.

When continuing development:

* Preserve the existing architecture.
* Do not redesign completed modules.
* Treat the backend implementation as the system of record.
* Implement only the requested module.
* Maintain the integration contract between modules.
* Reuse the existing prompt library.
* Follow the established coding standards.

The objective is to extend the project while preserving consistency across independently developed components.

---

# End of Project Overview

**Version 1.0**
    