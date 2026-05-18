def analyze_candidate(summary):

    skills = summary["skills"]

    score = min(len(skills) * 12, 95)

    strengths = []

    gaps = []

    role = "Software Engineer"

    if "Spark" in skills or "Hadoop" in skills:
        role = "Data Engineer"

    if "Machine Learning" in skills or "NLP" in skills:
        role = "AI/ML Engineer"

    if "AWS" in skills:
        strengths.append("Cloud platform exposure")

    if "Python" in skills:
        strengths.append("Strong Python skills")

    if "SQL" in skills:
        strengths.append("Database and querying expertise")

    if "Docker" not in skills:
        gaps.append("Docker knowledge not identified")

    if "Kubernetes" not in skills:
        gaps.append("Kubernetes exposure missing")

    return {
        "score": score,
        "role": role,
        "strengths": strengths,
        "gaps": gaps
    }
