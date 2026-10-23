"""Retrieve the most relevant document chunks for a query."""


import numpy as np


from app.embeddings import (
    generate_embeddings,
    generate_query_embedding,
)




def retrieve_relevant_chunks(
    query: str,
    chunks: list[str],
    top_k: int = 3,
) -> list[str]:
    """Return the chunks most relevant to a query."""


    if not query or not query.strip() or not chunks:
        return []


    # Generate document embeddings.
    chunk_embeddings = np.asarray(
        generate_embeddings(chunks),
        dtype=np.float32,
    )


    if chunk_embeddings.ndim != 2:
        raise ValueError("Chunk embeddings must be a 2D array.")


    if chunk_embeddings.shape[0] != len(chunks):
        raise ValueError(
            "The number of embeddings must match the number of chunks."
        )


    # Generate the query embedding.
    query_embedding = np.asarray(
        generate_query_embedding(query),
        dtype=np.float32,
    ).reshape(-1)


    if chunk_embeddings.shape[1] != query_embedding.shape[0]:
        raise ValueError("Document and query embedding dimensions differ.")


    # Calculate cosine similarity.
    query_norm = np.linalg.norm(query_embedding)
    chunk_norms = np.linalg.norm(chunk_embeddings, axis=1)
    denominators = chunk_norms * query_norm


    scores = np.zeros(len(chunks), dtype=np.float32)
    valid = denominators > 0


    scores[valid] = (
        chunk_embeddings[valid] @ query_embedding
    ) / denominators[valid]
    
    #Debug retrieval relevance
    print(f"Query: {query}")
    print("similarity scores:", scores.tolist())


    # Ignore chunks that are not sufficiently relevant.
    MIN_SIMILARITY = 0.15


    ranked_indices = np.argsort(scores)[::-1]
    ranked_indices = [
    int(index)
    for index in ranked_indices
    if scores[index] >= MIN_SIMILARITY
]


    count = min(max(top_k, 1), len(ranked_indices))
    best_indices = ranked_indices[:count]


    return [chunks[index] for index in best_indices]