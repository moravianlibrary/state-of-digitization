import math
from typing import Callable, List

import numpy as np
from Levenshtein import distance
from scipy.optimize import linear_sum_assignment

from ..custom_types import MatchMethod, RelevanceNormalization
from ..schemas import (
    Field,
    RelevanceNormalizationConfig,
    ScoreRule,
    ScoreRules,
)
from .interface import Entity, FindResponse

GetFieldValueFunc = Callable[[Field], str | List[str] | None]
GetEntityFieldValueFunc = Callable[[object, Field], str | List[str] | None]


def get_score(rule: ScoreRule, v1: str, v2: str) -> float:
    if rule.match_method == MatchMethod.Exact:
        return rule.score if v1 == v2 else 0.0
    if rule.match_method == MatchMethod.Levenshtein:
        max_len = max(len(v1), len(v2))
        return (
            rule.score * (1 - distance(v1, v2) / max_len)
            if max_len > 0
            else 0.0
        )
    return 0.0


def score_match(
    rules: ScoreRules,
    get_source_value: GetFieldValueFunc,
    get_target_value: GetFieldValueFunc,
) -> float:
    total_score = 0.0
    possible_score = 0.0

    for rule in rules:
        source_value = get_source_value(rule.source_field)
        target_value = get_target_value(rule.target_field)

        if source_value is None and target_value is None:
            continue

        possible_score += rule.score

        if source_value is None or target_value is None:
            continue

        source_value_list = (
            source_value if isinstance(source_value, list) else [source_value]
        )
        target_value_list = (
            target_value if isinstance(target_value, list) else [target_value]
        )

        m, n = len(source_value_list), len(target_value_list)

        cost_matrix = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                cost_matrix[i, j] = -get_score(
                    rule, source_value_list[i], target_value_list[j]
                )

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        match_score = -sum(cost_matrix[i, j] for i, j in zip(row_ind, col_ind))

        matches = max(m, n)
        if matches > 0:
            total_score += (match_score / max(m, n)) * rule.score

    return total_score


def normalize_results(
    results: FindResponse,
    normalization: RelevanceNormalization,
    softmax_temperature: float | None = None,
) -> List[float]:
    if normalization == RelevanceNormalization.Linear:
        total_score = sum(score for score, _ in results)
        return [(score / total_score, entity) for score, entity in results]
    elif normalization == RelevanceNormalization.Softmax:
        exp_scores = (
            [math.exp(score / softmax_temperature) for score, _ in results]
            if softmax_temperature
            else [math.exp(score) for score, _ in results]
        )
        sum_exp = sum(exp_scores)

        return [
            (exp_score / sum_exp, entity)
            for exp_score, (_, entity) in zip(exp_scores, results)
        ]


def score_results(
    entities: List[Entity],
    rules: ScoreRules,
    get_source_value: GetFieldValueFunc,
    get_target_value: GetEntityFieldValueFunc,
    rel_norm_config: RelevanceNormalizationConfig | None,
) -> FindResponse:
    if not entities:
        return []

    results = []

    for entity in entities:
        score = score_match(
            rules,
            get_source_value,
            lambda field: get_target_value(entity, field),
        )
        if score > 0:
            results.append((score, entity))

    if rel_norm_config:
        results = normalize_results(
            results,
            rel_norm_config.method,
            rel_norm_config.softmax_temperature,
        )

    return sorted(results, key=lambda x: x[0], reverse=True)
