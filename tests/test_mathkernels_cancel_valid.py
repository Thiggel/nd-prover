from .helpers import MathKernels, parse_formula


def test_mathkernels_cancel_valid():
    fraction_eq = parse_formula('(3*a*(a-4))/(3*a) = a - 4')
    numerator, denominator = fraction_eq.left.args
    assert MathKernels.cancel_valid(numerator, denominator, fraction_eq.right)
