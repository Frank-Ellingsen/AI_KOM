# Framsikt Integration Specification — Kristiansand Kommune EPM

## 1. Oversikt og Arkitektur
Framsikt utgjør det sentraliserte virksomhetsstyrings- og planleggingssystemet i Kristiansand kommune. systemet fungerer som **Master Data Source** for:
1. **Vedtatt Budsjett** (Opprinnelige rammene vedtatt av Bystyret jf. Kommuneloven § 14-3).
2. **Budsjettendringer** (Løpende politiske vedtak, tertialvise rammejusteringer, omdisponeringer og tilleggsløyvinger).
3. **Nøkkeltall og Parametre** (Demografi, elevtall, utgiftsbehov jf. Grønt hefte, dekningsgrader for helse og omsorg).
4. **Statistikk og Deflator** (Kommunal deflator, lønnsvekst inkl. pensjon, og prisvekst-indekser jf. RNB/SSB).

---

## 2. Datamodell & Dataflyt (Framsikt API -> Fabric Lakehouse / SQLite)

```
[ FRAMSIKT REST API ]
  │
  ├──► VedtattBudsjett (Sektor, Enhet, Funksjon, Art, År, Beløp)
  ├──► Budsjettendringer (VedtakID, Saksnr, Tertial, RammeEndring)
  ├──► NokkeltallParametre (Dekningsgrad, Elevtall, Demografi)
  └──► StatistikkDeflator (Deflator_Pst, Lonn_Pst, Pris_Pst)
        │
        ▼
[ ETL / PII-SCRUBBER & INTEGRATION PIPELINE ]
        │
        ▼
[ VISMA ENTERPRISE ERP ] (Bokført Regnskap: Art 1020 Vikar, Art 1690 NAV-refusjon)
        │
        ▼
[ KRISTIANSAND GOLDEN RECORD (Fabric / SQLite) ]
        │
        ├──► [Avvik YTD] = Bokført Regnskap (Visma) - (Vedtatt Budsjett + Endringer + Deflator (Framsikt))
        └──► [Avvik YTD Korrigert] = [Avvik YTD] + [ERP NAV-Etterslep]
```

---

## 3. Integrerte Framsikt-datastrukturer

### A. Vedtatt Budsjett & Budsjettendringer
* **Opprinnelig Vedtatt Ramme:** Importeres ved årets start.
* **Rammejusteringer:** Importeres fortløpende ved behandling av 1. tertial (T1), 2. tertial (T2) og Bystyrevedtak.
* **Formel for Konsekvensjustert Ramme:**
  $$\text{Konsekvensjustert Ramme} = \text{Vedtatt Budsjett} + \text{Budsjettendringer} + \text{Deflator-kompensasjon}$$

### B. Deflator & Pris/Lønnsjustering
* **Deflator-Mekanisme:** Framsikt leverer gjeldende deflatoranslag.
* **Eksempel fra 1. Tertial 2026:** Deflatoren ble oppjustert fra **3,5 % til 4,1 %** (lønnsvekst inkl. pensjon 3,6 %, prisvekst 4,9 %). Dette medførte en ekstra rammekompensasjon på **156 mill. kr** fordelt på tjenesteområdene via Framsikt-integrasjonen.

---

## 4. DAX & Logikk-implementering

```dax
// Vedtatt Budsjett fra Framsikt
Vedtatt Budsjett = SUM(Framsikt_Budsjett[Opprinnelig_Belop])

// Budsjettendringer fra Framsikt
Budsjettendringer = SUM(Framsikt_Endringer[Endring_Belop])

// Deflator-kompensasjon fra Framsikt
Deflator_Kompensasjon = SUM(Framsikt_Deflator[Deflator_Belop])

// Total Konsekvensjustert Ramme
Total_Justerte_Ramme = [Vedtatt Budsjett] + [Budsjettendringer] + [Deflator_Kompensasjon]

// Reelt Driftsavvik (Kombinasjon av Visma Regnskap og Framsikt Budsjett)
Reelt_Driftsavvik = [Bokfort_Regnskap_Visma] - [Total_Justerte_Ramme] + [ERP_NAV_Etterslep]
```

---

## 5. M365 & Plandisc Årshjul-kobling
Framsikt-oppdrag og budsjettbehandlinger synkroniseres automatisk med det digitale **Årshjulet (Plandisc)** i Microsoft Teams, slik at økonomirådgivere og enhetsledere får varsler i Outlook i forkant av alle rammejusteringer.
