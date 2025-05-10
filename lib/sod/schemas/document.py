from kramerius import KrameriusDocument
from pydantic import BaseModel
from rdcz import RDczDocument

from ..custom_types import SodSource


class SodDocument(BaseModel):
    source: SodSource
    name: str
    document: RDczDocument | KrameriusDocument
    score: float
