r"""
Free modules of finite rank

The class :class:`FiniteRankFreeModule` implements free modules of finite rank
over a commutative ring.

A *free module of finite rank* over a commutative ring `R` is a module `M` over
`R` that admits a *finite basis*, i.e. a finite familly of linearly independent
generators. Since `R` is commutative, it has the invariant basis number
property, so that the rank of the free module `M` is defined uniquely, as the
cardinality of any basis of `M`.

No distinguished basis of `M` is assumed. On the contrary, many bases can be
introduced on the free module along with change-of-basis rules (as module
automorphisms). Each
module element has then various representations over the various bases.

.. NOTE::

    The class :class:`FiniteRankFreeModule` does not inherit from
    :class:`~sage.modules.free_module.FreeModule_generic` since the latter
    is a derived class of :class:`~sage.modules.module.Module_old`,
    which does not conform to the new coercion model.
    Moreover, the class :class:`~sage.modules.free_module.FreeModule_generic`
    seems to assume a distinguished basis (cf. its method
    :meth:`~sage.modules.free_module.FreeModule_generic.basis`).
    Besides, the class :class:`FiniteRankFreeModule` does not inherit
    from the class
    :class:`~sage.combinat.free_module.CombinatorialFreeModule` (which conforms
    to the new coercion model) since this class is devoted to modules with a
    distinguished basis.

For the above reasons, the class :class:`FiniteRankFreeModule` inherits
directly from the generic class :class:`~sage.structure.parent.Parent`
with the category set to :class:`~sage.categories.modules.Modules`
and not to
:class:`~sage.categories.modules_with_basis.ModulesWithBasis`.

.. TODO::

    - implement submodules
    - create a FreeModules category (cf. the *TODO* statement in the
      documentation of :class:`~sage.categories.modules.Modules`: *Implement
      a ``FreeModules(R)`` category, when so prompted by a concrete use case*)

AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2014): initial version

EXAMPLES:

Let us define a free module of rank 2 over `\ZZ`::

    sage: M = FiniteRankFreeModule(ZZ, 2, name='M') ; M
    Rank-2 free module M over the Integer Ring

We introduce a first basis on ``M``::

    sage: e = M.basis('e') ; e
    Basis (e_0,e_1) on the Rank-2 free module M over the Integer Ring

The elements of the basis are of course module elements::

    sage: e[0]
    Element e_0 of the Rank-2 free module M over the Integer Ring
    sage: e[1]
    Element e_1 of the Rank-2 free module M over the Integer Ring
    sage: e[0].parent()
    Rank-2 free module M over the Integer Ring

We define a module element by its components w.r.t. basis ``e``::

    sage: u = M([2,-3], basis=e, name='u')
    sage: u.display(basis=e)
    u = 2 e_0 - 3 e_1

Since the first defined basis is considered as the default one on the module,
the above can be abridged to::

    sage: u = M([2,-3], name='u')
    sage: u.display()
    u = 2 e_0 - 3 e_1

Module elements can be compared::

    sage: u == 2*e[0] - 3*e[1]
    True

We define a second basis on M by linking it to ``e`` via a module
automorphism::

    sage: a = M.automorphism_tensor()
    sage: a.set_comp(basis=e)[0,1] = -1 ; a.set_comp(basis=e)[1,0] = 1 # only the non-zero components have to be set
    sage: a[:]  # a matrix view of the automorphism in the module's default basis
    [ 0 -1]
    [ 1  0]
    sage: f = e.new_basis(a, 'f') ; f
    Basis (f_0,f_1) on the Rank-2 free module M over the Integer Ring
    sage: f[0].display()
    f_0 = e_1
    sage: f[1].display()
    f_1 = -e_0

We may check that the basis ``f`` is the image of ``e`` by the
automorphism ``a``::

    sage: f[0] == a(e[0])
    True
    sage: f[1] == a(e[1])
    True

We introduce a new module element via its components w.r.t. basis ``f``::

    sage: v = M([2,4], basis=f, name='v')
    sage: v.display(basis=f)
    v = 2 f_0 + 4 f_1

The sum of the two module elements ``u`` and ``v`` can be performed even if
they have been defined on different bases, thanks to the known relation
between the two bases::

    sage: s = u + v ; s
    Element u+v of the Rank-2 free module M over the Integer Ring

We can display the result in either basis::

    sage: s.display(basis=e)    # a shortcut is s.display(), e being the default basis
    u+v = -2 e_0 - e_1
    sage: s.display(basis=f)
    u+v = -f_0 + 2 f_1

Of course, we can display each of the individual element in either basis::

    sage: u.display(basis=f)    # recall: u was introduced via basis e
    u = -3 f_0 - 2 f_1
    sage: v.display(basis=e)    # recall: v was introduced via basis f
    v = -4 e_0 + 2 e_1

Tensor products are implemented::

    sage: t = u*v ; t
    Type-(2,0) tensor u*v on the Rank-2 free module M over the Integer Ring
    sage: t.parent()
    Free module of type-(2,0) tensors on the
     Rank-2 free module M over the Integer Ring
    sage: t.display()
    u*v = -8 e_0*e_0 + 4 e_0*e_1 + 12 e_1*e_0 - 6 e_1*e_1

The automorphism ``a`` is considered as a tensor of type `(1,1)` on ``M``::

    sage: a.parent()
    Free module of type-(1,1) tensors on the
     Rank-2 free module M over the Integer Ring
    sage: a.display()
    -e_0*e^1 + e_1*e^0

As such, we can form its tensor product with ``t``, yielding a tensor of
type `(3,1)`::

    sage: (t*a).parent()
    Free module of type-(3,1) tensors on the
     Rank-2 free module M over the Integer Ring
    sage: (t*a).display()
    8 e_0*e_0*e_0*e^1 - 8 e_0*e_0*e_1*e^0 - 4 e_0*e_1*e_0*e^1
     + 4 e_0*e_1*e_1*e^0 - 12 e_1*e_0*e_0*e^1 + 12 e_1*e_0*e_1*e^0
     + 6 e_1*e_1*e_0*e^1 - 6 e_1*e_1*e_1*e^0

"""
#******************************************************************************
#       Copyright (C) 2014 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#       Copyright (C) 2014 Michal Bejger <bejger@camk.edu.pl>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.parent import Parent
from sage.categories.modules import Modules
from sage.categories.rings import Rings
from sage.tensor.modules.free_module_tensor import FiniteRankFreeModuleElement

class FiniteRankFreeModule(UniqueRepresentation, Parent):
    r"""
    Free module of finite rank over a commutative ring `R`.

    .. NOTE::

        The class :class:`FiniteRankFreeModule` does not inherit from
        :class:`~sage.modules.free_module.FreeModule_generic` since the latter
        is a derived class of :class:`~sage.modules.module.Module_old`,
        which does not conform to the new coercion model.
        Besides, the class :class:`FiniteRankFreeModule` does not inherit
        from the class :class:`CombinatorialFreeModule` since the latter is
        devoted to modules *with a basis*.

    .. NOTE::

        Following the recommendation exposed in
        `trac ticket 16427 <http://trac.sagemath.org/ticket/16427>`_
        the class :class:`FiniteRankFreeModule` inherits directly from
        :class:`~sage.structure.parent.Parent` and not from the Cython class
        :class:`~sage.modules.module.Module`.

    The class :class:`FiniteRankFreeModule` is a Sage *Parent* class whose
    elements belong to the class
    :class:`~sage.tensor.modules.free_module_tensor.FiniteRankFreeModuleElement`.

    INPUT:

    - ``ring`` -- commutative ring `R` over which the free module is
      constructed
    - ``rank`` -- positive integer; rank of the free module
    - ``name`` -- (default: ``None``) string; name given to the free module
    - ``latex_name`` -- (default: ``None``) string;  LaTeX symbol to denote
      the freemodule; if none is provided, it is set to ``name``
    - ``start_index`` -- (default: 0) integer; lower bound of the range of
      indices in bases defined on the free module
    - ``output_formatter`` -- (default: ``None``) function or unbound
      method called to format the output of the tensor components;
      ``output_formatter`` must take 1 or 2 arguments: the first argument
      must be an element of the ring `R` and  the second one, if any, some
      format specification

    EXAMPLES:

    Free module of rank 3 over `\ZZ`::

        sage: M = FiniteRankFreeModule(ZZ, 3) ; M
        Rank-3 free module over the Integer Ring
        sage: M = FiniteRankFreeModule(ZZ, 3, name='M') ; M  # declaration with a name
        Rank-3 free module M over the Integer Ring
        sage: M.category()
        Category of modules over Integer Ring
        sage: M.base_ring()
        Integer Ring
        sage: M.rank()
        3

    If the base ring is a field, the free module is in the category of vector
    spaces::

        sage: V = FiniteRankFreeModule(QQ, 3, name='V') ; V
        Rank-3 free module V over the Rational Field
        sage: V.category()
        Category of vector spaces over Rational Field

    The LaTeX output is adjusted via the parameter ``latex_name``::

        sage: latex(M)  # the default is the symbol provided in the string ``name``
        M
        sage: M = FiniteRankFreeModule(ZZ, 3, name='M', latex_name=r'\mathcal{M}')
        sage: latex(M)
        \mathcal{M}

    M is a *parent* object, whose elements are instances of
    :class:`~sage.tensor.modules.free_module_tensor.FiniteRankFreeModuleElement`::

        sage: v = M.an_element() ; v
        Element of the Rank-3 free module M over the Integer Ring
        sage: from sage.tensor.modules.free_module_tensor import FiniteRankFreeModuleElement
        sage: isinstance(v, FiniteRankFreeModuleElement)
        True
        sage: v in M
        True
        sage: M.is_parent_of(v)
        True

    The free module M has no distinguished basis::

        sage: M in ModulesWithBasis(ZZ)
        False
        sage: M in Modules(ZZ)
        True

    Bases have to be introduced by means of the method :meth:`basis`,
    the first defined basis being considered as the *default basis*, meaning
    it can be skipped in function arguments required a basis (this can
    be changed by means of the method :meth:`set_default_basis`)::

        sage: e = M.basis('e') ; e
        Basis (e_0,e_1,e_2) on the Rank-3 free module M over the Integer Ring
        sage: M.default_basis()
        Basis (e_0,e_1,e_2) on the Rank-3 free module M over the Integer Ring

    Constructing an element of ``M`` from (the integer) 0 yields
    the zero element of ``M``::

        sage: M(0)
        Element zero of the Rank-3 free module M over the Integer Ring
        sage: M(0) is M.zero()
        True

    Non-zero elements are constructed by providing their components in
    a given basis::

        sage: v = M([-1,0,3]) ; v  # components in the default basis (e)
        Element of the Rank-3 free module M over the Integer Ring
        sage: v.display()
        -e_0 + 3 e_2
        sage: f = M.basis('f')
        sage: v = M([-1,0,3], basis=f) ; v  # components in a specific basis
        Element of the Rank-3 free module M over the Integer Ring
        sage: v.display(f)
        -f_0 + 3 f_2
        sage: v = M([-1,0,3], basis=f, name='v') ; v
        Element v of the Rank-3 free module M over the Integer Ring
        sage: v.display(f)
        v = -f_0 + 3 f_2

    An alternative is to construct the element from an empty list of
    componentsand to set the nonzero components afterwards::

        sage: v = M([], name='v')
        sage: v.set_comp(e)[0] = -1
        sage: v.set_comp(e)[2] = 3
        sage: v.display(e)
        v = -e_0 + 3 e_2

    Indices on the free module, such as indices labelling the element of a
    basis, are provided by the generator method :meth:`irange`. By default,
    they range from 0 to the module's rank minus one::

        sage: for i in M.irange(): print i,
        0 1 2

    This can be changed via the parameter ``start_index`` in the module
    construction::

        sage: M = FiniteRankFreeModule(ZZ, 3, name='M', start_index=1)
        sage: for i in M.irange(): print i,
        1 2 3

    The parameter ``output_formatter`` in the constructor of the free module
    is used to set the output format of tensor components::

        sage: M = FiniteRankFreeModule(QQ, 3, output_formatter=Rational.numerical_approx)
        sage: e = M.basis('e')
        sage: v = M([1/3, 0, -2], basis=e)
        sage: v.comp(e)[:]
        [0.333333333333333, 0.000000000000000, -2.00000000000000]
        sage: v.display(e)  # default format (53 bits of precision)
        0.333333333333333 e_0 - 2.00000000000000 e_2
        sage: v.display(e, format_spec=10)  # 10 bits of precision
        0.33 e_0 - 2.0 e_2

    """

    Element = FiniteRankFreeModuleElement

    def __init__(self, ring, rank, name=None, latex_name=None, start_index=0,
                 output_formatter=None):
        r"""
        See :class:`FiniteRankFreeModule` for documentation and examples.

        TESTS::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: TestSuite(M).run()
            sage: e = M.basis('e')
            sage: TestSuite(M).run()
            sage: f = M.basis('f')
            sage: TestSuite(M).run()

        """
        if ring not in Rings().Commutative():
            raise TypeError("the module base ring must be commutative")
        Parent.__init__(self, base=ring, category=Modules(ring))
        self._ring = ring # same as self._base
        self._rank = rank
        self._name = name
        if latex_name is None:
            self._latex_name = self._name
        else:
            self._latex_name = latex_name
        self._sindex = start_index
        self._output_formatter = output_formatter
        # Dictionary of the tensor modules built on self
        #   (keys = (k,l) --the tensor type) :
        self._tensor_modules = {(1,0): self} # self is considered as the set of
                                            # tensors of type (1,0)
        # Dictionary of exterior powers of the dual of self
        #   (keys = p --the power degree) :
        self._dual_exterior_powers = {}
        self._known_bases = []  # List of known bases on the free module
        self._def_basis = None # default basis
        self._basis_changes = {} # Dictionary of the changes of bases
        # Zero element:
        if not hasattr(self, '_zero_element'):
            self._zero_element = self._element_constructor_(name='zero',
                                                            latex_name='0')
        # Identity endomorphism:
        self._identity_map = None # not defined yet


    #### Methods required for any Parent

    def _element_constructor_(self, comp=[], basis=None, name=None,
                              latex_name=None):
        r"""
        Construct an element of ``self``.

        EXAMPLES::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: e = M.basis('e')
            sage: v = M._element_constructor_(comp=[1,0,-2], basis=e, name='v') ; v
            Element v of the Rank-3 free module M over the Integer Ring
            sage: v.display()
            v = e_0 - 2 e_2
            sage: v == M([1,0,-2])
            True
            sage: v = M._element_constructor_(0) ; v
            Element zero of the Rank-3 free module M over the Integer Ring
            sage: v = M._element_constructor_() ; v
            Element of the Rank-3 free module M over the Integer Ring

        """
        if comp == 0:
            return self._zero_element
        resu = self.element_class(self, name=name, latex_name=latex_name)
        if comp:
            resu.set_comp(basis)[:] = comp
        return resu

    def _an_element_(self):
        r"""
        Construct some (unamed) element of the module.

        EXAMPLE::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: v = M._an_element_(); v
            Element of the Rank-3 free module M over the Integer Ring
            sage: v.display()
            e_0 + e_1 + e_2
            sage: v == M.an_element()
            True
            sage: v.parent()
            Rank-3 free module M over the Integer Ring

        """
        if self._def_basis is None:
            self.basis('e') 
        resu = self.element_class(self)
        resu.set_comp()[:] = [self._ring.an_element() for i in range(self._rank)]
        return resu

    #### End of methods required for any Parent

    #### Methods to be redefined by derived classes ####

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLE::

            sage: FiniteRankFreeModule(ZZ, 3, name='M')
            Rank-3 free module M over the Integer Ring

        """
        description = "Rank-{} free module ".format(self._rank)
        if self._name is not None:
            description += self._name + " "
        description += "over the " + str(self._ring)
        return description

    def _Hom_(self, other, category=None):
        r"""
        Construct the set of homomorphisms self --> other.

        INPUT:

        - ``other`` -- another free module of finite rank over the same ring
          as ``self``
        - ``category`` -- (default: ``None``) not used here (to ensure
          compatibility with generic hook ``_Hom_``)

        OUTPUT:

        - the hom-set Hom(M,N), where M is ``self`` and N is ``other``

        EXAMPLES::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: N = FiniteRankFreeModule(ZZ, 2, name='N')
            sage: H = M._Hom_(N) ; H
            Set of Morphisms from Rank-3 free module M over the Integer Ring
             to Rank-2 free module N over the Integer Ring in Category of
             modules over Integer Ring
            sage: H = Hom(M,N) ; H  # indirect doctest
            Set of Morphisms from Rank-3 free module M over the Integer Ring 
             to Rank-2 free module N over the Integer Ring in Category of 
             modules over Integer Ring

        """
        from free_module_homset import FreeModuleHomset
        return FreeModuleHomset(self, other)

    def tensor_module(self, k, l):
        r"""
        Return the free module of all tensors of type `(k, l)` defined on
        ``self``.

        INPUT:

        - ``k`` -- non-negative integer; the contravariant rank, the tensor
          type being `(k, l)`
        - ``l`` -- non-negative integer; the covariant rank, the tensor type
          being `(k, l)`

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.tensor_free_module.TensorFreeModule`
          representing the free module
          `T^{(k,l)}(M)` of type-`(k,l)` tensors on the free module ``self``

        EXAMPLES:

        Tensor modules over a free module over `\ZZ`::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: T = M.tensor_module(1,2) ; T
            Free module of type-(1,2) tensors on the Rank-3 free module M
             over the Integer Ring
            sage: T.an_element()
            Type-(1,2) tensor on the Rank-3 free module M over the Integer Ring

        Tensor modules are unique::

            sage: M.tensor_module(1,2) is T
            True

        The base module is itself the module of all type-`(1,0)` tensors::

            sage: M.tensor_module(1,0) is M
            True

        """
        from sage.tensor.modules.tensor_free_module import TensorFreeModule
        if (k,l) not in self._tensor_modules:
            self._tensor_modules[(k,l)] = TensorFreeModule(self, (k,l))
        return self._tensor_modules[(k,l)]

    def dual_exterior_power(self, p):
        r"""
        Return the `p`-th exterior power of the dual of ``self``.

        If `M` stands for the free module ``self``, the *p-th exterior power*
        of the dual of `M` is the set
        `\Lambda^p(M^*)` of all *alternating forms of degree* `p` on `M`, i.e. of
        all multilinear maps
        
        .. MATH::
        
            \underbrace{M\times\cdots\times M}_{p\ \; \mbox{times}}
            \longrightarrow R
        
        that vanish whenever any of two of their arguments are equals.
        `\Lambda^p(M^*)` is a free module of rank `\left({n\atop p}\right)`
        over the same ring as `M`, where `n` is the rank of `M`. 

        INPUT:

        - ``p`` -- positive integer

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.ext_pow_free_module.ExtPowerFreeModule`
          representing the free module `\Lambda^p(M^*)`

        EXAMPLES:

        """
        from sage.tensor.modules.ext_pow_free_module import ExtPowerFreeModule
        if p not in self._dual_exterior_powers:
            self._dual_exterior_powers[p] = ExtPowerFreeModule(self, p)
        return self._dual_exterior_powers[p]

    def basis(self, symbol=None, latex_symbol=None):
        r"""
        Define a basis of the free module.

        If the basis specified by the given symbol already exists, it is
        simply returned.

        INPUT:

        - ``symbol`` -- (default: ``None``) string; a letter (of a few letters)
          to denote a generic element of the basis; if ``None``, the module's
          default basis is returned
        - ``latex_symbol`` -- (default: ``None``) string; symbol to denote a
          generic element of the basis; if ``None``, the value of ``symbol``
          is used

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_basis.FreeModuleBasis`
          representing a basis on ``self``

        EXAMPLES:

        Bases on a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: e = M.basis('e') ; e
            Basis (e_0,e_1,e_2) on the Rank-3 free module M over the Integer Ring
            sage: e[0]
            Element e_0 of the Rank-3 free module M over the Integer Ring
            sage: latex(e)
            \left(e_0,e_1,e_2\right)

        The LaTeX symbol can be set explicitely, as the second argument of
        :meth:`basis`::

            sage: eps = M.basis('eps', r'\epsilon') ; eps
            Basis (eps_0,eps_1,eps_2) on the Rank-3 free module M
             over the Integer Ring
            sage: latex(eps)
            \left(\epsilon_0,\epsilon_1,\epsilon_2\right)

        If the provided symbol is that of an already defined basis, the latter
        is returned (no new basis is created)::

            sage: M.basis('e') is e
            True
            sage: M.basis('eps') is eps
            True

        If no symbol is provided, the module's default basis is returned::

            sage: M.basis()
            Basis (e_0,e_1,e_2) on the Rank-3 free module M over the Integer Ring
            sage: M.basis() is e
            True
            sage: M.basis() is M.default_basis()
            True

        The individual elements of the basis are labelled according the
        parameter ``start_index`` provided at the free module construction::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M', start_index=1)
            sage: e = M.basis('e') ; e
            Basis (e_1,e_2,e_3) on the Rank-3 free module M over the Integer Ring
            sage: e[1]
            Element e_1 of the Rank-3 free module M over the Integer Ring

        """
        from free_module_basis import FreeModuleBasis
        if symbol is None:
            return self.default_basis()

        for other in self._known_bases:
            if symbol == other._symbol:
                return other
        return FreeModuleBasis(self, symbol, latex_symbol)


    def tensor(self, tensor_type, name=None, latex_name=None, sym=None,
               antisym=None):
        r"""
        Construct a tensor on the free module.

        INPUT:

        - ``tensor_type`` -- pair ``(k, l)`` with ``k`` being the
          contravariant rank and ``l`` the covariant rank
        - ``name`` -- (default: ``None``) string; name given to the tensor
        - ``latex_name`` -- (default: ``None``) string;  LaTeX symbol to
          denote the tensor; if none is provided, the LaTeX symbol is set
          to ``name``
        - ``sym`` -- (default: ``None``) a symmetry or a list of symmetries
          among the tensor arguments: each symmetry is described by a tuple
          containing the positions of the involved arguments, with the
          convention ``position = 0`` for the first argument. For instance:

          * ``sym = (0,1)`` for a symmetry between the 1st and 2nd arguments
          * ``sym = [(0,2), (1,3,4)]`` for a symmetry between the 1st and 3rd
            arguments and a symmetry between the 2nd, 4th and 5th arguments.

        - ``antisym`` -- (default: ``None``) antisymmetry or list of
          antisymmetries among the arguments, with the same convention
          as for ``sym``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor.FreeModuleTensor`
          representing the tensor defined on ``self`` with the provided
          characteristics

        EXAMPLES:

        Tensors on a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: t = M.tensor((1,0), name='t') ; t
            Element t of the Rank-3 free module M over the Integer Ring
            sage: t = M.tensor((0,1), name='t') ; t
            Linear form t on the Rank-3 free module M over the Integer Ring
            sage: t = M.tensor((1,1), name='t') ; t
            Endomorphism tensor t on the Rank-3 free module M over the Integer Ring
            sage: t = M.tensor((0,2), name='t', sym=(0,1)) ; t
            Symmetric bilinear form t on the
             Rank-3 free module M over the Integer Ring
            sage: t = M.tensor((0,2), name='t', antisym=(0,1)) ; t
            Alternating form t of degree 2 on the
             Rank-3 free module M over the Integer Ring
            sage: t = M.tensor((1,2), name='t') ; t
            Type-(1,2) tensor t on the Rank-3 free module M over the Integer Ring

        See :class:`~sage.tensor.modules.free_module_tensor.FreeModuleTensor`
        for more examples and documentation.

        """
        from free_module_tensor_spec import FreeModuleEndomorphismTensor
        from free_module_alt_form import FreeModuleAltForm, FreeModuleLinForm
        if tensor_type == (1,0):
            return self.element_class(self, name=name, latex_name=latex_name)
            #!# the above is preferable to
            # return FiniteRankFreeModuleElement(self, name=name, latex_name=latex_name)
            # because self.element_class is a (dynamically created) derived
            # class of FiniteRankFreeModuleElement
        elif tensor_type == (0,1):
            return FreeModuleLinForm(self, name=name, latex_name=latex_name)
        elif tensor_type == (1,1):
            return FreeModuleEndomorphismTensor(self, name=name,
                                                latex_name=latex_name)
        elif tensor_type[0] == 0 and tensor_type[1] > 1 and antisym:
            if isinstance(antisym, list):
                antisym0 = antisym[0]
            else:
                antisym0 = antisym
            if len(antisym0) == tensor_type[1]:
                return FreeModuleAltForm(self, tensor_type[1], name=name,
                                         latex_name=latex_name)
            else:
                return self.tensor_module(*tensor_type).element_class(self,
                                        tensor_type, name=name,
                                        latex_name=latex_name, sym=sym,
                                        antisym=antisym)
        else:
            return self.tensor_module(*tensor_type).element_class(self,
                                    tensor_type, name=name,
                                    latex_name=latex_name, sym=sym,
                                    antisym=antisym)


    def tensor_from_comp(self, tensor_type, comp, name=None, latex_name=None):
        r"""
        Construct a tensor on the free module from a set of components.

        The tensor symmetries are deduced from those of the components.

        INPUT:

        - ``tensor_type`` -- pair ``(k, l)`` with ``k`` being the
          contravariant rank and ``l`` the covariant rank
        - ``comp`` -- instance of :class:`~sage.tensor.modules.comp.Components`
          representing the tensor components in a given basis
        - ``name`` -- (default: ``None``) string; name given to the tensor
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to denote
          the tensor; if none is provided, the LaTeX symbol is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor.FreeModuleTensor`
          representing the tensor defined on ``self`` with the provided
          characteristics.

        EXAMPLES:

        Construction of a tensor of rank 1::

            sage: from sage.tensor.modules.comp import Components, CompWithSym, CompFullySym, CompFullyAntiSym
            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: e = M.basis('e') ; e
            Basis (e_0,e_1,e_2) on the Rank-3 free module M over the Integer Ring
            sage: c = Components(ZZ, e, 1)
            sage: c[:]
            [0, 0, 0]
            sage: c[:] = [-1,4,2]
            sage: t = M.tensor_from_comp((1,0), c)
            sage: t
            Element of the Rank-3 free module M over the Integer Ring
            sage: t.display(e)
            -e_0 + 4 e_1 + 2 e_2
            sage: t = M.tensor_from_comp((0,1), c) ; t
            Linear form on the Rank-3 free module M over the Integer Ring
            sage: t.display(e)
            -e^0 + 4 e^1 + 2 e^2

        Construction of a tensor of rank 2::

            sage: c = CompFullySym(ZZ, e, 2)
            sage: c[0,0], c[1,2] = 4, 5
            sage: t = M.tensor_from_comp((0,2), c) ; t
            Symmetric bilinear form on the
             Rank-3 free module M over the Integer Ring
            sage: t.symmetries()
            symmetry: (0, 1);  no antisymmetry
            sage: t.display(e)
            4 e^0*e^0 + 5 e^1*e^2 + 5 e^2*e^1
            sage: c = CompFullyAntiSym(ZZ, e, 2)
            sage: c[0,1], c[1,2] = 4, 5
            sage: t = M.tensor_from_comp((0,2), c) ; t
            Alternating form of degree 2 on the
             Rank-3 free module M over the Integer Ring
            sage: t.display(e)
            4 e^0/\e^1 + 5 e^1/\e^2

        """
        from free_module_tensor_spec import FreeModuleEndomorphismTensor
        from free_module_alt_form import FreeModuleAltForm, FreeModuleLinForm
        from comp import CompWithSym, CompFullySym, CompFullyAntiSym
        #
        # 0/ Compatibility checks:
        if comp._ring is not self._ring:
             raise TypeError("the components are not defined on the same" +
                            " ring as the module")
        if comp._frame not in self._known_bases:
            raise TypeError("the components are not defined on a basis of" +
                            " the module")
        if comp._nid != tensor_type[0] + tensor_type[1]:
            raise TypeError("number of component indices not compatible with "+
                            " the tensor type")
        #
        # 1/ Construction of the tensor:
        if tensor_type == (1,0):
            resu = self.element_class(self, name=name, latex_name=latex_name)
            #!# the above is preferable to
            # resu = FiniteRankFreeModuleElement(self, name=name, latex_name=latex_name)
            # because self.element_class is a (dynamically created) derived
            # class of FiniteRankFreeModuleElement
        elif tensor_type == (0,1):
            resu = FreeModuleLinForm(self, name=name, latex_name=latex_name)
        elif tensor_type == (1,1):
            resu = FreeModuleEndomorphismTensor(self, name=name,
                                                latex_name=latex_name)
        elif tensor_type[0] == 0 and tensor_type[1] > 1 and \
                                        isinstance(comp, CompFullyAntiSym):
            resu = FreeModuleAltForm(self, tensor_type[1], name=name,
                                     latex_name=latex_name)
        else:
            resu = self.tensor_module(*tensor_type).element_class(self,
                                 tensor_type, name=name, latex_name=latex_name)
            # Tensor symmetries deduced from those of comp:
            if isinstance(comp, CompWithSym):
                resu._sym = comp._sym
                resu._antisym = comp._antisym
        #
        # 2/ Tensor components set to comp:
        resu._components[comp._frame] = comp
        #
        return resu

    def alternating_form(self, degree, name=None, latex_name=None):
        r"""
        Construct an alternating form on the free module.

        INPUT:

        - ``degree`` -- the degree of the alternating form (i.e. its
          tensor rank)
        - ``name`` -- (default: ``None``) string; name given to the
          alternating form
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
          denote the alternating form; if none is provided, the LaTeX symbol
          is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_alt_form.FreeModuleAltForm`
          (``degree`` > 1) or
          :class:`~sage.tensor.modules.free_module_alt_form.FreeModuleLinForm`
          (``degree`` = 1)

        EXAMPLES:

        Alternating forms on a rank-3 module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: a = M.alternating_form(2, 'a') ; a
            Alternating form a of degree 2 on the
             Rank-3 free module M over the Integer Ring

        The nonzero components in a given basis have to be set in a second
        step, thereby fully specifying the alternating form::

            sage: e = M.basis('e') ; e
            Basis (e_0,e_1,e_2) on the Rank-3 free module M over the Integer Ring
            sage: a.set_comp(e)[0,1] = 2
            sage: a.set_comp(e)[1,2] = -3
            sage: a.display(e)
            a = 2 e^0/\e^1 - 3 e^1/\e^2

        An alternating form of degree 1 is a linear form::

            sage: a = M.alternating_form(1, 'a') ; a
            Linear form a on the Rank-3 free module M over the Integer Ring

        To construct such a form, it is preferable to call the method
        :meth:`linear_form` instead::

            sage: a = M.linear_form('a') ; a
            Linear form a on the Rank-3 free module M over the Integer Ring

        See
        :class:`~sage.tensor.modules.free_module_alt_form.FreeModuleAltForm`
        for further documentation.

        """
        return self.dual_exterior_power(degree).element_class(self, degree,
                                                              name=name,
                                                         latex_name=latex_name)

    def linear_form(self, name=None, latex_name=None):
        r"""
        Construct a linear form on the free module.

        A *linear form* on a free module `M` over a ring `R` is a map
        `M \rightarrow R` that is linear. It can be viewed as a tensor of type
        `(0,1)` on `M`.

        INPUT:

        - ``name`` -- (default: ``None``) string; name given to the linear
          form
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
          denote the linear form; if none is provided, the LaTeX symbol
          is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_alt_form.FreeModuleLinForm`

        EXAMPLES:

        Linear form on a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: e = M.basis('e')
            sage: a = M.linear_form('A') ; a
            Linear form A on the Rank-3 free module M over the Integer Ring
            sage: a[:] = [2,-1,3]  # components w.r.t. the module's default basis (e)
            sage: a.display()
            A = 2 e^0 - e^1 + 3 e^2

        A linear form maps module elements to ring elements::

            sage: v = M([1,1,1])
            sage: a(v)
            4

        Test of linearity::

            sage: u = M([-5,-2,7])
            sage: a(3*u - 4*v) == 3*a(u) - 4*a(v)
            True

        See
        :class:`~sage.tensor.modules.free_module_alt_form.FreeModuleLinForm`
        for further documentation.

        """
        return self.dual_exterior_power(1).element_class(self, 1, name=name,
                                                         latex_name=latex_name)

    def endomorphism_tensor(self, name=None, latex_name=None):
        r"""
        Construct a tensor of type-(1,1) on the free module ``self``.

        .. NOTE::

            This method differs from :meth:`endomorphism` for it returns a
            tensor, while :meth:`endomorphism` returns an instance of Sage's :class:`~sage.categories.map.Map` (actually an instance of the subclass
            :class:`~sage.tensor.modules.free_module_morphism.FiniteRankFreeModuleMorphism`).

        INPUT:

        - ``name`` -- (default: ``None``) string; name given to the
          tensor
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
          denote the tensor; if none is provided, the LaTeX symbol
          is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleEndomorphismTensor`

        EXAMPLES:

        Endomorphism as a type-(1,1) tensor on a rank-3 module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: t = M.endomorphism_tensor('T') ; t
            Endomorphism tensor T on the Rank-3 free module M over the Integer Ring
            sage: t.parent()
            Free module of type-(1,1) tensors on the
             Rank-3 free module M over the Integer Ring
            sage: t.tensor_type()
            (1, 1)

        The method :meth:`tensor` with the argument ``(1,1)`` can be used as
        well::

            sage: t = M.tensor((1,1), name='T') ; t
            Endomorphism tensor T on the Rank-3 free module M over the Integer Ring

        See
        :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleEndomorphismTensor`
        for further documentation.

        """
        from free_module_tensor_spec import FreeModuleEndomorphismTensor
        return FreeModuleEndomorphismTensor(self, name=name, latex_name=latex_name)


    def automorphism_tensor(self, name=None, latex_name=None):
        r"""
        Construct an invertible type-(1,1) tensor on the free module ``self``.

        INPUT:

        - ``name`` -- (default: ``None``) string; name given to the
          tensor
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
          denote the tensor; if none is provided, the LaTeX symbol
          is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleAutomorphismTensor`

        EXAMPLES:

        Automorphism tensor on a rank-2 free module (vector space) on `\QQ`::

            sage: M = FiniteRankFreeModule(QQ, 2, name='M')
            sage: a = M.automorphism_tensor('A') ; a
            Automorphism tensor A on the Rank-2 free module M over the Rational Field
            sage: a.parent()
            Free module of type-(1,1) tensors on the
             Rank-2 free module M over the Rational Field
            sage: a.tensor_type()
            (1, 1)

        See
        :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleAutomorphismTensor`
        for further documentation.

        """
        from free_module_tensor_spec import FreeModuleAutomorphismTensor
        return FreeModuleAutomorphismTensor(self, name=name,
                                            latex_name=latex_name)


    def identity_tensor(self, name='Id', latex_name=None):
        r"""
        Construct the type-(1,1) tensor representing the identity map of
        the free module ``self``

        INPUT:

        - ``name`` -- (default: ``'Id'``) string; name given to the
          identity tensor
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
          denote the identity tensor; if none is provided, the LaTeX symbol
          is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleIdentityTensor`

        EXAMPLES:

        Identity tensor of a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: e = M.basis('e')
            sage: a = M.identity_tensor() ; a
            Identity tensor on the Rank-3 free module M over the Integer Ring

        The LaTeX symbol is set by default to `\mathrm{Id}`, but can
        be changed::

            sage: latex(a)
            \mathrm{Id}
            sage: a = M.identity_tensor(latex_name=r'\mathrm{1}')
            sage: latex(a)
            \mathrm{1}

        The identity is a tensor of type `(1,1)` on the free module::

            sage: a.parent()
            Free module of type-(1,1) tensors on the
             Rank-3 free module M over the Integer Ring
            sage: a.tensor_type()
            (1, 1)

        See
        :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleIdentityTensor`
        for further documentation.

        """
        from free_module_tensor_spec import FreeModuleIdentityTensor
        return FreeModuleIdentityTensor(self, name=name, latex_name=latex_name)


    def sym_bilinear_form(self, name=None, latex_name=None):
        r"""
        Construct a symmetric bilinear form on the free module.

        INPUT:

        - ``name`` -- (default: ``None``) string; name given to the symmetric
          bilinear form
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to
          denote the symmetric bilinear form; if none is provided, the LaTeX
          symbol is set to ``name``

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor.FreeModuleTensor`
          of tensor type `(0,2)` and symmetric

        EXAMPLES:

        Symmetric bilinear form on a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: a = M.sym_bilinear_form('A') ; a
            Symmetric bilinear form A on the
             Rank-3 free module M over the Integer Ring

        A symmetric bilinear form is a type-(0,2) tensor that is symmetric::

            sage: a.parent()
            Free module of type-(0,2) tensors on the
             Rank-3 free module M over the Integer Ring
            sage: a.tensor_type()
            (0, 2)
            sage: a.tensor_rank()
            2
            sage: a.symmetries()
            symmetry: (0, 1);  no antisymmetry

        Components with respect to a given basis::

            sage: e = M.basis('e')
            sage: a[0,0], a[0,1], a[0,2] = 1, 2, 3
            sage: a[1,1], a[1,2] = 4, 5
            sage: a[2,2] = 6

        Only independent components have been set; the other ones are
        deduced by symmetry::

            sage: a[1,0], a[2,0], a[2,1]
            (2, 3, 5)
            sage: a[:]
            [1 2 3]
            [2 4 5]
            [3 5 6]

        A symmetric bilinear form acts on pairs of module elements::

            sage: u = M([2,-1,3]) ; v = M([-2,4,1])
            sage: a(u,v)
            61
            sage: a(v,u) == a(u,v)
            True

        The sum of two symmetric bilinear forms is another symmetric bilinear
        form::

            sage: b = M.sym_bilinear_form('B')
            sage: b[0,0], b[0,1], b[1,2] = -2, 1, -3
            sage: s = a + b ; s
            Symmetric bilinear form A+B on the
             Rank-3 free module M over the Integer Ring
            sage: a[:], b[:], s[:]
            (
            [1 2 3]  [-2  1  0]  [-1  3  3]
            [2 4 5]  [ 1  0 -3]  [ 3  4  2]
            [3 5 6], [ 0 -3  0], [ 3  2  6]
            )

        Adding a symmetric bilinear from with a non-symmetric one results in a
        generic type-`(0,2)` tensor::

            sage: c = M.tensor((0,2), name='C')
            sage: c[0,1] = 4
            sage: s = a + c ; s
            Type-(0,2) tensor A+C on the Rank-3 free module M over the Integer Ring
            sage: s.symmetries()
            no symmetry;  no antisymmetry
            sage: s[:]
            [1 6 3]
            [2 4 5]
            [3 5 6]

        See :class:`~sage.tensor.modules.free_module_tensor.FreeModuleTensor`
        for more documentation.

        """
        return self.tensor_module(0,2).element_class(self, (0,2), name=name,
                                              latex_name=latex_name, sym=(0,1))

    #### End of methods to be redefined by derived classes ####

    def _latex_(self):
        r"""
        LaTeX representation of the object.

        EXAMPLES::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: M._latex_()
            'M'
            sage: latex(M)
            M
            sage: M1 = FiniteRankFreeModule(ZZ, 3, name='M', latex_name=r'\mathcal{M}')
            sage: M1._latex_()
            '\\mathcal{M}'
            sage: latex(M1)
            \mathcal{M}

        """
        if self._latex_name is None:
            return r'\mbox{' + str(self) + r'}'
        else:
           return self._latex_name

    def rank(self):
        r"""
        Return the rank of the free module ``self``.

        Since the ring over which ``self`` is built is assumed to be
        commutative (and hence has the invariant basis number property), the
        rank is defined uniquely, as the cardinality of any basis of ``self``.

        EXAMPLES:

        Rank of free modules over `\ZZ`::

            sage: M = FiniteRankFreeModule(ZZ, 3)
            sage: M.rank()
            3
            sage: M.tensor_module(0,1).rank()
            3
            sage: M.tensor_module(0,2).rank()
            9
            sage: M.tensor_module(1,0).rank()
            3
            sage: M.tensor_module(1,1).rank()
            9
            sage: M.tensor_module(1,2).rank()
            27
            sage: M.tensor_module(2,2).rank()
            81

        """
        return self._rank

    def zero(self):
        r"""
        Return the zero element.

        EXAMPLES:

        Zero elements of free modules over `\ZZ`::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: M.zero()
            Element zero of the Rank-3 free module M over the Integer Ring
            sage: M.zero().parent() is M
            True
            sage: M.zero() is M(0)
            True
            sage: T = M.tensor_module(1,1)
            sage: T.zero()
            Type-(1,1) tensor zero on the Rank-3 free module M over the Integer Ring
            sage: T.zero().parent() is T
            True
            sage: T.zero() is T(0)
            True

        Components of the zero element with respect to some basis::

            sage: e = M.basis('e')
            sage: M.zero().comp(e)[:]
            [0, 0, 0]
            sage: all(M.zero().comp(e)[i] == M.base_ring().zero() for i in M.irange())
            True
            sage: T.zero().comp(e)[:]
            [0 0 0]
            [0 0 0]
            [0 0 0]
            sage: M.tensor_module(1,2).zero().comp(e)[:]
            [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
             [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
             [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

        """
        return self._zero_element

    def dual(self):
        r"""
        Return the dual module.

        EXAMPLE:

        Dual of a free module over `\ZZ`::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: M.dual()
            Dual of the Rank-3 free module M over the Integer Ring
            sage: latex(M.dual())
            M^*

        The dual is a free module of the same rank as M::

            sage: isinstance(M.dual(), FiniteRankFreeModule)
            True
            sage: M.dual().rank()
            3

        It is formed by alternating forms of degree 1, i.e. linear forms::

            sage: M.dual() is M.dual_exterior_power(1)
            True
            sage: M.dual().an_element()
            Linear form on the Rank-3 free module M over the Integer Ring
            sage: a = M.linear_form()
            sage: a in M.dual()
            True

        The elements of a dual basis belong of course to the dual module::

            sage: e = M.basis('e')
            sage: e.dual_basis()[0] in M.dual()
            True

        """
        return self.dual_exterior_power(1)

    def irange(self, start=None):
        r"""
        Single index generator, labelling the elements of a basis.

        INPUT:

        - ``start`` -- (default: ``None``) integer; initial value of the
          index; if none is provided, ``self._sindex`` is assumed

        OUTPUT:

        - an iterable index, starting from ``start`` and ending at
          ``self._sindex + self.rank() - 1``

        EXAMPLES:

        Index range on a rank-3 module::

            sage: M = FiniteRankFreeModule(ZZ, 3)
            sage: for i in M.irange(): print i,
            0 1 2
            sage: for i in M.irange(start=1): print i,
            1 2

        The default starting value corresponds to the parameter ``start_index``
        provided at the module construction (the default value being 0)::

            sage: M1 = FiniteRankFreeModule(ZZ, 3, start_index=1)
            sage: for i in M1.irange(): print i,
            1 2 3
            sage: M2 = FiniteRankFreeModule(ZZ, 3, start_index=-4)
            sage: for i in M2.irange(): print i,
            -4 -3 -2

        """
        si = self._sindex
        imax = self._rank + si
        if start is None:
            i = si
        else:
            i = start
        while i < imax:
            yield i
            i += 1

    def default_basis(self):
        r"""
        Return the default basis of the free module.

        The *default basis* is simply a basis whose name can be skipped in
        methods requiring a basis as an argument. By default, it is the first
        basis introduced on the module. It can be changed by the method
        :meth:`set_default_basis`.

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_basis.FreeModuleBasis`

        EXAMPLES:

        At the module construction, no default basis is assumed::

            sage: M = FiniteRankFreeModule(ZZ, 2, name='M', start_index=1)
            sage: M.default_basis()
            No default basis has been defined on the
             Rank-2 free module M over the Integer Ring

        The first defined basis becomes the default one::

            sage: e = M.basis('e') ; e
            Basis (e_1,e_2) on the Rank-2 free module M over the Integer Ring
            sage: M.default_basis()
            Basis (e_1,e_2) on the Rank-2 free module M over the Integer Ring
            sage: f =  M.basis('f') ; f
            Basis (f_1,f_2) on the Rank-2 free module M over the Integer Ring
            sage: M.default_basis()
            Basis (e_1,e_2) on the Rank-2 free module M over the Integer Ring

        """
        if self._def_basis is None:
            print("No default basis has been defined on the " + str(self))
        return self._def_basis

    def set_default_basis(self, basis):
        r"""
        Sets the default basis of ``self``.

        The *default basis* is simply a basis whose name can be skipped in
        methods requiring a basis as an argument. By default, it is the first
        basis introduced on the module.

        INPUT:

        - ``basis`` -- instance of
          :class:`~sage.tensor.modules.free_module_basis.FreeModuleBasis`
          representing a basis on ``self``

        EXAMPLES:

        Changing the default basis on a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M', start_index=1)
            sage: e = M.basis('e') ; e
            Basis (e_1,e_2,e_3) on the Rank-3 free module M over the Integer Ring
            sage: f =  M.basis('f') ; f
            Basis (f_1,f_2,f_3) on the Rank-3 free module M over the Integer Ring
            sage: M.default_basis()
            Basis (e_1,e_2,e_3) on the Rank-3 free module M over the Integer Ring
            sage: M.set_default_basis(f)
            sage: M.default_basis()
            Basis (f_1,f_2,f_3) on the Rank-3 free module M over the Integer Ring

        """
        from free_module_basis import FreeModuleBasis
        if not isinstance(basis, FreeModuleBasis):
            raise TypeError("the argument is not a free module basis")
        if basis._fmodule is not self:
            raise ValueError("the basis is not defined on the current module")
        self._def_basis = basis

    def print_bases(self):
        r"""
        Display the bases that have been defined on the free module.

        Use the method :meth:`bases` to get the raw list of bases.

        EXAMPLES:

        Bases on a rank-4 free module::

            sage: M = FiniteRankFreeModule(ZZ, 4, name='M', start_index=1)
            sage: M.print_bases()
            No basis has been defined on the
             Rank-4 free module M over the Integer Ring
            sage: e = M.basis('e')
            sage: M.print_bases()
            Bases defined on the Rank-4 free module M over the Integer Ring:
             - (e_1,e_2,e_3,e_4) (default basis)
            sage: f = M.basis('f')
            sage: M.print_bases()
            Bases defined on the Rank-4 free module M over the Integer Ring:
             - (e_1,e_2,e_3,e_4) (default basis)
             - (f_1,f_2,f_3,f_4)
            sage: M.set_default_basis(f)
            sage: M.print_bases()
            Bases defined on the Rank-4 free module M over the Integer Ring:
             - (e_1,e_2,e_3,e_4)
             - (f_1,f_2,f_3,f_4) (default basis)

        """
        if not self._known_bases:
            print("No basis has been defined on the " + str(self))
        else:
            print("Bases defined on the " + str(self) + ":")
            for basis in self._known_bases:
                item = " - " + basis._name
                if basis is self._def_basis:
                    item += " (default basis)"
                print(item)

    def bases(self):
        r"""
        Return the list of bases that have been defined on the free module.

        Use the method :meth:`print_bases` to get a formatted output with more
        information.

        OUTPUT:

        - list of instances of class
          :class:`~sage.tensor.modules.free_module_basis.FreeModuleBasis`

        EXAMPLES:

        Bases on a rank-3 free module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M_3', start_index=1)
            sage: M.bases()
            []
            sage: e = M.basis('e')
            sage: M.bases()
            [Basis (e_1,e_2,e_3) on the Rank-3 free module M_3 over the Integer Ring]
            sage: f = M.basis('f')
            sage: M.bases()
            [Basis (e_1,e_2,e_3) on the Rank-3 free module M_3 over the Integer Ring,
             Basis (f_1,f_2,f_3) on the Rank-3 free module M_3 over the Integer Ring]

        """
        return self._known_bases

    def change_of_basis(self, basis1, basis2):
        r"""
        Return a change of basis previously defined on the free module.

        INPUT:

        - ``basis1`` -- basis 1, denoted `(e_i)` below
        - ``basis2`` -- basis 2, denoted `(f_i)` below

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleAutomorphismTensor`
          describing the automorphism `P` that relates the basis `(e_i)` to the
          basis `(f_i)` according to `f_i = P(e_i)`

        .. TODO::

            Suppose there exists change of bases
            `A \leftrightarrow B \leftrightarrow C`, then do we want to
            compute the change of basis `A \leftrightarrow C`?

        EXAMPLES:

        Changes of basis on a rank-2 free module::

            sage: M = FiniteRankFreeModule(QQ, 2, name='M', start_index=1)
            sage: e = M.basis('e')
            sage: a = M.automorphism_tensor()
            sage: a[:] = [[1, 2], [-1, 3]]
            sage: f = e.new_basis(a, 'f')
            sage: M.change_of_basis(e,f)
            Automorphism tensor on the Rank-2 free module M over the Rational Field
            sage: M.change_of_basis(e,f)[:]
            [ 1  2]
            [-1  3]
            sage: M.change_of_basis(f,e)[:]
            [ 3/5 -2/5]
            [ 1/5  1/5]

        """
        if (basis1, basis2) not in self._basis_changes:
            if (basis2, basis1) not in self._basis_changes:
                raise TypeError(("the change of basis from '{!r}' to '{!r}'"
                                + "has not been defined on the {!r}"
                                ).format(basis1, basis2, self))
            inv = self._basis_changes[(basis2, basis1)].inverse()
            self._basis_changes[(basis1, basis2)] = inv
            return inv
        return self._basis_changes[(basis1, basis2)]

    def set_change_of_basis(self, basis1, basis2, change_of_basis,
                         compute_inverse=True):
        r"""
        Relates two bases by an automorphism.

        This updates the internal dictionary ``self._basis_changes``.

        INPUT:

        - ``basis1`` -- basis 1, denoted `(e_i)` below
        - ``basis2`` -- basis 2, denoted `(f_i)` below
        - ``change_of_basis`` -- instance of class
          :class:`~sage.tensor.modules.free_module_tensor_spec.FreeModuleAutomorphismTensor`
          describing the automorphism `P` that relates the basis `(e_i)` to
          the basis `(f_i)` according to `f_i = P(e_i)`
        - ``compute_inverse`` (default: ``True``) -- if set to ``True``, the
          inverse automorphism is computed and the change from basis `(f_i)`
          to `(e_i)` is set to it in the internal dictionary
          ``self._basis_changes``

        EXAMPLES:

        Defining a change of basis on a rank-2 free module::

            sage: M = FiniteRankFreeModule(QQ, 2, name='M')
            sage: e = M.basis('e')
            sage: f = M.basis('f')
            sage: a = M.automorphism_tensor()
            sage: a[:] = [[1, 2], [-1, 3]]
            sage: M.set_change_of_basis(e, f, a)

        The change of basis and its inverse have been recorded::

            sage: M.change_of_basis(e,f)[:]
            [ 1  2]
            [-1  3]
            sage: M.change_of_basis(f,e)[:]
            [ 3/5 -2/5]
            [ 1/5  1/5]

        and are effective::

            sage: f[0].display(e)
            f_0 = e_0 - e_1
            sage: e[0].display(f)
            e_0 = 3/5 f_0 + 1/5 f_1

        """
        from free_module_tensor_spec import FreeModuleAutomorphismTensor
        if not isinstance(change_of_basis, FreeModuleAutomorphismTensor):
            raise TypeError("the argument change_of_basis must be some " +
                            "instance of FreeModuleAutomorphismTensor")
        self._basis_changes[(basis1, basis2)] = change_of_basis
        if compute_inverse:
            self._basis_changes[(basis2, basis1)] = change_of_basis.inverse()

    def hom(self, codomain, matrix_rep, bases=None, name=None,
            latex_name=None):
        r"""
        Homomorphism from ``self`` to a free module.

        Define a module homomorphism

        .. MATH::

            \phi:\ M \longrightarrow N,

        where `M` is ``self`` and  `N` is a free module of finite rank
        over the same ring `R` as ``self``.

        .. NOTE::

            This method is a redefinition of
            :meth:`sage.structure.parent.Parent.hom` because the latter assumes
            that ``self`` has some privileged generators, while an instance of
            :class:`FiniteRankFreeModule` has no privileged basis.

        INPUT:

        - ``codomain`` -- the target module `N`
        - ``matrix_rep`` -- matrix of size rank(N)*rank(M) representing the
          homomorphism with respect to the pair of bases defined by ``bases``;
          this entry can actually be any material from which a matrix of
          elements of `R` can be constructed; the *columns* of
          ``matrix_rep`` must be the components w.r.t. ``basis_N`` of
          the images of the elements of ``basis_M``.
        - ``bases`` -- (default: ``None``) pair ``(basis_M, basis_N)`` defining
          the matrix representation, ``basis_M`` being a basis of ``self`` and
          ``basis_N`` a basis of module `N` ; if None the pair formed by the
          default bases of each module is assumed.
        - ``name`` -- (default: ``None``) string; name given to the 
          homomorphism
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to denote
          the homomorphism; if None, ``name`` will be used.

        OUTPUT:

        - the homomorphism `\phi: M \rightarrow N` corresponding to the given
          specifications, as an instance of
          :class:`~sage.tensor.modules.free_module_morphism.FiniteRankFreeModuleMorphism`

        EXAMPLES:

        Homomorphism between two free modules over `\ZZ`::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: N = FiniteRankFreeModule(ZZ, 2, name='N')
            sage: e = M.basis('e')
            sage: f = N.basis('f')
            sage: phi = M.hom(N, [[-1,2,0], [5,1,2]]) ; phi
            Generic morphism:
              From: Rank-3 free module M over the Integer Ring
              To:   Rank-2 free module N over the Integer Ring

        Homomorphism defined by a matrix w.r.t. bases that are not the
        default ones::

            sage: ep = M.basis('ep', latex_symbol=r"e'")
            sage: fp = N.basis('fp', latex_symbol=r"f'")
            sage: phi = M.hom(N, [[3,2,1], [1,2,3]], bases=(ep, fp)) ; phi
            Generic morphism:
              From: Rank-3 free module M over the Integer Ring
              To:   Rank-2 free module N over the Integer Ring

        Call with all arguments specified::

            sage: phi = M.hom(N, [[3,2,1], [1,2,3]], bases=(ep, fp), 
            ....:             name='phi', latex_name=r'\phi')

        The parent::

            sage: phi.parent() is Hom(M,N)
            True

        See class
        :class:`~sage.tensor.modules.free_module_morphism.FiniteRankFreeModuleMorphism`
        for more documentation.

        """
        from sage.categories.homset import Hom
        homset = Hom(self, codomain)
        return homset(matrix_rep, bases=bases, name=name,
                      latex_name=latex_name)

    def endomorphism(self, matrix_rep, basis=None, name=None, latex_name=None):
        r"""
        Contruct an endomorphism of the free module ``self``.

        The returned object is a module morphism `\phi: M \rightarrow M`,
        where `M` is ``self``.

        .. NOTE::

            This method differs from :meth:`endomorphism_tensor` for it
            returns an instance of Sage's :class:`~sage.categories.map.Map`
            (actually an instance of the subclass
            :class:`~sage.tensor.modules.free_module_morphism.FiniteRankFreeModuleMorphism`),
            while :meth:`endomorphism_tensor` returns a tensor of type (1,1).
            Note that there are coercions between these two types.

        INPUT:

        - ``matrix_rep`` -- matrix of size rank(M)*rank(M) representing the
          endomorphism with respect to ``basis``;
          this entry can actually be any material from which a matrix of
          elements of ``self`` base ring can be constructed; the *columns* of
          ``matrix_rep`` must be the components w.r.t. ``basis`` of
          the images of the elements of ``basis``.
        - ``basis`` -- (default: ``None``) basis of ``self`` defining the
          matrix representation; if None the default basis of ``self`` is
          assumed.
        - ``name`` -- (default: ``None``) string; name given to the 
          endomorphism
        - ``latex_name`` -- (default: ``None``) string; LaTeX symbol to denote
          the endomorphism; if none is provided, ``name`` will be used.

        OUTPUT:

        - the endomorphism `\phi: M \rightarrow M` corresponding to the given
          specifications, as an instance of
          :class:`~sage.tensor.modules.free_module_morphism.FiniteRankFreeModuleMorphism`

        EXAMPLES:

        Construction of an endomorphism with minimal data (module's default
        basis and no name)::

            sage: M = FiniteRankFreeModule(ZZ, 2, name='M')
            sage: e = M.basis('e')
            sage: phi = M.endomorphism([[1,-2], [-3,4]]) ; phi
            Generic endomorphism of Rank-2 free module M over the Integer Ring
            sage: phi.matrix()  # matrix w.r.t the default basis
            [ 1 -2]
            [-3  4]

        Construction with full list of arguments (matrix given a basis
        different from the default one)::

            sage: a = M.automorphism_tensor() ; a[0,1], a[1,0] = 1, -1
            sage: ep = e.new_basis(a, 'ep', latex_symbol="e'")
            sage: phi = M.endomorphism([[1,-2], [-3,4]], basis=ep, name='phi',
            ....:                      latex_name=r'\phi')
            sage: phi
            Generic endomorphism of Rank-2 free module M over the Integer Ring
            sage: phi.matrix(ep)  # the input matrix
            [ 1 -2]
            [-3  4]
            sage: phi.matrix()  # matrix w.r.t the default basis
            [4 3]
            [2 1]

        """
        from sage.categories.homset import End
        if basis is None:
            basis = self.default_basis()
        return End(self)(matrix_rep, bases=(basis,basis), name=name, 
                         latex_name=latex_name)

    def identity_map(self):
        r"""
        Return the identity endomorphism of the free module ``self``.

        OUTPUT:

        - the identity map of ``self`` as an instance of
          :class:`~sage.tensor.modules.free_module_morphism.FiniteRankFreeModuleMorphism`

        EXAMPLES:

        Identity endomorphism of a rank-3 `\ZZ`-module::

            sage: M = FiniteRankFreeModule(ZZ, 3, name='M')
            sage: e = M.basis('e')
            sage: Id = M.identity_map() ; Id
            Identity endomorphism of Rank-3 free module M over the Integer Ring
            sage: latex(Id)
            \mathrm{Id}

        The identity endomorphism is actually the unit of End(M)::

            sage: Id is End(M).one()
            True

        """ 
        from sage.categories.homset import End
        if self._identity_map is None:
            self._identity_map = End(self).one()
        return self._identity_map
