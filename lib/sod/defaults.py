from kramerius import KrameriusConfig
from rdcz import RDczField

from .custom_types import MatchMethod
from .libids import LibId
from .schemas import (
    KrameriusRegistryConfig,
    RDczRegistryConfig,
    ScoreRule,
    SearchRules,
)

DEFAULT_RDCZ_REGISTRY_CONFIG = RDczRegistryConfig(
    registry_name="rdcz",
    identifiers_search_rules=SearchRules(
        query_mapping={
            LibId.Barcode: RDczField.Barcode,
            LibId.Isbn: RDczField.Isxn,
            LibId.Issn: RDczField.Isxn,
            LibId.Isxn: RDczField.Isxn,
            LibId.SystemNumber: RDczField.ControlNumber,
            LibId.Signature: RDczField.Signature,
            LibId.Nbn: RDczField.Nbn,
        },
        score_rules=[
            ScoreRule(
                source_field=LibId.Barcode,
                target_field=RDczField.Barcode,
                match_method=MatchMethod.Exact,
                score=1.0,
            ),
            ScoreRule(
                source_field=LibId.Isbn,
                target_field=RDczField.Isxn,
                match_method=MatchMethod.Exact,
                score=0.5,
            ),
            ScoreRule(
                source_field=LibId.Issn,
                target_field=RDczField.Isxn,
                match_method=MatchMethod.Exact,
                score=0.5,
            ),
            ScoreRule(
                source_field=LibId.Isxn,
                target_field=RDczField.Isxn,
                match_method=MatchMethod.Exact,
                score=0.5,
            ),
            ScoreRule(
                source_field=LibId.SystemNumber,
                target_field=RDczField.ControlNumber,
                match_method=MatchMethod.Exact,
                score=0.5,
            ),
            ScoreRule(
                source_field=LibId.Signature,
                target_field=RDczField.Signature,
                match_method=MatchMethod.Exact,
                score=0.5,
            ),
            ScoreRule(
                source_field=LibId.Nbn,
                target_field=RDczField.Nbn,
                match_method=MatchMethod.Exact,
                score=0.5,
            ),
        ],
    ),
)

# DEFAULT_KRAMERIUS_REGISTRY_CONFIG = KrameriusRegistryConfig(
#     KrameriusConfig(host="https://api.kramerius.mzk.cz/search"),
#     "mzk",
#     [
#         ScoreRule(
#             marc_field="control_fields.control_number",
#             target_field="control_number",
#             score=1,
#         ),
#         ScoreRule(
#             marc_field="numbers_and_codes.isbn.active",
#             target_field="isbn",
#             score=1,
#         ),
#         ScoreRule(
#             marc_field="numbers_and_codes.issn.active",
#             target_field="issn",
#             score=1,
#         ),
#         ScoreRule(
#             marc_field="numbers_and_codes.nbn.active",
#             target_field="nbn",
#             score=1,
#         ),
#         ScoreRule(
#             marc_field="local.location.signature",
#             target_field="signature",
#             score=1,
#         ),
#     ],
# )
