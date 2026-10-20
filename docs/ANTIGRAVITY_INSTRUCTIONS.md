# 🤖 Prompting- og Utviklingsguide for Antigravity AI Agent

Dette dokumentet gir instruksjoner til **Antigravity AI Agent** for videreutvikling og refakturering av kildekoden.

---

## 1. Kjerneprinsipper for Kildekoden
* **Pydantic v2 Prinsipper:** Alle verktøyinput må være strengt typet via Pydantic-modeller i `app/schemas/` (eller `app/schemas.py`).
* **Sikker SQL Parameterisering:** Bruk aldri rå string-formatering i SQL-spørringer. Alle verdier må sendes som bundne parametere (`?` eller `%s`).
* **Sikkerhet & RBAC:** Sørg for at `UserContext` alltid overvåker tilgangsgrensene før SQL kjøres.

---

## 2. Arbeidsflyt for Refakturering
1. **Oppdater Pydantic-modeller:** Legg til eventuelle nye felt i `app/schemas/advisor.py` (eksportert i `app/schemas/__init__.py`).
2. **Implementer Verktøy:** Utvid funksjonene i `app/tools.py`.
3. **Koble til Agenten:** Registrer det nye verktøyet i `app/agent.py`.
4. **Oppdater Dashboardet:** Legg til visningselementet i `app/frontend.py`.
5. **Kjør Testsettet:** Verifiser at uforanderlig audit-logging fungerer.
