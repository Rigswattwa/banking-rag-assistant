from fastapi import FastAPI, HTTPException
from app.schemas import AskRequest, AskResponse
from app.rag.ingestion import load_documents
from app.rag.chunking import chunk_documents
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import build_faiss_index, load_faiss_index
from app.rag.retriever import retrieve_docs
from app.rag.generator import generate_answer
from app.config import DOC_PATH, FAISS_INDEX_PATH
import os
import traceback

app = FastAPI(title="Banking RAG Knowledge Assistant")


db = None
embeddings = get_embedding_model()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    try:
        if os.path.exists(FAISS_INDEX_PATH):
            db = load_faiss_index(embeddings)
        else:
            documents = load_documents(DOC_PATH)
            chunks = chunk_documents(documents)
            db = build_faiss_index(chunks, embeddings)
        yield
    except Exception as e:
        raise RuntimeError(f"Failed to initialize RAG pipeline: {str(e)}")


app = FastAPI(title="Banking RAG Knowledge Assistant", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}

    
@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    if not db:
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    try:
        docs = retrieve_docs(db, payload.question)
        answer, sources = generate_answer(payload.question, docs)
        return AskResponse(answer=answer, sources=sources)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))