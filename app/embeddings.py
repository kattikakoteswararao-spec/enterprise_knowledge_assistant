"""Lightweight TF-IDF embedding implementation."""


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


_vectorizer = None




def generate_embeddings(texts: list[str]) -> np.ndarray:
    """Generate document vectors using a fitted TF-IDF vectorizer."""
    global _vectorizer


    if not texts:
        _vectorizer = None
        return np.empty((0, 0), dtype=np.float32)


    _vectorizer = TfidfVectorizer()
    matrix = _vectorizer.fit_transform(texts)


    return matrix.toarray().astype(np.float32)




def generate_query_embedding(query: str) -> np.ndarray:
    """Generate a query vector using the same fitted vectorizer."""
    if _vectorizer is None:
        raise RuntimeError(
            "Generate document embeddings before embedding a query."
        )


    return _vectorizer.transform([query]).toarray()[0].astype(np.float32)