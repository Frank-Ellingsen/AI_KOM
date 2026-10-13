from __future__ import annotations

import os
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "config.yaml"
PROMPTS_PATH = ROOT_DIR / "config" / "system_prompts.yaml"


def _read_yaml(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def get_settings():
    config = _read_yaml(CONFIG_PATH)
    prompts = _read_yaml(PROMPTS_PATH)

    default_db_path = ROOT_DIR / "data" / "db" / "kommune_rag_store.db"
    settings = {
        "llm_provider": os.getenv("LLM_PROVIDER", config.get("llm", {}).get("provider", "gemini")),
        "gemini_model": os.getenv("GEMINI_MODEL", config.get("llm", {}).get("model", "gemini-3.8-flash")),
        "ollama_model": os.getenv("OLLAMA_MODEL", config.get("ollama", {}).get("model", "llama3.1")),
        "temperature": float(os.getenv("TEMPERATURE", config.get("ollama", {}).get("temperature", 0.1))),
        "db_path": os.getenv("DB_PATH", config.get("paths", {}).get("db", str(default_db_path))),
        "top_k": int(os.getenv("RAG_TOP_K", config.get("rag", {}).get("top_k", 4))),
        "k_constant": int(os.getenv("RAG_K_CONSTANT", config.get("rag", {}).get("k_constant", 60))),
    }

    settings["system_prompt"] = (
        prompts.get("system", {}).get("legal_rag")
        or """Du er en spesialisert juridisk og økonomisk rådgiver for Kristiansand kommune.
Svar kun basert på de oppgitte kildene og siter dem tydelig.
"""
    )
    return settings
