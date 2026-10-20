# 📐 Systemarkitektur & Multi-Agent Veikart

## 1. Hybrid RAG + SQL Arkitektur

AI_KOM kombinerer to primære datastrier for å gi 100 % presise svar:
- **Strukturert ERP-transaksjonsdata**: Parameteriserte SQL-spørringer mot stg_erp_transactions med 6-nivås budsjetthierarki.
- **Ustrukturert Kunnskapsbase**: Grounded RAG-vektorsøk i tertialrapporter, økonomireglement og KOSTRA-veiledere.

---

## 2. 6-Nivås Budsjetthierarki

Sektor (1) -> Kommunalsjefområde (2) -> Enhet/Ansvar (3) -> KOSTRA-Funksjon (4) -> KOSTRA-Art (5) -> Bilag (6)

---

## 3. 🔄 Loop Engineering & Controlled Re-Act Patterns

I komplekst kommunalt økonomiarbeid er kontrollerte sløyfer avgjørende for å unngå uendelige kjøringer, token-spill og feilberegninger.

### Kjernekonsepter i Loop Engineering:

1. **Bounded Loops (Rekursjonsgrenser)**:
   - Hard grense på maksimalt 5 iterasjoner i agentløkka (max_iterations = 5 i agent.py).
   - Forhindrer at agenten låser seg i uendelige re-act feller ved uventede SQL-feil.

2. **Self-Correction & Reflection Loops (Selvkorrigering)**:
   - Fanger opp unntak som OperationalError eller ValidationError.
   - Feilmeldingen mates tilbake til LLM-konteksten i neste iterasjon for umiddelbar selvreparasjon før brukeren ser feilen.

3. **Human-in-the-Loop (HITL) Intercepts**:
   - Betingede forgreininger fryser agentens tilstand ved sensitive handlinger (process_budget_reallocation).
   - Omdisponeringer som krever Bystyregodkjenning stoppes og avventer eksplisitt godkjenning/avvisning fra saksbehandler.

4. **State Checkpointing & Audittrail**:
   - Tilstanden lagres etter hver sløyfe-itrasjon.
   - Hvert steg skrives uforanderlig til audit_log for kontroll fra Agder Kontrollutvalg og Kommunerevisjonen (NKRF).

---

## 4. Multi-Agent Veikart (LangGraph Subgraphs)

Neste evolusjonstrinn fra nåværende MVP er overgang til et LangGraph Multi-Agent System:
- **Supervisor Agent**: Ruter henvendelser til spesialiserte undergrafer.
- **Regnskapsagent**: Håndterer MVA, bilagsrevisjon og ERP-oppslag.
- **Budsjett- & EOY-agent**: Kjører Framsikt-prognoser og overtidstrender.
- **Saksbehandlings- & Jusagent**: Utarbeider saksframlegg jf. kommuneloven § 14-5.
- **Reviewer Agent (HITL)**: Kvalitetssjekker svar før endelig publisering.
