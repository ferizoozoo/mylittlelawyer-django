# MyLittleLawyer — Gemini Hackathon Project

An AI-powered web application that conducts a conversational Q&A with legal clients to collect the information needed to complete legal application forms. The initial scope focuses on Ontario Landlord and Tenant Board (LTB) applications, with an architecture that can expand to additional legal domains over time.

## Problem & Opportunity
Legal teams spend significant time on repetitive form completion. This project streamlines intake by guiding clients through a structured, explainable Q&A and producing ready-to-file documents. The goal is to reduce administrative overhead while preserving accuracy and confidentiality.

## High-Level Flow
1. Client starts a chatbot session.
2. The model confirms the type of application the user needs.
3. RAG/few-shot methods identify the best matching LTB form.
4. The model asks structured questions and clarifies legal terms on request.
5. Collected answers are compiled into JSON.
6. A deterministic layer fills official PDFs and returns the completed forms.

## Architecture (Three Layers)
**Layer 1 — Frontend (React)**  
User interface, authentication, and document retrieval/preview.

**Layer 2 — Django (Connector)**  
Session management, user data, forms metadata, and storage orchestration.

**Layer 3 — FastAPI (AI Layer)**  
Gemini 3 integration, RAG pipeline, prompt engineering, and form selection.

## Data & Storage
- PostgreSQL: users and structured application data
- MongoDB: chat sessions and metadata
- GCP Storage: PDF form storage and filled documents
- Vector DB: indexing statutes, rules, guidelines, and LTB forms

## AI & Retrieval Strategy
- Use few-shot learning and vector similarity to find the best LTB form based on the user's initial description.
- Convert relevant laws, regulations, and forms into vectorized embeddings.
- Retrieve best matches and convert back to text for the model's final prompt.

## Source Material (Initial Dataset)
We will curate and vectorize official Ontario sources, including:
- Residential Tenancies Act, S.O. 2006, c. 17
- Statutory Powers Procedure Act, R.S.O. 1990 c. S.22
- LTB Rules of Procedure
- LTB Practice Directions
- LTB Guidelines
- LTB Forms

## PDF Generation
- Final form completion is performed via the Adobe Acrobat PDF Services API.
- We will evaluate encryption strategies to minimize confidentiality risks.

## Roadmap (Post-Demo)
- Client portal with saved applications
- Role-based access control (admin/lawyer/client)
- Multi-tenant mode: law firms as service providers
- Marketplace discovery for firms and clients
