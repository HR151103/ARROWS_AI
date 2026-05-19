# ARROWS AI Talent Intelligence Platform

Enterprise AI-powered recruitment intelligence platform built using LangChain, RAG architecture, ChromaDB, semantic search, and LLM-based recruiter assistance.

---

# Overview

ARROWS AI is an intelligent recruitment intelligence platform designed to streamline candidate discovery, resume understanding, recruiter decision-making, and hiring workflows using Retrieval-Augmented Generation (RAG) and semantic AI technologies.

The platform enables recruiters to:
- Upload and parse resumes
- Remove duplicate resumes using semantic similarity
- Perform semantic candidate search
- Generate AI-assisted recruiter insights
- Match candidates against Job Descriptions
- Generate AI-based Job Descriptions
- Interact with an AI Recruiter Chatbot powered by LangChain + RAG

---

# Key Features

## Resume Parsing
- Extracts:
  - Candidate Name
  - Experience
  - Skills
  - Projects
  - Certifications
  - Education
  - Recommended Role
  - AI-generated candidate summary

---

## Resume Deduplication Engine
- Detects duplicate resumes using semantic similarity
- Prevents duplicate indexing
- Ensures clean recruiter search results

---

## Semantic Candidate Search
- Uses embeddings + vector similarity search
- Retrieves candidates based on meaning rather than keywords
- Supports role-based intelligent retrieval

---

## AI Job Description Generator
- Generates enterprise-grade job descriptions using LLMs
- Creates role-specific hiring requirements

---

## JD Match Engine
- Matches resumes against Job Descriptions
- Generates:
  - Match percentage
  - Skill alignment
  - Experience relevance
  - Recruiter insights

---

## AI Recruiter Chatbot (RAG)
Built using:
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq LLM
- RetrievalQA Chain

The chatbot:
- Understands recruiter queries
- Retrieves contextual resume intelligence
- Generates recruiter-focused AI responses

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend |
| Streamlit | Web Application |
| LangChain | RAG Framework |
| ChromaDB | Vector Database |
| HuggingFace Embeddings | Semantic Embeddings |
| Groq LLM | AI Reasoning |
| Sentence Transformers | Embedding Generation |
| Scikit-learn | Similarity Detection |
| Pandas | Data Handling |

---

# RAG Architecture

```text
Recruiter Query
        ↓
Embedding Generation
        ↓
Vector Similarity Retrieval
        ↓
LangChain Retriever
        ↓
Relevant Resume Chunks
        ↓
LLM Context Injection
        ↓
AI Recruiter Response
```

---

# Project Workflow

```text
Resume Upload
        ↓
Duplicate Detection
        ↓
AI Resume Parsing
        ↓
Semantic Candidate Search
        ↓
AI JD Generation
        ↓
JD Match Engine
        ↓
AI Recruiter Chatbot
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/HR151103/ARROWS_AI.git
```

---

## Navigate to Project

```bash
cd ARROWS_AI
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
streamlit run app.py
```

---

# Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

---

# Example Recruiter Queries

```text
Who fits Data Engineer roles?

Who has Azure Data Factory experience?

Find candidates with Spark and Kafka expertise.

Who worked on ETL migration projects?

Which candidate has cloud engineering exposure?

Generate recruiter insights for backend developers.
```

---

# Enterprise AI Capabilities

- Retrieval-Augmented Generation (RAG)
- Semantic Resume Intelligence
- AI Recruiter Assistance
- Context-Aware Candidate Retrieval
- Resume Knowledge Search
- LLM-based Candidate Reasoning

---

# Future Enhancements

- Hybrid RAG Search
- Candidate Comparison Dashboard
- AI Interview Question Generator
- Skill Gap Analysis
- Multi-Agent Recruiter AI
- Recruiter Conversation Memory
- ATS Integration
- Analytics Dashboard

---

# Author

Hrithik AR


---

# License

This project is intended for educational, research, and enterprise innovation purposes.
