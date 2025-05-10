from typing import List

from kramerius import KrameriusConfig, Model
from pydantic import BaseModel
from solrify import SolrConfig

from ..custom_types import RelevanceNormalization
from .scoring import QueryMapping, ScoreRules


class RegistryConfig(BaseModel):
    name: str
    query_mapping: QueryMapping
    score_rules: ScoreRules


class RDczRegistryConfig(RegistryConfig):
    rdcz_config: SolrConfig = SolrConfig(
        host="https://registrdigitalizace.cz/",
        endpoint="/rdcz/search/rdcz/select",
    )


class KrameriusRegistryConfig(RegistryConfig):
    kramerius_config: KrameriusConfig
    search_models: List[Model]


class RelevanceNormalizationConfig(BaseModel):
    method: RelevanceNormalization = RelevanceNormalization.Softmax
    softmax_temperature: float = 0.5


class SodRegistryConfig(BaseModel):
    rdcz_registry: RDczRegistryConfig
    kramerius_registries: List[KrameriusRegistryConfig] = []
    relevance_normalization: RelevanceNormalizationConfig | None = (
        RelevanceNormalizationConfig()
    )
