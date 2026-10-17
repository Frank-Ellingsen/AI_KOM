---
name: epm-variance-detect
description: >-
  Automatisk avviksdeteksjon (> 5 % / > 250k) mellom faktiske regnskapstall og periodiserte budsjettrammer jf. Kommuneloven § 14-5.
---

# 🛠️ Agent Skill: EPM Variance & Anomaly Detection (`epm-variance-detect`)

> **Formål:** Automatisk avviksdeteksjon og trendanalyse mellom faktiske regnskapstall fra ERP (Visma) og periodiserte rammer fra EPM (Framsikt).

---

## 📋 Skill Spesifikasjon & Metadata

| Egenskap | Verdi |
| :--- | :--- |
| **Skill Name** | `epm-variance-detect` |
| **Versjon** | `1.0.0` |
| **Terskler** | Relativt avvik > 5 % eller absolutte avvik > 250 000 kr |
| **Inndata** | `Fact_Regnskap`, `Fact_Budsjett` |

---

## ⚙️ Deteksjonsalgoritme & SQL

```sql
SELECT 
    f.funksjon_key,
    d.funksjon_navn,
    SUM(f.belop) AS faktisk_forbruk,
    SUM(b.budsjett_belop) AS vedtatt_budsjett,
    (SUM(b.budsjett_belop) - SUM(f.belop)) AS avvik_kroner,
    ROUND(((SUM(b.budsjett_belop) - SUM(f.belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 2) AS avvik_prosent,
    CASE 
        WHEN (SUM(b.budsjett_belop) - SUM(f.belop)) < -250000 AND (((SUM(b.budsjett_belop) - SUM(f.belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100) < -5.0 THEN '🔴 Rød (Kritisk merforbruk)'
        WHEN (SUM(b.budsjett_belop) - SUM(f.belop)) < 0 THEN '🟡 Gul (Moderat merforbruk)'
        ELSE '🟢 Grønn (I rute / Mindreforbruk)'
    END AS rag_status
FROM Fact_Regnskap f
JOIN Fact_Budsjett b ON f.funksjon_key = b.funksjon_key AND f.art_key = b.art_key
JOIN Dim_Funksjon d ON f.funksjon_key = d.funksjon_kode
GROUP BY f.funksjon_key
HAVING ABS(avvik_kroner) > 250000 AND ABS(avvik_prosent) > 5.0
ORDER BY avvik_kroner ASC;
```

### RAG-fargestandard & Automatisk Tiltaksanbefaling
* **🟢 Grønn (Positivt avvik > 0):** Mindreforbruk / besparelse innenfor vedtatt ramme.
* **🟡 Gul (Moderat negativt avvik):** Merforbruk under vesentlighetsterskel (oppfølging).
* **🔴 Rød (Negativt avvik < -5 % eller < -250k kr):** Vesentlig merforbruk som krever politisk sak til Bystyret / Formannskapet jf. **Kommuneloven § 14-5**. Genererer automatisk formelt saksfremlegg.
