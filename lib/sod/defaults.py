from kramerius import KrameriusConfig, KrameriusField, Model
from rdcz import RDczField

from .custom_types import MatchMethod, RelevanceNormalization
from .libids import LibId
from .schemas import (
    KrameriusRegistryConfig,
    RDczRegistryConfig,
    RelevanceNormalizationConfig,
    ScoreRule,
    SodRegistryConfig,
)

DEFAULT_RDCZ_REGISTRY_CONFIG = RDczRegistryConfig(
    name="rdcz",
    query_mapping={
        LibId.Barcode: RDczField.Barcode,
        LibId.Isbn: RDczField.Isxn,
        LibId.Issn: RDczField.Isxn,
        LibId.Isxn: RDczField.Isxn,
        LibId.SystemNumber: RDczField.ControlNumber,
        LibId.Signature: RDczField.Signature,
        LibId.Nbn: RDczField.Nbn,
    },
    score_rules=[
        ScoreRule(
            source_field=LibId.Barcode,
            target_field=RDczField.Barcode,
            match_method=MatchMethod.Exact,
            score=1.0,
        ),
        ScoreRule(
            source_field=LibId.Isbn,
            target_field=RDczField.Isxn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Issn,
            target_field=RDczField.Isxn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Isxn,
            target_field=RDczField.Isxn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.SystemNumber,
            target_field=RDczField.ControlNumber,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Signature,
            target_field=RDczField.Signature,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Nbn,
            target_field=RDczField.Nbn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
    ],
)

DEFAULT_KRAMERIUS_REGISTRY_CONFIG = KrameriusRegistryConfig(
    kramerius_config=KrameriusConfig(
        host="https://api.kramerius.mzk.cz/search"
    ),
    name="mzk",
    query_mapping={
        LibId.Barcode: KrameriusField.Barcode,
        LibId.Isbn: KrameriusField.Isbn,
        LibId.Issn: KrameriusField.Issn,
        LibId.Isxn: [KrameriusField.Isbn, KrameriusField.Issn],
        LibId.SystemNumber: KrameriusField.SystemNumber,
        LibId.Signature: KrameriusField.Signature,
        LibId.Nbn: KrameriusField.Nbn,
    },
    search_models=[
        Model.Periodical,
        Model.PeriodicalVolume,
        Model.Monograph,
        Model.MonographUnit,
        Model.Sheetmusic,
        Model.Convolute,
        Model.Map,
        Model.Graphic,
        Model.SoundRecording,
        Model.Archive,
        Model.Manuscript,
        Model.Picture,
    ],
    score_rules=[
        ScoreRule(
            source_field=LibId.Barcode,
            target_field=KrameriusField.Barcode,
            match_method=MatchMethod.Exact,
            score=1.0,
        ),
        ScoreRule(
            source_field=LibId.Isbn,
            target_field=KrameriusField.Isbn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Issn,
            target_field=KrameriusField.Issn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Isxn,
            target_field=KrameriusField.Isbn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Isxn,
            target_field=KrameriusField.Issn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.SystemNumber,
            target_field=KrameriusField.SystemNumber,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Signature,
            target_field=KrameriusField.Signature,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
        ScoreRule(
            source_field=LibId.Nbn,
            target_field=KrameriusField.Nbn,
            match_method=MatchMethod.Exact,
            score=0.5,
        ),
    ],
)

DEFAULT_RELEVANCE_NORMALIZATION_CONFIG = RelevanceNormalizationConfig(
    method=RelevanceNormalization.Softmax,
    softmax_temperature=0.5,
)

DEFAULT_SOD_REGISTRY_CONFIG = SodRegistryConfig(
    rdcz_registry=DEFAULT_RDCZ_REGISTRY_CONFIG,
    kramerius_registries=[DEFAULT_KRAMERIUS_REGISTRY_CONFIG],
    relevance_normalization=DEFAULT_RELEVANCE_NORMALIZATION_CONFIG,
)
