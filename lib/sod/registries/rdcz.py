from rdcz import RDczClient, RDczDocument

from ..custom_types import SodSource
from ..libids import LibIdValues
from ..schemas import RDczRegistryConfig, RelevanceNormalizationConfig
from ._solr import build_solr_query
from .interface import FindResponse, RegistryInterface
from .scoring import score_results


class RDczRegistry(RegistryInterface):
    def __init__(
        self,
        config: RDczRegistryConfig,
        rel_norm_config: RelevanceNormalizationConfig | None = None,
    ):
        self._config = config
        self._rel_norm_config = rel_norm_config

        self._client = RDczClient(config.rdcz_config)

    @property
    def source(self) -> SodSource:
        return SodSource.RDcz

    @property
    def name(self) -> str:
        return self._config.name

    def resolve(
        self, identifier_values: LibIdValues
    ) -> FindResponse[RDczDocument]:
        query = build_solr_query(identifier_values, self._config.query_mapping)
        documents = list(self._client.search(query))
        identifier_values_dict = dict(identifier_values)

        return score_results(
            documents,
            self._config.score_rules,
            lambda identifier: identifier_values_dict.get(identifier),
            lambda document, field: getattr(document, field.attr_name),
            self._rel_norm_config,
        )
