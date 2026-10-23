from pathlib import Path
from app.ingestion import read_document, ingest_directory


def test_document_folder():
    folder = Path("documents")
    assert folder.exists(), "Documents folder not found"
    assert folder.is_dir(), "Documents path is not a directory"
    print("PASS: Documents folder exists")


def test_read_company_policy():
    file_path = Path("documents/company_policy.txt")
    assert file_path.exists(), "Company policy file not found"


    documents = read_document(str(file_path))


    assert len(documents) > 0, "No text extracted"
    assert "Company Policy" in documents[0]["text"]
    assert documents[0]["source"] == "company_policy.txt"


    print("PASS: Company policy text extracted")


def test_ingest_directory():
    documents = ingest_directory("documents")


    assert len(documents) > 0, "No documents ingested"
    print(f"PASS: Ingested {len(documents)} document(s)")


if __name__ == "__main__":
    test_document_folder()
    test_read_company_policy()
    test_ingest_directory()
    print("ALL MANUAL TESTS PASSED")