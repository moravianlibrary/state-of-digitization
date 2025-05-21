from typing import List

from config import Config
from fastapi import APIRouter
from pydantic import BaseModel

from sod import (
    FindResponse,
    LibIdPatterns,
    LibIdValues,
    SodDocument,
    SodRegistry,
    SodRegistryConfig,
)

router = APIRouter()


@router.get("/default-registry-config", response_model=SodRegistryConfig)
def get_default_registry_config():
    return Config.DefaultRegistryConfig


@router.get("/custom-config-allowed", response_model=bool)
def is_custom_config_allowed():
    return Config.CustomConfigAllowed


@router.get("/lib-id-patterns", response_model=LibIdPatterns)
def get_lib_id_patterns():
    return Config.LibIdPatterns


class SearchRequest(BaseModel):
    table_values: List[LibIdValues]
    registry_config: SodRegistryConfig | None = None


@router.post("/search", response_model=List[FindResponse[SodDocument]])
def search_in_registries(data: SearchRequest):
    registry = (
        SodRegistry(data.registry_config)
        if Config.CustomConfigAllowed and data.registry_config
        else SodRegistry(Config.DefaultRegistryConfig)
    )

    return [registry.resolve(values_row) for values_row in data.table_values]
