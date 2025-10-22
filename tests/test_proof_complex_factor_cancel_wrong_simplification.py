import pytest

from .helpers import Justification, JustificationError, parse_formula, parse_rule


def test_complex_factor_cancel_wrong_simplification(build_factor_cancel_prefix):
    proof = build_factor_cancel_prefix()
    with pytest.raises(JustificationError):
        proof.add_line(
            parse_formula('(3*a*a - 12*a)/(3*a) = a - 5'),
            Justification(parse_rule('CANCEL'), (1, 4)),
        )
