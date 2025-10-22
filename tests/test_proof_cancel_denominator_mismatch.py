import pytest

from .helpers import FOL, Justification, JustificationError, Proof, parse_formula, parse_rule


def test_cancel_denominator_mismatch():
    conclusion = parse_formula('(5*2)/5 = 2')
    proof = Proof(FOL, [parse_formula('NZ(5)')], conclusion)
    proof.add_line(
        parse_formula('(5*2)/4 = 10/4'),
        Justification(parse_rule('ARITH'), ()),
    )
    with pytest.raises(JustificationError):
        proof.add_line(
            conclusion,
            Justification(parse_rule('CANCEL'), (1, 2)),
        )
