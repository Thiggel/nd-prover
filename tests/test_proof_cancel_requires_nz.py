import pytest

from .helpers import FOL, Justification, JustificationError, Proof, parse_formula, parse_rule


def test_cancel_requires_nz_premise():
    conclusion = parse_formula('(5*2)/5 = 2')
    proof = Proof(FOL, [], conclusion)
    proof.add_line(
        parse_formula('(5*2)/5 = 10/5'),
        Justification(parse_rule('ARITH'), ()),
    )
    with pytest.raises(JustificationError):
        proof.add_line(
            conclusion,
            Justification(parse_rule('CANCEL'), (1,)),
        )
