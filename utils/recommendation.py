def hiring_recommendation(skills, experience):

    recommendation = "Moderate Fit"

    strengths = []

    risks = []

    role = "Software Engineer"

    if "Spark" in skills or "Hadoop" in skills:

        role = "Data Engineer"

        strengths.append(
            "Strong Big Data ecosystem exposure"
        )

    if "Machine Learning" in skills or "NLP" in skills:

        role = "AI/ML Engineer"

        strengths.append(
            "AI and Machine Learning expertise"
        )

    if "AWS" in skills or "Azure" in skills:

        strengths.append(
            "Cloud platform experience"
        )

    if "Python" in skills:

        strengths.append(
            "Strong programming capability"
        )

    if "Docker" not in skills:

        risks.append(
            "Containerization experience not identified"
        )

    if "Kubernetes" not in skills:

        risks.append(
            "Kubernetes exposure missing"
        )

    if len(skills) >= 6:

        recommendation = "Strongly Recommended"

    elif len(skills) >= 4:

        recommendation = "Recommended"

    return {
        "role": role,
        "recommendation": recommendation,
        "strengths": strengths,
        "risks": risks
    }