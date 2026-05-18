import pdfplumber
import docx
import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

    return text

# =========================================================
# DOCX TEXT EXTRACTION
# =========================================================

def extract_text_from_docx(file):

    doc = docx.Document(file)

    text = "\n".join(
        [para.text for para in doc.paragraphs]
    )

    return text

# =========================================================
# LLM STRUCTURED PARSER
# =========================================================

def llm_resume_parser(text):

    prompt = f"""
You are an enterprise AI recruitment intelligence engine.

Analyze the resume professionally and extract structured candidate intelligence.

Return ONLY valid JSON.

Required JSON format:

{{
    "name": "",
    "experience": "",
    "skills": [],

    "projects": [
        {{
            "project_name": "",
            "skills_used": [],
            "project_summary": ""
        }}
    ],

    "certifications": [],
    "education": "",
    "recommended_role": "",
    "ai_summary": ""
}}

Instructions:

1. Extract only accurate and relevant information from the resume.

2. Skills should contain only professional or technical competencies.

3. Projects must be structured professionally.

4. For each project extract:
   - project_name
   - skills_used
   - concise project_summary

5. skills_used should include technologies/tools actually used in that project.

6. Certifications should contain only actual certifications.

7. Recommended role should reflect the candidate’s strongest professional suitability.

8. AI summary must sound like an enterprise recruiter briefing.

9. Avoid generic HR buzzwords and cliché phrases such as:
   - results-oriented
   - hardworking
   - passionate
   - excellent communication skills

10. AI summary should:
   - sound executive-level
   - concise
   - recruiter-oriented
   - enterprise-grade

11. Keep AI summary within 3-5 concise professional lines.

12. Do not hallucinate or invent information.

13. If information is unavailable, return clean empty values instead of guessing.

Resume Text:
{text[:4000]}
"""

    try:

        completion = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1
        )

        response = (
            completion
            .choices[0]
            .message
            .content
        )

        response = response.strip()

        if response.startswith("```json"):

            response = response.replace(
                "```json",
                ""
            )

        if response.endswith("```"):

            response = response.replace(
                "```",
                ""
            )

        parsed_json = json.loads(response)

        # =================================================
        # SAFETY DEFAULTS
        # =================================================

        parsed_json.setdefault(
            "name",
            "Unknown Candidate"
        )

        parsed_json.setdefault(
            "experience",
            "Not Mentioned"
        )

        parsed_json.setdefault(
            "skills",
            []
        )

        parsed_json.setdefault(
            "projects",
            []
        )

        parsed_json.setdefault(
            "certifications",
            []
        )

        parsed_json.setdefault(
            "education",
            "Not Available"
        )

        parsed_json.setdefault(
            "recommended_role",
            "Not Available"
        )

        parsed_json.setdefault(
            "ai_summary",
            "AI summary not available."
        )

        return parsed_json

    except Exception as e:

        return {

            "name":
            "Unknown Candidate",

            "experience":
            "Not Mentioned",

            "skills":
            [],

            "projects":
            [],

            "certifications":
            [],

            "education":
            "Not Available",

            "recommended_role":
            "Not Available",

            "ai_summary":
            f"AI parsing failed: {str(e)}"
        }

# =========================================================
# MAIN PARSER
# =========================================================

def parse_resume(file):

    filename = file.name.lower()

    text = ""

    if filename.endswith(".pdf"):

        text = extract_text_from_pdf(file)

    elif filename.endswith(".docx"):

        text = extract_text_from_docx(file)

    parsed_data = llm_resume_parser(text)

    parsed_data["text"] = text

    parsed_data["file_name"] = file.name

    return parsed_data