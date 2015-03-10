r"""
Examples of semigroups
"""
#*****************************************************************************
#  Copyright (C) 2008-2009 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.element_wrapper import ElementWrapper
from sage.categories.all import Semigroups
from sage.sets.family import Family

class LeftZeroSemigroup(UniqueRepresentation, Parent):
    r"""
    An example of a semigroup.

    This class illustrates a minimal implementation of a semigroup.

    EXAMPLES::

        sage: S = Semigroups().example(); S
        An example of a semigroup: the left zero semigroup

    This is the semigroup that contains all sorts of objects::

        sage: S.some_elements()
        [3, 42, 'a', 3.4, 'raton laveur']

    with product rule given by $a \times b = a$ for all $a, b$::

        sage: S('hello') * S('world')
        'hello'
        sage: S(3)*S(1)*S(2)
        3
        sage: S(3)^12312321312321
        3

    TESTS::

        sage: TestSuite(S).run(verbose = True)
        running ._test_an_element() . . . pass
        running ._test_associativity() . . . pass
        running ._test_category() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_pickling() . . . pass
        running ._test_some_elements() . . . pass
    """
    def __init__(self):
        r"""
        The left zero semigroup

        EXAMPLES::

            sage: S = Semigroups().example(); S
            An example of a semigroup: the left zero semigroup

        TESTS::

            sage: TestSuite(S).run()

        """
        Parent.__init__(self, category = Semigroups())

    def _repr_(self):
        r"""

        EXAMPLES::

            sage: Semigroups().example()._repr_()
            'An example of a semigroup: the left zero semigroup'

        """
        return "An example of a semigroup: the left zero semigroup"

    def product(self, x, y):
        r"""
        Returns the product of ``x`` and ``y`` in the semigroup, as per
        :meth:`Semigroups.ParentMethods.product`.

        EXAMPLES::

            sage: S = Semigroups().example()
            sage: S('hello') * S('world')
            'hello'
            sage: S(3)*S(1)*S(2)
            3

        """
        assert x in self
        assert y in self
        return x

    def an_element(self):
        r"""
        Returns an element of the semigroup.

        EXAMPLES::

            sage: Semigroups().example().an_element()
            42

        """
        return self(42)

    def some_elements(self):
        r"""
        Returns a list of some elements of the semigroup.

        EXAMPLES::

            sage: Semigroups().example().some_elements()
            [3, 42, 'a', 3.4, 'raton laveur']

        """
        return [self(i) for i in [3, 42, "a", 3.4, "raton laveur"]]

    class Element(ElementWrapper):
        def is_idempotent(self):
            r"""
            Trivial implementation of ``Semigroups.Element.is_idempotent``
            since all elements of this semigroup are idempotent!

            EXAMPLES::

                sage: S = Semigroups().example()
                sage: S.an_element().is_idempotent()
                True
                sage: S(17).is_idempotent()
                True

            """
            return True


class FreeSemigroup(UniqueRepresentation, Parent):
    r"""
    An example of semigroup.

    The purpose of this class is to provide a minimal template for
    implementing of a semigroup.

    EXAMPLES::

        sage: S = Semigroups().example("free"); S
        An example of a semigroup: the free semigroup generated by ('a', 'b', 'c', 'd')

    This is the free semigroup generated by::

        sage: S.semigroup_generators()
        Family ('a', 'b', 'c', 'd')

    and with product given by contatenation::

        sage: S('dab') * S('acb')
        'dabacb'

    TESTS::

        sage: TestSuite(S).run(verbose = True)
        running ._test_an_element() . . . pass
        running ._test_associativity() . . . pass
        running ._test_category() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_pickling() . . . pass
        running ._test_some_elements() . . . pass
    """
    def __init__(self, alphabet=('a','b','c','d')):
        r"""
        The free semigroup.

        INPUT::

        - ``alphabet`` -- a tuple of strings: the generators of the semigroup

        EXAMPLES::

            sage: from sage.categories.examples.semigroups import FreeSemigroup
            sage: F = FreeSemigroup(('a','b','c')); F
            An example of a semigroup: the free semigroup generated by ('a', 'b', 'c')

        TESTS::

            sage: F == loads(dumps(F))
            True

        """
        self.alphabet = alphabet
        Parent.__init__(self, category = Semigroups().FinitelyGenerated())

    def _repr_(self):
        r"""
        EXAMPLES::

            sage: from sage.categories.examples.semigroups import FreeSemigroup
            sage: FreeSemigroup(('a','b','c'))._repr_()
            "An example of a semigroup: the free semigroup generated by ('a', 'b', 'c')"

        """
        return "An example of a semigroup: the free semigroup generated by %s"%(self.alphabet,)

    def product(self, x, y):
        r"""
        Returns the product of ``x`` and ``y`` in the semigroup, as per
        :meth:`Semigroups.ParentMethods.product`.

        EXAMPLES::

            sage: F = Semigroups().example('free')
            sage: F.an_element() * F('a')^5
            'abcdaaaaa'

        """
        assert x in self
        assert y in self
        return self(x.value + y.value)

    @cached_method
    def semigroup_generators(self):
        r"""
        Returns the generators of the semigroup.

        EXAMPLES::

            sage: F = Semigroups().example('free')
            sage: F.semigroup_generators()
            Family ('a', 'b', 'c', 'd')

        """
        return Family([self(i) for i in self.alphabet])

    def an_element(self):
        r"""
        Returns an element of the semigroup.

        EXAMPLES::

            sage: F = Semigroups().example('free')
            sage: F.an_element()
            'abcd'

        """
        return self(''.join(self.alphabet))

    def _element_constructor_(self, x):
        r"""
        Construct an element of this semigroup from the data ``x``.

        INPUT::

        - ``x`` -- a string

        EXAMPLES::

            sage: F = Semigroups().example('free'); F
            An example of a semigroup: the free semigroup generated by ('a', 'b', 'c', 'd')
            sage: F._element_constructor_('a')
            'a'
            sage: F._element_constructor_('bad')
            'bad'

        TESTS::

            sage: F._element_constructor_('z')
            Traceback (most recent call last):
            ...
                assert a in self.alphabet
            AssertionError
            sage: bad = F._element_constructor_('bad'); bad
            'bad'
            sage: bad in F
            True


        TESTS::

            sage: S = Semigroups().Subquotients().example()
            sage: type(S._element_constructor_(17))
            <class 'sage.categories.examples.semigroups.QuotientOfLeftZeroSemigroup_with_category.element_class'>

        """
        for a in x:
            assert a in self.alphabet
        return self.element_class(self, x)

    class Element(ElementWrapper):
        r"""
        The class for elements of the free semigroup.
        """
        wrapped_class = str


class QuotientOfLeftZeroSemigroup(UniqueRepresentation, Parent):
    r"""
    Example of a quotient semigroup

    EXAMPLES::

        sage: S = Semigroups().Subquotients().example(); S
        An example of a (sub)quotient semigroup: a quotient of the left zero semigroup

    This is the quotient of::

        sage: S.ambient()
        An example of a semigroup: the left zero semigroup

    obtained by setting `x=42` for any `x\geq 42`::

        sage: S(100)
        42
        sage: S(100) == S(42)
        True

    The product is inherited from the ambient semigroup::

        sage: S(1)*S(2) == S(1)
        True

    TESTS::

        sage: TestSuite(S).run(verbose = True)
        running ._test_an_element() . . . pass
        running ._test_associativity() . . . pass
        running ._test_category() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_pickling() . . . pass
        running ._test_some_elements() . . . pass
    """
    def _element_constructor_(self, x):
        r"""
        Convert ``x`` into an element of this semigroup.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: S._element_constructor_(17)
            17

        TESTS::

            sage: S = Semigroups().Subquotients().example()
            sage: type(S._element_constructor_(17))
            <class 'sage.categories.examples.semigroups.QuotientOfLeftZeroSemigroup_with_category.element_class'>

        """
        return self.retract(self.ambient()(x))

    def __init__(self, category = None):
        r"""
        This quotient of the left zero semigroup of integers obtained by
        setting `x=42` for any `x\geq 42`.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example(); S
            An example of a (sub)quotient semigroup: a quotient of the left zero semigroup
            sage: S.ambient()
            An example of a semigroup: the left zero semigroup
            sage: S(100)
            42
            sage: S(100) == S(42)
            True
            sage: S(1)*S(2) == S(1)
            True

        TESTS::

            sage: TestSuite(S).run()
        """
        if category is None:
            category = Semigroups().Quotients()
        Parent.__init__(self, category = category)

    def _repr_(self):
        r"""

        EXAMPLES::

            sage: Semigroups().Subquotients().example()._repr_()
            'An example of a (sub)quotient semigroup: a quotient of the left zero semigroup'

        """
        return "An example of a (sub)quotient semigroup: a quotient of the left zero semigroup"

    def ambient(self):
        r"""
        Returns the ambient semigroup.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: S.ambient()
            An example of a semigroup: the left zero semigroup

        """
        return Semigroups().example()

    def lift(self, x):
        r"""
        Lift the element ``x`` into the ambient semigroup.

        INPUT::

        - ``x`` -- an element of ``self``.

        OUTPUT::

        - an element of ``self.ambient()``.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: x = S.an_element(); x
            42
            sage: S.lift(x)
            42
            sage: S.lift(x) in S.ambient()
            True
            sage: y = S.ambient()(100); y
            100
            sage: S.lift(S(y))
            42

        """
        assert x in self
        return x.value

    def the_answer(self):
        r"""
        Returns the Answer to Life, the Universe, and Everything as an
        element of this semigroup.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: S.the_answer()
            42

        """
        return self.retract(self.ambient()(42))

    def an_element(self):
        r"""
        Returns an element of the semigroup.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: S.an_element()
            42

        """
        return self.the_answer()

    def some_elements(self):
        r"""
        Returns a list of some elements of the semigroup.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: S.some_elements()
            [1, 2, 3, 8, 42, 42]

        """
        return [self.retract(self.ambient()(i))
                for i in [1, 2, 3, 8, 42, 100]]

    def retract(self, x):
        r"""
        Returns the retract ``x`` onto an element of this semigroup.

        INPUT::

        - ``x`` -- an element of the ambient semigroup (``self.ambient()``).

        OUTPUT::

        - an element of ``self``.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: L = S.ambient()
            sage: S.retract(L(17))
            17
            sage: S.retract(L(42))
            42
            sage: S.retract(L(171))
            42

        TESTS::

            sage: S.retract(L(171)) in S
            True

        """
        from sage.rings.integer_ring import ZZ
        assert x in self.ambient() and x.value in ZZ
        if x.value > 42:
            return self.the_answer()
        else:
            return self.element_class(self, x)

    class Element(ElementWrapper):
        pass

class IncompleteSubquotientSemigroup(UniqueRepresentation,Parent):
    def __init__(self, category = None):
        r"""
        An incompletely implemented subquotient semigroup, for testing purposes

        EXAMPLES::

            sage: S = sage.categories.examples.semigroups.IncompleteSubquotientSemigroup()
            sage: S
            A subquotient of An example of a semigroup: the left zero semigroup

        TESTS::

            sage: S._test_not_implemented_methods()
            Traceback (most recent call last):
              ...
            AssertionError: Not implemented method: lift

            sage: TestSuite(S).run(verbose = True)
            running ._test_an_element() . . . pass
            running ._test_associativity() . . . fail
            Traceback (most recent call last):
              ...
            NotImplementedError: <abstract method retract at ...>
            ------------------------------------------------------------
            running ._test_category() . . . pass
            running ._test_elements() . . .
              Running the test suite of self.an_element()
              running ._test_category() . . . pass
              running ._test_eq() . . . pass
              running ._test_not_implemented_methods() . . . pass
              running ._test_pickling() . . . pass
              pass
            running ._test_elements_eq_reflexive() . . . pass
            running ._test_elements_eq_symmetric() . . . pass
            running ._test_elements_eq_transitive() . . . pass
            running ._test_elements_neq() . . . pass
            running ._test_eq() . . . pass
            running ._test_not_implemented_methods() . . . fail
            Traceback (most recent call last):
              ...
            AssertionError: Not implemented method: lift
            ------------------------------------------------------------
            running ._test_pickling() . . . pass
            running ._test_some_elements() . . . pass
            The following tests failed: _test_associativity, _test_not_implemented_methods
        """
        Parent.__init__(self, category=Semigroups().Subquotients().or_subcategory(category))

    def ambient(self):
        r"""
        Returns the ambient semigroup.

        EXAMPLES::

            sage: S = Semigroups().Subquotients().example()
            sage: S.ambient()
            An example of a semigroup: the left zero semigroup

        """
        return Semigroups().example()

    class Element(ElementWrapper):
        pass
