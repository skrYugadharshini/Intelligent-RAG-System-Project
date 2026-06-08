import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("policies")


def get_level(level):
    return {
        "public": 1,
        "internal": 2,
        "confidential": 3,
        "highly-confidential": 4
    }.get(level, 1)


def retrieve(question, context, user_clearance):

    q_embed = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[q_embed],
        n_results=10
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    ids = results["ids"][0]

    output_docs = []

    user_max = max([get_level(x) for x in user_clearance])

    for i in range(len(docs)):

        meta = metas[i]

        # -------------------------
        # SECURITY FILTER
        # -------------------------
        if get_level(meta.get("security_level")) > user_max:
            continue

        # -------------------------
        # DEPRECATED DOWN-RANK
        # -------------------------
        if meta.get("status") == "DEPRECATED":
            continue

        output_docs.append({
            "id": ids[i],
            "text": docs[i],
            "metadata": meta
        })

    return output_docs