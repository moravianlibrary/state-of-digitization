from typing import List, Tuple

from pydantic import BaseModel
from sod import (
    Find,
    KrameriusRegistryConfig,
    LibId,
    RDczRegistryConfig,
    RelevanceNormalization,
)


class SodSettings(BaseModel):
    rdcz_registry: RDczRegistryConfig
    kramerius_registries: List[KrameriusRegistryConfig] | None = None
    normalization: RelevanceNormalization


class LibIdPattern(BaseModel):
    lib_id: LibId
    pattern: str


class SearchRequest(BaseModel):
    identifier_values: List[List[Tuple[LibId, str | None]]]
    settings: SodSettings | None = None


class SearchResponse(BaseModel):
    identifier_values: List[Tuple[LibId, str | None]]
    results: List[List[Tuple[str, str | None]]]
