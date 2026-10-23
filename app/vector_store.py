"""
Simple in-memory vector store for the Enterprise Knowledge Assistant.
Uses NumPy to store and search TF-IDF embeddings.
"""


import numpy as np


from app.embeddings import generate_embeddings




class VectorStore:
    """Store document chunks and their vector representations."""


    def __init__(self):
        self.chunks = []
        self.embeddings = None


    def add_documents(self, chunks: list[str]) -> None:
        """Generate embeddings and store document chunks."""
        if not chunks:
            return


        new_embeddings = np.asarray(
            generate_embeddings(chunks),
            dtype=np.float32,
        )


        if new_embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D array.")


        if self.embeddings is not None:
            if self.embeddings.shape[1] != new_embeddings.shape[1]:
                raise ValueError(
                    "Embedding dimensions do not match. "
                    "Use the same vectorizer for all documents."
                )


            self.embeddings = np.vstack(
                [self.embeddings, new_embeddings]
            )
        else:
            self.embeddings = new_embeddings


        self.chunks.extend(chunks)


    def search(self, query: str, top_k: int = 3) -> list[str]:
        """Return the most relevant stored chunks."""
        if not query or not query.strip() or not self.chunks:
            return []


        from app.embeddings import generate_query_embedding


        query_embedding = np.asarray(
            generate_query_embedding(query),
            dtype=np.float32,
        ).reshape(-1)


        if self.embeddings.shape[1] != query_embedding.shape[0]:
            raise ValueError("Query and document dimensions do not match.")


        query_norm = np.linalg.norm(query_embedding)
        chunk_norms = np.linalg.norm(self.embeddings, axis=1)
        denominators = chunk_norms * query_norm


        scores = np.zeros(len(self.chunks), dtype=np.float32)
        valid = denominators > 0


        scores[valid] = (
            self.embeddings[valid] @ query_embedding
        ) / denominators[valid]


        count = min(max(top_k, 1), len(self.chunks))
        best_indices = np.argsort(scores)[::-1][:count]


        return [self.chunks[int(i)] for i in best_indices]