import chromadb
import os

from groq import Groq
from dotenv import load_dotenv

from utils.embeddings import generate_embedding

load_dotenv()

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================================
# AI FIT EXPLANATION
# =========================================================

def generate_fit_reason(query, resume):

    prompt = f"""
You are an enterprise AI recruitment intelligence engine.

A recruiter searched for:
{query}

Candidate Information:

Skills:
{resume.get('skills', [])}

Experience:
{resume.get('experience', 'Not Mentioned')}

Projects:
{resume.get('projects', [])}

Generate a concise recruiter-style explanation describing WHY this profile is relevant for the search query.

Requirements:
- sound professional
- recruiter-oriented
- concise
- enterprise-grade
- avoid generic phrases
- maximum 3 lines
"""

    try:

        response = client_groq.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except:

        return (
            "Relevant profile identified "
            "through semantic candidate matching."
        )

# =========================================================
# SEMANTIC SEARCH
# =========================================================

def search_resumes(query, resume_data):

    client = chromadb.PersistentClient(
        path="chroma_db"
    )

    collection = client.get_or_create_collection(
        name="resume_collection"
    )

    query_embedding = generate_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    formatted_results = []

    for i in range(len(documents)):

        metadata = metadatas[i]

        matched_resume = None

        for resume in resume_data:

            if (
                resume["file_name"]
                ==
                metadata["file_name"]
            ):

                matched_resume = resume
                break

        if matched_resume:

            reason = generate_fit_reason(
                query,
                matched_resume
            )

            formatted_results.append({

                "file_name":
                matched_resume.get(
                    "file_name",
                    "Unknown Resume"
                ),

                "experience":
                matched_resume.get(
                    "experience",
                    "Not Mentioned"
                ),

                "skills":
                matched_resume.get(
                    "skills",
                    []
                ),

                "reason":
                reason
            })

    return formatted_results