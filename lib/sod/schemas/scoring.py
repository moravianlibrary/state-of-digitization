from enum import Enum
from typing import List, Mapping, Union

from pydantic import BaseModel
from solrify import MappingEnum

from ..custom_types import MatchMethod

type Field = Union[str, Enum, MappingEnum]

QueryMapping = Mapping[Field, Field | List[Field]]


class ScoreRule(BaseModel):
    source_field: Field
    target_field: Field
    match_method: MatchMethod = MatchMethod.Exact
    score: float = 1.0


ScoreRules = List[ScoreRule]
