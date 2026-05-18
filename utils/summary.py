import re

skills_database = [
    "Python",
    "SQL",
    "AWS",
    "Spark",
    "Hadoop",
    "Kafka",
    "Machine Learning",
    "NLP",
    "React",
    "Java",
    "Docker",
    "Kubernetes",
    "Power BI",
    "Azure",
    "ETL",
    "Airflow",
    "Hive",
    "PySpark"
]

def generate_summary(text):

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    experience = "Not Mentioned"

    match = re.search(
        r'(\d+(\.\d+)?)\+?\s+years',
        text,
        re.IGNORECASE
    )

    if match:

        experience = match.group(0)

    return {
        "name": "Resume Profile",
        "experience": experience,
        "skills": found_skills[:8]
    }
