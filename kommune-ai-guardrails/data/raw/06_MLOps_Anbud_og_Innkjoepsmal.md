# 06. Kravspesifikasjon og Anbudsmal for MLOps-Anskaffelse

## 1. Innledning og Formål
Dette dokumentet stiller skriveklare krav til anskaffelse av MLOps-/LLMOps-plattform og overordnet AI-infrastruktur i kommunal sektor. Kravspesifikasjonen sikrer at valgt leverandør oppfyller kravene i EU AI Act, GDPR, ISO 42001 og nasjonale føringer fra Digdir og KS Digital.

---

## 2. Kravmatrise (A- og B-krav for Anbud)

| Krav ID | Kategori | Kravbeskrivelse | Kravtype (A/B) | Leverandørens Besvarelse |
| :--- | :--- | :--- | :--- | :--- |
| **K-01** | **Gateway** | Løsningen skal tilby en sentral AI Gateway som isolerer fagsystemer fra underliggende modell-leverandører (*No Vendor Lock-in*). | **A-krav** | |
| **K-02** | **Sikkerhet** | Automatisk PII-skjerming og anonymisering av personopplysninger før data sendes til språkmodeller. | **A-krav** | |
| **K-03** | **Skytjeneste** | Alle modeller og datalager skal driftes innenfor EU/EØS med eksplisitt forbud mot leverandørtrening på kommunens data. | **A-krav** | |
| **K-04** | **Tilgang** | Sømløs integrasjon mot Entra ID / FellesID med arvet tilgangsstyring (RBAC/ABAC) i RAG-pipelines. | **A-krav** | |
| **K-05** | **MLOps** | Løsningen skal ha et integrert Modellregister (Model Registry) med støtte for versjonskontroll, Staging/Production-miljø og CI/CD. | **A-krav** | |
| **K-06** | **Logging** | Automatisk audit logging jf. EU AI Act art. 26 av alle forespørsler, uthentet RAG-kontekst, modellversjon og brukers godkjenning. | **A-krav** | |
| **K-07** | **Observability**| Dashbord for overvåking av datadrift, svarpresisjon, latency, feilrater og token-forbruk (FinOps). | **A-krav** | |
| **K-08** | **Testing** | Støtte for automatisert benchmarking mot Ground Truth-testsett før produksjonssetting. | **B-krav** | |
| **K-09** | **Beredskap** | Funksjonalitet for umiddelbar teknisk utkobling (*Kill-Switch*) og overgang til manuell fallback. | **A-krav** | |
| **K-10** | **SLA** | Garantert oppetid (SLA) på minimum 99,5 % for produksjonsendepunkter med definert responstid. | **B-krav** | |

*A-krav = Absolutte minstekrav (Må-krav). B-krav = Tildelingskrav (Evalueres på kvalitet/pris).*

---

## 3. Kontraktsvilkår for Datasuverenitet og AI Act

1. **Datagrenser:** Kommunens inndata, prompter, RAG-dokumenter og genererte utdata skal under ingen omstendighet benyttes av leverandøren eller underleverandører til å trene, finjustere eller forbedre kommersielle modeller.
2. **Endringsvarsling:** Leverandøren plikter å varsle kommunen minimum 30 dager før oppdateringer eller endringer i underliggende modellversjoner som kan påvirke svaroppførsel eller presisjon.
3. **Tilsynsinnsyn:** Leverandøren skal gi kommunen og relevante tilsynsmyndigheter (f.eks. Datatilsynet, Digitaliseringsdirektoratet) nødvendig innsyn i teknisk dokumentasjon og sikkerhetsarkitektur.

---
*Dokumentet inngår i MLOps-implementeringspakken for kommunal sektor.*
