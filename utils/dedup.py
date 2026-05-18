from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def deduplicate_resumes(resume_data, threshold=0.90):

    texts = [resume["text"] for resume in resume_data]

    embeddings = model.encode(texts)

    duplicates = []
    unique_resumes = []
    used_indexes = set()

    for i in range(len(resume_data)):

        if i in used_indexes:
            continue

        unique_resumes.append(resume_data[i])

        for j in range(i + 1, len(resume_data)):

            similarity = cosine_similarity(
                [embeddings[i]],
                [embeddings[j]]
            )[0][0]

            if similarity >= threshold:

                duplicates.append({
                    "original": resume_data[i]["file_name"],
                    "duplicate": resume_data[j]["file_name"],
                    "score": round(similarity * 100, 2)
                })

                used_indexes.add(j)

    return {
        "unique_resumes": unique_resumes,
        "duplicates": duplicates,
        "original_count": len(resume_data),
        "unique_count": len(unique_resumes)
    }