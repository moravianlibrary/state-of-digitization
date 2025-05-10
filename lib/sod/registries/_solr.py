from solrify import F, SearchQuery

from ..libids import LibIdValues
from ..schemas import QueryMapping


def build_solr_query(
    lib_id_values: LibIdValues, query_mapping: QueryMapping
) -> SearchQuery:
    query = SearchQuery()

    for lib_id, value in lib_id_values:
        if lib_id not in query_mapping:
            raise ValueError(f"Library ID {lib_id} not found in query mapping")

        fields = query_mapping[lib_id]
        if not isinstance(fields, list):
            fields = [fields]

        for field in fields:
            query |= F(field, value)

    return query
