import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================================
# AI JD GENERATOR
# =========================================================

def generate_jd(role_input):

    prompt = f"""
You are an enterprise recruitment AI assistant.

Generate a professional enterprise-grade job description.

Role Requirement:
{role_input}

The JD should contain:

1. Job Title
2. Role Summary
3. Key Responsibilities
4. Required Skills
5. Preferred Skills
6. Experience Required
7. Tools/Technologies
8. Educational Qualification

Requirements:
- professional
- recruiter-grade
- concise
- enterprise-style
- no generic buzzwords
- structured formatting
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

            temperature=0.3
        )

        response = (
            completion
            .choices[0]
            .message
            .content
        )

        return response

    except Exception as e:

        return f"JD generation failed: {str(e)}"