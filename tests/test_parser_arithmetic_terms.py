from .helpers import Const, Eq, Fraction, Func, Numeral, Pred, parse_formula


def test_parser_arithmetic_terms():
    formula = parse_formula('P(a)=1/3')
    assert formula == Eq(Func('P', (Const('a'),)), Numeral(Fraction(1, 3)))

    nz_formula = parse_formula('NZ(3*a)')
    assert nz_formula == Pred('NZ', (Func('*', (Numeral(Fraction(3, 1)), Const('a'))),))

    complex_eq = parse_formula('(3*a*a-12*a)/(3*a)=a-4')
    assert isinstance(complex_eq, Eq)
    assert isinstance(complex_eq.left, Func)
    assert complex_eq.left.fname == '/'
    numerator, denominator = complex_eq.left.args
    assert denominator == Func('*', (Numeral(Fraction(3, 1)), Const('a')))
    assert isinstance(numerator, Func)

    equality_with_pred = parse_formula('P(c)=1-P(a)-P(b)')
    assert isinstance(equality_with_pred, Eq)
    assert equality_with_pred.left == Func('P', (Const('c'),))
    assert isinstance(equality_with_pred.right, Func)
