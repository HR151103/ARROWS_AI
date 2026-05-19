from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

from langchain_groq import ChatGroq

from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# LOAD LLM
# =========================================================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# =========================================================
# EMBEDDINGS
# =========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================================================
# LOAD DOCUMENTS
# =========================================================

def load_documents(file_path):

    if file_path.endswith(".pdf"):

        loader = PyPDFLoader(file_path)

    else:

        loader = Docx2txtLoader(file_path)

    documents = loader.load()

    return documents

# =========================================================
# SPLIT DOCUMENTS
# =========================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks

# =========================================================
# CREATE VECTOR STORE
# =========================================================

def create_vectorstore(chunks):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="langchain_chroma_db"
    )

    return vectorstore

# =========================================================
# CREATE RAG CHAIN
# =========================================================

def create_rag_chain(vectorstore):

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 5}
        ),
        return_source_documents=True
    )

    return qa_chain