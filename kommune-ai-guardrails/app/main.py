from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

from kommune_ai_guardrails.config import get_settings
from kommune_ai_guardrails.rag import ask_kommune_ai_ollama


def main() -> int:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    settings = get_settings()
    print(f"Using Ollama model: {settings['ollama_model']}")

    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError:
        print("SentenceTransformers is not installed. Run: pip install -r requirements.txt")
        return 1

    model = SentenceTransformer("intfloat/multilingual-e5-small")
    query = "Hvilke regler gjelder dersom vi må endre budsjettet i løpet av året?"
    answer, chunk_ids, audit_hash = ask_kommune_ai_ollama(query, model, settings["ollama_model"])
    print("\nSvar:\n", answer)
    print(f"\nBrukte chunks: {chunk_ids}")
    print(f"Audit hash: {audit_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
