from .helpers import Fraction, MathKernels, Numeral, parse_formula


def test_mathkernels_eval_rational():
    eq = parse_formula('1 - 1/3 - 5/12 = 0')
    value = MathKernels.eval_rational(eq.left)
    assert value == Numeral(Fraction(1, 4))
