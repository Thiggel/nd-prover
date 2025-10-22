import pytest

from .helpers import Justification, JustificationError, parse_rule


def test_proof_spinner_arith_requires_citation(build_spinner_prefix, spinner_conclusion):
    proof = build_spinner_prefix()
    with pytest.raises(JustificationError):
        proof.add_line(spinner_conclusion, Justification(parse_rule('ARITH'), ()))
