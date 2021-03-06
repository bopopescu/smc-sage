r"""
Scalar field algebra

The class :class:`ScalarFieldAlgebra` implements the commutative algebra
`C^\infty(U)` of differentiable scalar fields on some open subset `U` of a
differentiable manifold `M` over `\RR`. By *scalar field*, it is meant a
function `U\rightarrow \RR`.
`C^\infty(U)` is an algebra over `\RR`, whose ring product is the pointwise
multiplication of real-valued functions, which is clearly commutative.
In the present implementation, the field `\RR`, over which the
albegra `C^\infty(U)` is constructed, is represented by Sage's Symbolic Ring
SR.

AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2014-2015): initial version

REFERENCES:

- S. Kobayashi & K. Nomizu : *Foundations of Differential Geometry*, vol. 1,
  Interscience Publishers (New York) (1963)
- J.M. Lee : *Introduction to Smooth Manifolds*, 2nd ed., Springer (New York)
  (2013)
- B O'Neill : *Semi-Riemannian Geometry*, Academic Press (San Diego) (1983)

"""

#******************************************************************************
#       Copyright (C) 2015 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#       Copyright (C) 2015 Michal Bejger <bejger@camk.edu.pl>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.categories.commutative_algebras import CommutativeAlgebras
from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ
from sage.symbolic.ring import SR
from sage.geometry.manifolds.scalarfield import ScalarField

class ScalarFieldAlgebra(UniqueRepresentation, Parent):
    r"""
    Commutative algebra `C^\infty(U)` of differentiable functions
    `U \rightarrow \RR`, where `U` is an open subset of some differentiable
    manifold over `\RR`. `C^\infty(U)` is a commutative algebra over `\RR`,
    the latter being represented by Sage's Symbolic Ring SR.

    The class :class:`ScalarFieldAlgebra` inherits from
    :class:`~sage.structure.parent.Parent`, with the category set to
    :class:`~sage.categories.commutative_algebras.CommutativeAlgebras`.
    The corresponding *element* class is
    :class:`~sage.geometry.manifolds.scalarfield.ScalarField`.

    INPUT:

    - ``domain`` -- the manifold open subset `U` on which the scalar fields are
      defined (must be an instance of class
      :class:`~sage.geometry.manifolds.domain.ManifoldOpenSubset`)

    EXAMPLES:

    Algebras of scalar fields on the sphere `S^2` and on some subdomain of it::

        sage: M = Manifold(2, 'M') # the 2-dimensional sphere S^2
        sage: U = M.open_subset('U') # complement of the North pole
        sage: c_xy.<x,y> = U.chart() # stereographic coordinates from the North pole
        sage: V = M.open_subset('V') # complement of the South pole
        sage: c_uv.<u,v> = V.chart() # stereographic coordinates from the South pole
        sage: M.declare_union(U,V)   # S^2 is the union of U and V
        sage: xy_to_uv = c_xy.transition_map(c_uv, (x/(x^2+y^2), y/(x^2+y^2)), \
                                             intersection_name='W', restrictions1= x^2+y^2!=0, \
                                             restrictions2= u^2+v^2!=0)
        sage: uv_to_xy = xy_to_uv.inverse()
        sage: CM = M.scalar_field_algebra() ; CM
        algebra of scalar fields on the 2-dimensional manifold 'M'
        sage: W = U.intersection(V)  # S^2 minus the two poles
        sage: CW = W.scalar_field_algebra() ; CW
        algebra of scalar fields on the open subset 'W' of the 2-dimensional manifold 'M'

    `C^\infty(M)` and `C^\infty(W)` belong to the category of commutative
    algebras over `\RR` (represented here by Sage's Symbolic Ring)::

        sage: CM.category()
        Category of commutative algebras over Symbolic Ring
        sage: CM.base_ring()
        Symbolic Ring
        sage: CW.category()
        Category of commutative algebras over Symbolic Ring
        sage: CW.base_ring()
        Symbolic Ring

    The elements of `C^\infty(M)` are scalar fields on M::

        sage: CM.an_element()
        scalar field on the 2-dimensional manifold 'M'
        sage: CM.an_element().display()  # this sample element is a constant field
        M --> R
        on U: (x, y) |--> 2
        on V: (u, v) |--> 2

    Those of `C^\infty(W)` are scalar fields on W::

        sage: CW.an_element()
        scalar field on the open subset 'W' of the 2-dimensional manifold 'M'
        sage: CW.an_element().display()  # this sample element is a constant field
        W --> R
        (x, y) |--> 2
        (u, v) |--> 2

    The zero element::

        sage: CM.zero()
        scalar field 'zero' on the 2-dimensional manifold 'M'
        sage: CM.zero().display()
        zero: M --> R
        on U: (x, y) |--> 0
        on V: (u, v) |--> 0

    ::

        sage: CW.zero()
        scalar field 'zero' on the open subset 'W' of the 2-dimensional
         manifold 'M'
        sage: CW.zero().display()
        zero: W --> R
           (x, y) |--> 0
           (u, v) |--> 0

    The unit element::

        sage: CM.one()
        scalar field on the 2-dimensional manifold 'M'
        sage: CM.one().display()
        M --> R
        on U: (x, y) |--> 1
        on V: (u, v) |--> 1

    ::

        sage: CW.one()
        scalar field on the open subset 'W' of the 2-dimensional manifold 'M'
        sage: CW.one().display()
        W --> R
        (x, y) |--> 1
        (u, v) |--> 1

    A generic element can be constructed as for any parent in Sage, namely
    by means of the ``__call__`` operator on the parent (here with the dictionary
    of the coordinate expressions defining the scalar field)::

        sage: f = CM({c_xy: atan(x^2+y^2), c_uv: pi/2 - atan(u^2+v^2)}) ; f
        scalar field on the 2-dimensional manifold 'M'
        sage: f.display()
        M --> R
        on U: (x, y) |--> arctan(x^2 + y^2)
        on V: (u, v) |--> 1/2*pi - arctan(u^2 + v^2)
        sage: f.parent()
        algebra of scalar fields on the 2-dimensional manifold 'M'

    Specific elements can also be constructed in this way::

        sage: CM(0) == CM.zero()
        True
        sage: CM(1) == CM.one()
        True

    Note that the zero scalar field is cached::

        sage: CM(0) is CM.zero()
        True

    Elements can also be constructed by means of the method
    :meth:`~sage.geometry.manifolds.domain.ManifoldOpenSubset.scalar_field` acting on
    the domain (this allows one to set the name of the scalar field at the
    construction)::

        sage: f1 = M.scalar_field({c_xy: atan(x^2+y^2), c_uv: pi/2 - atan(u^2+v^2)}, name='f')
        sage: f1.parent()
        algebra of scalar fields on the 2-dimensional manifold 'M'
        sage: f1 == f
        True
        sage: M.scalar_field(0, chart='all') is CM.zero()
        True

    The algebra `C^\infty(M)` coerces to `C^\infty(W)` since `W` is an open
    subset of `M`::

        sage: CW.has_coerce_map_from(CM)
        True

    The reverse is of course false::

        sage: CM.has_coerce_map_from(W)
        False

    The coercion map is nothing but the restriction to `W` of scalar fields
    on `M`::

        sage: fW = CW(f) ; fW
        scalar field on the open subset 'W' of the 2-dimensional manifold 'M'
        sage: fW.display()
        W --> R
        (x, y) |--> arctan(x^2 + y^2)
        (u, v) |--> 1/2*pi - arctan(u^2 + v^2)

    ::

        sage: CW(CM.one()) == CW.one()
        True

    The coercion map allows for the addition of elements of `C^\infty(W)`
    with elements of `C^\infty(M)`, the result being an element of
    `C^\infty(W)`::

        sage: s = fW + f
        sage: s.parent()
        algebra of scalar fields on the open subset 'W' of the 2-dimensional manifold 'M'
        sage: s.display()
        W --> R
        (x, y) |--> 2*arctan(x^2 + y^2)
        (u, v) |--> pi - 2*arctan(u^2 + v^2)

    Other coercions are those from the rational field, leading to constant
    scalar fields::

        sage: h = CM(2/3) ; h
        scalar field on the 2-dimensional manifold 'M'
        sage: h.display()
        M --> R
        on U: (x, y) |--> 2/3
        on V: (u, v) |--> 2/3

    and those from the Symbolic Ring, also leading to constant scalar fields::

        sage: h = CM(pi*sqrt(2)) ; h
        scalar field on the 2-dimensional manifold 'M'
        sage: h.display()
        M --> R
        on U: (x, y) |--> sqrt(2)*pi
        on V: (u, v) |--> sqrt(2)*pi

    TESTS OF THE ALGEBRA LAWS:

    Ring laws::

        sage: s = f + h ; s
        scalar field on the 2-dimensional manifold 'M'
        sage: s.display()
        M --> R
        on U: (x, y) |--> sqrt(2)*pi + arctan(x^2 + y^2)
        on V: (u, v) |--> 1/2*pi*(2*sqrt(2) + 1) - arctan(u^2 + v^2)

    ::

        sage: s = f - h ; s
        scalar field on the 2-dimensional manifold 'M'
        sage: s.display()
        M --> R
        on U: (x, y) |--> -sqrt(2)*pi + arctan(x^2 + y^2)
        on V: (u, v) |--> -1/2*pi*(2*sqrt(2) - 1) - arctan(u^2 + v^2)

    ::

        sage: s = f*h ; s
        scalar field on the 2-dimensional manifold 'M'
        sage: s.display()
        M --> R
        on U: (x, y) |--> sqrt(2)*pi*arctan(x^2 + y^2)
        on V: (u, v) |--> 1/2*sqrt(2)*(pi^2 - 2*pi*arctan(u^2 + v^2))

    ::

        sage: s = f/h ; s
        scalar field on the 2-dimensional manifold 'M'
        sage: s.display()
        M --> R
        on U: (x, y) |--> 1/2*sqrt(2)*arctan(x^2 + y^2)/pi
        on V: (u, v) |--> 1/4*sqrt(2)*(pi - 2*arctan(u^2 + v^2))/pi

    ::

        sage: f*(h+f) == f*h + f*f
        True

    Ring laws with coercion::

        sage: f - fW == CW.zero()
        True
        sage: f/fW == CW.one()
        True
        sage: s = f*fW ; s
        scalar field on the open subset 'W' of the 2-dimensional manifold 'M'
        sage: s.display()
        W --> R
        (x, y) |--> arctan(x^2 + y^2)^2
        (u, v) |--> 1/4*pi^2 - pi*arctan(u^2 + v^2) + arctan(u^2 + v^2)^2
        sage: s/f == fW
        True

    Multiplication by a real number::

        sage: s = 2*f ; s
        scalar field on the 2-dimensional manifold 'M'
        sage: s.display()
        M --> R
        on U: (x, y) |--> 2*arctan(x^2 + y^2)
        on V: (u, v) |--> pi - 2*arctan(u^2 + v^2)

    ::

        sage: 0*f == CM.zero()
        True
        sage: 1*f == f
        True
        sage: 2*(f/2) == f
        True
        sage: (f+2*f)/3 == f
        True
        sage: 1/3*(f+2*f) == f
        True

    Sage test suite for algebras is passed::

        sage: TestSuite(CM).run(verbose=True)
        running ._test_additive_associativity() . . . pass
        running ._test_an_element() . . . pass
        running ._test_associativity() . . . pass
        running ._test_category() . . . pass
        running ._test_characteristic() . . . pass
        running ._test_distributivity() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_nonzero_equal() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_one() . . . pass
        running ._test_pickling() . . . pass
        running ._test_prod() . . . pass
        running ._test_some_elements() . . . pass
        running ._test_zero() . . . pass

    It is passed also for `C^\infty(W)`::

        sage: TestSuite(CW).run()

    """

    Element = ScalarField

    def __init__(self, domain):
        Parent.__init__(self, base=SR, category=CommutativeAlgebras(SR))
        self._domain = domain
        self._populate_coercion_lists_()
        self._zero = None # zero element (not constructed yet)

    #### Methods required for any Parent
    def _element_constructor_(self, coord_expression=None, name=None,
                              latex_name=None):
        r"""
        Construct a scalarfield
        """
        if coord_expression == 0:
            # construct the zero element
            if self._zero is None:
                self._zero = self.element_class(self._domain,
                                                coord_expression=0,
                                                name='zero', latex_name='0')
            return self._zero
        if isinstance(coord_expression, ScalarField):
            if self._domain.is_subset(coord_expression._domain):
                # restriction of the scalar field to self._domain:
                sexpress = {}
                for chart, funct in coord_expression._express.iteritems():
                    for schart in self._domain._atlas:
                        if schart in chart._subcharts:
                            sexpress[schart] = funct.expr()
                resu = self.element_class(self._domain,
                                          coord_expression=sexpress, name=name,
                                          latex_name=latex_name)
            else:
                raise TypeError("Cannot coerce the " + str(coord_expression) +
                                "to a scalar field on the " + str(self._domain))
        else:
            # generic constructor:
            resu = self.element_class(self._domain,
                                      coord_expression=coord_expression,
                                      name=name, latex_name=latex_name)
        return resu

    def _an_element_(self):
        r"""
        Construct some (unamed) element of the module
        """
        return self.element_class(self._domain, coord_expression=2)


    def _coerce_map_from_(self, other):
        r"""
        Determine whether coercion to self exists from other parent
        """
        if other is SR:
            return True  # coercion from the base ring (multiplication by the
                         # algebra unit, i.e. self.one())
        elif other is ZZ:
           return True   # important to define self(1) (for self.one())
        elif other is QQ:
            return True
        elif isinstance(other, ScalarFieldAlgebra):
            return self._domain.is_subset(other._domain)
        else:
            return False

    #### End of methods required for any Parent

    def _repr_(self):
        r"""
        String representation of the object.
        """
        return "algebra of scalar fields on the " + str(self._domain)

    def _latex_(self):
        r"""
        LaTeX representation of the object.
        """
        return r"C^\infty("  + self._domain._latex_name + ")"
