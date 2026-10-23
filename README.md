Enterprise Knowledge Assistant

1. Project Overview
The Enterprise Knowledge Assistant is a Python-based Retrieval-Augmented Generation (RAG) application. It allows users to ask questions about company documents and receive answers based on relevant document content.
The application uses FastAPI to expose REST API endpoints and Swagger UI to test the APIs.


2. Technologies Used
Python
FastAPI
Uvicorn
NumPy
Scikit-learn
TF-IDF vectorization
PyMuPDF
python-docx
Pytest


3. Project Structure
enterprise_knowledge_assistant/
├── app/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── ingestion.py
│   ├── rag.py
│   ├── retrieval.py
│   └── vector_store.py
├── documents/
│   └── company_policy.txt
├── data/
├── docs/
├── tests/
├── main.py
├── requirements.txt
├── test_ingestion_manual.py
└── README.md


4. Installation
Create and activate a Python virtual environment.
On Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Install the project dependencies:
python -m pip install -r requirements.txt
Ensure that scikit-learn is included in requirements.txt because the embedding module imports TfidfVectorizer.


5. Running the Application
From the project root directory, run:
python -m uvicorn main:app --reload
Open Swagger UI in a browser:
http://127.0.0.1:8000/docs
Use the available endpoints to submit questions and inspect the responses.


6. How the Application Works
Document ingestion reads supported company documents.
Text is divided into smaller chunks.
TF-IDF converts text into numerical vectors.
The vector store keeps document chunks and their vectors.
Retrieval compares the question vector with stored document vectors.
The RAG module prepares an answer using the retrieved text.
FastAPI returns the answer and source information.


7. Example Questions
How many annual leave days are available?
What training is required?
How should employees report security incidents?
Can employees share their passwords with other employees?
Answers depend on the content available in the indexed documents.


8. Running Tests
Run the automated tests using:
python -m pytest -v
The ingestion test run completed successfully with three passing tests in the development environment.


9. Retrieval Design
The current embedding implementation uses TF-IDF vectorization. The vector store uses NumPy to calculate cosine similarity between the question vector and document vectors.
This provides a lightweight retrieval approach without requiring an external vector database.
TF-IDF primarily captures lexical similarity. It does not provide the same semantic understanding as a pretrained sentence-embedding model.


10. Limitations and Future Improvements
Expand the document collection to the required 20–50 documents.
Add document metadata and page-level citations where supported.
Improve configurable chunking and duplicate handling.
Evaluate retrieval quality with relevant and irrelevant questions.
Consider hybrid retrieval or reranking.
Add an architecture diagram and a detailed retrieval design note.
Expand automated tests for API behavior and failure handling.


11. Current Validation
FastAPI Swagger interface tested successfully.
Example question-answer requests returned HTTP 200.
Three ingestion tests passed.
Embedding module import test passed.