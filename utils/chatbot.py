from groq import Groq
from dotenv import load_dotenv

from utils.search import search_resumes

import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================================
# QUERY GUARDRAIL
# =========================================================

def detect_query_type(query):

    prompt = f"""
Classify this query into ONLY one category:

1. recruitment
2. general

Examples:

"Who fits for AI roles?" → recruitment
"Find Data Engineers" → recruitment
"Show candidates with Python" → recruitment

"What is SaaS?" → general
"What is cloud computing?" → general

Query:
{query}

Return ONLY:
recruitment
OR
general
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip().lower()

    except:

        return "general"

# =========================================================
# AI RECRUITER INSIGHT
# =========================================================

def generate_ai_insight(candidate, query):

    prompt = f"""
You are an enterprise AI recruiter assistant.

A recruiter asked:
'{query}'

Analyze this candidate profile and provide a recruiter-style evaluation.

Candidate Resume Name:
{candidate['file_name']}

Experience:
{candidate['experience']}

Skills:
{candidate['skills']}

Your response should:
- explain why the candidate fits or does not fit
- mention technical strengths
- identify role suitability
- mention missing skills if any
- sound natural and professional
- avoid excessive bullet points
- answer conversationally like an AI recruiter copilot

Keep the response concise but intelligent.
"""

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"""
AI recruiter analysis unavailable.

Error:
{str(e)}
"""

# =========================================================
# MAIN CHATBOT
# =========================================================

def recruiter_chat(query, resume_data):

    # -----------------------------------------------------
    # GUARDRAIL
    # -----------------------------------------------------

    query_type = detect_query_type(query)

    if query_type == "general":

        return """
This AI Recruiter Assistant is designed specifically for recruitment and candidate intelligence workflows.

Please ask recruitment-related questions such as:
- Who fits for AI roles?
- Show Data Engineer candidates
- Find candidates with Python skills
- Who is suitable for analyst roles?
"""

    # -----------------------------------------------------
    # SEARCH RESUMES
    # -----------------------------------------------------

    results = search_resumes(
        query,
        resume_data
    )

    if not results:

        return "No highly relevant candidates found."

    ranked_candidates = []

    # -----------------------------------------------------
    # PROCESS RESULTS
    # -----------------------------------------------------

    for i, item in enumerate(results):

        summary = {

            "name":
            item.get(
                "file_name",
                "Unknown Resume"
            ),

            "experience":
            item.get(
                "experience",
                "Not Mentioned"
            ),

            "skills":
            item.get(
                "skills",
                []
            )
        }

        skills = summary.get(
            "skills",
            []
        )

        # Ignore weak resumes
        if len(skills) < 2:
            continue

        match_score = max(
            95 - (i * 10),
            30
        )

        candidate = {

            "file_name":
            summary["name"],

            "experience":
            summary["experience"],

            "skills":
            summary["skills"]
        }

        ai_response = generate_ai_insight(
            candidate,
            query
        )

        ranked_candidates.append({

            "name":
            summary["name"],

            "experience":
            summary["experience"],

            "skills":
            summary["skills"],

            "score":
            match_score,

            "ai_response":
            ai_response
        })

    # -----------------------------------------------------
    # NO RESULTS
    # -----------------------------------------------------

    if len(ranked_candidates) == 0:

        return "No highly relevant candidates found."

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    response = []

    for candidate in ranked_candidates:

        candidate_text = f"""
## 📄 {candidate['name']} — {candidate['score']}% Match

💼 Experience:  
{candidate['experience']}

🛠️ Core Skills:  
{", ".join(candidate['skills'][:6])}

🤖 AI Recruiter Insight:  
{candidate['ai_response']}
"""

        response.append(candidate_text)

    return "\n\n".join(response)