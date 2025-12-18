from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.config import OPENAI_API_KEY, LLM_MODEL


def generate_answer(query: str, docs):
    context = "\n\n".join(
        d.page_content for d in docs if query.lower() in d.page_content.lower()
    )
    if not context:
        context = "\n\n".join(d.page_content for d in docs)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a banking policy assistant.\n"
            "Answer the question using the context below.\n"
            "If the answer is partially available, answer using best judgment "
            "but do NOT fabricate facts.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer in a clear, concise manner:"
        )
    )

    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model=LLM_MODEL,
        temperature=0
    )

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": query})

    sources = [
        {
            "source": d.metadata.get("source", "unknown"),
            "snippet": d.page_content[:300]
        }
        for d in docs
    ]

    return response.content, sources