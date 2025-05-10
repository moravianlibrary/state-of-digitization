from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar

from pydantic import BaseModel

from ..custom_types import SodSource
from ..libids import LibId

Entity = TypeVar("Entity", bound=BaseModel)
FindResponse = List[Tuple[float, Entity]]


class RegistryInterface(ABC):
    @property
    @abstractmethod
    def source(self) -> SodSource:
        """Source of the registry"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the registry"""
        pass

    @abstractmethod
    def resolve(
        self, identifier_values: List[Tuple[LibId, str]]
    ) -> FindResponse[Entity]:
        pass
