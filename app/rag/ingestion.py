import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

def load_documents(doc_path: str):
    documents = []
    for file in os.listdir(doc_path):
        full_path = os.path.join(doc_path, file)
    if file.endswith('.pdf'):
        documents.extend(PyPDFLoader(full_path).load())
    elif file.endswith('.txt'):
        documents.extend(TextLoader(full_path).load())
    elif file.endswith('.docx'):
        documents.extend(Docx2txtLoader(full_path).load())
    return documents