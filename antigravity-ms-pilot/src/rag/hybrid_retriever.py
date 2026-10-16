"""
Hybrid Search (Lexical + Semantic) with Table-Aware Chunking
Kristiansand Kommune — AI Guardrails & M365 Copilot Pilot
"""

import re
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Chunk:
    id: str
    content: str
    source: str
    title: str = ""
    section_ref: str = ""
    is_table: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class TableAwareChunker:
    """
    Deler dokumenter i semantiske biter uten å ødelegge markdown-tabeller.
    Tabeller holdes samlet i ett chunk for å bevare rader og kolonner.
    """

    def __init__(self, max_chunk_chars: int = 1200, overlap_chars: int = 150):
        self.max_chunk_chars = max_chunk_chars
        self.overlap_chars = overlap_chars

    def chunk_document(self, text: str, source: str, default_title: str = "") -> List[Chunk]:
        chunks: List[Chunk] = []
        lines = text.splitlines()
        
        current_chunk_lines: List[str] = []
        current_chars = 0
        in_table = False
        table_lines: List[str] = []
        chunk_counter = 0

        current_heading = default_title

        for line in lines:
            stripped = line.strip()

            # Oppdag overskrifter for kontekst
            if stripped.startswith("#"):
                current_heading = stripped.lstrip("#").strip()

            # Oppdag markdown-tabellinjers start/slutt
            is_table_line = stripped.startswith("|") and stripped.endswith("|")

            if is_table_line:
                if not in_table:
                    # Flush vanlig tekst før tabellen
                    if current_chunk_lines:
                        chunk_text = "\n".join(current_chunk_lines).strip()
                        if chunk_text:
                            chunk_counter += 1
                            chunks.append(Chunk(
                                id=f"{source}_chunk_{chunk_counter}",
                                content=chunk_text,
                                source=source,
                                title=current_heading,
                                is_table=False
                            ))
                        current_chunk_lines = []
                        current_chars = 0
                    in_table = True
                table_lines.append(line)
            else:
                if in_table:
                    # Tabellen er ferdig
                    in_table = False
                    table_text = "\n".join(table_lines).strip()
                    if table_text:
                        chunk_counter += 1
                        chunks.append(Chunk(
                            id=f"{source}_chunk_{chunk_counter}_table",
                            content=table_text,
                            source=source,
                            title=current_heading,
                            is_table=True
                        ))
                    table_lines = []

                current_chunk_lines.append(line)
                current_chars += len(line) + 1

                if current_chars >= self.max_chunk_chars:
                    chunk_text = "\n".join(current_chunk_lines).strip()
                    if chunk_text:
                        chunk_counter += 1
                        chunks.append(Chunk(
                            id=f"{source}_chunk_{chunk_counter}",
                            content=chunk_text,
                            source=source,
                            title=current_heading,
                            is_table=False
                        ))
                    # Ta med overlap
                    current_chunk_lines = current_chunk_lines[-2:] if len(current_chunk_lines) > 2 else []
                    current_chars = sum(len(l) + 1 for l in current_chunk_lines)

        # Flush eventuell gjenstående tabell
        if table_lines:
            chunk_counter += 1
            chunks.append(Chunk(
                id=f"{source}_chunk_{chunk_counter}_table",
                content="\n".join(table_lines).strip(),
                source=source,
                title=current_heading,
                is_table=True
            ))

        # Flush eventuell gjenstående tekst
        if current_chunk_lines:
            chunk_text = "\n".join(current_chunk_lines).strip()
            if chunk_text:
                chunk_counter += 1
                chunks.append(Chunk(
                    id=f"{source}_chunk_{chunk_counter}",
                    content=chunk_text,
                    source=source,
                    title=current_heading,
                    is_table=False
                ))

        return chunks


class HybridRetriever:
    """
    Hybrid Retriever som kombinerer leksikalsk BM25-lignende matching og paragrafgjenkjenning.
    """

    def __init__(self):
        self.chunks: List[Chunk] = []

    def add_chunks(self, chunks: List[Chunk]) -> None:
        self.chunks.extend(chunks)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.chunks or not query:
            return []

        q_lower = query.lower()
        terms = re.findall(r"\w+", q_lower)
        if not terms:
            return []

        scored_results = []
        for c in self.chunks:
            c_text_lower = c.content.lower()
            c_title_lower = c.title.lower()

            # Leksikalsk poengsum basert på termfrekvens
            score = 0.0
            for term in terms:
                count_in_text = c_text_lower.count(term)
                count_in_title = c_title_lower.count(term)
                score += (count_in_text * 1.0) + (count_in_title * 3.0)

            # Ekstra boost for eksakt paragraf- eller kilde-match
            if "§" in query and "§" in c.content:
                # Sjekk om samme paragrafnummer finnes
                query_paras = re.findall(r"§\s*(\d+(?:-\d+)?)", query)
                for p in query_paras:
                    if f"§ {p}" in c.content or f"§{p}" in c.content:
                        score += 15.0

            if score > 0:
                scored_results.append({
                    "chunk": c,
                    "score": round(score, 3)
                })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]
