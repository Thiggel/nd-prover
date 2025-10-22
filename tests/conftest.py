import pytest

from .helpers import (
    FOL,
    Justification,
    Proof,
    parse_formula,
    parse_rule,
)


@pytest.fixture
def spinner_premises():
    return [
        parse_formula('P(a) = 1/3'),
        parse_formula('P(b) = 5/12'),
        parse_formula('P(a) + P(b) + P(c) = 1'),
    ]


@pytest.fixture
def spinner_conclusion():
    return parse_formula('P(c) = 1/4')


@pytest.fixture
def build_spinner_prefix(spinner_premises, spinner_conclusion):
    def _build():
        proof = Proof(FOL, spinner_premises, spinner_conclusion)
        proof.add_line(
            parse_formula('P(c) = 1 - P(a) - P(b)'),
            Justification(parse_rule('ALG'), (3,)),
        )
        proof.add_line(
            parse_formula('P(c) = 1 - 1/3 - P(b)'),
            Justification(parse_rule('=E'), (1, 4)),
        )
        proof.add_line(
            parse_formula('P(c) = 1 - 1/3 - 5/12'),
            Justification(parse_rule('=E'), (2, 5)),
        )
        return proof

    return _build


@pytest.fixture
def build_factor_cancel_prefix():
    def _build():
        conclusion = parse_formula('(3*a*a - 12*a)/(3*a) = a - 4')
        proof = Proof(FOL, [parse_formula('NZ(3*a)')], conclusion)
        proof.add_line(
            parse_formula('3*a*a - 12*a = 3*a*(a - 4)'),
            Justification(parse_rule('FACT'), ()),
        )
        proof.add_line(
            parse_formula('(3*a*a - 12*a)/(3*a) = (3*a*a - 12*a)/(3*a)'),
            Justification(parse_rule('=I'), ()),
        )
        proof.add_line(
            parse_formula('(3*a*(a - 4))/(3*a) = (3*a*a - 12*a)/(3*a)'),
            Justification(parse_rule('=E'), (2, 3)),
        )
        return proof

    return _build
