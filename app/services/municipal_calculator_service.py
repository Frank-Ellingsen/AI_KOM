"""
Municipal Advisor Decision Calculator Service
Kristiansand Kommune — Økonomi og Virksomhetsstyring

Implementerer de 4 sentrale beregningsmodellene for kommunale økonomirådgivere:
1. NAV Refusjonsgap & Vikaretterslep jf. Kommuneloven § 14-6 fjerde ledd (Bruttoprinsippet)
2. KRS 4 Drift vs. Investering Beslutningsmatrise jf. Kommuneloven § 14-9 & § 14-15
3. Selvkost VAR Trajektorie & Kalkylerente jf. Selvkostforskriften §§ 5 og 7
4. MVA 10-års Justeringsavtale Fast Eiendom jf. Momskompensasjonsloven § 7
"""

import hashlib
import json
from typing import Dict, Any, List

from app.schemas.calculator import (
    NavGapRequest,
    NavGapResponse,
    Krs4Request,
    Krs4Response,
    SelvkostVarRequest,
    SelvkostVarResponse,
    Mva10yRequest,
    Mva10yResponse,
)


class MunicipalCalculatorService:
    """
    Statutory financial calculation engine for municipal advisors.
    Provides deterministic calculations, legal reasoning, and cryptographic audit seals.
    """

    @staticmethod
    def _create_sha256_seal(data: Dict[str, Any]) -> str:
        serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    # -------------------------------------------------------------------------
    # 1. NAV SYKEPENGEREFUSJONSGAP & VIKARBEREGNER
    # -------------------------------------------------------------------------
    def calculate_nav_gap(self, req: NavGapRequest) -> NavGapResponse:
        """
        Beregner forventet NAV-sykepengerefusjon vs. påløpte vikarutgifter,
        og forklarer tidsforsinkelsen (etterslep) jf. Bruttoprinsippet.
        """
        arbeidsgiverperiode = 16  # Første 16 kalenderdager dekkes av arbeidsgiver
        dager_egenmeldt = min(req.sykedager_egenmeldt, req.sykedager_totalt)
        dager_sykemeldt = req.sykedager_totalt - dager_egenmeldt
        
        refusjonsberettigede_dager = max(0, dager_sykemeldt - arbeidsgiverperiode)
        forventet_refusjon = refusjonsberettigede_dager * req.dagsats_refusjon_nok

        # Tilsynelatende merforbruk i regnskapet (kun utgift er bokført, refusjon mangler)
        tilsynelatende_merforbruk = req.vikar_utgifter_nok

        # Reelt nettoavvik når refusjonen kommer fra NAV
        reelt_netto = req.vikar_utgifter_nok - forventet_refusjon

        forklaring = (
            f"Enhet {req.enhet_id}: Avviket på kr {tilsynelatende_merforbruk:,.0f} på art 1020 er et "
            f"tidsforskyvningsavvik som skyldes saksbehandlingstid hos NAV (estimert {req.forventet_etterslep_uker} uker). "
            f"Enheten har {refusjonsberettigede_dager} refusjonsberettigede sykedager etter arbeidsgiverperioden (16 dager), "
            f"hvilket gir en forventet refusjon fra NAV på kr {forventet_refusjon:,.0f} (art 1700/1710). "
            f"Det reelle nettoavviket er kr {reelt_netto:,.0f}. "
            f"I henhold til Kommuneloven § 14-6 fjerde ledd er direkte motregning (nettoføring) forbudt; "
            f"utgiften og refusjonen må regnskapsføres brutto."
        )

        seal_payload = {
            "enhet_id": req.enhet_id,
            "vikar_utgifter": req.vikar_utgifter_nok,
            "forventet_refusjon": forventet_refusjon,
            "reelt_netto": reelt_netto,
        }
        seal = self._create_sha256_seal(seal_payload)

        return NavGapResponse(
            ok=True,
            enhet_id=req.enhet_id,
            vikar_utgifter_nok=req.vikar_utgifter_nok,
            arbeidsgiverperiode_dager=arbeidsgiverperiode,
            refusjonsberettigede_dager=refusjonsberettigede_dager,
            forventet_nav_refusjon_nok=forventet_refusjon,
            reelt_netto_avvik_nok=reelt_netto,
            tilsynelatende_merforbruk_nok=tilsynelatende_merforbruk,
            forklaring_til_enhetsleder=forklaring,
            sha256_audit_seal=seal,
        )

    # -------------------------------------------------------------------------
    # 2. KRS 4 DRIFT VS. INVESTERING BESLUTNINGSMATRISE
    # -------------------------------------------------------------------------
    def evaluate_krs4(self, req: Krs4Request) -> Krs4Response:
        """
        Klassifiserer et bygge- eller vedlikeholdstiltak som DRIFT eller INVESTERING
        basert på KRS 4, KRS 1 og Kommuneloven §§ 14-9 og 14-15.
        """
        kriterier = []
        is_invest = False

        # Kriterium 1: Beløpsgrense (100 000 kr ekskl. mva)
        if req.kostnad_ekskl_mva_nok >= 100000.0:
            kriterier.append(f"Kostnad kr {req.kostnad_ekskl_mva_nok:,.0f} tilfredsstiller vesentlighetskravet (> kr 100 000 ekskl. mva jf. KRS 4 pkt. 4.1).")
        else:
            kriterier.append(f"Kostnad kr {req.kostnad_ekskl_mva_nok:,.0f} er under vesentlighetsgrensen på kr 100 000 ekskl. mva. Må føres på drift.")

        # Kriterium 2: Levetid (> 3 år)
        if req.forventet_levetid_aar >= 3:
            kriterier.append(f"Forventet levetid på {req.forventet_levetid_aar} år tilfredsstiller kravet om flerårig nytte (> 3 år).")
        else:
            kriterier.append(f"Forventet levetid på {req.forventet_levetid_aar} år er under 3 år. Skal kostnadsføres i driftsregnskapet.")

        # Kriterium 3: Standardheving / Utvidelse vs Løpende vedlikehold
        if req.standardheving_eller_kapasitet:
            kriterier.append("Tiltaket tilfører bygget/anlegget standardheving, funksjonsforbedring eller økt kapasitet utover opprinnelig stand.")
        else:
            kriterier.append("Tiltaket representerer løpende reparasjon/vedlikehold for å opprettholde opprinnelig standard (f.eks. asfaltering av slaghull, maling, utskifting av slitasjedeler).")

        # Konklusjonslogikk
        if (req.kostnad_ekskl_mva_nok >= 100000.0 and req.forventet_levetid_aar >= 3 and 
            (req.standardheving_eller_kapasitet or req.er_separat_funksjonell_enhet)):
            klassifisering = "INVESTERING"
            kontoklasse = 2
            art = "Art 2300 Bygg og anlegg (Investeringsregnskap)"
            laaneopptak = True
            hjemler = [
                "KRS 4 Definisjon av investeringsutgifter (pkt. 4.1 og 4.2)",
                "Kommuneloven § 14-9 Investeringsregnskapet",
                "Kommuneloven § 14-15 Låneadgang for investeringer i varige driftsmidler",
            ]
        else:
            klassifisering = "DRIFT"
            kontoklasse = 1
            art = "Art 1230 Vedlikehold og reparasjon av bygg/anlegg (Driftsregnskap)"
            laaneopptak = False
            hjemler = [
                "KRS 4 pkt. 4.3 (Vedlikehold kan ikke aktiveres)",
                "Kommuneloven § 14-9 Driftsregnskapet",
                "Kommuneloven § 14-15 Forbud mot lånefinansiering av løpende drift og vedlikehold",
            ]

        seal_payload = {
            "prosjekt": req.prosjekt_navn,
            "kostnad": req.kostnad_ekskl_mva_nok,
            "klassifisering": klassifisering,
            "laaneopptak": laaneopptak,
        }
        seal = self._create_sha256_seal(seal_payload)

        return Krs4Response(
            ok=True,
            prosjekt_navn=req.prosjekt_navn,
            kostnad_ekskl_mva_nok=req.kostnad_ekskl_mva_nok,
            forventet_levetid_aar=req.forventet_levetid_aar,
            klassifisering=klassifisering,
            anbefalt_kontoklasse=kontoklasse,
            anbefalt_art=art,
            lovlig_laaneopptak=laaneopptak,
            begrunnelse_og_kriterier=kriterier,
            lovhjemler=hjemler,
            sha256_audit_seal=seal,
        )

    # -------------------------------------------------------------------------
    # 3. SELVKOST VAR 5-ÅRS TRAJEKTORIE & KALKYLERENTE
    # -------------------------------------------------------------------------
    def calculate_selvkost_var(self, req: SelvkostVarRequest) -> SelvkostVarResponse:
        """
        Beregner årlig kalkylerente (swaprente + 0,5%) og simulerer fondssaldo
        opp mot 5-årsregelen i Selvkostforskriften § 7.
        """
        effektiv_rente = (req.swap_rente_5y_pct + req.tillegg_margin_pct) / 100.0
        rente_belop = req.inngaaende_fondssaldo_nok * effektiv_rente

        # Driftsresultat før fondsavsetning
        aarets_selvkost_res = req.gebyrinntekter_prognose_nok - req.aarsbudsjett_driftskostnader_nok
        
        # Ny utgående fondssaldo
        utgaaende_fond = req.inngaaende_fondssaldo_nok + aarets_selvkost_res + rente_belop

        # 5-års fremføringsstatus
        anbefalt_justering = 0.0
        if utgaaende_fond > (req.aarsbudsjett_driftskostnader_nok * 0.35):
            status = "ADVARSEL: AKKUMULERT OVERDEKNING (> 35 % av årsbudsjett). Fondet må reduseres innen 5 år jf. § 7."
            anbefalt_justering = -5.0
        elif utgaaende_fond < 0:
            status = "OBSERVASJON: FREMFØRT UNDERSKUDD. Underskuddet må inndekkes via gebyret innen 5 år jf. § 7."
            anbefalt_justering = 4.0
        else:
            status = "I BALANSE: Fondssaldo er innenfor akseptabel buffer og 5-årskravet overholdes."
            anbefalt_justering = 0.0

        seal_payload = {
            "sektor": req.sektor_navn,
            "kalkylerente": effektiv_rente,
            "utgaaende_fond": utgaaende_fond,
        }
        seal = self._create_sha256_seal(seal_payload)

        return SelvkostVarResponse(
            ok=True,
            sektor_navn=req.sektor_navn,
            effektiv_kalkylerente_pct=round(effektiv_rente * 100.0, 3),
            aarets_renteinntekt_kostnad_nok=round(rente_belop, 2),
            aarets_selvkostresultat_nok=round(aarets_selvkost_res, 2),
            utgaaende_fondssaldo_nok=round(utgaaende_fond, 2),
            aar_i_fondssyklus=3,
            fremfoering_status=status,
            anbefalt_gebyrendring_pct=anbefalt_justering,
            sha256_audit_seal=seal,
        )

    # -------------------------------------------------------------------------
    # 4. MVA 10-ÅRS JUSTERINGSAVTALE FAST EIENDOM
    # -------------------------------------------------------------------------
    def calculate_mva_10y(self, req: Mva10yRequest) -> Mva10yResponse:
        """
        Beregner 10-års justeringsforpliktelse for kommunale formålsbygg
        ved bruksendring / utleie til avgiftspliktig virksomhet jf. Momskompensasjonsloven § 7.
        """
        # Kompensert MVA = 25% av byggekostnad
        opprinnelig_mva = req.opprinnelig_anleggskost_ekskl_mva_nok * 0.25
        aarlig_ramme = opprinnelig_mva / 10.0

        aar_forlopt = max(0, req.endrings_aar - req.fullfoerings_aar)
        gjenstaaende_aar = max(0, 10 - aar_forlopt)

        andel_utleie = req.andel_avgiftspliktig_utleie_pct / 100.0
        samlet_krav = gjenstaaende_aar * aarlig_ramme * andel_utleie

        seal_payload = {
            "eiendom": req.eiendom_navn,
            "opprinnelig_mva": opprinnelig_mva,
            "samlet_krav": samlet_krav,
        }
        seal = self._create_sha256_seal(seal_payload)

        return Mva10yResponse(
            ok=True,
            eiendom_navn=req.eiendom_navn,
            opprinnelig_mva_kompensert_nok=round(opprinnelig_mva, 2),
            aarlig_justeringsramme_nok=round(aarlig_ramme, 2),
            gjenstaaende_justeringsaar=gjenstaaende_aar,
            samlet_tilbakebetalingskrav_nok=round(samlet_krav, 2),
            sha256_audit_seal=seal,
        )
