# 🏛️ Kristiansand Kommune — Framsikt EPM & Budsjett Dokumentasjonspakke

> **Kanonisk dokumentasjonspakke for kommunal økonomistyring, stillingsbudsjett, KOSTRA-kontoplan og selvkost i Framsikt.**  
> Tilpasset for **Frank Ellingsen** (Senior Financial Controller) og integrert i [`index.html`](../index.html).

---

## 🧭 Kanoniske Dokumenter (Optimalisert for LLM & Vektorsøk)

| Dokument | Hovedinnhold | Lovhjemmel & Standarder | Filsti |
| :--- | :--- | :--- | :--- |
| **Budsjettering & Årshjul** | Måltall (11,48 mrd, $\ge 1,0\%$ driftsres, $\ge 4,0\%$ fond, $<8,8$ mrd lån), 6 områder, 8-faset internt årshjul fra mai til des. | Kommuneloven kap. 14, Bystyrets reglement | [`budsjettering-kristiansand-kommune.md`](./budsjettering-kristiansand-kommune.md) |
| **Stillings- & Lønnsbudsjett** | Fastlønn (1010) vs variable potter (1020/1050/1090), feriepenger (12%/14,3%), SPK vs KLP, AGA Sone 1 (14,1%), Excel import/eksport. | Kommuneloven § 14-6, HTA § 4, KRS 6 | [`lonnsbudsjettering-kristiansand-framsikt.md`](./lonnsbudsjettering-kristiansand-framsikt.md) |
| **Driftsarter & Selvkost** | Varekjøp (1100–1270), overføringer (1300–1480), finans/fond (1500–1930), selvkostkalkyler for VAR & Byggesak med 5-årsregel. | Kommuneloven § 15-1, Selvkostforskriften | [`driftsarter-og-selvkost-alle-omrader-framsikt.md`](./driftsarter-og-selvkost-alle-omrader-framsikt.md) |
| **KOSTRA Konteringsregler** | Lønnsarter, sosiale kostnader og refusjoner (1690). Krav om bruttoføring og forbud mot netting. Sjekkliste før budsjettlåsing. | KOSTRA-forskriften, Budsjettforskrift § 14-6 | [`kostra-artskontoer-konteringsregler-framsikt.md`](./kostra-artskontoer-konteringsregler-framsikt.md) |

---

## ⚡ Interaktiv Implementering i Huben
Alle 4 dokumenter er direkte implementert som kjørbare motorer i [`index.html`](../index.html) under **Kommunal Budsjettmodul** (`#budsjett-modul-seksjon`):
1. **Lønnskalkulator**: Beregner bruttolønn, feriepenger, KLP/SPK og AGA (14,1%) med live KOSTRA-konteringssplitt.
2. **Selvkostkalkulator**: Full selvkostkalkyle for Vann, Avløp, Renovasjon og Byggesak med 5-årsfondregulering.
3. **Budsjett-Årshjul**: 8 interaktive faser med oppgavepakker, roller og frister.
4. **KOSTRA-tabell**: Søkbar og filtrerbar oversikt over alle kommunale arter.
5. **QA-Motor**: 8-punkts sjekkliste med SHA-256 kryptografisk forsegling.
