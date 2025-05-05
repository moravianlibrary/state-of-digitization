from rdcz import RDczField

from .libids import LibId
from .rdcz_registry import RDczRegistry
from .schemas import RDczRegistryConfig, ScoreRule, SearchRules
from .scoring import MatchMethod, RelevanceNormalization

if __name__ == "__main__":
    INPUT_FILE = "/home/robert/documents/work/diginex/input.txt"

    with open(INPUT_FILE, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    registry = RDczRegistry()

    for line in lines:
        documents = registry.find_by_identifiers(
            [
                (LibId.from_value(line), line),
            ],
            RelevanceNormalization.Softmax,
        )
        print("-" * 35)
        if not documents:
            print(f"Not found: {line}")
        else:
            for score, document in documents:
                print(f"Found: {line} with score {score}")
                print(document)
        print("-" * 35)
