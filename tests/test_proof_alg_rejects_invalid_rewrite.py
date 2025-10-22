import pytest

from .helpers import FOL, Justification, JustificationError, Proof, parse_formula, parse_rule


def test_alg_rejects_invalid_rewrite(spinner_premises, spinner_conclusion):
    proof = Proof(FOL, spinner_premises, spinner_conclusion)
    with pytest.raises(JustificationError):
        proof.add_line(
            parse_formula('P(c) = 1 - P(a)'),
            Justification(parse_rule('ALG'), (3,)),
        )
