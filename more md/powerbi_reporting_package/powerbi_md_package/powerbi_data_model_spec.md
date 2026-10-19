# Power BI Data Model & RLS Architecture Specification

## 1. Stjerneschema (Star Schema) Layout

Datamodellen bygger på **`Fact_Regnskap`** koblet mot fire dimensjonstabeller:

```
                  ┌─────────────────────────────┐
                  │   Dim_Virksomhetsomrade     │
                  │ (6 Virksomhetsområder)      │
                  └──────────────┬──────────────┘
                                 │ 1:N
                                 ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Dim_Funksjon   │1:N │  Fact_Regnskap   │N:1 │    Dim_Ansvar    │
│ (KOSTRA 100-390) ├───►│ (M1-M8 Actuals & │◄───┤  (81 Enheter)    │
└──────────────────┘    │  Budsjett 7.24B) │    └──────────────────┘
                        └────────┬─────────┘
                                 │ N:1
                                 ▼
                        ┌──────────────────┐
                        │     Dim_Art      │
                        │ (1000-1900 Artek)│
                        └──────────────────┘
```

---

## 2. Row-Level Security (RLS) Definisjoner

Power BI RLS sikrer at enhetsledere kun ser sine egne ansvarssteder, mens kommunalsjefer ser sitt virksomhetsområde:

### RLS Rolle 1: `Enhetsleder_Role`
```dax
[Ansvar] = LOOKUPVALUE('User_Access'[Ansvar_Kode], 'User_Access'[User_UPN], USERPRINCIPALNAME())
```

### RLS Rolle 2: `Sektorleder_Role`
```dax
[Virksomhetsomrade_Navn] = LOOKUPVALUE('User_Access'[Virksomhetsomrade], 'User_Access'[User_UPN], USERPRINCIPALNAME())
```

### RLS Rolle 3: `Kommunedirektor_Controller_Role`
*(Ingen filtere – tilgang til alle 81 enheter og 6 virksomhetsområder)*
