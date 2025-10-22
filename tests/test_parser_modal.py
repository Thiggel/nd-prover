from .helpers import Box, Dia, PropVar, parse_formula


def test_parser_modal():
    assert parse_formula('boxA') == Box(PropVar('A'))
    assert parse_formula('[]A') == Box(PropVar('A'))
    assert parse_formula('□A') == Box(PropVar('A'))
    assert parse_formula('diaB') == Dia(PropVar('B'))
    assert parse_formula('<>C') == Dia(PropVar('C'))
    assert parse_formula('♢C') == Dia(PropVar('C'))
