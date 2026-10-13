# 📖 Brukerveiledning og SOP (Standard Operating Procedure)

> **Brukerveiledning for saksbehandlere, økonomirådgivere, ledergruppe og revisorer som benytter Kommune AI Guardrails.**

---

## 👥 Målgrupper og Roller

1. **Saksbehandlere og Økonomirådgivere:** Stiller spørsmål til regelverk, kontoplaner og tertialrapporter for å få rask beslutningsstøtte.
2. **Kommunalsjefer og Ledelse:** Mottar AI-genererte avviksanalyser og saksutredninger med kildehenvisninger.
3. **Kommunerevisjonen og Kontrollutvalget:** Innsyn i historiske spørringer, kilde-chunks og SHA-256 verifisering i Audit-portalen.

---

## 💡 Hvordan Stille Gode Spørsmål (Prompting Best Practice)

For å få maksimal nytte av den lokale RAG-motoren bør du følge tre enkle prinsipper:

### 1. Vær konkret på tema og kontekst
* ❌ *Dårlig:* "Hva gjør vi med penger som er til overs?"
* ✅ *God:* "Hvilke regler gjelder for overføring av unyttede midler i investeringsregnskapet ved årsavslutning?"

### 2. Nachspør paragrafhjemler
* ❌ *Dårlig:* "Kan vi endre budsjettet?"
* ✅ *God:* "Hvilke krav stiller Kommuneloven § 14-5 til at Bystyret må vedta budsjettendringer ved vesentlige avvik?"

### 3. Bruk faguttrykk når det er naturlig
* ❌ *Dårlig:* "Hvor skal vi føre støtte til idrettslaget?"
* ✅ *God:* "Hvilken KOSTRA-funksjon og art skal benyttes for tilskudd til private idrettsanlegg?"

---

## 🖥️ Bruk av Streamlit Web-UI Trinn for Trinn

1. **Åpne Portalen:** Naviger til `http://localhost:8501` i nettleseren din.
2. **Velg Modell i Sidemenyen:** Velg foretrukken lokal modell (f.eks. `llama3.1` for generelle juridiske spørsmål eller `qwen2.5` for komplekse analyser).
3. **Skriv Spørsmålet:** Skriv inn spørsmålet ditt i tekstfeltet på hovedsiden.
4. **Les Svaret:** AI-svaret vises under "📋 Svar fra AI-assistenten". Sjekk paragrafhenvisningene (f.eks. *Jfr. Kommuneloven § 14-5*).
5. **Inspect Kilde-Chunks & Audit Trail:** Ekspander feltet "🔍 Se fullstendig Audit Trail Stempel" for å se hvilke kilder som ble hentet og hvilken SHA-256 hash som ble generert.

---

## 🛡️ Retningslinjer for Menneskelig Overprøving (Human-in-the-Loop)

* ⚠️ **AI gir aldri autonom godkjenning:** Svaret fra systemet er et **utkast og beslutningsstøtte**, ikke et juridisk bindende enkeltvedtak.
* 📌 **Saksbehandlers ansvar:** Saksbehandler plikter å kontrollere at de siterte paragrafene faktisk stemmer før teksten lims inn i et formelt saksfremlegg.
* 🚫 **Rapportering av avvik:** Dersom AI-en gir et utilstrekkelig svar eller ikke finner kilden, meldes dette inn via avviksknappen i portalen slik at regelverksdatabasen kan oppdateres.
