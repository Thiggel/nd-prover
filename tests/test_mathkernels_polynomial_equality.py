from .helpers import MathKernels, parse_formula


def test_mathkernels_polynomial_equality():
    eq = parse_formula('3*a*a - 12*a = 3*a*(a - 4)')
    assert MathKernels.polynomial_equal(eq.left, eq.right)
