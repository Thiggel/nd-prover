import pytest

from .helpers import FOL, Justification, JustificationError, Proof, parse_formula, parse_rule


def test_probability_sum_wrong_alg_citation():
    premises = [
        parse_formula('P(a) = 2/5'),
        parse_formula('Q(a) = 3/10'),
        parse_formula('P(a) + Q(a) = R(a)'),
    ]
    proof = Proof(FOL, premises, parse_formula('R(a) = P(a) + Q(a)'))
    with pytest.raises(JustificationError):
        proof.add_line(
            parse_formula('R(a) = P(a) + Q(a)'),
            Justification(parse_rule('ALG'), (1,)),
        )
