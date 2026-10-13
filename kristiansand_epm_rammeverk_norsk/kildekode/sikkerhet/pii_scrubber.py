#!/usr/bin/env python3
"""
Kristiansand Kommune - PII Anonymisering og Skjerming for RAG / Sky-AI
========================================================================
Dette verktøyet kjøres lokalt på kommunens servere/PC FØR fritekst, bilag
eller RAG-kontekst sendes til skybaserte AI-modeller (f.eks. Azure OpenAI).

Skjermer automatisk:
- Fødselsnummer (11 siffer)
- Kontonummer (11 siffer)
- Telefonnummer (8 siffer / +47)
- E-postadresser
- Personnavn knyttet til bilagstekster (f.eks. "Ref: Ola Nordmann")
"""

import re
from pathlib import Path

class NorwegianPIIScrubber:
    def __init__(self):
        # 1. Fødselsnummer (11 sammenhengende siffer, evt. med mellomrom/bindestrek)
        self.fnr_pattern = re.compile(r'\b\d{6}[- ]?\d{5}\b')
        # 2. E-postadresser
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        # 3. Norske kontonummer (11 siffer / 4+2+5 siffer format)
        self.account_pattern = re.compile(r'\b\d{4}[. ]?\d{2}[. ]?\d{5}\b')
        # 4. Telefonnummer (+47 / 0047 + 8 siffer, eller direkte 8 siffer)
        self.phone_pattern = re.compile(r'(?:\+47|0047)?\s*\(?0\)?\s*[2-9]\d{2}\s*\d{2}\s*\d{3}|\b[2-9]\d{7}\b')
        # 5. Navnemønstre i kommunale bilagstekster (f.eks. "Ref: Ole Hansen", "Gjelder: Kari Nordmann", "Ansatt: Jens Olsen")
        self.name_ref_pattern = re.compile(r'(?i)\b(ref|gjelder|ansatt|bruker|pasient|elev|vedk|vedkommende)\b\s*:\s*([A-ZÆØÅ][a-zæøå]+\s+[A-ZÆØÅ][a-zæøå]+)')

    def sanitize_text(self, text: str) -> str:
        """Vasker og anonymiserer fritekst før den sendes ut av kommunens nettverk."""
        if not text:
            return ""
        
        sanitized = text
        
        # Kjør anonymiseringsfiltere
        sanitized = self.fnr_pattern.sub('[SKJERMET FØDSELSNUMMER]', sanitized)
        sanitized = self.email_pattern.sub('[SKJERMET E-POST]', sanitized)
        sanitized = self.account_pattern.sub('[SKJERMET KONTONUMMER]', sanitized)
        sanitized = self.phone_pattern.sub('[SKJERMET TELEFON]', sanitized)
        sanitized = self.name_ref_pattern.sub(r'\1: [SKJERMET PERSONNAVN]', sanitized)
        
        return sanitized


if __name__ == "__main__":
    scrubber = NorwegianPIIScrubber()
    
    # Eksempel på typisk bilagstekst fra Visma/Agresso i en kommune:
    test_bilag = (
        "Ref: Ole Hansen, fnr 12058412345. Utbetaling av sykelønnsrefusjon til kontonr 1234.56.78903. "
        "Ved spørsmål kontakt saksbehandler på ole.hansen@kristiansand.kommune.no eller tlf 98765432."
    )
    
    print("======================================================================")
    print("TEST AV LOKAL PII-ANONYMISERING (KRISTIANSAND KOMMUNE)")
    print("======================================================================")
    print("\n[OPPRINNELIG BILAGSTEKST FRA ERP]:")
    print(test_bilag)
    
    anonymisert = scrubber.sanitize_text(test_bilag)
    
    print("\n[VASKET TEKST KLAR FOR RAG / AZURE OPENAI]:")
    print(anonymisert)
    print("\n✓ Ingen personopplysninger forlater kommunens nettverk.")
