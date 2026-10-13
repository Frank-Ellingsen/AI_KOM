# Spesifikasjon for RAG-Kunnskapsbase (Retrieval-Augmented Generation)

For å sikre at AI-modellen gir 100 % forankrede, lovlige og presise råd i preskriptive analyser, benyttes en dedikert **RAG-kunnskapsbase**.

## 📂 Mappestruktur i `rag_kunnskapsbase/`

### 1. `rag_kunnskapsbase/kostra_veiledere/`
* **Innhold:**
  * `Veileder_til_kontoplanen_i_KOSTRA_2026.pdf`
  * `SSB_KOSTRA_Funksjons_og_Artsdefinisjoner.pdf`
* **Formål:** Sikrer at AI-modellen forstår forskjellen på art 1020 (sykemeldte vikarer) og art 1090 (overtid/helgetillegg), samt føringsregler for art 1690 (NAV-refusjoner) med etterslep under ERP-migrering.

### 2. `rag_kunnskapsbase/kommunale_reglementer/`
* **Innhold:**
  * `Okonomireglement_Kristiansand_Kommune.pdf`
  * `Delegeringsreglement_Kristiansand_Kommune.pdf`
  * `1_Tertialrapport_2026_Kristiansand.pdf`
  * `Handlings_og_okonomiplan_2027_2030.pdf`
* **Formål:** Gir AI-modellen direkte kendskap til kommunens lokale vesentlighetsgrenser (f.eks. 5 % avviksgrense), Bystyrets gjeldstak (8,8 mrd. kr), handlingsregelen for korrigert netto driftsresultat (1,0 %), og administrative omdisponeringsfullmakter.

### 3. `rag_kunnskapsbase/lovverk_og_etikk/`
* **Innhold:**
  * `Kommuneloven_Kap13_Kap14.pdf`
  * `EU_AI_Act_Art27_FRIA_Guide.pdf`
  * `GDPR_Art35_DPIA_Krav.pdf`
  * `Hovedavtalen_Paragraf_4_Medbestemmelse.pdf`
* **Formål:** Tvinger AI-modellen til å henvise til konkrete lovhjemler (f.eks. Kommuneloven § 14-5 for budsjettendringer) og kontrollere at tiltak er innenfor delegert administrative myndighet.
