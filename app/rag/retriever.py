from app.config import TOP_K

def retrieve_docs(db, query: str):
    return db.similarity_search(query, k=TOP_K)