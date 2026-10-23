"""
RAG answer generation using retrieved document chunks.
"""


from app.retrieval import retrieve_relevant_chunks




def answer_question(
    question: str,
    chunks: list[dict] | list[str],
    top_k: int = 3,
) -> dict:
    """Return a concise answer based on the available company documents."""


    if not question or not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }


    if not chunks:
        return {
            "answer": "No documents are available.",
            "sources": [],
        }


    question = question.strip()
    question_lower = question.lower()


    # Preserve the original document metadata.
    document_chunks = []


    for item in chunks:
        if isinstance(item, dict):
            text = item.get("text", "")
            source = item.get("source", "unknown")


            if isinstance(text, str) and text.strip():
                document_chunks.append({
                    "text": text.strip(),
                    "source": source,
                })


        elif isinstance(item, str) and item.strip():
            document_chunks.append({
                "text": item.strip(),
                "source": "unknown",
            })


    if not document_chunks:
        return {
            "answer": "No readable text was found in the documents.",
            "sources": [],
        }


    # Retrieve relevant text using the existing retrieval module.
    text_chunks = [item["text"] for item in document_chunks]


    try:
        retrieved = retrieve_relevant_chunks(
            question,
            text_chunks,
            top_k=top_k,
        )
    except Exception:
        retrieved = []


    # Match retrieved text back to its original source document.
    relevant = []


    if retrieved:
        for result in retrieved:
            if isinstance(result, dict):
                result_text = result.get("text", "")
            else:
                result_text = result


            if not isinstance(result_text, str):
                continue


            for item in document_chunks:
                if (
                    item["text"] == result_text
                    and item not in relevant
                ):
                    relevant.append(item)


    # Safe fallback: find chunks containing words from the question.
    if not relevant:
        question_words = {
            word.strip(".,?!:;()[]{}\"'")
            for word in question_lower.split()
            if len(word.strip(".,?!:;()[]{}\"'")) > 2
        }


        scored = []


        for item in document_chunks:
            text_lower = item["text"].lower()
            score = sum(
                1 for word in question_words
                if word in text_lower
            )


            if score > 0:
                scored.append((score, item))


        scored.sort(key=lambda pair: pair[0], reverse=True)
        relevant = [item for _, item in scored[:top_k]]


    if not relevant:
        return {
            "answer": (
                "I could not find relevant information "
                "for this question in the available documents."
            ),
            "sources": [],
        }


    # Build a concise, question-focused answer from matching sentences.
    answer_sentences = []


    for item in relevant:
        text = item["text"]


        # Split policy text into individual sentences.
        sentences = text.replace("\n", " ").split(".")


        for sentence in sentences:
            sentence = sentence.strip()


            if not sentence:
                continue


            sentence_lower = sentence.lower()


            # Match the type of question to the relevant policy statement.
            if (
                any(word in question_lower for word in
                    ["security incident", "security issue", "incident"])
                and any(word in sentence_lower for word in
                    ["security incident", "report", "support team", "it support"])
            ):
                answer_sentences.append(sentence)


            elif (
                any(word in question_lower for word in
                    ["annual leave", "leave days", "vacation"])
                and any(word in sentence_lower for word in
                    ["annual leave", "days of annual leave"])
            ):
                answer_sentences.append(sentence)


            elif (
                any(word in question_lower for word in
                    ["password", "passwords"])
                and any(word in sentence_lower for word in
                    ["password", "shared"])
            ):
                answer_sentences.append(sentence)


            elif (
                any(word in question_lower for word in
                    ["training", "security training"])
                and any(word in sentence_lower for word in
                    ["training", "every year"])
            ):
                answer_sentences.append(sentence)


            elif (
                any(word in question_lower for word in
                    ["manager", "approval", "submit leave"])
                and any(word in sentence_lower for word in
                    ["manager", "approval", "leave requests"])
            ):
                answer_sentences.append(sentence)


    # Remove duplicate sentences while preserving their order.
    answer_sentences = list(dict.fromkeys(answer_sentences))


    if answer_sentences:
        answer = " ".join(answer_sentences[:3]) + "."
    else:
        # Return only the first relevant passage, not every document.
        answer = relevant[0]["text"].strip()


        if len(answer) > 500:
            answer = answer[:500].rsplit(" ", 1)[0] + "..."


    # Return source filenames with only relevant sentences.
    sources = []


    for item in relevant:
        source_name = item.get("source", "unknown")
        text = item.get("text", "")


        matching_sentences = []


        for sentence in text.replace("\n", " ").split("."):
            sentence = sentence.strip()


            if not sentence:
                continue


            sentence_lower = sentence.lower()


            if (
                "security incident" in question_lower
                or "security issue" in question_lower
                or "incident" in question_lower
            ):
                if (
                    "security incident" in sentence_lower
                    or (
                        "report" in sentence_lower
                        and "security" in sentence_lower
                    )
                ):
                    matching_sentences.append(sentence)


            elif "password" in question_lower:
                if "password" in sentence_lower:
                    matching_sentences.append(sentence)


            elif "annual leave" in question_lower or "vacation" in question_lower:
                if "annual leave" in sentence_lower:
                    matching_sentences.append(sentence)


            elif "training" in question_lower:
                if "training" in sentence_lower:
                    matching_sentences.append(sentence)


            else:
                if any(
                    word in sentence_lower
                    for word in question_lower.split()
                    if len(word) > 3
                ):
                    matching_sentences.append(sentence)


        source_text = ". ".join(matching_sentences).strip()


        if source_text:
            source_entry = {
                "document": source_name,
                "text": source_text + ".",
            }


            if source_entry not in sources:
                sources.append(source_entry)


    return {
        "answer": answer,
        "sources": sources,
    }