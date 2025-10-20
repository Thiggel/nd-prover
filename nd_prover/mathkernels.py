from __future__ import annotations

from fractions import Fraction
from typing import Dict, Tuple

from .logic import Const, Func, Numeral, Term, Var


Monomial = Tuple[Tuple[str, int], ...]
Polynomial = Dict[Monomial, Fraction]


class MathKernels:
    @staticmethod
    def eval_rational(term: Term) -> Numeral:
        value = MathKernels._eval_fraction(term)
        return Numeral(Fraction(value))

    @staticmethod
    def equal_terms(left: Term, right: Term) -> bool:
        if left == right:
            return True
        try:
            return MathKernels._eval_fraction(left) == MathKernels._eval_fraction(right)
        except ValueError:
            pass
        try:
            return MathKernels._to_poly(left) == MathKernels._to_poly(right)
        except ValueError:
            return left == right

    @staticmethod
    def polynomial_equal(left: Term, right: Term) -> bool:
        try:
            return MathKernels._to_poly(left) == MathKernels._to_poly(right)
        except ValueError:
            return MathKernels.equal_terms(left, right)

    @staticmethod
    def cancel_valid(numerator: Term, denominator: Term, simplified: Term) -> bool:
        product = Func('*', (denominator, simplified))
        return MathKernels.polynomial_equal(numerator, product)

    @staticmethod
    def _eval_fraction(term: Term) -> Fraction:
        match term:
            case Numeral(value=value):
                return value
            case Func(fname='+', args=(left, right)):
                return MathKernels._eval_fraction(left) + MathKernels._eval_fraction(right)
            case Func(fname='-', args=(left, right)):
                return MathKernels._eval_fraction(left) - MathKernels._eval_fraction(right)
            case Func(fname='-', args=(inner,)):
                return -MathKernels._eval_fraction(inner)
            case Func(fname='*', args=(left, right)):
                return MathKernels._eval_fraction(left) * MathKernels._eval_fraction(right)
            case Func(fname='/', args=(left, right)):
                denominator = MathKernels._eval_fraction(right)
                if denominator == 0:
                    raise ValueError('division by zero')
                return MathKernels._eval_fraction(left) / denominator
            case Const() | Var():
                raise ValueError('non-ground term')
        raise ValueError('unsupported term for arithmetic evaluation')

    @staticmethod
    def _to_poly(term: Term) -> Polynomial:
        match term:
            case Numeral(value=value):
                return MathKernels._poly_constant(value)
            case Const(name=name) | Var(name=name):
                return MathKernels._poly_variable(name)
            case Func(fname='+', args=(left, right)):
                return MathKernels._poly_add(MathKernels._to_poly(left), MathKernels._to_poly(right))
            case Func(fname='-', args=(left, right)):
                return MathKernels._poly_add(
                    MathKernels._to_poly(left), MathKernels._poly_neg(MathKernels._to_poly(right))
                )
            case Func(fname='-', args=(inner,)):
                return MathKernels._poly_neg(MathKernels._to_poly(inner))
            case Func(fname='*', args=(left, right)):
                return MathKernels._poly_mul(MathKernels._to_poly(left), MathKernels._to_poly(right))
            case Func(fname='/', args=(left, right)):
                denominator = MathKernels._eval_fraction(right)
                if denominator == 0:
                    raise ValueError('division by zero')
                return MathKernels._poly_scale(MathKernels._to_poly(left), Fraction(1, 1) / denominator)
        raise ValueError('unsupported term for polynomial conversion')

    @staticmethod
    def _poly_constant(value: Fraction) -> Polynomial:
        return {(): Fraction(value)}

    @staticmethod
    def _poly_variable(name: str) -> Polynomial:
        return {((name, 1),): Fraction(1)}

    @staticmethod
    def _poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
        result = dict(left)
        for mon, coeff in right.items():
            result[mon] = result.get(mon, Fraction(0)) + coeff
        return MathKernels._poly_clean(result)

    @staticmethod
    def _poly_neg(poly: Polynomial) -> Polynomial:
        return {mon: -coeff for mon, coeff in poly.items()}

    @staticmethod
    def _poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
        result: Polynomial = {}
        for m1, c1 in left.items():
            for m2, c2 in right.items():
                mon = MathKernels._combine_monomials(m1, m2)
                result[mon] = result.get(mon, Fraction(0)) + c1 * c2
        return MathKernels._poly_clean(result)

    @staticmethod
    def _poly_scale(poly: Polynomial, factor: Fraction) -> Polynomial:
        if factor == 0:
            return {(): Fraction(0)}
        return MathKernels._poly_clean({mon: coeff * factor for mon, coeff in poly.items()})

    @staticmethod
    def _poly_clean(poly: Polynomial) -> Polynomial:
        cleaned = {mon: coeff for mon, coeff in poly.items() if coeff != 0}
        return cleaned or {(): Fraction(0)}

    @staticmethod
    def _combine_monomials(m1: Monomial, m2: Monomial) -> Monomial:
        powers: Dict[str, int] = {}
        for name, power in m1:
            powers[name] = powers.get(name, 0) + power
        for name, power in m2:
            powers[name] = powers.get(name, 0) + power
        return tuple(sorted((name, power) for name, power in powers.items() if power))
