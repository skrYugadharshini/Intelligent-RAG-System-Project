from fastapi import FastAPI
from pydantic import BaseModel
from retrieval import retrieve
from groq import Groq

app = FastAPI()

client = Groq(api_key="")


class QueryRequest(BaseModel):
    question: str
    context: dict = {}
    user_clearance: list = []


def build_prompt(question, docs):

    context_text = "\n\n".join([d["text"] for d in docs])

    return f"""
You are a policy assistant.

Use ONLY the context below:

{context_text}

Question: {question}

Answer clearly and short.
"""


@app.get("/")
def home():
    return {"status": "RAG system running"}


@app.post("/query")
def query(data: QueryRequest):

    docs = retrieve(
        data.question,
        data.context,
        data.user_clearance
    )

    if not docs:
        return {
            "answer": "Insufficient policy certainty",
            "sources": [],
            "overall_confidence": 0.0
        }

    prompt = build_prompt(data.question, docs)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": [
            {
                "id": d["id"],
                "title": d["metadata"].get("title", ""),
                "security_level": d["metadata"].get("security_level", "")
            }
            for d in docs
        ],
        "overall_confidence": 0.85
    }