import streamlit as st
import pandas as pd
import chromadb

from utils.parser import parse_resume
from utils.embeddings import generate_embedding
from utils.search import search_resumes
from utils.jd_generator import generate_jd
from utils.jd_match import match_jd
from utils.dedup import deduplicate_resumes
from utils.chatbot import recruiter_chat

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ARROWS AI",
    layout="wide"
)

st.title("ARROWS AI Talent Intelligence Platform")

st.write(
    "AI-powered recruitment intelligence platform for semantic candidate retrieval, "
    "resume parsing, JD matching, duplicate detection, and recruiter assistance."
)

# =========================================================
# CHROMA DB
# =========================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

try:

    collection = client.get_collection(
        name="resume_collection"
    )

except:

    collection = client.create_collection(
        name="resume_collection"
    )
# =========================================================
# SESSION STATE
# =========================================================

if "resume_data" not in st.session_state:

    st.session_state.resume_data = []

if "unique_resume_data" not in st.session_state:

    st.session_state.unique_resume_data = []

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# =========================================================
# PROCESS RESUMES
# =========================================================

if uploaded_files:

    resume_data = []

    for file in uploaded_files:

        try:

            parsed = parse_resume(file)

            parsed["file_name"] = file.name

            embedding = generate_embedding(
                parsed["text"]
            )

            parsed["embedding"] = embedding

            resume_data.append(parsed)

        except Exception as e:

            st.error(
                f"Error processing {file.name}: {e}"
            )

    # =====================================================
    # DEDUPLICATION
    # =====================================================

    dedup_results = deduplicate_resumes(
        resume_data
    )

    unique_resume_data = dedup_results[
        "unique_resumes"
    ]

    duplicates = dedup_results[
        "duplicates"
    ]

    original_count = dedup_results[
        "original_count"
    ]

    unique_count = dedup_results[
        "unique_count"
    ]

    # =====================================================
    # INDEX ONLY UNIQUE RESUMES
    # =====================================================

    for resume in unique_resume_data:

        try:

            collection.add(

                documents=[
                    resume["text"]
                ],

                embeddings=[
                    resume["embedding"]
                ],

                metadatas=[
                    {
                        "file_name":
                        resume["file_name"]
                    }
                ],

                ids=[
                    resume["file_name"]
                ]
            )

        except:
            pass

    st.session_state.resume_data = (
        resume_data
    )

    st.session_state.unique_resume_data = (
        unique_resume_data
    )

    st.session_state.duplicates = (
        duplicates
    )

    st.session_state.original_count = (
        original_count
    )

    st.session_state.unique_count = (
        unique_count
    )

    st.success(
        "Resumes Indexed Successfully"
    )

# =========================================================
# SESSION DATA
# =========================================================

resume_data = st.session_state.get(
    "resume_data",
    []
)

unique_resume_data = st.session_state.get(
    "unique_resume_data",
    []
)

duplicates = st.session_state.get(
    "duplicates",
    []
)

original_count = st.session_state.get(
    "original_count",
    0
)

unique_count = st.session_state.get(
    "unique_count",
    0
)

# =========================================================
# METRICS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Uploaded Resumes",
        original_count
    )

with col2:

    st.metric(
        "Unique Resumes After Deduplication",
        unique_count
    )

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([

    "Duplicate Detection",

    "Parsed Resume Details",

    "Semantic Search",

    "AI JD Generator",

    "JD Match Engine",

    "AI Recruiter Chatbot"
])
# =========================================================
# TAB 1 — DUPLICATE DETECTION
# =========================================================

with tab1:

    st.header(
        "Resume Deduplication Engine"
    )

    st.write(
        "Detect and remove duplicate resumes using semantic similarity."
    )

    st.success(
        f"Original Resumes: {original_count}"
    )

    st.success(
        f"Unique Resumes After Deduplication: {unique_count}"
    )

    if duplicates:

        st.subheader(
            "Duplicate Resumes Detected"
        )

        for dup in duplicates:

            st.warning(
                f"""
Duplicate Resume:
{dup['duplicate']}

Original Resume:
{dup['original']}

Similarity Score:
{dup['score']}%
"""
            )

    else:

        st.success(
            "No duplicate resumes detected."
        )

# =========================================================
# TAB 2 — PARSED RESUME DETAILS
# =========================================================

with tab2:

    st.header(
        "Parsed Resume Details"
    )

    if len(unique_resume_data) == 0:

        st.warning(
            "No resumes uploaded."
        )

    else:

        resume_names = [

            resume.get(
                "file_name",
                "Unknown Resume"
            )

            for resume in unique_resume_data
        ]

        selected_resume = st.selectbox(
            "Select Resume",
            resume_names
        )

        selected_data = None

        for resume in unique_resume_data:

            if (
                resume.get("file_name")
                ==
                selected_resume
            ):

                selected_data = resume
                break

        if selected_data:

            st.subheader(
                selected_data.get(
                    "file_name",
                    "Unknown Resume"
                )
            )

            st.markdown("---")

            st.markdown("### Candidate Name")

            st.write(
                selected_data.get(
                    "name",
                    "Not Available"
                )
            )

            st.markdown("### Experience")

            st.write(
                selected_data.get(
                    "experience",
                    "Not Mentioned"
                )
            )

            skills = selected_data.get(
                "skills",
                []
            )

            if skills:

                st.markdown("### Skills")

                st.write(
                    ", ".join(skills)
                )

            projects = selected_data.get(
                "projects",
                []
            )

            if projects:

                st.markdown("### Projects")

                for project in projects[:5]:

                    st.write(
                        f"- {project}"
                    )

            certifications = selected_data.get(
                "certifications",
                []
            )

            if certifications:

                st.markdown(
                    "### Certifications"
                )

                for cert in certifications[:5]:

                    st.write(
                        f"- {cert}"
                    )

            education = selected_data.get(
                "education",
                "Not Available"
            )

            st.markdown("### Education")

            st.write(education)

            recommended_role = selected_data.get(
                "recommended_role",
                "Not Available"
            )

            st.markdown(
                "### Recommended Role"
            )

            st.write(recommended_role)

            ai_summary = selected_data.get(
                "ai_summary",
                "AI summary not available."
            )

            st.markdown(
                "### AI Candidate Summary"
            )

            st.write(ai_summary)

# =========================================================
# TAB 3 — SEMANTIC SEARCH
# =========================================================

with tab3:

    st.header(
        "Semantic Candidate Search"
    )

    query = st.text_input(
        "Search Candidates"
    )

    if query:

        results = search_resumes(
            query,
            unique_resume_data
        )

        if results:

            for candidate in results:

                st.subheader(
                    f"{candidate.get('file_name', 'Unknown Resume')}"
                )

                st.markdown(
                    "### Experience"
                )

                st.write(
                    candidate.get(
                        "experience",
                        "Not Mentioned"
                    )
                )

                skills = candidate.get(
                    "skills",
                    []
                )

                if skills:

                    st.markdown(
                        "### Skills"
                    )

                    st.write(
                        ", ".join(skills)
                    )

                st.markdown(
                    "### Why This Resume Fits"
                )

                st.write(
                    candidate.get(
                        "reason",
                        "Relevant candidate based on semantic retrieval."
                    )
                )

                st.markdown("---")

        else:

            st.warning(
                "No matching candidates found."
            )
# =========================================================
# TAB 4 — AI JD GENERATOR
# =========================================================

with tab4:

    st.header(
        "AI Job Description Generator"
    )

    role_input = st.text_area(
        "Enter Role Requirement"
    )

    if st.button(
        "Generate JD"
    ):

        if role_input:

            generated_jd = generate_jd(
                role_input
            )

            st.markdown(
                generated_jd
            )

        else:

            st.warning(
                "Please enter role requirements."
            )

# =========================================================
# TAB 5 — JD MATCH ENGINE
# =========================================================

with tab5:

    st.header(
        "JD Match Engine"
    )

    jd_text = st.text_area(
        "Paste Job Description"
    )

    if st.button(
        "Match Candidates"
    ):

        matches = match_jd(
            jd_text,
            unique_resume_data
        )

        if matches:

            table_data = []

            for candidate in matches:

                table_data.append({

                    "Resume":
                    candidate.get(
                        "name",
                        "Unknown"
                    ),

                    "Match %":
                    candidate.get(
                        "score",
                        0
                    ),

                    "Experience":
                    candidate.get(
                        "experience",
                        "NA"
                    ),

                    "Skills":
                    ", ".join(
                        candidate.get(
                            "skills",
                            []
                        )
                    )
                })

            df = pd.DataFrame(
                table_data
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.warning(
                "No matching resumes found."
            )

# =========================================================
# TAB 6 — AI RECRUITER CHATBOT
# =========================================================

with tab6:

    st.header(
        "AI Recruiter Chatbot"
    )

    chat_query = st.text_input(
        "Ask AI Recruiter"
    )

    if chat_query:

        response = recruiter_chat(
            chat_query,
            unique_resume_data
        )

        st.markdown(response)