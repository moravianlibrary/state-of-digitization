import json
from os import getenv
from typing import List

from pydantic import ValidationError

from sod import (
    DEFAULT_SOD_REGISTRY_CONFIG,
    LibId,
    LibIdPatterns,
    SodRegistryConfig,
)

SOD_SETTINGS_PATH = getenv("SOD_SETTINGS_PATH", None)
LIB_ID_PATTERNS_PATH = getenv("LIB_ID_PATTERNS_PATH", None)
CUSTOM_CONFGI_ALLOWED = getenv("CUSTOM_CONFIG_ALLOWED", "false")

ALLOW_ORIGINS = getenv("ALLOW_ORIGINS", None)
ALLOW_METHODS = getenv("ALLOW_METHODS", None)
ALLOW_HEADERS = getenv("ALLOW_HEADERS", None)


class staticproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget()


class Config:
    _registry_config: SodRegistryConfig | None = None
    _lib_id_patterns: LibIdPatterns | None = None

    @staticproperty
    def DefaultRegistryConfig() -> SodRegistryConfig:
        if Config._registry_config is not None:
            return Config._registry_config

        if SOD_SETTINGS_PATH:
            with open(SOD_SETTINGS_PATH, "r") as f:
                try:
                    data = json.load(f)
                    Config._registry_config = SodRegistryConfig.model_validate(
                        data
                    )
                except (json.JSONDecodeError, ValidationError) as e:
                    raise ValueError(f"Invalid registry config: {e}")
        else:
            Config._registry_config = DEFAULT_SOD_REGISTRY_CONFIG

        return Config._registry_config

    @staticproperty
    def LibIdPatterns() -> LibIdPatterns:
        if Config._lib_id_patterns is not None:
            return Config._lib_id_patterns

        if LIB_ID_PATTERNS_PATH:
            with open(LIB_ID_PATTERNS_PATH, "r") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        raise TypeError(
                            "Lib ID patterns must be a dictionary."
                        )
                    Config._lib_id_patterns = {
                        LibId(key): val for key, val in data.items()
                    }
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    raise ValueError(f"Invalid lib ID patterns config: {e}")
        else:
            Config._lib_id_patterns = LibId._patterns

        return Config._lib_id_patterns

    @staticproperty
    def CustomConfigAllowed() -> bool:
        return CUSTOM_CONFGI_ALLOWED.lower() == "true"

    @staticproperty
    def AllowOrigins() -> List[str]:
        return ALLOW_ORIGINS.split(",") if ALLOW_ORIGINS else ["*"]

    @staticproperty
    def AllowMethods() -> List[str]:
        return ALLOW_METHODS.split(",") if ALLOW_METHODS else ["*"]

    @staticproperty
    def AllowHeaders() -> List[str]:
        return ALLOW_HEADERS.split(",") if ALLOW_HEADERS else ["*"]
