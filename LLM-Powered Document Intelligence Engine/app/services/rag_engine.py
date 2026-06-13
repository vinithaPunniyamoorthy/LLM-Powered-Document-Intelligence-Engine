from app.services.chunking import split_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import VectorStore


class RAGEngine:
    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or VectorStore()

    def ingest(self, filename: str, text: str, document_id: int):
        chunks = split_text(text)
        embeddings = generate_embeddings(chunks)
        ids = [f"{document_id}-{index}" for index in range(len(chunks))]
        self.vector_store.add(chunks, embeddings, ids)
        return len(chunks)

    def answer(self, question: str, model_embedding_fn):
        query_embedding = model_embedding_fn(question)
        chunks = self.vector_store.search(query_embedding, top_k=4)
        context = "\n\n".join(item["text"] for item in chunks)

        if not context.strip():
            return {
                "answer": "No relevant documents are available yet. Upload documents and ask again.",
                "sources": [],
            }

        answer = (
            "Based on the uploaded documents, here is the best answer:\n\n"
            + context[:1500]
            + "\n\n"
            + "(This demo uses local embeddings and a simple retrieval pipeline.)"
        )

        return {"answer": answer, "sources": [item["id"] for item in chunks]}
