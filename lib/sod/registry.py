from .custom_types import SodSource
from .libids import LibIdValues
from .registries import (
    FindResponse,
    KrameriusRegistry,
    RDczRegistry,
    normalize_results,
)
from .schemas import SodDocument, SodRegistryConfig


class SodRegistry:
    def __init__(self, config: SodRegistryConfig):
        self._config = config
        self._rel_norm_config = config.relevance_normalization

        self._registries = [RDczRegistry(config.rdcz_registry)]
        self._registries.extend(
            KrameriusRegistry(kramerius_registry)
            for kramerius_registry in config.kramerius_registries
        )

    def resolve(
        self, identifier_values: LibIdValues
    ) -> FindResponse[SodDocument]:
        results: FindResponse[SodDocument] = []

        for registry in self._registries:
            for score, document in registry.resolve(identifier_values):
                results.append(
                    (
                        score,
                        SodDocument(
                            source=registry.source,
                            name=registry.name,
                            document=document,
                            score=score,
                        ),
                    )
                )

        if self._rel_norm_config is None:
            return sorted(
                results,
                key=lambda x: (
                    0 if x[1].source == SodSource.RDcz else 1,
                    x[1].name,
                    -x[0],
                ),
            )

        results = normalize_results(
            results,
            self._rel_norm_config.method,
            self._rel_norm_config.softmax_temperature,
        )

        return sorted(
            results,
            key=lambda x: (
                0 if x[1].source == SodSource.RDcz else 1,
                x[1].name,
                -x[0],
            ),
        )
