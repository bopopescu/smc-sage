r"""
Finite semilattices and lattices

This module implements finite (semi)lattices. It defines:

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :class:`FiniteJoinSemilattice` | A class for finite join semilattices.
    :class:`FiniteMeetSemilattice` | A class for finite meet semilattices.
    :class:`FiniteLatticePoset` | A class for finite lattices.
    :meth:`JoinSemilattice` | Construct a join semi-lattice.
    :meth:`LatticePoset` | Construct a lattice.
    :meth:`MeetSemilattice` | Construct a meet semi-lattice.

List of (semi)lattice methods
-----------------------------

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~FiniteLatticePoset.complements` | Return the list of complements of an element, or the dictionary of complements for all elements.
    :meth:`~FiniteLatticePoset.maximal_sublattices` | Return maximal sublattices of the lattice.
    :meth:`~FiniteLatticePoset.frattini_sublattice` | Return the intersection of maximal sublattices.
    :meth:`~FiniteLatticePoset.is_atomic` | Return ``True`` if the lattice is atomic.
    :meth:`~FiniteLatticePoset.is_complemented` | Return ``True`` if the lattice is complemented.
    :meth:`~FiniteLatticePoset.is_distributive` | Return ``True`` if the lattice is distributive.
    :meth:`~FiniteLatticePoset.is_lower_semimodular` | Return ``True`` if the lattice is lower semimodular.
    :meth:`~FiniteLatticePoset.is_modular` | Return ``True`` if the lattice is lower modular.
    :meth:`~FiniteLatticePoset.is_modular_element` | Return ``True`` if given element is modular in the lattice.
    :meth:`~FiniteLatticePoset.is_upper_semimodular` | Return ``True`` if the lattice is upper semimodular.
    :meth:`~FiniteLatticePoset.is_planar` | Return ``True`` if the lattice is *upward* planar, and ``False`` otherwise.
    :meth:`~FiniteLatticePoset.is_supersolvable` | Return ``True`` if the lattice is supersolvable.
    :meth:`~FiniteJoinSemilattice.join` | Return the join of given elements in the join semi-lattice.
    :meth:`~FiniteJoinSemilattice.join_matrix` | Return the matrix of joins of all elements of the join semi-lattice.
    :meth:`~FiniteMeetSemilattice.meet` | Return the meet of given elements in the meet semi-lattice.
    :meth:`~FiniteMeetSemilattice.meet_matrix` | Return the matrix of meets of all elements of the meet semi-lattice.
"""
#*****************************************************************************
#       Copyright (C) 2008 Peter Jipsen <jipsen@chapman.edu>,
#                          Franco Saliola <saliola@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.categories.finite_lattice_posets import FiniteLatticePosets
from sage.combinat.posets.posets import Poset, FinitePoset
from sage.combinat.posets.elements import (LatticePosetElement,
                                           MeetSemilatticeElement,
                                           JoinSemilatticeElement)

####################################################################################

def MeetSemilattice(data, *args, **options):
    r"""
    Construct a meet semi-lattice from various forms of input data.

    INPUT:

    - ``data``, ``*args``, ``**options`` -- data and options that will
      be passed down to :func:`Poset` to construct a poset that is
      also a meet semilattice.

    .. seealso:: :func:`Poset`, :func:`JoinSemilattice`, :func:`LatticePoset`

    EXAMPLES:

    Using data that defines a poset::

          sage: MeetSemilattice([[1,2],[3],[3]])
          Finite meet-semilattice containing 4 elements

          sage: MeetSemilattice([[1,2],[3],[3]], cover_relations = True)
          Finite meet-semilattice containing 4 elements

    Using a previously constructed poset::

          sage: P = Poset([[1,2],[3],[3]])
          sage: L = MeetSemilattice(P); L
          Finite meet-semilattice containing 4 elements
          sage: type(L)
          <class 'sage.combinat.posets.lattices.FiniteMeetSemilattice_with_category'>

    If the data is not a lattice, then an error is raised::

          sage: elms = [1,2,3,4,5,6,7]
          sage: rels = [[1,2],[3,4],[4,5],[2,5]]
          sage: MeetSemilattice((elms, rels))
          Traceback (most recent call last):
          ...
          ValueError: Not a meet semilattice.
    """
    if isinstance(data,FiniteMeetSemilattice) and len(args) == 0 and len(options) == 0:
        return data
    P = Poset(data, *args, **options)
    if not P.is_meet_semilattice():
        raise ValueError("Not a meet semilattice.")
    return FiniteMeetSemilattice(P)

class FiniteMeetSemilattice(FinitePoset):
    """
    .. note::
        We assume that the argument passed to MeetSemilattice is the poset
        of a meet-semilattice (i.e. a poset with greatest lower bound for
        each pair of elements).

    TESTS::

        sage: M = MeetSemilattice([[1,2],[3],[3]])
        sage: TestSuite(M).run()

    ::

        sage: P = Poset([[1,2],[3],[3]])
        sage: M = MeetSemilattice(P)
        sage: TestSuite(M).run()

    """
    Element = MeetSemilatticeElement

    def _repr_(self):
        r"""
        TESTS::

            sage: M = MeetSemilattice([[1,2],[3],[3]])
            sage: M._repr_()
            'Finite meet-semilattice containing 4 elements'

        ::

            sage: P = Poset([[1,2],[3],[3]])
            sage: M = MeetSemilattice(P)
            sage: M._repr_()
            'Finite meet-semilattice containing 4 elements'
        """
        s  = "Finite meet-semilattice containing %s elements" %self._hasse_diagram.order()
        if self._with_linear_extension:
            s += " with distinguished linear extension"
        return s

    def meet_matrix(self):
        """
        Return a matrix whose ``(i,j)`` entry is ``k``, where
        ``self.linear_extension()[k]`` is the meet (greatest lower bound) of
        ``self.linear_extension()[i]`` and ``self.linear_extension()[j]``.

        EXAMPLES::

            sage: P = LatticePoset([[1,3,2],[4],[4,5,6],[6],[7],[7],[7],[]], facade = False)
            sage: M = P.meet_matrix(); M
            [0 0 0 0 0 0 0 0]
            [0 1 0 1 0 0 0 1]
            [0 0 2 2 2 0 2 2]
            [0 1 2 3 2 0 2 3]
            [0 0 2 2 4 0 2 4]
            [0 0 0 0 0 5 5 5]
            [0 0 2 2 2 5 6 6]
            [0 1 2 3 4 5 6 7]
            sage: M[P(4).vertex,P(3).vertex] == P(0).vertex
            True
            sage: M[P(5).vertex,P(2).vertex] == P(2).vertex
            True
            sage: M[P(5).vertex,P(2).vertex] == P(5).vertex
            False
        """
        return self._hasse_diagram.meet_matrix()

    def meet(self, x, y=None):
        r"""
        Return the meet of given elements in the lattice.

        EXAMPLES::

            sage: D = Posets.DiamondPoset(5)
            sage: D.meet(1, 2)
            0
            sage: D.meet(1, 1)
            1
            sage: D.meet(1, 0)
            0
            sage: D.meet(1, 4)
            1

        Using list of elements as an argument. Meet of empty list is
        the bottom element::

            sage: B4=Posets.BooleanLattice(4)
            sage: B4.meet([3,5,6])
            0
            sage: B4.meet([])
            15

        Test that this method also works for facade lattices::

            sage: L = LatticePoset([[1,2],[3],[3]], facade = True)
            sage: L.meet(2, 3)
            2
            sage: L.meet(1, 2)
            0

        """
        if y is not None: # Handle basic case fast
            i, j = map(self._element_to_vertex, (x,y))
            return self._vertex_to_element(self._hasse_diagram._meet[i,j])
        m = self.cardinality()-1 # m = top element
        for i in (self._element_to_vertex(_) for _ in x):
            m = self._hasse_diagram._meet[i, m]
        return self._vertex_to_element(m)

####################################################################################

def JoinSemilattice(data, *args, **options):
    r"""
    Construct a join semi-lattice from various forms of input data.

    INPUT:

    - ``data``, ``*args``, ``**options`` -- data and options that will
      be passed down to :func:`Poset` to construct a poset that is
      also a join semilattice.

    .. seealso:: :func:`Poset`, :func:`MeetSemilattice`, :func:`LatticePoset`

    EXAMPLES:

    Using data that defines a poset::

          sage: JoinSemilattice([[1,2],[3],[3]])
          Finite join-semilattice containing 4 elements

          sage: JoinSemilattice([[1,2],[3],[3]], cover_relations = True)
          Finite join-semilattice containing 4 elements

    Using a previously constructed poset::

          sage: P = Poset([[1,2],[3],[3]])
          sage: J = JoinSemilattice(P); J
          Finite join-semilattice containing 4 elements
          sage: type(J)
          <class 'sage.combinat.posets.lattices.FiniteJoinSemilattice_with_category'>

    If the data is not a lattice, then an error is raised::

          sage: elms = [1,2,3,4,5,6,7]
          sage: rels = [[1,2],[3,4],[4,5],[2,5]]
          sage: JoinSemilattice((elms, rels))
          Traceback (most recent call last):
          ...
          ValueError: Not a join semilattice.
    """
    if isinstance(data,FiniteJoinSemilattice) and len(args) == 0 and len(options) == 0:
        return data
    P = Poset(data, *args, **options)
    if not P.is_join_semilattice():
        raise ValueError("Not a join semilattice.")
    return FiniteJoinSemilattice(P)

class FiniteJoinSemilattice(FinitePoset):
    """
    We assume that the argument passed to FiniteJoinSemilattice is the
    poset of a join-semilattice (i.e. a poset with least upper bound
    for each pair of elements).

    TESTS::

        sage: J = JoinSemilattice([[1,2],[3],[3]])
        sage: TestSuite(J).run()

    ::

        sage: P = Poset([[1,2],[3],[3]])
        sage: J = JoinSemilattice(P)
        sage: TestSuite(J).run()

    """
    Element = JoinSemilatticeElement

    def _repr_(self):
        r"""
        TESTS::

            sage: J = JoinSemilattice([[1,2],[3],[3]])
            sage: J._repr_()
            'Finite join-semilattice containing 4 elements'

        ::

            sage: P = Poset([[1,2],[3],[3]])
            sage: J = JoinSemilattice(P)
            sage: J._repr_()
            'Finite join-semilattice containing 4 elements'
        """
        s = "Finite join-semilattice containing %s elements"%self._hasse_diagram.order()
        if self._with_linear_extension:
            s += " with distinguished linear extension"
        return s

    def join_matrix(self):
        """
        Return a matrix whose ``(i,j)`` entry is ``k``, where
        ``self.linear_extension()[k]`` is the join (least upper bound) of
        ``self.linear_extension()[i]`` and ``self.linear_extension()[j]``.

        EXAMPLES::

            sage: P = LatticePoset([[1,3,2],[4],[4,5,6],[6],[7],[7],[7],[]], facade = False)
            sage: J = P.join_matrix(); J
            [0 1 2 3 4 5 6 7]
            [1 1 3 3 7 7 7 7]
            [2 3 2 3 4 6 6 7]
            [3 3 3 3 7 7 7 7]
            [4 7 4 7 4 7 7 7]
            [5 7 6 7 7 5 6 7]
            [6 7 6 7 7 6 6 7]
            [7 7 7 7 7 7 7 7]
            sage: J[P(4).vertex,P(3).vertex] == P(7).vertex
            True
            sage: J[P(5).vertex,P(2).vertex] == P(5).vertex
            True
            sage: J[P(5).vertex,P(2).vertex] == P(2).vertex
            False
        """
        return self._hasse_diagram.join_matrix()

    def join(self, x, y=None):
        r"""
        Return the join of given elements in the lattice.

        INPUT:

        -  ``x, y`` - two elements of the (semi)lattice OR

        -  ``x`` - a list or tuple of elements

        EXAMPLES::

            sage: D = Posets.DiamondPoset(5)
            sage: D.join(1, 2)
            4
            sage: D.join(1, 1)
            1
            sage: D.join(1, 4)
            4
            sage: D.join(1, 0)
            1

        Using list of elements as an argument. Join of empty list is
        the bottom element::

            sage: B4=Posets.BooleanLattice(4)
            sage: B4.join([2,4,8])
            14
            sage: B4.join([])
            0

        Test that this method also works for facade lattices::

            sage: L = LatticePoset([[1,2],[3],[3]], facade = True)
            sage: L.join(1, 0)
            1
            sage: L.join(1, 2)
            3

        """
        if y is not None: # Handle basic case fast
            i, j = map(self._element_to_vertex, (x,y))
            return self._vertex_to_element(self._hasse_diagram._join[i,j])
        j = 0 # j = bottom element
        for i in (self._element_to_vertex(_) for _ in x):
            j = self._hasse_diagram._join[i, j]
        return self._vertex_to_element(j)


####################################################################################

def LatticePoset(data, *args, **options):
    r"""
    Construct a lattice from various forms of input data.

    INPUT:

    - ``data``, ``*args``, ``**options`` -- data and options that will
      be passed down to :func:`Poset` to construct a poset that is
      also a lattice.

    OUTPUT:

        FiniteLatticePoset -- an instance of :class:`FiniteLatticePoset`

    .. seealso:: :class:`Posets`, :class:`FiniteLatticePosets`, :func:`JoinSemiLattice`, :func:`MeetSemiLattice`

    EXAMPLES:

    Using data that defines a poset::

        sage: LatticePoset([[1,2],[3],[3]])
        Finite lattice containing 4 elements

        sage: LatticePoset([[1,2],[3],[3]], cover_relations = True)
        Finite lattice containing 4 elements

    Using a previously constructed poset::

        sage: P = Poset([[1,2],[3],[3]])
        sage: L = LatticePoset(P); L
        Finite lattice containing 4 elements
        sage: type(L)
        <class 'sage.combinat.posets.lattices.FiniteLatticePoset_with_category'>

    If the data is not a lattice, then an error is raised::

        sage: elms = [1,2,3,4,5,6,7]
        sage: rels = [[1,2],[3,4],[4,5],[2,5]]
        sage: LatticePoset((elms, rels))
        Traceback (most recent call last):
        ...
        ValueError: Not a lattice.

    Creating a facade lattice::

        sage: L = LatticePoset([[1,2],[3],[3]], facade = True)
        sage: L.category()
        Join of Category of finite lattice posets and Category of finite enumerated sets and Category of facade sets
        sage: parent(L[0])
        Integer Ring
        sage: TestSuite(L).run(skip = ['_test_an_element']) # is_parent_of is not yet implemented

    """
    if isinstance(data,FiniteLatticePoset) and len(args) == 0 and len(options) == 0:
        return data
    P = Poset(data, *args, **options)
    if not P.is_lattice():
        raise ValueError("Not a lattice.")

    return FiniteLatticePoset(P, category = FiniteLatticePosets(), facade = P._is_facade)

class FiniteLatticePoset(FiniteMeetSemilattice, FiniteJoinSemilattice):
    """
    We assume that the argument passed to FiniteLatticePoset is the
    poset of a lattice (i.e. a poset with greatest lower bound and
    least upper bound for each pair of elements).

    TESTS::

        sage: L = LatticePoset([[1,2],[3],[3]])
        sage: TestSuite(L).run()

    ::

        sage: P = Poset([[1,2],[3],[3]])
        sage: L = LatticePoset(P)
        sage: TestSuite(L).run()

    """
    Element = LatticePosetElement

    def _repr_(self):
        r"""
        TESTS::

            sage: L = LatticePoset([[1,2],[3],[3]])
            sage: L._repr_()
            'Finite lattice containing 4 elements'

        ::

            sage: P = Poset([[1,2],[3],[3]])
            sage: L = LatticePoset(P)
            sage: L._repr_()
            'Finite lattice containing 4 elements'
        """
        s = "Finite lattice containing %s elements"%self._hasse_diagram.order()
        if self._with_linear_extension:
            s += " with distinguished linear extension"
        return s

    def is_distributive(self):
        r"""
        Return ``True`` if the lattice is distributive, and ``False``
        otherwise.

        A lattice `(L, \vee, \wedge)` is distributive if meet
        distributes over join: `x \wedge (y \vee z) = (x \wedge y)
        \vee (x \wedge z)` for every `x,y,z \in L` just like `x \cdot
        (y+z)=x \cdot y + x \cdot z` in normal arithmetic. For duality
        in lattices it follows that then also join distributes over
        meet.

        EXAMPLES::

            sage: L = LatticePoset({0:[1,2],1:[3],2:[3]})
            sage: L.is_distributive()
            True
            sage: L = LatticePoset({0:[1,2,3],1:[4],2:[4],3:[4]})
            sage: L.is_distributive()
            False
        """
        if self.cardinality() == 0: return True
        return (self.is_graded() and
         self.rank() == len(self.join_irreducibles()) ==
         len(self.meet_irreducibles()))

    def is_complemented(self):
        r"""
        Returns ``True`` if ``self`` is a complemented lattice, and
        ``False`` otherwise.

        EXAMPLES::

            sage: L = LatticePoset({0:[1,2,3],1:[4],2:[4],3:[4]})
            sage: L.is_complemented()
            True

            sage: L = LatticePoset({0:[1,2],1:[3],2:[3],3:[4]})
            sage: L.is_complemented()
            False
        """
        return self._hasse_diagram.is_complemented_lattice()

    def breadth(self, certificate=False):
        r"""
        Return the breadth of the lattice.

        The breadth of a lattice is the largest integer `n` such that
        any join of elements `x_1, x_2, \ldots, x_{n+1}` is join of a
        proper subset of `x_i`.

        INPUT:

        - ``certificate`` -- (boolean; default: ``False``) -- whether to
          return an integer (the breadth) or a certificate, i.e. a biggest
          set whose join differs from the join of any subset.

        EXAMPLES::

            sage: D10 = Posets.DiamondPoset(10)
            sage: D10.breadth()
            2

            sage: B3 = Posets.BooleanLattice(3)
            sage: B3.breadth()
            3
            sage: B3.breadth(certificate=True)
            [1, 2, 4]

        Smallest example of a lattice with breadth 4::

            sage: L = LatticePoset(DiGraph('O]???w?K_@S?E_??Q?@_?D??I??W?B??@??C??O?@???'))
            sage: L.breadth()
            4

        ALGORITHM:

        For a lattice to have breadth at least `n`, it must have an
        `n`-element antichain `A` with join `j`. Element `j` must
        cover at least `n` elements. There must also be `n-2` levels
        of elements between `A` and `j`.  So we start by searching
        elements that could be our `j` and then just check possible
        antichains `A`.

        TESTS::

            sage: Posets.ChainPoset(0).breadth()
            0
            sage: Posets.ChainPoset(1).breadth()
            1
        """
        # A place for optimization: Adding a doubly irreducible element to
        # a lattice does not change the breadth, except from 1 to 2.
        # Hence we could start by removing double irreducibles.

        from sage.combinat.subsets_pairwise import PairwiseCompatibleSubsets

        # First check if breadth is zero (empty lattice) or one (a chain).
        n = self.cardinality()
        if n == 0:
            return [] if certificate else 0
        if self.is_chain():
            return [self.bottom()] if certificate else 1
        # Breadth is at least two.

        # Work directly with the Hasse diagram
        H = self._hasse_diagram

        # Helper function: Join of elements in the list L.
        jn = H._join
        def join(L):
            j = 0
            for i in L:
                j = jn[i, j]
            return j

        indegs = [H.in_degree(i) for i in range(n)]
        max_breadth = max(indegs)

        for B in range(max_breadth, 1, -1):
            for j in H:
                if indegs[j] < B: continue

                # Get elements more than B levels below it.
                too_close = set(H.breadth_first_search(j,
                                                      neighbors=H.neighbors_in,
                                                      distance=B-2))
                elems = [e for e in H.order_ideal([j]) if e not in too_close]

                achains = PairwiseCompatibleSubsets(elems,
                                          lambda x,y: H.are_incomparable(x,y))
                achains_n = achains.elements_of_depth_iterator(B)

                for A in achains_n:
                    if join(A) == j:
                        if all(join(A[:i]+A[i+1:]) != j for i in range(B)):
                            if certificate:
                                return [self._vertex_to_element(e) for e in A]
                            else:
                                return B
        assert False, "BUG: breadth() in lattices.py have an error."

    def complements(self, element=None):
        r"""
        Return the list of complements of an element in the lattice,
        or the dictionary of complements for all elements.

        Elements `x` and `y` are complements if their meet and join
        are respectively the bottom and the top element of the lattice.

        INPUT:

        - ``element`` - an element of the poset whose complement is
          returned. If ``None`` (default) then dictionary of
          complements for all elements having at least one
          complement is returned.

        EXAMPLES::

            sage: L=LatticePoset({0:['a','b','c'], 'a':[1], 'b':[1], 'c':[1]})
            sage: C = L.complements()

        Let us check that `'a'` and `'b'` are complements of each other::

            sage: 'a' in C['b']
            True
            sage: 'b' in C['a']
            True

        Full list of complements::

            sage: L.complements() # random
            {0: [1], 1: [0], 'a': ['b', 'c'], 'b': ['c', 'a'], 'c': ['b', 'a']}

            sage: L=LatticePoset({0:[1,2],1:[3],2:[3],3:[4]})
            sage: L.complements() # random
            {0: [4], 4: [0]}
            sage: L.complements(1)
            []

        TESTS::

            sage: L=LatticePoset({0:['a','b','c'], 'a':[1], 'b':[1], 'c':[1]})
            sage: for v,v_complements in L.complements().items():
            ....:     for v_c in v_complements:
            ....:         assert L.meet(v,v_c) == L.bottom()
            ....:         assert L.join(v,v_c) == L.top()
        """
        if element is None:
            jn = self.join_matrix()
            mt = self.meet_matrix()
            n = self.cardinality()
            zero = 0
            one = n-1
            c = [[] for x in range(n)]
            for x in range(n):
                for y in range(x,n):
                    if jn[x][y]==one and mt[x][y]==zero:
                        c[x].append(y)
                        c[y].append(x)

            comps={}
            for i in range(n):
                if len(c[i]) > 0:
                    comps[self._vertex_to_element(i)] = (
                        [self._vertex_to_element(x) for x in c[i]] )
            return comps

        # Looking for complements of one element.
        if not element in self:
            raise ValueError("element (=%s) not in poset"%element)
        return [x for x in self if
         self.meet(x, element)==self.bottom() and
         self.join(x, element)==self.top()]

    def is_atomic(self):
        r"""
        Returns ``True`` if ``self`` is an atomic lattice and ``False`` otherwise.

        A lattice is atomic if every element can be written as a join of atoms.

        EXAMPLES::

            sage: L = LatticePoset({0:[1,2,3],1:[4],2:[4],3:[4]})
            sage: L.is_atomic()
            True

            sage: L = LatticePoset({0:[1,2],1:[3],2:[3],3:[4]})
            sage: L.is_atomic()
            False

        NOTES:

        See [Sta97]_, Section 3.3 for a discussion of atomic lattices.

        REFERENCES:

        .. [Sta97] Stanley, Richard.
           Enumerative Combinatorics, Vol. 1.
           Cambridge University Press, 1997

        """
        bottom_element = self.bottom()
        for x in self:
            if x == bottom_element:
                continue
            lcovers = self.lower_covers(x)
            if bottom_element in lcovers:
                continue
            if len(lcovers)<=1:
                return False
        return True

    def is_planar(self):
        r"""
        Return ``True`` if the lattice is *upward* planar, and ``False``
        otherwise.

        A lattice is upward planar if its Hasse diagram has a planar drawing in
        the `\mathbb{R}^2` plane, in such a way that `x` is strictly below `y`
        (on the vertical axis) whenever `x<y` in the lattice.

        Note that the scientific litterature on posets often omits "upward" and
        shortens it to "planar lattice" (e.g. [GW14]_), which can cause
        confusion with the notion of graph planarity in graph theory.

        .. NOTE::

            Not all lattices which are planar -- in the sense of graph planarity
            -- admit such a planar drawing (see example below).

        ALGORITHM:

        Using the result from [Platt76]_, this method returns its result by
        testing that the hasse diagram of the lattice is planar (in the sense of
        graph theory) when an edge is added between the top and bottom elements.

        EXAMPLES:

        The Boolean lattice of `2^3` elements is not upward planar, even if
        it's covering relations graph is planar::

            sage: B3 = Posets.BooleanLattice(3)
            sage: B3.is_planar()
            False
            sage: G = B3.cover_relations_graph()
            sage: G.is_planar()
            True

        Ordinal product of planar lattices is obviously planar. Same does
        not apply to cartesian products::

            sage: P = Posets.PentagonPoset()
            sage: Pc = P.product(P)
            sage: Po = P.ordinal_product(P)
            sage: Pc.is_planar()
            False
            sage: Po.is_planar()
            True

        TESTS::

            sage: Posets.ChainPoset(0).is_planar()
            True
            sage: Posets.ChainPoset(1).is_planar()
            True

        REFERENCES:

        .. [GW14] G. Gratzer and F. Wehrung,
           Lattice Theory: Special Topics and Applications Vol. 1,
           Springer, 2014.

        .. [Platt76] C. R. Platt,
           Planar lattices and planar graphs,
           Journal of Combinatorial Theory Series B,
           Vol 21, no. 1 (1976): 30-39.

        """
        # The 8-element Boolean lattice is the smallest non-planar lattice.
        if self.cardinality() < 8:
            return True
        g = self._hasse_diagram.copy(immutable=False)
        g.add_edge(0, self.cardinality()-1)
        return g.is_planar()

    def is_modular(self, L=None):
        r"""
        Return ``True`` if the lattice is modular and ``False`` otherwise.

        Using the parameter ``L``, this can also be used to check that
        some subset of elements are all modular.

        INPUT:

        - ``L`` -- (default: ``None``) a list of elements to check being
          modular, if ``L`` is ``None``, then this checks the entire lattice

        An element `x` in a lattice `L` is *modular* if `x \leq b` implies

        .. MATH::

            x \vee (a \wedge b) = (x \vee a) \wedge b

        for every `a, b \in L`. We say `L` is modular if `x` is modular
        for all `x \in L`. There are other equivalent definitions,
        see :wikipedia:`Modular_lattice`.

        .. SEEALSO::

            :meth:`is_upper_semimodular`, :meth:`is_lower_semimodular`
            and :meth:`is_modular_element`

        EXAMPLES::

            sage: L = posets.DiamondPoset(5)
            sage: L.is_modular()
            True

            sage: L = posets.PentagonPoset()
            sage: L.is_modular()
            False

            sage: L = posets.ChainPoset(6)
            sage: L.is_modular()
            True

            sage: L = LatticePoset({1:[2,3],2:[4,5],3:[5,6],4:[7],5:[7],6:[7]})
            sage: L.is_modular()
            False
            sage: [L.is_modular([x]) for x in L]
            [True, True, False, True, True, False, True]

        ALGORITHM:

        Based on pp. 286-287 of Enumerative Combinatorics, Vol 1 [EnumComb1]_.
        """
        if not self.is_ranked():
            return False
        H = self._hasse_diagram
        n = H.order()
        if L is None:
            return all(H._rank[a] + H._rank[b] ==
                       H._rank[H._meet[a, b]] + H._rank[H._join[a, b]]
                       for a in range(n) for b in range(a + 1, n))

        L = [self._element_to_vertex_dict[x] for x in L]
        return all(H._rank[a] + H._rank[b] ==
                   H._rank[H._meet[a, b]] + H._rank[H._join[a, b]]
                   for a in L for b in range(n))

    def is_modular_element(self, x):
        r"""
        Return ``True`` if ``x`` is a modular element and ``False`` otherwise.

        INPUT:

        - ``x`` -- an element of the lattice

        An element `x` in a lattice `L` is *modular* if `x \leq b` implies

        .. MATH::

            x \vee (a \wedge b) = (x \vee a) \wedge b

        for every `a, b \in L`.

        .. SEEALSO::

            :meth:`is_modular` to check modularity for the full lattice or
            some set of elements

        EXAMPLES::

            sage: L = LatticePoset({1:[2,3],2:[4,5],3:[5,6],4:[7],5:[7],6:[7]})
            sage: L.is_modular()
            False
            sage: [L.is_modular_element(x) for x in L]
            [True, True, False, True, True, False, True]
        """
        return self.is_modular([x])

    def is_upper_semimodular(self):
        r"""
        Return ``True`` if the lattice is upper semimodular and
        ``False`` otherwise.

        A lattice is upper semimodular if for any `x` in the poset that is
        covered by `y` and `z`, both `y` and `z` are covered by their join.

        See also :meth:`is_modular` and :meth:`is_lower_semimodular`.

        See :wikipedia:`Semimodular_lattice`

        EXAMPLES::

            sage: L = posets.DiamondPoset(5)
            sage: L.is_upper_semimodular()
            True

            sage: L = posets.PentagonPoset()
            sage: L.is_upper_semimodular()
            False

            sage: L = posets.ChainPoset(6)
            sage: L.is_upper_semimodular()
            True

            sage: L = LatticePoset(posets.IntegerPartitions(4))
            sage: L.is_upper_semimodular()
            True

        ALGORITHM:

        Based on pp. 286-287 of Enumerative Combinatorics, Vol 1 [EnumComb1]_.
        """
        if not self.is_ranked():
            return False
        H = self._hasse_diagram
        n = H.order()
        return all(H._rank[a] + H._rank[b] >=
                   H._rank[H._meet[a, b]] + H._rank[H._join[a, b]]
                   for a in range(n) for b in range(a + 1, n))

    def is_lower_semimodular(self):
        r"""
        Return ``True`` if the lattice is lower semimodular and
        ``False`` otherwise.

        A lattice is lower semimodular if for any `x` in the poset that covers
        `y` and `z`, both `y` and `z` cover their meet.

        See also :meth:`is_modular` and :meth:`is_upper_semimodular`.

        See :wikipedia:`Semimodular_lattice`

        EXAMPLES::

            sage: L = posets.DiamondPoset(5)
            sage: L.is_lower_semimodular()
            True

            sage: L = posets.PentagonPoset()
            sage: L.is_lower_semimodular()
            False

            sage: L = posets.ChainPoset(6)
            sage: L.is_lower_semimodular()
            True

        ALGORITHM:

        Based on pp. 286-287 of Enumerative Combinatorics, Vol 1 [EnumComb1]_.
        """
        if not self.is_ranked():
            return False
        H = self._hasse_diagram
        n = H.order()
        return all(H._rank[a] + H._rank[b] <=
                   H._rank[H._meet[a,b]] + H._rank[H._join[a,b]]
                   for a in range(n) for b in range(a+1, n))

    def is_supersolvable(self):
        """
        Return ``True`` if ``self`` is a supersolvable lattice and
        ``False`` otherwise.

        A lattice `L` is *supersolvable* if there exists a maximal chain `C`
        such that every `x \in C` is a modular element in `L`.

        EXAMPLES::

            sage: L = posets.DiamondPoset(5)
            sage: L.is_supersolvable()
            True

            sage: L = posets.PentagonPoset()
            sage: L.is_supersolvable()
            False

            sage: L = posets.ChainPoset(6)
            sage: L.is_supersolvable()
            True

            sage: L = LatticePoset({1:[2,3],2:[4,5],3:[5,6],4:[7],5:[7],6:[7]})
            sage: L.is_supersolvable()
            True
            sage: L.is_modular()
            False

            sage: L = LatticePoset({0: [1, 2, 3, 4], 1: [5, 6, 7],
            ....:                   2: [5, 8, 9], 3: [6, 8, 10], 4: [7, 9, 10],
            ....:                   5: [11], 6: [11], 7: [11], 8: [11],
            ....:                   9: [11], 10: [11]})
            sage: L.is_supersolvable()
            False
        """
        from sage.misc.cachefunc import cached_function

        if not self.is_ranked():
            return False

        H = self._hasse_diagram
        height = self.height()
        n = H.order()
        cur = H.maximal_elements()[0]
        next_ = [H.neighbor_in_iterator(cur)]

        @cached_function
        def is_modular_elt(a):
            return all(H._rank[a] + H._rank[b] ==
                       H._rank[H._meet[a, b]] + H._rank[H._join[a, b]]
                       for b in range(n))

        if not is_modular_elt(cur):
            return False
        while len(next_) < height:
            try:
                cur = next(next_[-1])
            except StopIteration:
                next_.pop()
                if not next_:
                    return False
                continue
            if is_modular_elt(cur):
                next_.append(H.neighbor_in_iterator(cur))
        return True

    def sublattice(self, elms):
        r"""
        Return the smallest sublattice containing elements on the given list.

        INPUT:

        - ``elms`` -- a list of elements of the lattice.

        EXAMPLES::

            sage: L=LatticePoset(( [], [[1,2],[1,17],[1,8],[2,3],[2,22],[2,5],[2,7],[17,22],[17,13],[8,7],[8,13],[3,16],[3,9],[22,16],[22,18],[22,10],[5,18],[5,14],[7,9],[7,14],[7,10],[13,10],[16,6],[16,19],[9,19],[18,6],[18,33],[14,33],[10,19],[10,33],[6,4],[19,4],[33,4]] ))
            sage: L.sublattice([14, 13, 22]).list()
            [1, 2, 8, 7, 14, 17, 13, 22, 10, 33]

            sage: L = Posets.BooleanLattice(3)
            sage: L.sublattice([3,5,6,7])
            Finite lattice containing 8 elements

        .. NOTE::

            This is very unoptimal algorithm. Better one is described on
            "Computing the sublattice of a lattice generated by a set of
            elements" by K. Bertet and M. Morvan. Feel free to implement it.
        """
        gens_remaining = set(elms)
        current_set = set()

        # We add elements one by one in 'current_set'.
        #
        # When adding a point g to 'current_set', we add to 'gens_remaning' all
        # meet/join obtained from g and another point of 'current_set'
        while gens_remaining:
            g = gens_remaining.pop()
            if g in current_set:
                continue
            for x in current_set:
                gens_remaining.add(self.join(x,g))
                gens_remaining.add(self.meet(x,g))
            current_set.add(g)

        return LatticePoset(self.subposet(current_set))

    def maximal_sublattices(self):
        r"""
        Return maximal (proper) sublattices of the lattice.

        EXAMPLES::

            sage: L = LatticePoset(( [], [[1,2],[1,17],[1,8],[2,3],[2,22],
            ....:                         [2,5],[2,7],[17,22],[17,13],[8,7],
            ....:                         [8,13],[3,16],[3,9],[22,16],[22,18],
            ....:                         [22,10],[5,18],[5,14],[7,9],[7,14],
            ....:                         [7,10],[13,10],[16,6],[16,19],[9,19],
            ....:                         [18,6],[18,33],[14,33],[10,19],
            ....:                         [10,33],[6,4],[19,4],[33,4]] ))
            sage: maxs = L.maximal_sublattices()
            sage: len(maxs)
            7
            sage: sorted(maxs[0].list())
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 16, 18, 19, 22, 33]
        """
        n = self.cardinality()
        if n < 2:
            return []
        if n == 2:
            return [self.sublattice([self.bottom()]), self.sublattice([self.top()])]
        return [self.sublattice([self[x] for x in d]) for d in self._hasse_diagram.maximal_sublattices()]

    def frattini_sublattice(self):
        r"""
        Return the Frattini sublattice of the lattice.

        The Frattini sublattice `\Phi(L)` is the intersection of all
        proper maximal sublattices of `L`. It is also the set of
        "non-generators" - if the sublattice generated by set `S` of
        elements is whole lattice, then also `S \setminus \Phi(L)`
        generates whole lattice.

        EXAMPLES::

            sage: L = LatticePoset(( [], [[1,2],[1,17],[1,8],[2,3],[2,22],
            ....:                         [2,5],[2,7],[17,22],[17,13],[8,7],
            ....:                         [8,13],[3,16],[3,9],[22,16],[22,18],
            ....:                         [22,10],[5,18],[5,14],[7,9],[7,14],
            ....:                         [7,10],[13,10],[16,6],[16,19],[9,19],
            ....:                         [18,6],[18,33],[14,33],[10,19],
            ....:                         [10,33],[6,4],[19,4],[33,4]] ))
            sage: sorted(L.frattini_sublattice().list())
            [1, 2, 4, 10, 19, 22, 33]
        """
        return LatticePoset(self.subposet([self[x] for x in
                self._hasse_diagram.frattini_sublattice()]))

    def moebius_algebra(self, R):
        """
        Return the Mobius algebra of ``self`` over ``R``.

        EXAMPLES::

            sage: L = posets.BooleanLattice(4)
            sage: L.moebius_algebra(QQ)
            Moebius algebra of Finite lattice containing 16 elements over Rational Field
        """
        from sage.combinat.posets.moebius_algebra import MoebiusAlgebra
        return MoebiusAlgebra(R, self)

    def quantum_moebius_algebra(self, q=None):
        """
        Return the quantum Mobius algebra of ``self`` with parameter ``q``.

        INPUT:

        - ``q`` -- (optional) the deformation parameter `q`

        EXAMPLES::

            sage: L = posets.BooleanLattice(4)
            sage: L.quantum_moebius_algebra()
            Quantum Moebius algebra of Finite lattice containing 16 elements
             with q=q over Univariate Laurent Polynomial Ring in q over Integer Ring
        """
        from sage.combinat.posets.moebius_algebra import QuantumMoebiusAlgebra
        return QuantumMoebiusAlgebra(self, q)

    def is_dismantlable(self, certificate=False):
        r"""
        Return ``True`` if the lattice is dismantlable, and ``False``
        otherwise.

        An `n`-element lattice `L_n` is dismantlable if there is a sublattice
        chain `L_{n-1} \supset L_{n-2}, \supset \cdots, \supset L_0` so that
        every `L_i` is a sublattice of `L_{i+1}` with one element less, and
        `L_0` is the empty lattice. In other words, a dismantlable lattice
        can be reduced to empty lattice removing doubly irreducible
        element one by one.

        INPUT:

        - ``certificate`` (boolean) -- Whether to return a certificate.

          * If ``certificate = False`` (default), returns ``True`` or
            ``False`` accordingly.

          * If ``certificate = True``, returns:

            * ``(True, elms)`` when the lattice is dismantlable, where
              ``elms`` is elements listed in a possible removing order.

            * ``(False, crown)`` when the lattice is not dismantlable,
              where ``crown`` is a subposet of `2k` elements
              `a_1, \ldots, a_k, b_1, \ldots, b_k` with covering
              relations `a_i \lessdot b_i` and `a_i \lessdot b_{i+1}`
              for `i \in [1, \ldots, k-1]`, and `a_k \lessdot b_1`.

        EXAMPLES::

            sage: DL12 = LatticePoset((divisors(12), attrcall("divides")))
            sage: DL12.is_dismantlable()
            True
            sage: DL12.is_dismantlable(certificate=True)
            (True, [4, 2, 1, 3, 6, 12])

            sage: B3 = Posets.BooleanLattice(3)
            sage: B3.is_dismantlable()
            False
            sage: B3.is_dismantlable(certificate=True)
            (False, Finite poset containing 6 elements)

        Every planar lattice is dismantlable. Converse is not true::

            sage: L = LatticePoset( ([], [[0, 1], [0, 2], [0, 3], [0, 4],
            ....:                         [1, 7], [2, 6], [3, 5], [4, 5],
            ....:                         [4, 6], [4, 7], [5, 8], [6, 8],
            ....:                         [7, 8]]) )
            sage: L.is_dismantlable()
            True
            sage: L.is_planar()
            False

        TESTS::

            sage: Posets.ChainPoset(0).is_dismantlable()
            True
            sage: Posets.ChainPoset(1).is_dismantlable()
            True

            sage: L = LatticePoset(DiGraph('L@_?W?E?@CCO?A?@??_?O?Jw????C?'))
            sage: L.is_dismantlable()
            False
            sage: c = L.is_dismantlable(certificate=True)[1]
            sage: (3 in c, 12 in c, 9 in c)
            (True, False, True)
        """
        from sage.graphs.digraph import DiGraph
        from copy import copy

        H = copy(self._hasse_diagram)
        cert = []
        # Smallest lattice that is not dismantlable is the
        # Boolean lattice with 2^3=8 elements. Hence the limit 7.
        limit = 0 if certificate else 7

        while H.order() > limit:
            for e in H:
                i = H.in_degree(e)
                o = H.out_degree(e)
                if i < 2 and o < 2:
                    if certificate:
                        cert.append(e)
                    if i == 1 and o == 1:  # Remove inside the lattice
                        lower = H.neighbors_in(e)[0]
                        upper = H.neighbors_out(e)[0]
                        H.delete_vertex(e)
                        if not upper in H.depth_first_search(lower):
                            H.add_edge(lower, upper)
                    else:  # Remove the top or bottom element
                        H.delete_vertex(e)
                    break
            else:
                if not certificate:
                    return False
                k = 3
                while True:
                    crown = DiGraph({i: [k + i, k + (i + 1) % k]
                                     for i in range(k)})
                    sg = H.transitive_closure().subgraph_search(crown, True)
                    if sg:
                        elms = [self[e] for e in sg]
                        return (False, self.subposet(elms))
                    k += 1
        if not certificate:
            return True
        return (True, [self[e] for e in cert])

############################################################################

FiniteMeetSemilattice._dual_class = FiniteJoinSemilattice
FiniteJoinSemilattice._dual_class = FiniteMeetSemilattice
FiniteLatticePoset   ._dual_class = FiniteLatticePoset
