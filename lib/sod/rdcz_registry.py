from typing import List, Tuple

from marcdantic import MarcIssue, MarcRecord
from rdcz import RDczClient, RDczDocument
from solrify import F, SearchQuery

from .custom_types import RelevanceNormalization
from .libids import LibId
from .registry import FindResponse, RegistryInterface
from .schemas import RDczRegistryConfig
from .scoring import score_results


class RDczRegistry(RegistryInterface):
    def __init__(self, config: RDczRegistryConfig):
        self._config = config
        self._client = RDczClient(config.rdcz_config)

    def find_by_identifiers(
        self,
        identifier_values: List[Tuple[LibId, str]],
        relevance_normalization: RelevanceNormalization | None = None,
        softmax_temperature: float | None = None,
    ) -> FindResponse[RDczDocument]:
        query = SearchQuery()

        for identifier, value in identifier_values:
            if (
                identifier
                not in self._config.identifiers_search_rules.query_mapping
            ):
                raise ValueError(
                    f"Identifier {identifier} not found in query mapping"
                )

            query |= F(
                self._config.identifiers_search_rules.query_mapping[
                    identifier
                ],
                value,
            )

        documents: List[RDczDocument] = list(self._client.search(query))

        identifier_values_dict = dict(identifier_values)

        return score_results(
            documents,
            self._config.identifiers_search_rules.score_rules,
            relevance_normalization,
            lambda identifier: identifier_values_dict.get(identifier),
            lambda document, rdcz_field: getattr(
                document, rdcz_field.attr_name
            ),
            softmax_temperature=softmax_temperature,
        )

    def find_by_marc_record(
        self, record: MarcRecord
    ) -> FindResponse[RDczDocument]:
        pass

    def find_by_marc_issue(
        self, record: MarcRecord, issue: MarcIssue
    ) -> FindResponse[RDczDocument]:
        pass
