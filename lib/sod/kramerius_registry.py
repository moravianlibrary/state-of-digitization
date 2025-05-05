from typing import List, Tuple

from kramerius import KrameriusClient, KrameriusDocument
from marcdantic import MarcIssue, MarcRecord

from .custom_types import RelevanceNormalization
from .libids import LibId
from .registry import FindResponse, RegistryInterface
from .schemas import KrameriusRegistryConfig


class KrameriusRegistry(RegistryInterface):
    def __init__(self, config: KrameriusRegistryConfig):
        self._config = config
        self._client = KrameriusClient(config.kramerius_config)

    def find_by_identifiers(
        self,
        identifier_values: List[Tuple[LibId, str]],
        relevance_normalization: RelevanceNormalization | None = None,
    ) -> FindResponse[KrameriusDocument]:
        raise NotImplementedError(
            "KrameriusRegistry does not support find_by_identifiers"
        )

    def find_by_marc_record(
        self, record: MarcRecord
    ) -> FindResponse[KrameriusDocument]:
        raise NotImplementedError(
            "KrameriusRegistry does not support find_by_marc_record"
        )

    def find_by_marc_issue(
        self, record: MarcRecord, issue: MarcIssue
    ) -> FindResponse[KrameriusDocument]:
        raise NotImplementedError(
            "KrameriusRegistry does not support find_by_marc_issue"
        )
