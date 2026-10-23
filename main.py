"""
Enterprise Knowledge Assistant
FastAPI application for answering questions using company documents.
"""


from pathlib import Path


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from app.ingestion import ingest_directory
from app.chunking import chunk_text
from app.rag import answer_question




# --------------------------------------------------
# FastAPI application
# --------------------------------------------------


app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="RAG-based company document question-answering API",
    version="1.0.0",
)




# --------------------------------------------------
# Request model
# --------------------------------------------------


class QuestionRequest(BaseModel):
    question: str




# --------------------------------------------------
# Find documents directory
# --------------------------------------------------


def find_documents_directory() -> Path:
    """Find the folder containing company documents."""


    project_dir = Path(__file__).resolve().parent


    possible_paths = [
        project_dir / "documents",
        project_dir / "docs" / "documents",
        project_dir / "app" / "documents",
    ]


    for path in possible_paths:
        if path.is_dir():
            return path


    checked_paths = ", ".join(str(path) for path in possible_paths)


    raise FileNotFoundError(
        f"Documents directory not found. Checked: {checked_paths}"
    )




# --------------------------------------------------
# Home endpoint
# --------------------------------------------------


@app.get("/")
def home():
    return {
        "message": "Enterprise Knowledge Assistant API is running",
        "docs": "/docs",
        "endpoint": "POST /ask",
    }




# --------------------------------------------------
# Health check endpoint
# --------------------------------------------------


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Enterprise Knowledge Assistant",
    }




# --------------------------------------------------
# Ask a question endpoint
# --------------------------------------------------


@app.post("/ask")
def ask_question_endpoint(request: QuestionRequest):
    """
    Answer a question using the available company documents.
    """


    question = request.question.strip()


    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )


    try:
        # 1. Locate the documents directory.
        documents_path = find_documents_directory()


        # 2. Load documents.
        documents = ingest_directory(str(documents_path))


        if not documents:
            raise HTTPException(
                status_code=404,
                detail="No readable documents were found.",
            )


        # 3. Split documents into chunks and preserve metadata.
        chunks = []


        for item in documents:


            if isinstance(item, dict):
                # Read document text.
                text = (
                    item.get("text")
                    or item.get("content")
                    or item.get("page_content")
                    or ""
                )


                # Preserve the document name or path.
                source = (
                    item.get("source")
                    or item.get("filename")
                    or item.get("file_name")
                    or item.get("file_path")
                    or item.get("path")
                )


                # Use a document path if available.
                if source:
                    source = str(source)
                    source_name = Path(source).name
                else:
                    source_name = "unknown"


            elif isinstance(item, str):
                # Ingestion returned plain text without metadata.
                text = item
                source_name = "unknown"


            else:
                continue


            if not isinstance(text, str) or not text.strip():
                continue


            # Split the document into smaller chunks.
            text_chunks = chunk_text(
                text.strip(),
                chunk_size=500,
                overlap=50,
            )


            # Attach source information to each chunk.
            for text_chunk in text_chunks:
                chunks.append(
                    {
                        "text": text_chunk,
                        "source": source_name,
                    }
                )


        # 4. Check whether any text was extracted.
        if not chunks:
            raise HTTPException(
                status_code=404,
                detail="No text could be extracted from the documents.",
            )


        # 5. Retrieve relevant chunks and generate an answer.
        result = answer_question(question, chunks)


        return result


    except HTTPException:
        raise


    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to process the question: {exc}",
        ) from exc




# --------------------------------------------------
# Run directly with Python, if required
# --------------------------------------------------


if __name__ == "__main__":
    import uvicorn


    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )