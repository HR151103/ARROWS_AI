from utils.summary import generate_summary


def match_jd(jd_text, resume_data):

    jd_summary = generate_summary(jd_text)

    jd_skills = set(
        skill.lower()
        for skill in jd_summary.get("skills", [])
    )

    ranked_results = []

    for resume in resume_data:

        summary = generate_summary(
            resume["text"]
        )

        candidate_skills = set(
            skill.lower()
            for skill in summary.get("skills", [])
        )

        matched_skills = jd_skills.intersection(
            candidate_skills
        )

        if len(jd_skills) == 0:

            match_percent = 0

        else:

            match_percent = int(
                (
                    len(matched_skills)
                    / len(jd_skills)
                ) * 100
            )

        ranked_results.append({

            "name": resume["name"],

            "experience": summary.get(
                "experience",
                "Not Mentioned"
            ),

            "skills": list(candidate_skills),

            "matched_skills": list(matched_skills),

            "score": match_percent
        })

    ranked_results = sorted(
        ranked_results,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_results