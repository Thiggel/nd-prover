import pytest

from .helpers import Const, Eq, ParsingError, parse_formula


def test_parser_equality():
    assert parse_formula('a=b') == Eq(Const('a'), Const('b'))
    assert parse_formula('k = m') == Eq(Const('k'), Const('m'))
    with pytest.raises(ParsingError):
        parse_formula('ab=c')
    with pytest.raises(ParsingError):
        parse_formula('a=bc')
    with pytest.raises(ParsingError):
        parse_formula('B=c')
