# -*- coding: utf-8 -*-
"""
Municipal Advisor Decision Calculator CLI Runner
Kristiansand Kommune — Økonomi og Virksomhetsstyring

Beregner og genererer formelle rådgivernotater for:
1. NAV-refusjonsgap (art 1020 vs 1700/1710) jf. Kommuneloven § 14-6 fjerde ledd
2. KRS 4 Drift vs Investering beslutningsmatrise jf. Kommuneloven § 14-9/§ 14-15
3. Selvkost VAR trajektorie og swaprente jf. Selvkostforskriften §§ 5 og 7
4. MVA 10-års justeringsforpliktelse fast eiendom jf. Momskompensasjonsloven § 7
"""

import sys
import argparse
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.services.municipal_calculator_service import MunicipalCalculatorService
from app.schemas.calculator import (
    NavGapRequest,
    Krs4Request,
    SelvkostVarRequest,
    Mva10yRequest,
)


def main():
    parser = argparse.ArgumentParser(
        description="Beslutnings- og Beregningsmotor for Kommunale Økonomirådgivere"
    )
    parser.add_argument(
        "--type",
        choices=["nav-gap", "krs4", "selvkost", "mva-10y"],
        required=True,
        help="Beregningstype",
    )
    # NAV parametere
    parser.add_argument("--enhet", default="2020", help="Enhets-ID (f.eks. '2020')")
    parser.add_argument("--vikar", type=float, default=800000.0, help="Vikarutgifter NOK (art 1020)")
    parser.add_argument("--sykedager", type=int, default=120, help="Totale sykedager")
    parser.add_argument("--egenmeldt", type=int, default=20, help="Egenmeldte dager")
    parser.add_argument("--dagsats", type=float, default=2200.0, help="Refusjonsdagsats NAV")
    parser.add_argument("--etterslep", type=int, default=8, help="Etterslep uker hos NAV")

    # KRS 4 parametere
    parser.add_argument("--prosjekt", default="Rehabilitering av bygg", help="Prosjektnavn")
    parser.add_argument("--kostnad", type=float, default=450000.0, help="Kostnad ekskl. mva NOK")
    parser.add_argument("--levetid", type=int, default=20, help="Levetid i år")
    parser.add_argument("--standardheving", action="store_true", help="Medfører standardheving/kapasitetsøkning")
    parser.add_argument("--separat-enhet", action="store_true", help="Er separat funksjonell enhet")

    # Selvkost parametere
    parser.add_argument("--sektor", default="Vann", help="Sektor ('Vann' el 'Avløp')")
    parser.add_argument("--fond", type=float, default=15000000.0, help="Inngående fondssaldo NOK")
    parser.add_argument("--driftskostnad", type=float, default=80000000.0, help="Driftskostnad NOK")
    parser.add_argument("--gebyrinntekt", type=float, default=82000000.0, help="Gebyrinntekter NOK")
    parser.add_argument("--swaprente", type=float, default=3.85, help="5-årig swaprente i prosent")

    # MVA 10-år parametere
    parser.add_argument("--eiendom", default="Idrettshall", help="Eiendom / Formålsbygg")
    parser.add_argument("--ferdig-aar", type=int, default=2020, help="Fullføringsår for bygget")
    parser.add_argument("--endrings-aar", type=int, default=2026, help="Endringsår / Utleieår")
    parser.add_argument("--utleie-andel", type=float, default=25.0, help="Andel avgiftspliktig utleie i prosent")

    parser.add_argument("--json", action="store_true", help="Skriv ut resultat som JSON")

    args = parser.parse_args()
    svc = MunicipalCalculatorService()

    if args.type == "nav-gap":
        req = NavGapRequest(
            enhet_id=args.enhet,
            vikar_utgifter_nok=args.vikar,
            sykedager_totalt=args.sykedager,
            sykedager_egenmeldt=args.egenmeldt,
            dagsats_refusjon_nok=args.dagsats,
            forventet_etterslep_uker=args.etterslep,
        )
        res = svc.calculate_nav_gap(req)
        if args.json:
            print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("🏛️  KRISTIANSAND KOMMUNE — NAV SYKEPENGEREFUSJONSGAP KALKULATOR")
            print("    Hjemmel: Kommuneloven § 14-6 fjerde ledd (Bruttoprinsippet)")
            print("=" * 80)
            print(f"Enhet:                      {res.enhet_id}")
            print(f"Bokført vikarutgift:        kr {res.vikar_utgifter_nok:,.0f} (Art 1020)")
            print(f"Arbeidsgiverperiode:        {res.arbeidsgiverperiode_dager} dager")
            print(f"Refusjonsberettigede dager: {res.refusjonsberettigede_dager} dager")
            print(f"Forventet NAV-refusjon:     kr {res.forventet_nav_refusjon_nok:,.0f} (Art 1700/1710)")
            print(f"Reelt nettoavvik:           kr {res.reelt_netto_avvik_nok:,.0f}")
            print(f"SHA-256 revisjonsstempel:   {res.sha256_audit_seal}")
            print("-" * 80)
            print("VEILEDNINGSTEKST TIL ENHETSLEDER:")
            print(res.forklaring_til_enhetsleder)
            print("=" * 80)

    elif args.type == "krs4":
        req = Krs4Request(
            prosjekt_navn=args.prosjekt,
            kostnad_ekskl_mva_nok=args.kostnad,
            forventet_levetid_aar=args.levetid,
            standardheving_eller_kapasitet=args.standardheving,
            er_separat_funksjonell_enhet=args.separat_enhet,
        )
        res = svc.evaluate_krs4(req)
        if args.json:
            print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print("🏛️  KRISTIANSAND KOMMUNE — KRS 4 DRIFT VS. INVESTERING BESLUTNINGSMATRISE")
            print("    Hjemler: KRS 4, Kommuneloven §§ 14-9 og 14-15")
            print("=" * 80)
            print(f"Tiltak:                     {res.prosjekt_navn}")
            print(f"Kostnad ekskl. mva:         kr {res.kostnad_ekskl_mva_nok:,.0f}")
            print(f"Forventet levetid:          {res.forventet_levetid_aar} år")
            print(f"KLASSIFISERING:             >>> {res.klassifisering} <<<")
            print(f"Anbefalt kontering:         Kontoklasse {res.anbefalt_kontoklasse} ({res.anbefalt_art})")
            print(f"Adgang til lånefinansiering:{'JA (Lovlig jf. § 14-15)' if res.lovlig_laaneopptak else 'NEI (STRENGT FORBUDT jf. § 14-15)'}")
            print(f"SHA-256 revisjonsstempel:   {res.sha256_audit_seal}")
            print("-" * 80)
            print("VURDERINGSKRITERIER:")
            for k in res.begrunnelse_og_kriterier:
                print(f"  • {k}")
            print("=" * 80)

    elif args.type == "selvkost":
        req = SelvkostVarRequest(
            sektor_navn=args.sektor,
            inngaaende_fondssaldo_nok=args.fond,
            aarsbudsjett_driftskostnader_nok=args.driftskostnad,
            gebyrinntekter_prognose_nok=args.gebyrinntekt,
            swap_rente_5y_pct=args.swaprente,
            tillegg_margin_pct=0.50,
        )
        res = svc.calculate_selvkost_var(req)
        if args.json:
            print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print(f"🏛️  KRISTIANSAND KOMMUNE — SELVKOST VAR KALKYLE ({res.sektor_navn.upper()})")
            print("    Hjemmel: Selvkostforskriften §§ 5 og 7")
            print("=" * 80)
            print(f"Effektiv kalkylerente:      {res.effektiv_kalkylerente_pct:.3f} % (5-år swap {args.swaprente}% + 0.50%)")
            print(f"Årets renteavkastning:      kr {res.aarets_renteinntekt_kostnad_nok:,.0f}")
            print(f"Årets selvkostresultat:     kr {res.aarets_selvkostresultat_nok:,.0f}")
            print(f"Utgående fondssaldo:        kr {res.utgaaende_fondssaldo_nok:,.0f} (Fond 2560)")
            print(f"5-års fremføringsstatus:    {res.fremfoering_status}")
            print(f"Anbefalt gebyrjustering:    {res.anbefalt_gebyrendring_pct:+.1f} %")
            print(f"SHA-256 revisjonsstempel:   {res.sha256_audit_seal}")
            print("=" * 80)

    elif args.type == "mva-10y":
        req = Mva10yRequest(
            eiendom_navn=args.eiendom,
            opprinnelig_anleggskost_ekskl_mva_nok=args.kostnad,
            fullfoerings_aar=args.ferdig_aar,
            endrings_aar=args.endrings_aar,
            andel_avgiftspliktig_utleie_pct=args.utleie_andel,
        )
        res = svc.calculate_mva_10y(req)
        if args.json:
            print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        else:
            print("=" * 80)
            print(f"🏛️  KRISTIANSAND KOMMUNE — MVA 10-ÅRS JUSTERINGSFORPLIKTELSE")
            print(f"    Eiendom: {res.eiendom_navn} | Hjemmel: Momskompensasjonsloven § 7")
            print("=" * 80)
            print(f"Opprinnelig kompensert MVA: kr {res.opprinnelig_mva_kompensert_nok:,.0f}")
            print(f"Årlig justeringsbeløp:      kr {res.aarlig_justeringsramme_nok:,.0f} (1/10 per år)")
            print(f"Gjenstående justeringsår:   {res.gjenstaaende_justeringsaar} av 10 år")
            print(f"Samlet tilbakebetaling:     kr {res.samlet_tilbakebetalingskrav_nok:,.0f} til Skatteetaten")
            print(f"Kontering:                  {res.kontering_balansekonto}")
            print(f"SHA-256 revisjonsstempel:   {res.sha256_audit_seal}")
            print("=" * 80)


if __name__ == "__main__":
    main()
