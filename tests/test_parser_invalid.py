import pytest

from .helpers import ParsingError, parse_formula


def test_parser_invalid_inputs():
    for raw in ['A=', '', '()', 'AB', 'A∧', '∀APa']:
        with pytest.raises(ParsingError):
            parse_formula(raw)
