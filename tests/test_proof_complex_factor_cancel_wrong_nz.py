import pytest

from .helpers import FOL, Justification, JustificationError, Proof, parse_formula, parse_rule


def test_complex_factor_cancel_wrong_nz():
    conclusion = parse_formula('(3*a*a - 12*a)/(3*a) = a - 4')
    proof = Proof(FOL, [parse_formula('NZ(a)')], conclusion)
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
    with pytest.raises(JustificationError):
        proof.add_line(
            conclusion,
            Justification(parse_rule('CANCEL'), (1, 4)),
        )
