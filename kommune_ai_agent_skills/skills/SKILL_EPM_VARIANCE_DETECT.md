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
    (SUM(f.belop) - SUM(b.budsjett_belop)) AS avvik_kroner,
    ROUND(((SUM(f.belop) - SUM(b.budsjett_belop)) / NULLIF(SUM(b.budsjett_belop), 0)) * 100, 2) AS avvik_prosent
FROM Fact_Regnskap f
JOIN Fact_Budsjett b ON f.funksjon_key = b.funksjon_key AND f.art_key = b.art_key
JOIN Dim_Funksjon d ON f.funksjon_key = d.funksjon_kode
GROUP BY f.funksjon_key
HAVING ABS(avvik_kroner) > 250000 AND ABS(avvik_prosent) > 5.0
ORDER BY ABS(avvik_kroner) DESC;
```

### Automatisk Tiltaksanbefaling
Dersom et avvik krever politisk omdisponering jf. **Kommuneloven § 14-5**, genererer skillen automatisk et tekstutkast for 1. eller 2. tertialrapport.
