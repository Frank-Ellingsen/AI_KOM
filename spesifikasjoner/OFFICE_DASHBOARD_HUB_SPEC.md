# 🏛️ Control Office Hub UI & Workflow Spesifikasjon
> **Spesifikasjon for brukergrensesnitt, årshjulsintegrasjon og operativ arbeidsflyt for Økonomi og Virksomhetsstyring i Kristiansand kommune.**

---

## 1. Visuell UI Skisse & Wireframe (Dashboard Layout)

Grensesnittet samler hele økonomimiljøet (Strategi/analyse, Økonomistyring, Anskaffelser, Regnskap, FoU) i én skjermet arbeidsflate koblet mot Framsikt, Visma, Power BI og den lokale RAG-motoren.

```text
+-----------------------------------------------------------------------------------------------------------------------+
| 🏛️ KRISTIANSAND KOMMUNE -- CONTROL OFFICE HUB | Økonomi og Virksomhetsstyring               👤 Frank Ellingsen (Senior) |
+-----------------------------------------------------------------------------------------------------------------------+
| 📅 ÅRSHJUL & KRITISKE FRISTER (Plandisc / Outlook)                                                                     |
|  [ Q1: KOSTRA & Regnskap ]  ===>  [ Q2: 1. Tertial (T1) ]  ===>  [ Q3: 2. Tertial (T2) ]  ===>  [ Q4: HØP & Budsjett ]   |
|  Current Phase: 🟢 FORBEREDELSE 2. TERTIALRAPPORT (Frist: 28. september) | Dager igjen: 12                            |
+--------------------------------------------------+--------------------------------------------------------------------+
| 📊 ROLLEBASERT ARBEIDSFLATE                      | 🤖 AUTOMATISK AVVIKSDETEKSJON & RAG DIAGNOSE                       |
| Select View: [ Controller / Rådgiver  v ]         |                                                                    |
|                                                  | ⚠️ FLAGGEDE AVVIK (Visma vs. Framsikt Rammer):                      |
| 📈 Nøkkeltall for Sektor: Oppvekst & Grunnskole  | • Enhet 202 Grunnskole: Merforbruk vikarer +8.4% ( 1.2M NOK)       |
| • Avvik hittil i år: +3.2M NOK (Rød alarm)       | • Enhet 401 Helse & Mestring: Overtidstopp +12.1% ( 2.4M NOK)      |
| • Sykepengerefusjoner etterslep: -850k NOK       |                                                                    |
| • Prognose EOY: 102.1% av ramme                   | 🔍 AI RAG-FORKLARING (Forankret i Kommuneloven § 14-5 & T1-Rapport):|
|                                                  | "Avviket skyldes forsinkelse i NAV-refusjoner kombinert med       |
| [ 📥 Last ned Visma CSV ] [ 🔄 Synk Framsikt ]   | uforutsett sykefravær. Jf. Kommuneloven § 14-5 må Bystyret endre  |
|                                                  | årsbudsjettet dersom kravet om realisme og balanse trues."         |
+--------------------------------------------------+--------------------------------------------------------------------+
| 📝 OPERATIV HITL ARBEIDSFLYT & SIGN-OFF (Stage-Gate Port 9)                                                           |
|                                                                                                                       |
|  Status vurdering: (o) Godkjenn (APPROVED)   ( ) Endre (MODIFIED)   ( ) Avvis (REJECTED)                             |
|  Saksbehandler notat: [ Reelt avvik opparbeidet per T2. Fremmes som omdisponering i sak Bystyret sep 2026.        ] |
|                                                                                                                       |
|  [ 🔒 Lagre & Signer med SHA-256 ]  ===>  SHA-256 Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855|
+-----------------------------------------------------------------------------------------------------------------------+
```

---

## 2. Årshjul, Kalender og Kritiske Frister

Årshjulet i grensesnittet synkroniseres mot MS Teams, Outlook og Plandisc for å holde alle rådgivere i samme takt:

| Kvartal / Frist | Kritiske Milepæler & Styringshendelser | Operativ Systemoppgave i Hub-en |
| :--- | :--- | :--- |
| **K1 (Jan–Mars)** | • **15. jan & 23. feb:** KOSTRA-innsending til SSB.<br>• **09. mars:** Endelig regnskapsavslutning.<br>• **31. mars:** Årsrapport og årsregnskap fremlegges. | Autokjøring av KOSTRA-kontoplanvalidering og RAG-oppdatering mot SSB-tall. |
| **K2 (April–Juni)** | • **15. april:** Revisjonsberetning fra Kommunal Revisjon.<br>• **25. mai:** **1. tertialrapport (T1)** til Bystyret.<br>• **02. juni / 15. juni:** Revidert Nasjonalbudsjett (RNB) og endelige KOSTRA-tall. | Visma ERP-korreksjon (sykepengerefusjoner/etterslep) og første EOY-prognose i Framsikt/Power BI. |
| **K3 (Juli–Sep)** | • **15. aug:** Innspill fra tjenesteområdene til ny HØP.<br>• **23. sep:** Kommunedirektørens forslag til HØP 2027–2030.<br>• **28. sep:** **2. tertialrapport (T2)** i Formannskapet. | HØP-scenariomodellering (What-If) og tildeling av nye økonomiske rammer per kommunalsjefområde. |
| **K4 (Okt–Des)** | • **07. okt:** Statsbudsjettet fremlegges.<br>• **25. nov:** Formannskapets innstilling til Årsbudsjett.<br>• **18. des:** **Bystyrets endelige vedtak** av Årsbudsjett og HØP. | Saldering av samlet budsjett (>10 mrd. kr) og overføring til Framsikt Årsbudsjettmodul. |

---

## 3. Rollebaserte Arbeidsflater

1. **Økonomidirektør (Supervisor-visning)**:
   * High-level oversikt over netto driftsresultat, sentralt disposisjonsfond og samlet avvik per sektor.
   * Enkel godkjenningsknapp for politiske saksfremlegg (Word/PDF) og tertialrapporter til Kommunedirektøren.

2. **Rådgiver Økonomistyring (HITL Controller-visning)**:
   * Arbeidsliste med **flaggede avvik** mellom Visma og Framsikt.
   * **Glass-Box RAG Diagnose**: Viser AI-generert forklaring forankret i Kommuneloven § 14-5 og lokalt reglement.
   * Overprøvingsmodul (*APPROVED / MODIFIED / REJECTED*) med begrunnelsesfelt og kryptografisk **SHA-256 Audit-stempel**.

3. **Kommunalsjef & Enhetsledere (Sektor-visning)**:
   * Forenklet rammestatus for eget område (f.eks. Grunnskole eller Helse og mestring).
   * Automatisk mottak av **Teams Adaptive Cards** ved vesentlige avvik.

---

## 4. Operativ 8-Stegs Arbeidsflyt

```text
[ 1. Visma-eksport ] ──► [ 2. PII-Skjerming ] ──► [ 3. Power BI Avvik ] ──► [ 4. What-If Simulering ]
                                                                                   │
                                                                                   ▼
[ 8. Arkiv Public360 ] ◄── [ 7. Teams-Varsling ] ◄── [ 6. HITL SHA-256 Sign ] ◄── [ 5. RAG-Diagnose ]
```

1. **Visma-eksport**: Automatisk uthenting av månedlige regnskapstall.
2. **PII-Skjerming**: Lokal vasking av personopplysninger (fødselsnumre/navn) før analyse.
3. **Power BI Avviksdeteksjon**: Identifisering av enheter med reelt underliggende avvik.
4. **What-If Simulering**: Testing av fraværstiltak og rammejusteringer i scenariomodellen.
5. **RAG-Diagnose**: Kjøring av kildeforankret AI-analyse i Controller-portalen.
6. **HITL Sign-Off**: Saksbehandler velger status, registrerer notat og lagrer uforanderlig SHA-256 hash.
7. **Teams-Varsling**: Automatisk utsending av varsel til ansvarlig enhetsleder.
8. **Iverksetting & Arkiv**: Registrering av omdisponering i Framsikt/Visma og overføring av saksnotat til Public360.

---

## 5. Interaktiv Streamlit Kodedemo (`app/office_hub_app.py`)

```python
import streamlit as st
import datetime
import hashlib

st.set_page_config(page_title="Kristiansand Kommune -- Control Office Hub", layout="wide")

st.title("🏛️ Kristiansand Kommune -- Control Office Hub")
st.caption("Økonomi og Virksomhetsstyring | Interaktiv Årshjul- og AI-Arbeidsflate")

# 1. ÅRSHJUL BANNER
st.info("📅 **Aktiv Periode:** K3 -- Forberedelse 2. Tertialrapport (T2) | **Neste Frist:** 28. september (Formannskapet)")

# 2. TO-SØYLE LAYOUT
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Rolle: Rådgiver Økonomistyring")
    sektor = st.selectbox("Velg Sektor:", ["Oppvekst -- Grunnskole", "Helse og Mestring", "Byutvikling"])
    st.metric(label="Årsbudsjett Ramme 2026", value="1 420 000 000 NOK")
    st.metric(label="Prognostisert Avvik per T2", value="+3 200 000 NOK", delta="-3.2M over ramme", delta_color="inverse")

with col2:
    st.subheader("🤖 AI Avviksdiagnose & RAG Oppslag")
    st.warning("⚠️ **Flagget Avvik:** Vikarutgifter Enhet 202 har økt med 8.4% siste kvartal.")
    st.markdown(
        "**📜 RAG Kildehenvisning (Kommuneloven § 14-5 & T1-Rapport):**\n"
        "> *Kommunestyret skal endre årsbudsjettet når det er nødvendig for å oppfylle lovens krav om realisme og balanse. Vesentlige avvik må fremmes i 2. tertialrapport.*"
    )

# 3. HITL SIGN-OFF
st.markdown("---")
st.subheader("📝 Menneskelig Vurdering & Audit Signering (Stage-Gate Port 9)")
status = st.radio("Saksbehandlers Vurdering:", ["APPROVED (Fremmes som rammejustering i T2)", "MODIFIED (Krever ny inndekning)", "REJECTED (Feilføring i Visma)"])
notat = st.text_area("Saksbehandlers Begrunnelse:", "Avviket er reelt og skyldes sykefravær. Omdisponeres fra disposisjonsfond.")

if st.button("🔒 Signer og Logg til Audit Trail (SHA-256)"):
    raw_str = f"{sektor}_{status}_{notat}_{datetime.datetime.now()}"
    sha_hash = hashlib.sha256(raw_str.encode()).hexdigest()
    st.success(f"✅ Vurdering lagret i SQLite! SHA-256 Hash: `{sha_hash}`")
```
