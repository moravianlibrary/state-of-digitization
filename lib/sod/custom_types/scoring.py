from enum import Enum


class MatchMethod(Enum):
    Exact = "Exact"
    Levenshtein = "Levenshtein"


class RelevanceNormalization(Enum):
    Linear = "Linear"
    Softmax = "Softmax"
