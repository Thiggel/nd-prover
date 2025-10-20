import unittest
from fractions import Fraction

from nd_prover import *
from nd_prover.logic import (
    FOL,
    Justification,
    JustificationError,
    Line,
    Proof,
    Rules,
)
from nd_prover.mathkernels import MathKernels


class TestParseFormula(unittest.TestCase):
    def test_propvar(self):
        self.assertEqual(parse_formula('A'), PropVar('A'))
        self.assertEqual(parse_formula('X'), PropVar('X'))

    def test_pred(self):
        self.assertEqual(parse_formula('Pb'), Pred('P', (Const('b'),)))
        self.assertEqual(parse_formula('Fcdc'), Pred('F', (Const('c'), Const('d'), Const('c'))))
        self.assertEqual(parse_formula('Kxy'), Pred('K', (Var('x'), Var('y'))))

    def test_forall_exists(self):
        self.assertEqual(parse_formula('forallzPz'), Forall(Var('z'), Pred('P', (Var('z'),))))
        self.assertEqual(parse_formula('∀sPs'), Forall(Var('s'), Pred('P', (Var('s'),))))
        self.assertEqual(parse_formula('existszLz'), Exists(Var('z'), Pred('L', (Var('z'),))))
        self.assertEqual(parse_formula('∃yPy'), Exists(Var('y'), Pred('P', (Var('y'),))))

    def test_equality(self):
        self.assertEqual(parse_formula('a=b'), Eq(Const('a'), Const('b')))
        self.assertEqual(parse_formula('k = m'), Eq(Const('k'), Const('m')))
        with self.assertRaises(ParsingError):
            parse_formula('ab=c')
        with self.assertRaises(ParsingError):
            parse_formula('a=bc')
        with self.assertRaises(ParsingError):
            parse_formula('B=c')

    def test_falsum(self):
        self.assertEqual(parse_formula('falsum'), Falsum())
        self.assertEqual(parse_formula('⊥'), Falsum())
        self.assertEqual(parse_formula('XX'), Falsum())
        self.assertEqual(parse_formula('#'), Falsum())

    def test_not(self):
        self.assertEqual(parse_formula('~A'), Not(PropVar('A')))
        self.assertEqual(parse_formula('¬A'), Not(PropVar('A')))
        self.assertEqual(parse_formula('¬Pb'), Not(Pred('P', (Const('b'),))))

    def test_and(self):
        self.assertEqual(parse_formula('A and B'), And(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('(A ∧ B)'), And(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('A&B'), And(PropVar('A'), PropVar('B')))

    def test_or(self):
        self.assertEqual(parse_formula('A or B'), Or(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('(A∨B)'), Or(PropVar('A'), PropVar('B')))

    def test_imp(self):
        self.assertEqual(parse_formula('A -> B'), Imp(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('A⇒B'), Imp(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('A⊃B'), Imp(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('A> B'), Imp(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('(A→B)'), Imp(PropVar('A'), PropVar('B')))

    def test_iff(self):
        self.assertEqual(parse_formula('A <-> B'), Iff(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('A↔B'), Iff(PropVar('A'), PropVar('B')))
        self.assertEqual(parse_formula('A≡B'), Iff(PropVar('A'), PropVar('B')))

    def test_box_dia(self):
        self.assertEqual(parse_formula('boxA'), Box(PropVar('A')))
        self.assertEqual(parse_formula('[]A'), Box(PropVar('A')))
        self.assertEqual(parse_formula('□A'), Box(PropVar('A')))
        self.assertEqual(parse_formula('diaB'), Dia(PropVar('B')))
        self.assertEqual(parse_formula('<>C'), Dia(PropVar('C')))
        self.assertEqual(parse_formula('♢C'), Dia(PropVar('C')))

    def test_compound(self):
        self.assertEqual(
            parse_formula('(A and (B or C))'),
            And(PropVar('A'), Or(PropVar('B'), PropVar('C')))
        )
        self.assertEqual(
            parse_formula('¬(A→(B∧C))'),
            Not(Imp(PropVar('A'), And(PropVar('B'), PropVar('C'))))
        )
        self.assertEqual(
            parse_formula('(A∧B)→(C∨¬D)'),
            Imp(And(PropVar('A'), PropVar('B')), Or(PropVar('C'), Not(PropVar('D'))))
        )
        self.assertEqual(
            parse_formula('∀x(Px→Qx)'),
            Forall(Var('x'), Imp(Pred('P', (Var('x'),)), Pred('Q', (Var('x'),))))
        )
        self.assertEqual(
            parse_formula('□(A↔¬B)'),
            Box(Iff(PropVar('A'), Not(PropVar('B'))))
        )
        self.assertEqual(
            parse_formula('¬¬A'),
            Not(Not(PropVar('A')))
        )

    def test_strip_parens(self):
        self.assertEqual(parse_formula('(((A)))'), PropVar('A'))
        self.assertEqual(parse_formula('((A∧B))'), And(PropVar('A'), PropVar('B')))

    def test_invalid(self):
        with self.assertRaises(ParsingError):
            parse_formula('A=')
        with self.assertRaises(ParsingError):
            parse_formula('')
        with self.assertRaises(ParsingError):
            parse_formula('()')
        with self.assertRaises(ParsingError):
            parse_formula('AB')
        with self.assertRaises(ParsingError):
            parse_formula('A∧')
        with self.assertRaises(ParsingError):
            parse_formula('∀APa')

    def test_arithmetic_terms(self):
        formula = parse_formula('P(a)=1/3')
        self.assertEqual(
            formula,
            Eq(Func('P', (Const('a'),)), Numeral(Fraction(1, 3)))
        )

        nz_formula = parse_formula('NZ(3*a)')
        self.assertEqual(
            nz_formula,
            Pred('NZ', (Func('*', (Numeral(Fraction(3, 1)), Const('a'))),))
        )

        complex_eq = parse_formula('(3*a*a-12*a)/(3*a)=a-4')
        self.assertIsInstance(complex_eq, Eq)
        self.assertIsInstance(complex_eq.left, Func)
        self.assertEqual(complex_eq.left.fname, '/')
        numerator, denominator = complex_eq.left.args
        self.assertEqual(denominator, Func('*', (Numeral(Fraction(3, 1)), Const('a'))))
        self.assertIsInstance(numerator, Func)

        equality_with_pred = parse_formula('P(c)=1-P(a)-P(b)')
        self.assertIsInstance(equality_with_pred, Eq)
        self.assertEqual(equality_with_pred.left, Func('P', (Const('c'),)))
        self.assertIsInstance(equality_with_pred.right, Func)


class TestParseRule(unittest.TestCase):
    def test_alg_rule(self):
        self.assertEqual(parse_rule('ALG').name, 'ALG')

    def test_ai_alias(self):
        self.assertEqual(parse_rule('AI').name, '∀I')

    def test_arrow_elim_alias(self):
        self.assertEqual(parse_rule('->E').name, '→E')


class TestMathKernels(unittest.TestCase):
    def test_eval_rational(self):
        eq = parse_formula('1 - 1/3 - 5/12 = 0')
        value = MathKernels.eval_rational(eq.left)
        self.assertEqual(value, Numeral(Fraction(1, 4)))

    def test_polynomial_equality(self):
        eq = parse_formula('3*a*a - 12*a = 3*a*(a - 4)')
        self.assertTrue(MathKernels.polynomial_equal(eq.left, eq.right))

    def test_cancel_valid(self):
        fraction_eq = parse_formula('(3*a*(a-4))/(3*a) = a - 4')
        numerator, denominator = fraction_eq.left.args
        self.assertTrue(MathKernels.cancel_valid(numerator, denominator, fraction_eq.right))

    def test_equations_equivalent_with_functions(self):
        original = parse_formula('P(a) + P(b) + P(c) = 1')
        rearranged = parse_formula('P(c) = 1 - P(a) - P(b)')
        self.assertTrue(MathKernels.equations_equivalent(original, rearranged))


class TestALGRule(unittest.TestCase):
    def setUp(self):
        self.eq_line = parse_formula('P(a) + P(b) + P(c) = 1')
        self.rearranged = parse_formula('P(c) = 1 - P(a) - P(b)')

    def test_alg_accepts_rearrangement_with_citation(self):
        line = Line(3, self.eq_line, Justification(Rules.PR, ()))
        result = FOL.ALG([line], self.rearranged)
        self.assertEqual(result, [self.rearranged])

    def test_alg_accepts_ground_identity_without_citation(self):
        identity = parse_formula('2/3 + 1/6 = 5/6')
        self.assertEqual(FOL.ALG([], identity), [identity])


class TestARITHRule(unittest.TestCase):
    def test_arith_ground_identity(self):
        conclusion = parse_formula('1 - 1/3 - 5/12 = 1/4')
        self.assertEqual(FOL.ARITH([], conclusion), [conclusion])

    def test_arith_with_citation(self):
        cited_eq = parse_formula('P(c) = 1 - 1/3 - 5/12')
        conclusion = parse_formula('P(c) = 1/4')
        line = Line(7, cited_eq, Justification(Rules.PR, ()))
        self.assertEqual(FOL.ARITH([line], conclusion), [conclusion])

    def test_arith_with_citation_symmetric(self):
        cited_eq = parse_formula('1 - 1/3 - 5/12 = P(c)')
        conclusion = parse_formula('1/4 = P(c)')
        line = Line(8, cited_eq, Justification(Rules.PR, ()))
        self.assertEqual(FOL.ARITH([line], conclusion), [conclusion])


class TestErrorReporting(unittest.TestCase):
    def test_error_messages_include_line_number(self):
        premises = [
            parse_formula('P(a) = 1/3'),
            parse_formula('P(b) = 5/12'),
            parse_formula('P(a) + P(b) + P(c) = 1'),
        ]
        conclusion = parse_formula('P(c) = 1/4')
        proof = Proof(FOL, premises, conclusion)

        with self.assertRaises(JustificationError) as ctx:
            proof.add_line(
                parse_formula('P(c) = 1 - P(a) - P(b)'),
                Justification(parse_rule('ALG'), (1, 2)),
            )

        self.assertTrue(str(ctx.exception).startswith('Line 4:'))

if __name__ == '__main__':
    unittest.main()
