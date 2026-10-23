"""Split document text into smaller chunks for retrieval."""




def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text into chunks with a small overlap."""


    if not text or not text.strip():
        return []


    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")


    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between zero and chunk_size.")


    words = text.split()
    chunks = []
    start = 0


    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))


        if end == len(words):
            break


        start = end - overlap


    return chunks