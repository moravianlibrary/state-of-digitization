from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar

from marcdantic import MarcIssue, MarcRecord
from pydantic import BaseModel

from .custom_types import RelevanceNormalization
from .libids import LibId

Entity = TypeVar("Entity", bound=BaseModel)
FindResponse = List[Tuple[float, Entity]]


class RegistryInterface(ABC):
    @abstractmethod
    def find_by_identifiers(
        self,
        identifier_values: List[Tuple[LibId, str]],
        relevance_normalization: RelevanceNormalization | None = None,
    ) -> FindResponse[Entity]:
        pass

    @abstractmethod
    def find_by_marc_record(self, record: MarcRecord) -> FindResponse[Entity]:
        pass

    @abstractmethod
    def find_by_marc_issue(
        self, record: MarcRecord, issue: MarcIssue
    ) -> FindResponse[Entity]:
        pass
