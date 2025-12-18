import os
from langchain_community.vectorstores import FAISS
from app.config import FAISS_INDEX_PATH

def build_faiss_index(docs, embeddings):
    db = FAISS.from_documents(docs, embeddings)
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    db.save_local(FAISS_INDEX_PATH)
    return db

def load_faiss_index(embeddings):
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

