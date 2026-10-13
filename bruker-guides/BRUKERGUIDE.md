# 📖 BRUKERGUIDE & SOP (Standard Operating Procedure)

## Kristiansand Kommune — AI & RAG Regelverksassistent

---

## 📋 Innholdsfortegnelse
1. [Innledning & Formål](#1-innledning--formål)
2. [Slik Åpner Du Assistenten (Startknapp)](#2-slik-åpner-du-assistenten-startknapp)
3. [Oversikt over Brukergrensesnittet (Control Office Hub)](#3-oversikt-over-brukergrensesnittet-control-office-hub)
4. [Steg-for-Steg Brukerveiledning](#4-steg-for-steg-brukerveiledning)
   - [A. Oppslag i Regelverk og Lover](#a-oppslag-i-regelverk-og-lover)
   - [B. Avviksdeteksjon (Visma vs. Framsikt)](#b-avviksdeteksjon-visma-vs-framsikt)
   - [C. Utarbeidelse av Tertialrapport & Saksfremlegg](#c-utarbeidelse-av-tertialrapport--saksfremlegg)
5. [Menneskelig Overprøving (Human-in-the-Loop & Audit Stempel)](#5-menneskelig-overprøving-human-in-the-loop--audit-stempel)
6. [Retningslinjer for God Prompting & Spørringer](#6-retningslinjer-for-god-prompting--spørringer)
7. [Datasikkerhet, Personvern & Etikk](#7-datasikkerhet-personvern--etikk)
8. [Feilsøking og Brukerstøtte](#8-feilsøking-og-brukerstøtte)

---

## 1. Innledning & Formål

Denne brukerveilederen beskriver den operative hverdagen for ansatte ved **Økonomi og Virksomhetsstyring i Kristiansand kommune**.

AI-assistenten er utformet for å forenkle og kvalitetssikre arbeidshverdagen innen:
- **Tolkning av regelverk:** Raske og kildeforankrede oppslag i Kommuneloven, KOSTRA-veilederen, Selvkostforskriften og lokalt Økonomireglement.
- **Budsjettoppfølging:** Automatisk sammenstilling av faktiske regnskapstall fra Visma ERP og budsjettrammer fra Framsikt EPM.
- **Saksforberedelse:** Automatisk generering av utkast til tertialrapporter, omdisponeringssaker og politiske saksfremlegg til Formannskapet og Bystyret.

> ⚠️ **VIKTIG PRINSIPP:** AI-systemet fatter **0 autonome vedtak**. Systemet gir rådgivende forslag der du som saksbehandler/rådgiver alltid har det fulle faglige og juridiske ansvaret for endelig beslutning (*Human-in-the-Loop*).

---

## 2. Slik Åpner Du Assistenten (Startknapp)

Du kan åpne AI-assistenten på tre enkle måter:

### Måte 1: Startknapp på Intranett / Teams
1. Gå til kommunens internportal (*Aktiv Kommune* / *MS Teams* / *Framsikt*).
2. Klikk på knappen **«🚀 Åpne AI Regelverksassistent»**.
3. Nettleseren åpner automatisk dashbordet.

### Måte 2: Skrivebordssnarvei på PC-en
1. Dobbelklikk på **[`start_kommune_ai.bat`](file:///C:/Users/frank/Desktop/AI_KOM/start_kommune_ai.bat)** (eller skrivebordsikonet).
2. Motoren starter lokalt i bakgrunnen, og nettleseren åpner automatisk `http://localhost:8501`.

### Måte 3: Direkte Webadresse (Sentral Server)
1. Åpne din vanlige nettleser (Edge / Chrome).
2. Skriv inn den interne serveradressen oppgitt fra IKT Agder (f.eks. `http://[internt-servernavn]:8501`).

---

## 3. Oversikt over Brukergrensesnittet (Control Office Hub)

Skjermbildet er delt inn i fire oversiktlige soner:

1. **📅 Årshjul & Fristindikator (Topplinje):** Viser hvor i det kommunale styringsåret vi befinner oss (K1–K4), med nedtelling til neste kritiske frist (f.eks. *2. tertialrapport til Formannskapet*).
2. **📊 Sektor- & Rollevelger (Venstremeny):** Velg din rolle (*Økonomidirektør*, *Controller/Rådgiver*, *Enhetsleder*) for å få tilpasset visning.
3. **🤖 AI RAG-Søk & Avviksmonitor (Hovedvindu):** 
   - Søkefelt for fritekstspørringer i lover og forskrifter.
   - Liste over flaggede avvik mellom Visma-transaksjoner og Framsikt-rammer.
   - AI-genererte forklaringer med eksplisitte paragrafhenvisninger (§).
4. **📝 HITL Saksbehandlingsfelt & SHA-256 Stempel (Bunnlinje):** Sone for godkjenning, registrering av notat og kryptografisk signering for Kommunerevisjonen.

---

## 4. Steg-for-Steg Brukerveiledning

### A. Oppslag i Regelverk og Lover
1. Klikk i søkefeltet **«💬 Hva lurer du på i regelverket?»**.
2. Skriv spørsmålet ditt (f.eks.: *"Hvilke regler gjelder for endring av årsbudsjettet i løpet av året?"*).
3. Trykk **«🔍 Søk og Generer Svar»**.
4. **Les svaret:** AI-en viser et kort sammendrag med direkte henvisning til § (f.eks. *Kommuneloven § 14-5* og *Økonomireglementet § 3-1*).
5. **Verifiser kilden:** Utvid feltet *«Se benyttede kilde-chunks»* dersom du vil lese den eksakte lovteksten som ligger til grunn.

### B. Avviksdeteksjon (Visma vs. Framsikt)
1. Velg din sektorenhet i menyen (f.eks. *Oppvekst / 202 Grunnskole*).
2. Trykk på knappen **«📊 Analyser Avvik mot Framsikt»**.
3. Systemet sammenligner påløpte bilag fra Visma mot periodisert budsjett.
4. Dersom avviket overstiger 5 % eller 250 000 kr, flagges dette med rød alarm, og AI-en gir en innledende årsaksanalyse (f.eks. *etterslep på NAV-refusjoner eller uforutsett vikarforbruk*).

### C. Utarbeidelse av Tertialrapport & Saksfremlegg
1. Velg fanen **«📝 Generer Saksutkast»**.
2. Klikk **«Bygg utkast til Tertialrapport»**.
3. AI-en utarbeider et strukturert saksfremlegg til Bystyret/Formannskapet med:
   - Innledning og bakgrunn.
   - Økonomisk status og avviksforklaring.
   - Konsekvenser for drift og investering.
   - Forslag til vedtak jf. Kommuneloven § 14-5.

---

## 5. Menneskelig Overprøving (Human-in-the-Loop & Audit Stempel)

Når du har gått gjennom AI-svaret eller saksutkastet, må du utføre **HITL Sign-Off**:

1. **Velg Status:**
   - 🟢 **APPROVED (Godkjent):** Du er enig i vurderingen og kildebruken.
   - 🟡 **MODIFIED (Endret):** Du har justert teksten eller tallene manuelt.
   - 🔴 **REJECTED (Avvist):** Vurderingen er feilaktig eller urelevant.
2. **Skriv saksbehandlingsnotat:** Legg inn en kort faglig begrunnelse i notatfeltet.
3. **Klikk «🔒 Lagre & Signer med SHA-256»:**
   - Systemet genererer en uforanderlig kryptografisk hash.
   - Handlingen logges direkte i databasen for **Kommunerevisjonen** og Kontrollutvalget.

---

## 6. Retningslinjer for God Prompting & Spørringer

For å få best mulig resultat fra AI-assistenten:

| Do's (Gjør dette) | Don'ts (Unngå dette) |
| :--- | :--- |
| ✅ Vær spesifikk på fagområde (*"Hva gjelder for selvkost innen feiing?"*). | ❌ Ikke still for generelle spørsmål (*"Hva er reglene?"*). |
| ✅ Referer til konkrete tidsrom eller enheter (*"T1 2026 for Grunnskole"*). | ❌ Ikke lim inn ubehandlede lister med personopplysninger. |
| ✅ Be om §-henvisning dersom du trenger det til et politisk saksfremlegg. | ❌ Ikke stol blint på tall uten å sjekke Visma/Framsikt motrapporten. |

---

## 7. Datasikkerhet, Personvern & Etikk

- **Ingen PII-lekkasje:** Systemet vasker automatisk bort fødselsnumre, navn og e-postadresser. Du skal likevel tilstede best mulig praksis og unngå å lime inn sensitive personopplysninger i fritekstfeltet.
- **Skjermet drift:** Systemet kjører 100 % lokalt innenfor kommunens sikkerhetssone. Ingen data forlater rådhuset.
- **Innsyn & Transparens:** Alle spørringer er registrert i henhold til EU AI Act og kan gjenfinnes i kommunens offentlige Algoritmeregister.

---

## 8. Feilsøking og Brukerstøtte

* **Problem: Nettsiden laster ikke eller viser "Connection Refused".**
  * *Løsning:* Sjekk at den lokale startknappen har startet Ollama og Streamlit. Dobbelklikk på `start_app.bat` på nytt.
* **Problem: AI-en svarer "Finner ikke relevant informasjon i kildene".**
  * *Løsning:* Omformuler spørsmålet med mer presise fagbegreper (f.eks. bruk *"kontoklasse 1"* i stedet for *"drift"*).
* **Brukerstøtte:**
  * **IT-Brukerstøtte (IKT Agder):** Tlf: 38 00 00 00
  * **Fagstøtte Økonomi:** Kontakt Seniorrådgiver Frank Ellingsen / Økonomistyring.
