import os

import numpy as np

try:
    import faiss
except ImportError:  # pragma: no cover - fallback for minimal environments
    faiss = None


class VectorStore:
    def __init__(self, path: str = "./chroma_db"):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.index = faiss.IndexFlatL2(64) if faiss is not None else None
        self.documents = []
        self.vectors = []

    def add(self, documents, embeddings, ids):
        vectors = np.array(embeddings, dtype="float32")
        if self.index is not None:
            self.index.add(vectors)
        else:
            self.vectors.extend(vectors)

        for doc_id, doc_text in zip(ids, documents):
            self.documents.append({"id": doc_id, "text": doc_text})

    def search(self, query_embedding, top_k: int = 4):
        if self.index is not None:
            distances, indices = self.index.search(np.array([query_embedding], dtype="float32"), top_k)
            result = []
            for idx in indices[0]:
                if idx < 0 or idx >= len(self.documents):
                    continue
                result.append(self.documents[int(idx)])
            return result

        query_vector = np.array(query_embedding, dtype="float32")
        scores = []
        for index, vector in enumerate(self.vectors):
            norm_product = np.linalg.norm(query_vector) * np.linalg.norm(vector)
            similarity = float(np.dot(query_vector, vector) / (norm_product + 1e-9))
            scores.append((similarity, index))

        scores.sort(key=lambda item: item[0], reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k] if idx < len(self.documents)]
