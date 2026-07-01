Perfect. This document is **not** an architecture document. It is an **engineering handoff**. If I started a brand-new ChatGPT session tomorrow, this document would contain everything needed to build the RAG module without redesigning the project.

I recommend saving it as:

```text
docs/rag_module_implementation_guide.md
```

---

# Agentic Fraud Investigation Copilot

# RAG Module Implementation Guide

**Module:** Policy Knowledge Service (RAG)

**Version:** 1.0

**Status:** Ready for Implementation

---

# 1. Module Purpose

The Policy Knowledge Service is responsible for providing relevant internal fraud policy information to the Fraud Investigation Agent.

This module **does not perform fraud investigations**.

This module **does not communicate directly with the user**.

Its only responsibility is to retrieve the most relevant policy content based on an investigation request.

The backend will then combine the retrieved policy context with transaction data and customer information before sending the complete prompt to the OpenAI model.

This module should remain independent of the backend and Streamlit UI.

---

# 2. Business Objective

Fraud analysts rely on internal policy documents when making decisions.

Instead of requiring analysts to manually search hundreds of pages of documentation, this module retrieves the most relevant policy sections automatically.

Benefits include:

* Faster investigations
* Consistent policy application
* Explainable AI recommendations
* Reduced hallucinations
* Improved analyst productivity

---

# 3. Module Responsibilities

The Policy Knowledge Service is responsible for:

* Loading policy PDF documents
* Extracting document text
* Splitting documents into chunks
* Creating embeddings
* Storing embeddings in ChromaDB
* Performing semantic similarity searches
* Returning relevant policy context

This module **must not**:

* Call the OpenAI Chat Completion API
* Make fraud recommendations
* Perform prompt engineering
* Generate investigation summaries
* Implement Streamlit pages

---

# 4. Folder Ownership

This module owns only:

```text
rag/

    loader.py

    embeddings.py

    vector_store.py

    retriever.py

    utils.py
```

Do not modify:

```text
backend/

ui/

sample_data/

policies/
```

---

# 5. Existing Project Assets

The project already contains:

## Policy Documents

Located in:

```text
policies/
```

Current policy library:

* Fraud Investigation Policy (FP-214)
* Customer Verification Policy (CV-102)
* Card Dispute & Chargeback Policy (DP-310)
* Merchant Risk Classification Policy (MR-501)
* Device Intelligence Policy (DI-220)
* Travel Exception Policy (TE-118)
* High-Value Transaction Policy (HV-410)
* Escalation & Case Management Policy (EC-150)
* Fraud Analyst Investigation Playbook (AP-001)
* Regulatory & Compliance Guidelines (RC-700)

These PDF documents should be indexed by this module.

---

# 6. RAG Workflow

The expected workflow is:

```text
Policy PDFs

↓

Load Documents

↓

Extract Text

↓

Split Into Chunks

↓

Generate Embeddings

↓

Store in ChromaDB

↓

Receive User Query

↓

Similarity Search

↓

Return Policy Context
```

---

# 7. Recommended Chunking Strategy

Recommended chunk size:

* 500–800 characters

Overlap:

* 100 characters

Each chunk should preserve:

* Policy title
* Policy identifier (e.g., FP-214)
* Section heading
* Section content

Metadata should remain attached to each chunk.

---

# 8. Embedding Strategy

Use the OpenAI Embeddings API.

Generate one embedding per chunk.

Store:

* Embedding vector
* Policy name
* Policy identifier
* Section heading
* Original chunk text

---

# 9. ChromaDB

Create one collection named:

```text
fraud_policy_knowledge_base
```

Each record should include:

* id
* document
* embedding
* metadata

Metadata should include:

```text
policy_name

policy_id

section

source_file
```

---

# 10. Public Interface

The module should expose one primary function.

```python
def retrieve_policy_context(
    query: str,
    top_k: int = 3
) -> str:
```

Input:

Natural language query.

Example:

```text
Unknown device

High-value purchase

Travel exception
```

Output:

Single string containing the retrieved policy context.

Example:

```text
High-Value Transaction Policy (HV-410)

Section 3

Transactions above $2,000 originating from unknown devices require step-up authentication before approval.

Customer Verification Policy (CV-102)

Section 2

Identity verification should be completed using an approved authentication method before approval.
```

The backend will append this text to the Investigation Prompt.

---

# 11. Backend Integration

The backend already exposes:

```python
run_investigation(
    case,
    policy_context
)
```

This module should only provide:

```python
policy_context
```

It must not invoke the backend.

It must not modify prompts.

It must not call OpenAI Chat Completion.

---

# 12. Error Handling

If no relevant policy is found:

Return an empty string.

Do not raise an exception.

The backend is responsible for deciding how to proceed when no policy context is available.

---

# 13. Logging

Use concise logging.

Examples:

```text
Loading policy documents

Indexed 10 PDF documents

Generated 132 embeddings

Created ChromaDB collection

Retrieving policy context

Retrieved 3 matching policy sections
```

Avoid excessive or verbose logging.

---

# 14. Coding Standards

Follow:

* Python 3.12
* Type hints
* PEP 8
* Modular functions
* Docstrings
* Logging
* Environment variables
* Error handling

Do not hardcode file paths.

Read configuration from `.env` where applicable.

---

# 15. Deliverables

The completed module should include:

```text
rag/

loader.py

embeddings.py

vector_store.py

retriever.py

utils.py
```

The module should:

* Index all policy PDFs
* Store embeddings in ChromaDB
* Retrieve relevant policy content
* Return policy context as a string
* Be independently testable

---

# 16. Definition of Done

The module is complete when:

* All policy PDFs are indexed.
* ChromaDB is populated.
* Similarity search returns relevant policy sections.
* The backend can call `retrieve_policy_context()` without modification.
* No backend or UI code is changed.
* The module follows the project's coding standards.

---

# 17. Guidance for Future LLM Sessions

This project already contains:

* Complete architecture
* Completed backend implementation
* Prompt library
* Sample investigation cases
* Policy PDF library

Do **not** redesign the architecture.

Do **not** modify backend interfaces.

Implement only the Policy Knowledge Service (RAG) using the existing contracts.

The objective is to produce a modular RAG implementation that integrates cleanly with the completed backend.

---

# End of RAG Module Implementation Guide

**Version 1.0**
