from kramerius import KrameriusClient, KrameriusDocument, KrameriusField
from solrify import F, G

from ..custom_types import SodSource
from ..libids import LibIdValues
from ..schemas import KrameriusRegistryConfig, RelevanceNormalizationConfig
from ._solr import build_solr_query
from .interface import FindResponse, RegistryInterface
from .scoring import score_results


class KrameriusRegistry(RegistryInterface):
    def __init__(
        self,
        config: KrameriusRegistryConfig,
        rel_norm_config: RelevanceNormalizationConfig | None = None,
    ):
        self._config = config
        self._rel_norm_config = rel_norm_config

        self._client = KrameriusClient(config.kramerius_config)

    @property
    def source(self) -> SodSource:
        return SodSource.Kramerius

    @property
    def name(self) -> str:
        return self._config.name

    def resolve(
        self, identifier_values: LibIdValues
    ) -> FindResponse[KrameriusDocument]:
        query = G(
            build_solr_query(identifier_values, self._config.query_mapping)
        ) & F(KrameriusField.Model, self._config.search_models)

        documents = list(self._client.Search.search(query))

        identifier_values_dict = dict(identifier_values)

        return score_results(
            documents,
            self._config.score_rules,
            lambda identifier: identifier_values_dict.get(identifier),
            lambda document, field: getattr(document, field.attr_name),
            self._rel_norm_config,
        )
