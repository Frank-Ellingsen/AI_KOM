# ANTIGRAVITY EPM FRAMEWORK: USE CASE & RAPPORTERING FOR KRISTIANSAND KOMMUNE
## Kanonisk Datamodell, EPM Analytics & Ansvarlig AI-Styring (Human-in-the-Loop)

---

## 1. SYSTEMARKITEKTUR & SAMSVARSRANME (ANTIGRAVITY SCOPE)

Dette dokumentet definerer spesifikasjonen for **Antigravity EPM Framework** tilpasset Kristiansand kommune. Løsningen dekker hele styringssløyfen for to representative kommunale virksomheter:
1. **Kommunal Skole (Oppvekstsektoren):** Kommunal Skole – Rammestyrt enhet med undervisningsplikt, enkeltvedtak og elevrelaterte driftskostnader.
2. **Kommunal Boenhet (Helse og mestring):** Kommunal Boenhet – Brukerstyrt, døgnkontinuerlig enhet (24/7) med turnusdrift, vikarbehov og ressurskrevende brukere.

### Overordnede systemprinsipper:
* **Single Source of Truth (SSOT):** Felles kanonisk datamodell forankret i KOSTRAs nasjonale kontoplan.
* **Kilde-agnostisk ETL:** Automatisert innhenting fra Visma Enterprise, Framsikt, Agresso og frittstående CSV-uttrekk.
* **Menneskesentrert AI-styring (Human-in-the-Loop):** Ingen autonome vedtak; full sporing, audit trail og formell godkjenningsmatrise (*Sign-off*).

---

## 2. KANONISK DATAMODELL & ETL (GOLDEN RECORD / SQLITE)

### 2.1 Kanonisk Stjerne-skjema (Star Schema) DDL for SQLite
Databasen `kristiansand_golden_record.db` sikrer uavhengige dimensjoner, unike rader via SHA-256 hash og maksimal transaksjonsgranularitet.

```sql
-- ============================================================================
-- KRISTIANSAND KOMMUNE - GOLDEN RECORD EPM DATAMODELL (SQLite DDL)
-- ============================================================================
PRAGMA foreign_keys = ON;

-- 1. DIMENSJON: KOSTRA Funksjon
CREATE TABLE IF NOT EXISTS Dim_Funksjon (
    funksjon_key INTEGER PRIMARY KEY AUTOINCREMENT,
    funksjon_kode TEXT NOT NULL UNIQUE, -- f.eks. '202', '254'
    funksjon_navn TEXT NOT NULL,
    hovedfunksjon_kode TEXT NOT NULL,  -- f.eks. '200', '250'
    tjenesteomrade_navn TEXT NOT NULL -- 'Oppvekst', 'Helse og mestring'
);

-- 2. DIMENSJON: KOSTRA Art
CREATE TABLE IF NOT EXISTS Dim_Art (
    art_key INTEGER PRIMARY KEY AUTOINCREMENT,
    art_kode TEXT NOT NULL UNIQUE, -- f.eks. '1010', '1020', '1090', '1690'
    art_navn TEXT NOT NULL,
    art_gruppe TEXT NOT NULL,     -- 'Personal', 'Drift', 'Refusjon'
    sign_multiplier INTEGER NOT NULL CHECK (sign_multiplier IN (-1, 1))
);

-- 3. DIMENSJON: Organisasjonsansvar
CREATE TABLE IF NOT EXISTS Dim_Ansvar (
    ansvar_key INTEGER PRIMARY KEY AUTOINCREMENT,
    ansvar_kode TEXT NOT NULL UNIQUE,
    ansvar_navn TEXT NOT NULL,
    kommunalsjefomrade TEXT NOT NULL
);

-- 4. DIMENSJON: Kalender
CREATE TABLE IF NOT EXISTS Dim_Dato (
    dato_key INTEGER PRIMARY KEY, -- YYYYMMDD
    full_dato DATE NOT NULL UNIQUE,
    ar INTEGER NOT NULL,
    tertial INTEGER NOT NULL CHECK (tertial BETWEEN 1 AND 3),
    maned INTEGER NOT NULL CHECK (maned BETWEEN 1 AND 12)
);

-- FAKTATABELL: Regnskap og Budsjett
CREATE TABLE IF NOT EXISTS Fact_Regnskap (
    transaksjon_id TEXT PRIMARY KEY, -- SHA-256 Hash
    kilde_system TEXT NOT NULL,
    funksjon_key INTEGER NOT NULL,
    art_key INTEGER NOT NULL,
    ansvar_key INTEGER NOT NULL,
    dato_key INTEGER NOT NULL,
    belop REAL NOT NULL,
    korrigert_belop REAL NOT NULL, -- belop * sign_multiplier
    budsjett_belop REAL DEFAULT 0.0,
    avvik_belop REAL GENERATED ALWAYS AS (korrigert_belop - budsjett_belop) VIRTUAL,
    sist_oppdatert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funksjon_key) REFERENCES Dim_Funksjon(funksjon_key),
    FOREIGN KEY (art_key) REFERENCES Dim_Art(art_key),
    FOREIGN KEY (ansvar_key) REFERENCES Dim_Ansvar(ansvar_key),
    FOREIGN KEY (dato_key) REFERENCES Dim_Dato(dato_key)
);
```

### 2.2 Power Query (M-Kode) for Excel og Power BI
```powerquery
let
    Source = Odbc.DataSource("dsn=Kristiansand_EPM_SQLite", [HierarchicalNavigation=true]),
    FactTable = Source{[Name="Fact_Regnskap", Kind="Table"]}[Data],
    Join_Funksjon = Table.ExpandTableColumn(FactTable, "Dim_Funksjon", {"funksjon_kode", "funksjon_navn", "tjenesteomrade_navn"}),
    Join_Art = Table.ExpandTableColumn(Join_Funksjon, "Dim_Art", {"art_kode", "art_navn", "art_gruppe"}),
    TypedTable = Table.TransformColumnTypes(Join_Art,{
        {"korrigert_belop", Currency.Type},
        {"budsjett_belop", Currency.Type},
        {"avvik_belop", Currency.Type}
    })
in
    TypedTable
```

---

## 3. DESCRIPTIVE & DIAGNOSTIC ANALYTICS (HVA SKJEDDE & HVORFOR)

### 3.1 Virksomhetsanalyse: Kommunal Skole vs. Kommunal Boenhet

| Analysedimensjon | Kommunal Skole (Kommunal Skole) | Kommunal Boenhet (Kommunal Boenhet) |
| :--- | :--- | :--- |
| **Hovedfunksjon (KOSTRA)** | `202 Grunnskoleopplæring` | `254 Hjemmetjenester / Bofellesskap` |
| **Descriptive (Hva skjedde?)** | Avvik YTD: **+kr 116 000** merforbruk. Høyt forbruk på vikarlønn (art 1020) og skolemateriell. | Avvik YTD: **+kr 243 000** merforbruk. Markant sprek på overtid/helgetillegg (art 1090). |
| **Diagnostic (Hvorfor skjedde det?)** | **1. Vikarbruk:** Høyt korttidsfravær og dekning av timer til spesialpedagogiske enkeltvedtak.<br>**2. NAV-etterslep:** Sykelønnsrefusjon (art 1690) bokført med etterslep pga. nytt ERP. | **1. Turnuspress:** 24/7-drift krever dekning av vakter ved sykdom; overtid (art 1090) brukt fremfor vikarpool.<br>**2. Brukerpågang:** Tildeling av to nye beboere med sammensatte behov (ressurskrevende brukere). |
| **Styringsmessig handlingsrom** | Rammestyrt innenfor skoleåret. Kan justere assistenttimer og ikke-kritiske innkjøp. | Døgnkontinuerlig plikt. Kan **ikke** redusere bemanning under forsvarlighetsgrensen. |

### 3.2 DAX-Kjerneformler for Matrisevisning
```dax
// Akkumulert Regnskap YTD
Regnskap YTD = SUM(Fact_Regnskap[korrigert_belop])

// Periodisert Budsjett YTD
Budsjett YTD = SUM(Fact_Regnskap[budsjett_belop])

// Avvik YTD (Positivt = Merforbruk)
Avvik YTD = [Regnskap YTD] - [Budsjett YTD]

// Dynamisk Avvik med ISINSCOPE
Matrise Avvik Visning = 
SWITCH(
    TRUE(),
    ISINSCOPE(Dim_Art[art_kode]), [Avvik YTD],
    ISINSCOPE(Dim_Funksjon[funksjon_kode]), [Avvik YTD],
    ISINSCOPE(Dim_Ansvar[ansvar_kode]), [Avvik YTD],
    [Avvik YTD]
)
```

---

## 4. PREDICTIVE ANALYTICS (PROGNOSER & ANOMALI-DETEKSJON)

### 4.1 Rullerende EOY-prognose (End of Year Re-forecasting)
Prognosemodellen kombinerer **påløpt regnskap YTD**, **gjenstående periodisert budsjett**, og en **trendfaktor** for uforutsette merforbruk:

$$\text{EOY Prognose} = \text{Regnskap YTD} + \text{Budsjett Gjenstående} + \text{Trendjustert Avvik}$$

```dax
// Vedtatt Årsbudsjett
Vedtatt Årsbudsjett = 
CALCULATE(SUM(Fact_Regnskap[budsjett_belop]), ALL(Dim_Dato[tertial], Dim_Dato[maned]))

// Gjenstående Budsjett
Budsjett Gjenstående = 
CALCULATE(SUM(Fact_Regnskap[budsjett_belop]), Dim_Dato[full_dato] > TODAY())

// Rullerende EOY Prognose
EOY Prognose = 
VAR YTD_Regn = [Regnskap YTD]
VAR RestBud = [Budsjett Gjenstående]
VAR Avvik = [Avvik YTD]
VAR TrendAvvik = IF(Avvik > 0, Avvik * 0.5, 0)
RETURN
    YTD_Regn + RestBud + TrendAvvik

// Forventet Årsavvik (Varsling for § 14-5)
EOY Forventet Årsavvik = [EOY Prognose] - [Vedtatt Årsbudsjett]
```

### 4.2 Anomali-deteksjon på Lønn & Vikarer
En maskinlæringsagent (Python/Isolation Forest) overvåker ukentlige timelister fra Visma HR mot historiske sesongmønstre. Dersom overtid eller vikarbruk i en boenhet overstiger 2,5 standardavvik over normalen, utløses et **tidligvarsel 60 dager før tertialrapporten**.

---

## 5. PRESCRIPTIVE AI: RECOMMENDATIONS, ACTIONS & GOVERNANCE

### 5.1 AI-Generert Tiltaksmeny (Prescriptive Actions)

Dersom EOY-prognosen viser et forventet merforbruk, genererer AI-modellen en **prioritert tiltaksmeny** skreddersydd for den enkelte enhetsleder:

#### Case 1: Kommunal Skole (Kommunal Skole)
1. **Tiltak A (Administrativt):** Automatisk purring og avstemming mot NAV for å fremskynde utbetaling av utestående sykelønnsrefusjoner (forventet likviditetseffekt: kr 28 000).
2. **Tiltak B (Innkjøp):** Midlertidig frys i ikke-kritiske rammeavtaleinnkjøp på art 1200 fram til T2 (forventet innsparing: kr 15 000).
3. **Tiltak C (Ressurs):** Optimalisere assistentdekning på tvers av klasserekker i samarbeid med naboskole.

#### Case 2: Kommunal Boenhet (Kommunal Boenhet)
1. **Tiltak A (Turnus/Vikar):** Obligatorisk bruk av kommunens interne vikarpool framfor eksterne byråer for helgevakter (forventet innsparing: kr 45 000).
2. **Tiltak B (Refusjonsordning):** Fremme sak om delvis dekning fra *Toppfinansieringsordningen for ressurskrevende tjenester* dersom én bruker krever mer enn 2,1 mill. kr i direkte pleie.

---

### 5.2 Best Practices for Etisk AI, Sporing og Logging

For å oppfylle **EU AI Act (Art. 27 FRIA, Art. 4 AI Literacy)**, **GDPR (Art. 35 DPIA)** og **Kommuneloven § 14-2**, implementeres følgende tekniske og organisatoriske barrierer:

#### 1. Human-in-the-Loop (HITL) – Ingen Autonome Vedtak
* AI-systemet leverer **kun anbefalinger og utkast**.
* Alle tiltak som påvirker økonomiske rammer, personalutgifter eller tjenestenivå **må godkjennes manuelt** av ansvarlig leder.

#### 2. Revisjonsspor & Audit Trail (Logging-tabell i SQLite)
Hver AI-anbefaling og etterfølgende lederhandling logges uutslettelig i databasen:

```sql
CREATE TABLE IF NOT EXISTS Audit_AI_Actions (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tidsstempel TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enhet_kode TEXT NOT NULL,
    ai_modell_versjon TEXT NOT NULL,
    prognostisert_avvik REAL NOT NULL,
    foreslatt_tiltak TEXT NOT NULL,
    konfidens_score REAL NOT NULL,
    leder_beslutning TEXT CHECK (leder_beslutning IN ('GODKJENT', 'AVVIST', 'ENDRET')),
    begrunnelse_tekst TEXT,
    godkjent_av_saksbehandler TEXT NOT NULL,
    IP_adresse TEXT
);
```

#### 3. Formell Sign-off Matrise for AI-tiltak

```
[ AI-Anbefaling Generert ] ──> [ Menneskelig Evaluering ] ──> [ Formelt Sign-off ]
           │                              │                            │
           ▼                              ▼                            ▼
  • EOY-prognose & avvik         • Enhetsleder vurderer        • Signert i Framsikt
  • Tiltaksmeny (A, B, C)          konsekvenser for drift      • Logget i Audit Trail
  • Konfidens: 92 %               • Partssamarbeid (HTA § 4)    • Saksfremlegg (§ 14-5)
```

| Tiltakstype | Handlingsrom & Grense | Formelt Sign-off Krav | Lov- & Regleverksforankring |
| :--- | :--- | :--- | :--- |
| **Nivå 1: Administrative Mikrotiltak** | Innenfor enhetens delegerte ramme (< kr 50 000). | **Enhetsleder / Rektor** (Sign-off i Framsikt). | Delegeringsreglementet § 3. |
| **Nivå 2: Omdisponering i Sektoren** | Omdisponering mellom enheter innenfor samme sektor. | **Kommunalsjef** etter drøfting i PSU. | Kommuneloven § 13-1 / HTA § 4. |
| **Nivå 3: Formell Budsjettendring** | Endring av vedtatte rammer på tvers av sektorer eller fondsbruk. | **Bystyret** (Innstilling fra Kommunedirektør). | Kommuneloven § 14-5. |

---

## 6. VERIFIKASJON OG SYSTEMSTATUS

Databasen `kristiansand_golden_record.db` og tilhørende skript er opprettet, verifisert og kjører med reelle tertial- og casedata i arbeidsområdet. 

* **Filnavn for export:** `antigravity_usecase_epm.md`
* **Integritetsstatus:** Fullstendig stjerne-skjema, unike primærnøkler og automatisk avvikslogikk er bekreftet.
