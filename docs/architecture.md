User
              |
              v
        Swagger UI (/docs)
              |
              v
        FastAPI Application
            main.py
              |
              v
       Question Processing
              |
              v
         RAG Module
          app/rag.py
              |
              v
      Retrieval Component
       app/retrieval.py
              |
              v
         Vector Store
     app/vector_store.py
              |
              v
        TF-IDF Embeddings
      app/embeddings.py
              |
              v
       Relevant Text Chunks
              |
              v
       Grounded Answer
              |
              v
     Answer and Source Text
          returned to User




       DOCUMENT INGESTION


 Company Documents
        |
        v
 app/ingestion.py
        |
        v
 Text Extraction
        |
        v
 app/chunking.py
        |
        v
 app/embeddings.py
        |
        v
 app/vector_store.py
        |
        v
 Indexed Document Chunks