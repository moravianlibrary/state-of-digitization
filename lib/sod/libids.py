import re
from enum import Enum
from typing import ClassVar, List, Mapping, Tuple


class LibIdBase:
    _patterns: ClassVar["LibIdPatterns"] = {}

    @classmethod
    def set_patterns(cls, id_patterns: "LibIdPatterns"):
        cls._patterns = dict(id_patterns)

    @classmethod
    def from_value(cls, value: str) -> "LibId | None":
        for lib_id, pattern in cls._patterns.items():
            if re.match(pattern, value):
                return lib_id
        return None


class LibId(LibIdBase, Enum):
    SystemNumber = "SystemNumber"
    Isbn = "Isbn"
    Issn = "Issn"
    Isxn = "Isxn"
    Signature = "Signature"
    Barcode = "Barcode"
    Nbn = "Nbn"


LibIdPatterns = Mapping[LibId, str]
LibIdValues = List[Tuple[LibId, str | None]]

DEFAULT_LIB_ID_PATTERNS: LibIdPatterns = {
    LibId.Barcode: r"^\d{10}$",
    LibId.SystemNumber: r"^\d{9}$",
    LibId.Isbn: r"^(97(8|9))?\d{9}(\d|X)$",
    LibId.Issn: r"^\d{4}-\d{3}[\dxX]$",
    LibId.Isxn: r"^\d{4}-\d{3}[\dxX]$",
    LibId.Nbn: r"^cnb\d{9}$",
    LibId.Signature: r"^.+$",
}

LibId.set_patterns(DEFAULT_LIB_ID_PATTERNS)
