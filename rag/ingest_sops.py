import json
from pathlib import Path

import ollama


KNOWLEDGE_BASE = Path("knowledge_base")
OUTPUT_FILE = Path("rag/knowledge_index.json")
EMBEDDING_MODEL = "embeddinggemma"


def load_documents():
    documents = []

    for filepath in KNOWLEDGE_BASE.glob("*.md"):
        content = filepath.read_text(encoding="utf-8")

        documents.append({
            "source": filepath.name,
            "content": content
        })

    return documents


def chunk_text(text):
    lines = text.splitlines()

    chunks = []
    current_chunk = []
    document_title = ""
    current_section = None

    for line in lines:
        stripped = line.strip()

        # Store the H1 title, but do not create a standalone chunk for it.
        if stripped.startswith("# ") and not stripped.startswith("## "):
            if not document_title:
                document_title = stripped
            continue

        # Each H2 heading begins a new section.
        if stripped.startswith("## "):
            if current_section is not None and current_chunk:
                chunk = "\n".join(current_chunk).strip()

                if chunk:
                    chunks.append(chunk)

            current_section = stripped

            current_chunk = []

            if document_title:
                current_chunk.append(document_title)
                current_chunk.append("")

            current_chunk.append(current_section)
            continue

        # Ignore content before the first H2 section.
        if current_section is None:
            continue

        current_chunk.append(line)

    # Save final section.
    if current_section is not None and current_chunk:
        chunk = "\n".join(current_chunk).strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def build_index():
    documents = load_documents()

    records = []

    for document in documents:
        chunks = chunk_text(document["content"])

        for chunk_number, chunk in enumerate(chunks):
            response = ollama.embed(
                model=EMBEDDING_MODEL,
                input=chunk
            )

            embedding = response["embeddings"][0]

            records.append({
    "source": document["source"],
    "chunk": chunk_number,
    "section": section,
    "text": chunk,
    "embedding": embedding
})

            print(
                f"Indexed {document['source']} "
                f"chunk {chunk_number}"
            )

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(records),
        encoding="utf-8"
    )

    print(f"\nIndexed {len(records)} chunks.")


if __name__ == "__main__":
    build_index()