Banking RAG Assistant – LLMOps Capstone Project

An end-to-end LLMOps project implementing a Retrieval-Augmented Generation (RAG) pipeline using FastAPI, Streamlit, Docker, Azure AKS, ACR, and GitHub Actions CI/CD.
This project demonstrates production-ready MLOps/LLMOps practices, including containerization, Kubernetes deployment, CI/CD automation, security, and cost optimization.

Features

- RAG Pipeline using OpenAI + embeddings
- FastAPI backend for inference
- Streamlit UI for interactive Q&A
- Dockerized services
- Deployed on Azure AKS
- Images stored in Azure Container Registry (ACR)
- CI pipeline to build & push images on every GitHub commit
- Secrets managed securely (GitHub Secrets + Kubernetes Secrets)

Run FastAPI
uvicorn app.main:app --reload

Run Streamlit
streamlit run streamlit_app.py

Docker Build (Local)
docker build -t banking-rag-api .
docker build -t banking-rag-ui -f Dockerfile.streamlit .

Deployment on AKS (Summary):
Images are pushed to Azure Container Registry
AKS pulls images using managed identity
Services are exposed using LoadBalancer
Secrets are injected using Kubernetes Secrets

CI/CD (Implemented)
Trigger
- On every push to main branch

CI Pipeline
- Build Docker images
- Push images to Azure Container Registry
- GitHub Actions handles authentication using an Azure Service Principal.
