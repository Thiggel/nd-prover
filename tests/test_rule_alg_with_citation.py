import pytest

from .helpers import (
    FOL,
    Justification,
    JustificationError,
    Line,
    Rules,
    parse_formula,
)


def test_rule_alg_accepts_rearrangement_with_citation():
    eq_line = parse_formula('P(a) + P(b) + P(c) = 1')
    rearranged = parse_formula('P(c) = 1 - P(a) - P(b)')
    line = Line(3, eq_line, Justification(Rules.PR, ()))
    assert FOL.ALG([line], rearranged) == [rearranged]


def test_rule_alg_accepts_scaling_with_citation():
    eq_line = parse_formula('C(p) = 20')
    scaled = parse_formula('2 * C(p) = 40')
    line = Line(3, eq_line, Justification(Rules.PR, ()))
    assert FOL.ALG([line], scaled) == [scaled]


def test_rule_alg_rejects_inconsistent_scaling():
    eq_line = parse_formula('C(p) = 20')
    invalid = parse_formula('2 * C(p) = 30')
    line = Line(3, eq_line, Justification(Rules.PR, ()))
    with pytest.raises(JustificationError):
        FOL.ALG([line], invalid)
