from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}




def read_document(file_path: str) -> list[dict]:
    """Read a PDF, TXT, or DOCX file and return extracted text."""
    path = Path(file_path)


    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")


    extension = path.suffix.lower()
    results = []


    if extension == ".pdf":
        import fitz


        with fitz.open(path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text().strip()


                if text:
                    results.append({
                        "text": text,
                        "source": path.name,
                        "page": page_number,
                    })


    elif extension == ".txt":
        text = path.read_text(encoding="utf-8").strip()


        if text:
            results.append({
                "text": text,
                "source": path.name,
                "page": None,
            })


    elif extension == ".docx":
        from docx import Document


        document = Document(path)


        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ).strip()


        if text:
            results.append({
                "text": text,
                "source": path.name,
                "page": None,
            })


    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Supported formats are PDF, TXT, and DOCX."
        )


    return results




def ingest_directory(directory_path: str) -> list[dict]:
    """Read all supported documents in a directory."""
    directory = Path(directory_path)


    if not directory.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {directory}"
        )


    if not directory.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {directory}"
        )


    documents = []


    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                extracted_documents = read_document(str(path))


                for document in extracted_documents:
                    document["source"] = path.name


                documents.extend(extracted_documents)


            except Exception as exc:
                print(f"Could not read {path.name}: {exc}")


    return documents