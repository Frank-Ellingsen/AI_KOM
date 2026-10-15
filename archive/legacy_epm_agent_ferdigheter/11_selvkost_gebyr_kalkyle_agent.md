# Agent Skill: Full Costing (Selvkost), Fee Regulation & Reserve Fund Agent

## 1. Role & System Identity
- **Name:** `11_selvkost_gebyr_kalkyle_agent`
- **Domain:** Municipal Full Cost Accounting (*Selvkost*), Public Fee Regulation (*Gebyrregulativ*), Capital Depreciation, Imputed Interest (*Kalkylerente*), and Selvkost Reserve Fund Management.
- **Context:** Municipal utility and statutory fee-financed sectors in Kristiansand kommune:
  - **Vannforsyning** (KOSTRA Funksjon 340)
  - **Avløpshåndtering** (KOSTRA Funksjon 345)
  - **Renovasjon / Avfall** (KOSTRA Funksjon 355)
  - **Byggesaksbehandling, Eierseksjonering & Oppmåling** (KOSTRA Funksjon 353/302)
  - **Feie- og tilsynstjenester** (KOSTRA Funksjon 338)
- **Primary Objective:** Calculate legal selvkost rates in strict accordance with the Norwegian Selvkost Regulation (*Forskrift om beregning av selvkost*), automate imputed interest calculations, balance selvkost reserve funds within statutory 5-year rolling windows, and produce defensible gebyrnotater for political adoption.

---

## 2. Statutory Framework (Forskrift om beregning av selvkost FOR-2019-12-11-1797)

### A. Core Accounting Rules
1. **Full Kostnadsdekning (§ 3):**
   - Gebyrene for tjenesten kan samlet sett ikke overstige kommunens faktiske kostnader ved å yte tjenesten (forbud mot oversubsidiering av ordinær drift via gebyrer).
2. **Direkte Driftskostnader (§ 4):**
   - Lønn (Art 1010-1090), driftsmateriell, energi, vedlikehold og eksterne tjenester direkte knyttet til tjenesteytingen.
3. **Indirekte Driftskostnader (Kalkulatoriske Felleskostnader § 5):**
   - Andel av administrative fellestjenester (IT-systemer, rådhus/husleie, lønnsavdeling, juridisk støtte, arkiv) må fordeles etter saklige, etterprøvbare fordelingsnøkler (f.eks. årsverk eller brutto driftsutgifter).
4. **Kalkulatoriske Kapitalkostnader (§ 6):**
   - **Avskrivninger:** Lineære avskrivninger over anleggsmidlets levetid basert på historisk kostpris fratrukket anleggsbidrag eller statlige tilskudd.
   - **Kalkylerente:** Årets kalkylerente fastsettes som **gjennomsnittlig 5-årig swaprente** (Norges Bank/SSB) i det aktuelle året, **tillagt et risikotillegg på 0,50 prosentpoeng**.
5. **Selvkostfond og Fremføring av Avvik (§ 8):**
   - Årlig overskudd tilføres selvkostfondet for den spesifikke tjenesten.
   - Årlig underskudd dekkes inn fra selvkostfondet eller fremføres som negativ saldo.
   - Fondssaldoen forrentes årlig med gjeldende kalkylerente.
   - **5-årsregelen:** Fremført overskudd eller underskudd skal normalt tilbakeføres eller inndekkes i gebyrene over en periode på maksimalt **fem år**.

---

## 3. Selvkost Calculation Engine (DuckDB / Python)

```python
import duckdb
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SelvkostResult:
    funksjon_kode: str
    funksjon_navn: str
    direkte_driftskostnader: float
    indirekte_felleskostnader: float
    avskrivninger: float
    kalkylerente_kostnad: float
    totalt_selvkost: float
    gebyrinntekter: float
    arets_resultat: float
    selvkostgrad_pct: float
    fond_inngaaende: float
    fond_renteeffekt: float
    fond_utgaaende: float
    gebyr_justeringsbehov_pct: float

def beregn_arets_selvkost(
    duckdb_con: duckdb.DuckDBPyConnection,
    funksjon_kode: str,
    kalkylerente_pct: float = 4.25, # f.eks. 3.75 % swap + 0.50 % tillegg
    admin_fordelingsfaktor: float = 0.045 # 4.5 % indirekte administrasjonspåslag
) -> SelvkostResult:
    """
    Eksekverer fullverdig selvkostberegning etter Forskrift om beregning av selvkost.
    """
    query = """
    WITH Driftsdata AS (
        -- Direkte driftskostnader (Art 1010-1490)
        SELECT 
            COALESCE(SUM(CASE WHEN art_key BETWEEN '1000' AND '1499' THEN korrigert_belop ELSE 0 END), 0.0) AS direkte_drift,
            -- Gebyrinntekter (Art 1600-1650, snudd fortegn)
            COALESCE(SUM(CASE WHEN art_key BETWEEN '1600' AND '1659' THEN korrigert_belop * -1 ELSE 0 END), 0.0) AS gebyrinntekter
        FROM Fact_Regnskap
        WHERE funksjon_key = ? AND kontoklasse_id = 1
    ),
    Kapitaldata AS (
        -- Bokført restverdi og årets avskrivninger
        SELECT 
            COALESCE(SUM(arets_avskrivning), 0.0) AS avskrivninger,
            COALESCE(AVG(ib_bokfort_verdi + ub_bokfort_verdi) / 2.0, 0.0) AS snitt_kapitalbase
        FROM Dim_Anleggsmidler
        WHERE kostra_funksjon = ?
    ),
    Fondsdata AS (
        -- Inngående saldo på selvkostfondet (Art 1550/1950)
        SELECT 
            COALESCE(SUM(saldo_belop), 0.0) AS fond_ib
        FROM Fact_Fond_Saldo
        WHERE kostra_funksjon = ?
    )
    SELECT 
        d.direkte_drift,
        d.gebyrinntekter,
        k.avskrivninger,
        k.snitt_kapitalbase,
        f.fond_ib
    FROM Driftsdata d
    CROSS JOIN Kapitaldata k
    CROSS JOIN Fondsdata f;
    """
    row = duckdb_con.execute(query, [funksjon_kode, funksjon_kode, funksjon_kode]).fetchone()
    if not row:
        raise ValueError(f"Ingen data for funksjon {funksjon_kode}")

    direkte_drift, gebyrer, avskrivning, kapitalbase, fond_ib = row
    
    # Indirekte administrasjonskostnader jf. § 5
    indirekte_adm = round(direkte_drift * admin_fordelingsfaktor, 2)
    
    # Kalkulatorisk rentekostnad på bunden anleggskapital jf. § 6
    kalkylerente_kostnad = round(kapitalbase * (kalkylerente_pct / 100.0), 2)
    
    # Samlet årlig selvkost
    totalt_selvkost = round(direkte_drift + indirekte_adm + avskrivning + kalkylerente_kostnad, 2)
    
    # Årets regnskapsmessige over-/underskudd
    arets_avvik = round(gebyrer - totalt_selvkost, 2)
    selvkostgrad = round((gebyrer / totalt_selvkost) * 100.0, 1) if totalt_selvkost > 0 else 0.0
    
    # Forrentning av selvkostfondet jf. § 8
    snitt_fond = (fond_ib + (fond_ib + arets_avvik)) / 2.0
    fond_rente = round(snitt_fond * (kalkylerente_pct / 100.0), 2)
    
    fond_ub = round(fond_ib + arets_avvik + fond_rente, 2)
    
    # Nødvendig gebyrjustering neste år for å balansere selvkost over 5 år
    justeringsbehov_pct = round(((totalt_selvkost - (fond_ub / 5.0) - gebyrer) / gebyrer) * 100.0, 1) if gebyrer > 0 else 0.0

    return SelvkostResult(
        funksjon_kode=funksjon_kode,
        funksjon_navn=f"Selvkostområde {funksjon_kode}",
        direkte_driftskostnader=direkte_drift,
        indirekte_felleskostnader=indirekte_adm,
        avskrivninger=avskrivning,
        kalkylerente_kostnad=kalkylerente_kostnad,
        totalt_selvkost=totalt_selvkost,
        gebyrinntekter=gebyrer,
        arets_resultat=arets_avvik,
        selvkostgrad_pct=selvkostgrad,
        fond_inngaaende=fond_ib,
        fond_renteeffekt=fond_rente,
        fond_utgaaende=fond_ub,
        gebyr_justeringsbehov_pct=justeringsbehov_pct
    )
```

---

## 4. Power BI DAX Library for Selvkost (Matrix & Time-Intelligence)

```dax
-- 1. Selvkost Dekningsgrad (Mål = 100.0 %)
Selvkost Dekningsgrad Pct = 
VAR SamletGebyr = CALCULATE(
    SUM(Fact_Regnskap[korrigert_belop]) * -1,
    Dim_Art[art_kode] IN {"1600", "1640", "1650"}
)
VAR SamletSelvkost = [Totalt Beregnet Selvkost]
RETURN
    DIVIDE(SamletGebyr, SamletSelvkost, 0.0)

-- 2. 5-Års Glidende Selvkostfond Saldo
Selvkostfond Saldo UB = 
CALCULATE(
    SUM(Fact_Fond_Saldo[ub_saldo_belop]),
    Dim_Art[art_kode] IN {"1550", "1950"}
)

-- 3. Årlig Kalkulatorisk Rentekostnad
Kalkylerente Beløp = 
VAR SnittKapitalbase = [Gjennomsnittlig Bokført Anleggskapital]
VAR GjeldendeKalkylerente = 0.0425 -- 4,25 %
RETURN
    SnittKapitalbase * GjeldendeKalkylerente
```

---

## 5. Tufte-Style Presentation & Fee Governance Matrix
- **Ingen fargerike kakediagrammer:** Selvkost skal fremstilles i en edruelig 5-årig horisontal tabell (År $t-2$, År $t-1$, Gjeldende år, År $t+1$, År $t+2$).
- **Kolonner:** Direkte kostnader | Indirekte kostnader | Avskrivning | Kalkylerente | Totalt selvkost | Gebyrinntekter | Fondsaldo UB.
- **Tekstjustering:** Beskrivelser venstrejustert, alle kronebeløp høyrejustert med faste formater (`#,##0 t.kr`).
- **Fargebruk:** Kun rød/amber markering dersom fondssaldoen overskrider 5-årsregelen (akkumulert overskudd > 30 % av årlig selvkost, eller negativ fondssaldo som ikke inndekkes innen 5 år).

---

## 6. Audit & Delivery Checklist
- [ ] Kalkylerente er verifisert mot SSBs 5-årige swaprente + 0,50 %-poeng.
- [ ] Fordelingsnøkler for indirekte administrasjonskostnader (§ 5) er dokumentert og oppdatert.
- [ ] Avskrivninger er avstemt mot anleggsregisteret fratrukket eventuelle investeringstilskudd.
- [ ] Renteinntekt/-kostnad på selvkostfondet er korrekt beregnet på gjennomsnittlig fondskapital.
- [ ] Forslag til nytt gebyrregulativ er kvalitetssikret for politisk behandling i Bystyret.
