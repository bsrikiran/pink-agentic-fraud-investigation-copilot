Agentic Fraud Investigation Copilot
UI / Streamlit Module Implementation Guide

Module: Streamlit User Interface

Version: 1.0

Status: Ready for Implementation

1. Module Purpose

The Streamlit UI provides the user interface for the Agentic Fraud Investigation Copilot.

Its purpose is to allow fraud analysts to:

Select an investigation case
Execute an AI-assisted investigation
Review the AI recommendation
Review supporting policy references
Make the final investigation decision

The UI is intentionally lightweight.

Business logic belongs in the backend.

Policy retrieval belongs in the RAG module.

The UI should orchestrate these modules without duplicating their responsibilities.

2. Business Objective

Fraud analysts need a simple interface that allows them to investigate suspicious transactions quickly.

The UI should emphasize:

Simplicity
Explainability
Human-in-the-Loop decision making
Easy navigation
Professional appearance

The interface should resemble an internal enterprise operations dashboard rather than a consumer application.

3. Module Responsibilities

The UI is responsible for:

Displaying investigation cases
Invoking the backend investigation workflow
Displaying AI recommendations
Presenting retrieved policy references
Supporting analyst review
Displaying investigation metrics

The UI must not:

Build prompts
Call the OpenAI API directly
Perform policy retrieval
Implement fraud rules
Modify backend logic
4. Folder Ownership

Implement only:

ui/

    components.py

    pages.py

    styles.py

and

app.py

Do not modify:

backend/

rag/

sample_data/

policies/
5. Existing Project Assets

The project already contains:

Backend

Completed.

Provides:

Fraud investigation workflow
Structured JSON response
RAG

Provides:

Retrieved policy context
Sample Investigation Cases

Located in:

sample_data/

Files:

fraud_investigation_cases.csv
fraud_investigation_cases.json

The UI should load cases from these files.

6. Screen Navigation

The application should contain a single Streamlit application with multiple logical sections.

Recommended navigation:

Home

↓

Investigation

↓

Results

↓

Human Review

↓

Metrics

A sidebar may be used for navigation if desired.

7. Home Screen

Display:

Project title
Project description
Technology stack
Current implementation status

Include a button:

Start Investigation
8. Investigation Screen

Allow the analyst to:

Select an investigation case.

Recommended control:

SelectBox

Display key case information.

Example:

Customer
Merchant
Amount
Transaction Location
Account Age
Known Device
Travel Notice

Provide a button:

Run Investigation

This button should:

Retrieve policy context from the RAG module.
Call the backend.
Display results.
9. Results Screen

Display the backend response.

Recommended layout:

Investigation Summary

Display:

Investigation Summary
Fraud Score

Display:

Large metric card.

Example:

Fraud Score

85
Risk Level

Display:

Low
Medium
High
Recommendation

Display one recommendation only.

Examples:

Approve
Decline Transaction
Request Customer Verification
Manual Review
Escalate Investigation
Fraud Indicators

Display as bullet points.

Example:

Unknown device
Geographic anomaly
High-value transaction
Reasoning

Display each reasoning statement separately.

Supporting Policies

Display policy names returned by the backend.

Examples:

High-Value Transaction Policy (HV-410)
Customer Verification Policy (CV-102)
10. Human Review Screen

The analyst remains the final decision maker.

Provide buttons:

Approve

Reject

Needs Manual Review

Display confirmation after selection.

No database persistence is required for Version 1.0.

11. Metrics Screen

Display simple dashboard metrics.

Examples:

Total Investigation Cases
Average Fraud Score
Recommendation Distribution
Risk Distribution

Charts may be implemented using Streamlit's native chart components.

No external BI tools are required.

12. Backend Integration

The UI should call only the backend public interface.

Example workflow:

User selects case

↓

Retrieve policy context (RAG)

↓

Run backend investigation

↓

Receive JSON response

↓

Render results

The UI should never construct prompts or call the OpenAI API directly.

13. Error Handling

Display user-friendly messages.

Examples:

Unable to load investigation cases.
Policy retrieval unavailable.
Investigation failed.
OpenAI request failed.

Do not display stack traces to the user.

14. Logging

Use concise logging.

Examples:

Application started

Loaded 12 investigation cases

Selected CASE-004

Running investigation

Displaying results
15. UI Design Principles

The interface should prioritize:

Readability
Minimalism
Professional appearance
Fast navigation
Clear hierarchy of information

Avoid excessive colors or animations.

The UI should resemble an internal banking operations application.

16. Technology Requirements

Use:

Python 3.12
Streamlit
Pandas

Reuse existing project dependencies.

No JavaScript frameworks are required.

17. Deliverables

The completed module should include:

ui/

components.py

pages.py

styles.py

app.py

The application should:

Load investigation cases.
Call the RAG module.
Call the backend.
Display structured investigation results.
Support analyst review.
Display metrics.
18. Definition of Done

The module is complete when:

The application launches successfully using:
streamlit run app.py
All investigation cases can be selected.
The backend returns investigation results.
Policy references are displayed.
Human review controls function.
Metrics render successfully.
No backend or RAG code is modified.
The module follows the project's coding standards.
19. Guidance for Future LLM Sessions

The project already contains:

Complete architecture
Completed backend implementation
Prompt library
Sample investigation cases
Policy library
Integration contracts
Coding standards

Do not redesign the architecture.

Do not modify backend interfaces.

Do not modify the RAG module.

Implement only the Streamlit UI using the existing contracts.

The objective is to create a clean, professional interface that demonstrates how an enterprise fraud analyst would interact with the Agentic Fraud Investigation Copilot.

End of UI / Streamlit Module Implementation Guide

Version: 1.0