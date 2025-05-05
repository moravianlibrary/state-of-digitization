from kramerius import KrameriusConfig
from pydantic import BaseModel
from solrify import SolrConfig

from .scoring import SearchRules


class RegistryConfig(BaseModel):
    registry_name: str
    identifiers_search_rules: SearchRules | None = None
    record_search_rules: SearchRules | None = None
    items_search_rules: SearchRules | None = None


class RDczRegistryConfig(RegistryConfig):
    rdcz_config: SolrConfig = SolrConfig(
        host="https://registrdigitalizace.cz/",
        endpoint="/rdcz/search/rdcz/select",
    )


class KrameriusRegistryConfig(RegistryConfig):
    kramerius_config: KrameriusConfig
