# Oppstartsveileder og startknapp for AI-assistenten

Dette dokumentet beskriver oppsett for enkel oppstart og startknapp for saksbehandlere og økonomirådgivere i Kristiansand kommune.

---

## 1. Oppstart fra skrivebordet (Fysisk Startknapp)

Saksbehandlere kan starte løsningen lokalt med et enkelt dobbelklikk på:
📁 **[`start_kommune_ai.bat`](file:///C:/Users/frank/Desktop/AI_KOM/start_kommune_ai.bat)**

### Funksjonalitet:
Oppstartsskriptet verifiserer Python-miljøet, starter Control Office Hub på port 8501, og åpner automatisk nettleseren på `http://localhost:8501`.

---

## 2. Startknapp på intranett og nettside

For å starte den lokale applikasjonen direkte fra en knapp på intranettet (f.eks. *Aktiv Kommune*, *Teams* eller *Framsikt*), benyttes en tilpasset protokoll i operativsystemet.

* **Sømløs oppstart:** Saksbehandler klikker på en startknapp på nettsiden.
* **Automatisk åpning:** Nettleseren åpner AI-assistentens arbeidsflate umiddelbart.

---

## 3. Sentral serverdrift

Dersom løsningen driftes på en intern server i kommunens IKT-infrastruktur:

1. **Ingen lokal installasjon:** Brukerne trenger ingen installasjon på egen PC.
2. **Direkte nettadresse:** Brukerne åpner kun den interne nettadressen i sin vanlige nettleser.
3. **Kontinuerlig drift:** AI-tjenesten kjører kontinuerlig som en bakgrunnstjeneste.

---

## 🛡️ Sikkerhet og GDPR-samsvar

* **Skjermet databehandling:** Alt datagrunnlag og alle oppslag holdes innenfor kommunens godkjente sone.
* **Innsyn og sporevne:** Alle økter logges med uforanderlig **SHA-256 Audit Trail** for Kommunerevisjonen.
