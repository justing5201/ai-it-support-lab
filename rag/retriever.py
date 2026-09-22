import json
import math
from pathlib import Path

import ollama


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "rag/knowledge_index.json"
KNOWLEDGE_BASE = ROOT / "knowledge_base"
EMBEDDING_MODEL = "embeddinggemma"


def load_full_sop(source):
    filepath = (KNOWLEDGE_BASE / source).resolve()

    if filepath.parent != KNOWLEDGE_BASE.resolve() or filepath.suffix != ".md":
        raise ValueError("Invalid SOP path")

    if not filepath.exists():
        raise FileNotFoundError(
            f"SOP file not found: {source}"
        )

    return filepath.read_text(
        encoding="utf-8"
    )


def cosine_similarity(vector_a, vector_b):
    if not vector_a or len(vector_a) != len(vector_b) or not all(math.isfinite(x) for x in [*vector_a, *vector_b]):
        raise ValueError("Invalid embedding dimensions or values")
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def load_index():
    return json.loads(
        INDEX_FILE.read_text(
            encoding="utf-8"
        )
    )


def retrieve_relevant_sops(
    query,
    top_k=3
):
    index = load_index()

    response = ollama.Client(timeout=60).embed(
        model=EMBEDDING_MODEL,
        input=query
    )

    query_embedding = response[
        "embeddings"
    ][0]

    results = []

    for record in index:
        score = cosine_similarity(
            query_embedding,
            record["embedding"]
        )

        results.append({
            "source": record["source"],
            "chunk": record["chunk"],
            "section": record.get(
                "section",
                "Unknown"
            ),
            "text": record["text"],
            "score": score
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:top_k]
