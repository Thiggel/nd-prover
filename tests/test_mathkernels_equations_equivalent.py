from .helpers import MathKernels, parse_formula


def test_mathkernels_equations_equivalent_with_functions():
    original = parse_formula('P(a) + P(b) + P(c) = 1')
    rearranged = parse_formula('P(c) = 1 - P(a) - P(b)')
    assert MathKernels.equations_equivalent(original, rearranged)
