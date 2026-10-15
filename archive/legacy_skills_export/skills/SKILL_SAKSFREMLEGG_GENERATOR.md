# 📝 Agent Skill: Kommunalt Saksfremlegg & Rapportgenerator (`SKILL_SAKSFREMLEGG_GENERATOR`)

> **Versjon:** 1.0  
> **Kategori:** Politiske Saker & Saksbehandling  
> **Standard:** Kommuneloven § 13-1, Offentleglova, Språkrådets klarspråkstandard  

---

## 🎯 Formål
Dette agent-skill-et automatiserer utarbeidelsen av formelle **saksfremlegg til Bystyret, Formannskapet og hovedutvalg**, samt **tertialrapporter** og politiske notater. Saker bygges med 100 % kildeforankring i lover, forskrifter og økonomireglement.

---

## 📋 Standard Mal for Kommunalt Saksfremlegg

### 1. Saksstruktur
1. **Arkivsak-ID / Behandlingsorgan:** (f.eks. *Formannskapet / Bystyret*).
2. **Saksammendrag:** Kort, poengtert oppsummering av bakgrunnen og hvorfor saken fremmes.
3. **Kommunedirektørens Forslag til Vedtak:** Krystallklart, juridisk og økonomisk forpliktende vedtakstekst.
4. **Saksopplysning & Bakgrunn:**
   * Faktisk beskrivelse av situasjonen (f.eks. merforbruk i helse, statlige rammeendringer).
   * Tabell med regnskapstall, tertialprognoser og avvik.
5. **Juridisk & Økonomisk Vurdering:**
   * **Rettslig hjemmel:** Henvisning til Kommuneloven (f.eks. § 14-5 om budsjettbalanse) eller særlover.
   * **Konsekvenser for Økonomiplan / HØP:** Sjekk mot handlefrihet og disposisjonsfond.
6. **Medvirkning & Risiko:**
   * Konsekvenser for barn/unge, folkehelse og klima/miljø.
   * Vurdering av PII/Personvern (GDPR) og etiske retningslinjer.

---

## ⚙️ Eksekveringsregler
* **Klarspråk:** Skriv i aktivt, tilgjengelig og presist norsk (unngå overdreven byråkratisjargon).
* **Forankrede Vedtak:** Forslag til vedtak må spesifisere *eksakt* beløp, kontoklasse (Drift/Investering) og hvilken dekning/finansiering som benyttes (f.eks. *Inndekking skjer ved bruk av disposisjonsfond*).
* **Menneske-i-sløyfen (HITL):** Utkastet merkes alltid med `[UTKAST — MÅ GODKJENNES AV SAKSBEHANDLER/KOMMUNEDIREKTØR]`.
