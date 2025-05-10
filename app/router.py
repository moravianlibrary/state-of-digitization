from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sod import (
    DEFAULT_RDCZ_REGISTRY_CONFIG,
    LibId,
    RDczRegistry,
    RelevanceNormalization,
)

from schemas import LibIdPattern, SearchRequest, SodSettings

registry = RDczRegistry(DEFAULT_RDCZ_REGISTRY_CONFIG)
NORMALIZATION = RelevanceNormalization.Softmax

router = APIRouter()


@router.get("/settings")
def get_settings(response_model=SodSettings):
    return {
        "rdcz_registry": DEFAULT_RDCZ_REGISTRY_CONFIG,
        "kramerius_registries": [],
        "normalization": NORMALIZATION,
    }


@router.get("/lib-id-patterns")
def get_lib_id_patterns(response_model=List[LibIdPattern]):
    return LibId._patterns.items()


@router.post("/search")
def search_in_registries(data: SearchRequest):
    results = []
    for group in data.identifiers:
        identifier_values = [(LibId[g[0]], g[1]) for g in group if g[1]]
        response = registry.find_by_identifiers(
            identifier_values, NORMALIZATION
        )
        # format and return results
        results.append(response)
    return results
