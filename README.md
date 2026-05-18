# ARROWS AI

AI Talent Intelligence Platform for resume search, JD matching, duplicate detection, and recruiter chatbot assistance.

## What it does

- Semantic resume search using ChromaDB vector store and sentence-transformer embeddings
- Resume upload and indexing pipeline
- JD matching for comparing resumes against a job description
- Duplicate resume detection and cleanup
- AI recruiter chatbot with candidate ranking and hiring recommendation
- Stable resume parsing with regex-based skills and experience extraction

## Key features

- `utils/model_loader.py` centralizes model loading to avoid repeated large model initialization
- `utils/embeddings.py` stores resume text embeddings in ChromaDB with filename metadata
- `utils/search.py` performs semantic search and returns resume text plus filename from in-memory resume data
- `utils/summary.py` extracts skills and experience from resume text reliably without external LLM dependencies
- `utils/chatbot.py` ranks candidates, computes readiness, and generates recruiter-friendly responses
- `utils/recommendation.py` provides hiring recommendations, best role, strengths, and risk areas
- `app.py` provides Streamlit UI for uploading resumes, semantic search, JD match, dedup, and recruiter chatbot

## Project structure

- `app.py` - Streamlit application entry point
- `requirements.txt` - Python dependencies
- `utils/`
  - `embeddings.py` - store resume embeddings and manage vector DB
  - `search.py` - semantic search logic
  - `summary.py` - resume text parser for experience and skills
  - `chatbot.py` - recruiter chatbot ranking and response generation
  - `recommendation.py` - hiring recommendation engine
  - `readiness.py` - readiness scoring logic
  - `dedup.py` - duplicate resume detection
  - `jd_match.py` - JD matching logic
  - `parser.py` - resume text extraction logic for PDF/DOCX
- `resumes/` - uploaded resume files
- `chroma_db/` - local ChromaDB store

## Installation

1. Create or activate a Python environment (Python 3.13 recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. If you installed packages manually, verify `chromadb`, `sentence-transformers`, and `streamlit` are available.

## How to run

1. Delete and recreate `chroma_db/` before uploading fresh resumes if the DB contains stale metadata.
2. Start the app:

```bash
python -m streamlit run app.py
```

3. Open the local Streamlit URL shown in your terminal.
4. Upload resumes and use the tabs:
   - `Semantic Search` to search candidate resumes by query
   - `JD Match Engine` to compare resumes against a job description
   - `Duplicate Detection` to find and remove resume duplicates
   - `AI Recruiter Chatbot` to generate ranked candidate guidance

## Recommended workflow

1. Upload resume files (`.pdf` or `.docx`).
2. Ensure the vector database is fresh by deleting `chroma_db/` and recreating the folder if needed.
3. Use Semantic Search for recruiter-style candidate retrieval.
4. Use the AI Recruiter Chatbot for ranking and hiring recommendations.

## Notes

- The current parser in `utils/summary.py` uses a stable regex-based method to avoid unstable LLM dependencies.
- The chatbot and search UI use resume filenames directly for clean candidate names.
- The project emphasizes stability and recruiter-focused output for demo readiness.

## Troubleshooting

- If search results show `Unknown` names, confirm `resume_data` is being passed into search and that uploaded files are stored successfully.
- If Streamlit crashes on app start, ensure all dependencies are installed and no old Lock files or stale `chroma_db/` objects remain.

## License

This repository is for internal demo and development use. Adapt as needed for your hiring intelligence workflow.
