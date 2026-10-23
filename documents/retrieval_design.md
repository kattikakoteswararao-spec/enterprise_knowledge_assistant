Retrieval Design Note


1. Overview


The Enterprise Knowledge Assistant uses Retrieval-Augmented Generation (RAG) principles to answer questions using information from company documents.


2. Document Ingestion


The ingestion component reads supported documents and extracts their text. The extracted text is divided into smaller chunks so that relevant information can be retrieved efficiently.


3. Chunking Strategy


The application splits document text into smaller sections. This helps the retrieval component identify relevant information without processing an entire document for every question.


4. Embeddings


The current implementation uses a TF-IDF vectorizer from scikit-learn to represent text numerically.


Document chunks and user questions are transformed into vectors using the same fitted vectorizer.


5. Vector Storage and Search


The application uses a NumPy-based in-memory vector store.


Cosine similarity is used to compare the question vector with stored document vectors. The application returns the highest-scoring relevant chunks.


This implementation is a lightweight in-memory search solution rather than a persistent vector database.


6. Answer Generation


The RAG component uses retrieved document text to prepare an answer. The API returns the answer together with source information to help users identify the supporting document.


7. Failure Handling


The application should handle empty questions, missing documents, empty retrieval results, and embedding dimension mismatches appropriately.


If relevant information cannot be found, the application should avoid presenting unsupported information as fact.


8. Current Limitations


The vector store keeps data in memory.
TF-IDF primarily matches text based on word importance and does not provide the full semantic understanding of a pretrained embedding model.
The current implementation does not demonstrate a persistent vector database or a complete hybrid search and reranking pipeline.
The current test suite includes three passing ingestion tests; additional retrieval and API tests would improve coverage.


9. Future Improvements


Support 20–50 documents in the ingestion pipeline.
Add persistent vector storage.
Evaluate semantic embedding models.
Implement hybrid retrieval or reranking.
Add tests for irrelevant questions, duplicate chunks, source attribution, and API error handling.


10. Conclusion


The application provides a foundation for document ingestion, TF-IDF vector search, retrieval, and source-attributed question answering through FastAPI. Further improvements can strengthen retrieval quality, scalability, and test coverage.