# 🧩 Navigasjonsarkitektur & Tooltip-Spesifikasjon

## 1. Hovedskjermbilde (Layout & Slicers)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 🏛️ Kristiansand Kommune — AI_KOM Hub    [👤 Marianne | Sykehjem 5200 ⚙️]│
├──────────────────────────────────────────────────────────────────────────┤
│ 🟢 Status: I Balanse  │  Budsjett: 145,0 MNOK  │  Regnskap YTD: 96,2 MNOK │
├──────────────────────────────────────────────────────────────────────────┤
│ 🎯 Raske Handlinger:                                                     │
│ [ 📄 Generer Saksfremlegg ]  [ 🧾 Ny Utgående Faktura ]  [ 🔍 Søk KOSTRA ] │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Innbakte Tooltips & Mikrotekter (Ordliste i flukt)

| Felt / Begrep | Plassering i Grensesnitt | Innbakt Tooltip-tekst (Hover / ℹ️) |
| :--- | :--- | :--- |
| **RAG-Status** | Ved siden av enhetsnavn | ℹ️ *Grønn = Avvik innenfor ±2%. Rav = Avvik 2-5%. Rød = Merforbruk over 5% (krever avviksnotat jf. Kommuneloven § 14-5).* |
| **KOSTRA Funksjon 254** | I regnskapstabellen | ℹ️ *Sykehjem og helsehus. Omfatter døgnopphold, medisinsk oppfølging og pleie i institusjon.* |
| **Art 1090 (Overtid)** | Under lønnskostnader | ℹ️ *Overtidsgodtgjørelse. Merk: Husk å sjekke om tidsbruken utløser sykelønnsrefusjon fra NAV (Art 1600).* |
| **Bruttoprinsippet** | Ved utgående faktura | ℹ️ *Kommuneloven § 14-6: Alle utgifter og inntekter skal føres brutto. Det er ikke tillatt å motregne utgifter direkte mot inntekter.* |
| **SHA-256 Revisorstempel** | Ved godkjenningsknapp | ℹ️ *Kryptografisk digitalt stempel som beviser for Kommunerevisjonen at notatet ble godkjent av deg i henhold til EU AI Act Art. 14.* |

---

## 3. Navigasjonsprinsipper

1. **Global Søkestang (`Cmd/Ctrl + K`)**:
   - Brukeren kan skrive fritekst som *"Hvordan fakturere Vennesla for legevakt?"* eller *"Art 1090"*, og får svar direkte uten å forlate siden.
2. **Kaskaderende Slicers**:
   - Ved valg av *Helse og mestring* i sektorsliceren, oppdateres enhetslisten til **kun** å vise de 22 helseenhetene.
3. **Statusbaserte Snarveier**:
   - Dersom enheten har merforbruk, dukker en primærknapp opp med teksten: **"🔴 Løs avvik (1 klikk)"**.
