from sympy.assumptions.newask import newask

from sympy import symbols, Q, assuming, Implies

from sympy.utilities.pytest import raises

x, y = symbols('x y')

def test_newask():
    # No relevant facts
    assert newask(Q.real(x), Q.real(x)) is True
    assert newask(Q.real(x), ~Q.real(x)) is False
    assert newask(Q.real(x)) is None

    assert newask(Q.real(x), Q.positive(x)) is True
    assert newask(Q.positive(x), Q.real(x)) is None
    assert newask(Q.real(x), ~Q.positive(x)) is None
    assert newask(Q.positive(x), ~Q.real(x)) is False

    raises(ValueError, lambda: newask(Q.real(x), Q.real(x) & ~Q.real(x)))

    with assuming(Q.positive(x)):
        assert newask(Q.real(x)) is True
        assert newask(~Q.positive(x)) is False
        raises(ValueError, lambda: newask(Q.real(x), ~Q.positive(x)))

    assert newask(Q.zero(x), Q.nonzero(x)) is False
    assert newask(Q.positive(x), Q.zero(x)) is False
    assert newask(Q.real(x), Q.zero(x)) is True
    assert newask(Q.zero(x), Q.zero(x*y)) is None
    assert newask(Q.zero(x*y), Q.zero(x))

def test_zero():
    """
    Everything in this test doesn't work with ask, and most things would be
    very difficult or impossible to make work under the current handlers
    model.
    """
    assert newask(Q.zero(x) | Q.zero(y), Q.zero(x*y)) is True
    assert newask(Q.zero(x*y), Q.zero(x) | Q.zero(y)) is True

    assert newask(Implies(Q.zero(x), Q.zero(x*y))) is True

    # This one in particular requires computing the fixed-point of the
    # relevant facts, because going from Q.nonzero(x*y) -> ~Q.zero(x*y) and
    # Q.zero(x*y) -> Equivalent(Q.zero(x*y), Q.zero(x) | Q.zero(y)) takes two
    # steps.

    assert newask(Q.zero(x) | Q.zero(y), Q.nonzero(x*y)) is False