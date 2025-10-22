import pytest

from .helpers import Justification, JustificationError, parse_formula, parse_rule


def test_proof_spinner_arith_wrong_value(build_spinner_prefix):
    proof = build_spinner_prefix()
    with pytest.raises(JustificationError):
        proof.add_line(
            parse_formula('P(c) = 2/3'),
            Justification(parse_rule('ARITH'), (6,)),
        )
