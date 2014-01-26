r"""
Tensor free modules

The class :class:`FiniteFreeModule` implements free modules `M` of finite rank
over a commutative ring `R`. It inherits (via :class:`TensorFreeModule`) from 
the generic class :class:`sage.modules.module.Module`. 

The class :class:`TensorFreeModule` implements the free modules `T^{(k,l)}(M)` 
of tensors of type `(k,l)` acting as multilinear forms on a free module `M` 
of finite rank over a commutative ring `R`. The module `T^{(k,l)}(M)` is
canonically identified with the following tensor product:

.. MATH::

    T^{(k,l)}(M) = \underbrace{M\otimes\cdots\otimes M}_{k\ \; \mbox{times}}
    \otimes \underbrace{M^*\otimes\cdots\otimes M^*}_{l\ \; \mbox{times}}
    
where `M^*` stands for the dual of the free module `M`. 
In particular, the free module `M` itself is canonically identified 
with `T^{(1,0)}(M)`. Accordingly, the class :class:`FiniteFreeModule` 
inherits from  :class:`TensorFreeModule`. 

AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2014): initial version

EXAMPLES:

    Free module of rank 3 over `\ZZ`::
    
        sage: M = FiniteFreeModule(ZZ, 3, name='M') ; M
        rank-3 free module M over the Integer Ring
        sage: M.category()
        Category of modules over Integer Ring
        sage: M.rank()
        3

    Set of all tensors of type (1,2) defined on the module M::
    
        sage: T = M.tensor_module(1,2) ; T
        free module of type-(1,2) tensors on the rank-3 free module M over the Integer Ring
        sage: T.category()
        Category of modules over Integer Ring
        sage: T.rank()
        27

    The module `M` itself is considered as the set of tensors of type (1,0)::
    
        sage: M is M.tensor_module(1,0)
        True

    If the base ring is a field, the free module is in the category of vector 
    spaces::
    
        sage: M = FiniteFreeModule(QQ, 3, name='M') ; M
        rank-3 free module M over the Rational Field
        sage: M.category()
        Category of vector spaces over Rational Field
  
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

from sage.modules.module import Module
from free_module_tensor import FreeModuleTensor, FreeModuleVector

# From sage/modules/module.pyx:
# ----------------------------
### The new Module class that should be the base of all Modules
### The derived Module class must implement the element
### constructor:
#
# class MyModule(sage.modules.module.Module):
#     Element = MyElement
#     def _element_constructor_(self, x):
#         return self.element_class(x)
#


class TensorFreeModule(Module):
    r"""
    Set `T^{(k,l)}(M)` of tensors of type `(k,l)` acting as multilinear 
    forms on a free module `M` over a commutative ring `R`. 
    `T^{(k,l)}(M)` is a free module over `R`, which can be canonically 
    identified with the following tensor product of modules:

    .. MATH::
    
        T^{(k,l)}(M) = \underbrace{M\otimes\cdots\otimes M}_{k\ \; \mbox{times}}
        \otimes \underbrace{M^*\otimes\cdots\otimes M^*}_{l\ \; \mbox{times}}
        
    where `M^*` stands for the dual of the free module `M`. 
    
    .. NOTE::
    
        The class :class:`TensorFreeModule` inherits from the generic class
        :class:`sage.modules.module.Module` and not from 
        :class:`sage.modules.free_module.FreeModule_generic` since the latter 
        is a derived class of :class:`sage.modules.module.Module_old`, which 
        does not conform to the new coercion model.
        Besides, the class :class:`TensorFreeModule` does not inherit 
        from the class :class:`CombinatorialFreeModule` since the latter is
        devoted to modules *with a basis*. 

    :class:`TensorFreeModule` is a Sage *Parent* class whose elements belong 
    to the class :class:`FreeModuleTensor`. 

    INPUT:
    
    - ``fmodule`` -- free module `M` of finite rank (must be an instance of 
      :class:`FiniteFreeModule`)
    - ``tensor_type`` -- pair (k,l) with k being the contravariant rank and l 
      the covariant rank
    - ``name`` -- (string; default: None) name given to the tensor module
    - ``latex_name`` -- (string; default: None) LaTeX symbol to denote the 
      tensor module; if none is provided, it is set to ``name``
    
    EXAMPLES:
    
    Set of tensors of type (1,2) on a free module of rank 3 over `\ZZ`::
    
        sage: M = FiniteFreeModule(ZZ, 3, name='M')
        sage: T = TensorFreeModule(M, (1,2)) ; T
        free module of type-(1,2) tensors on the rank-3 free module M over the Integer Ring
        
    T is a module (actually a free module) over `\ZZ`::
    
        sage: T.category()
        Category of modules over Integer Ring
        sage: T in Modules(ZZ)
        True
        sage: T.rank()
        27

    T is a *parent* object, whose elements are instances of 
    :class:`FreeModuleTensor`::

        sage: t = T.an_element() ; t
        type-(1,2) tensor on the rank-3 free module M over the Integer Ring
        sage: from sage.geometry.manifolds.free_module_tensor import FreeModuleTensor
        sage: isinstance(t, FreeModuleTensor)
        True
        sage: t in T
        True
        sage: T.is_parent_of(t)
        True

    Elements can be constructed by means of the __call__ operator acting 
    on the parent; 0 yields the zero element::
        
        sage: T(0)
        type-(1,2) tensor zero on the rank-3 free module M over the Integer Ring
        sage: T(0) is T.zero()
        True
        
    Non-zero elements are constructed by providing their components in 
    a given basis::
    
        sage: e = M.new_basis('e') ; e
        basis (e_0,e_1,e_2) on the rank-3 free module M over the Integer Ring
        sage: comp = [[[i-j+k for k in range(3)] for j in range(3)] for i in range(3)]
        sage: t = T(comp, basis=e, name='t') ; t
        type-(1,2) tensor t on the rank-3 free module M over the Integer Ring
        sage: t.comp(e)[:]
        [[[0, 1, 2], [-1, 0, 1], [-2, -1, 0]],
         [[1, 2, 3], [0, 1, 2], [-1, 0, 1]],
         [[2, 3, 4], [1, 2, 3], [0, 1, 2]]]
        sage: t.view(e)
        t = e_0*e^0*e^1 + 2 e_0*e^0*e^2 - e_0*e^1*e^0 + e_0*e^1*e^2 - 2 e_0*e^2*e^0 - e_0*e^2*e^1 + e_1*e^0*e^0 + 2 e_1*e^0*e^1 + 3 e_1*e^0*e^2 + e_1*e^1*e^1 + 2 e_1*e^1*e^2 - e_1*e^2*e^0 + e_1*e^2*e^2 + 2 e_2*e^0*e^0 + 3 e_2*e^0*e^1 + 4 e_2*e^0*e^2 + e_2*e^1*e^0 + 2 e_2*e^1*e^1 + 3 e_2*e^1*e^2 + e_2*e^2*e^1 + 2 e_2*e^2*e^2

    An alternative is to construct the tensor from an empty list of components
    and to set the nonzero components afterwards::
    
        sage: t = T([], name='t')
        sage: t.set_comp(e)[0,1,1] = -3
        sage: t.set_comp(e)[2,0,1] = 4
        sage: t.view(e)
        t = -3 e_0*e^1*e^1 + 4 e_2*e^0*e^1
    
    See the documentation of :class:`FreeModuleTensor` for the full list of
    arguments that can be provided to the __call__ operator. For instance, to
    contruct a tensor symmetric with respect to the last two indices::
    
        sage: t = T([], name='t', sym=(1,2))
        sage: t.set_comp(e)[0,1,1] = -3
        sage: t.set_comp(e)[2,0,1] = 4
        sage: t.view(e)  # notice that t^2_{10} has be set equal to t^2_{01} by symmetry
        t = -3 e_0*e^1*e^1 + 4 e_2*e^0*e^1 + 4 e_2*e^1*e^0
    
    The tensor modules over a given module `M` are unique::
    
        sage: T is M.tensor_module(1,2)
        True

    Instead of a direct call to the constructor of class 
    :class:`TensorFreeModule`, one should construct them by the method
    :meth:`FiniteFreeModule.tensor_module` of the base module::
    
        sage: T = M.tensor_module(1,2) ; T
        free module of type-(1,2) tensors on the rank-3 free module M over the Integer Ring
        sage: F = M.tensor_module(0,1) ; F
        free module of type-(0,1) tensors on the rank-3 free module M over the Integer Ring
        
    The base module itself is considered as the set of type-(1,0) tensors::
    
        sage: M is M.tensor_module(1,0)
        True
            
    """
    
    Element = FreeModuleTensor
    
    def __init__(self, fmodule, tensor_type, name=None, latex_name=None):
        self.tensor_type = tuple(tensor_type)
        Module.__init__(self, fmodule.ring)
        self.name = name
        if latex_name is None:
            self.latex_name = self.name
        else:
            self.latex_name = latex_name
        self._rank = pow(fmodule._rank, self.tensor_type[0] + self.tensor_type[1])
        self.fmodule = fmodule
        # Unique representation:
        if self.tensor_type in self.fmodule.tensor_modules:
            raise TypeError("The module of tensors of type" + 
                            str(self.tensor_type) + 
                            " has already been created.")
        else:
            self.fmodule.tensor_modules[self.tensor_type] = self
        # Zero element:
        ze = self._element_constructor_(name='zero', latex_name='0')
        for basis in self.fmodule.known_bases:
            ze.components[basis] = ze._new_comp(basis)
            # since a just-created set of components is initialized to zero
        self._zero_element = ze
    
    #### Methods required for any Parent 
    def _element_constructor_(self, comp=[], basis=None, name=None, 
                              latex_name=None, sym=None, antisym=None):
        r"""
        Construct a tensor
        """
        if comp == 0:
            return self._zero_element
        resu = self.element_class(self.fmodule, self.tensor_type, name=name, 
                                  latex_name=latex_name, sym=sym, 
                                  antisym=antisym)
        if comp != []:
            resu.set_comp(basis)[:] = comp
        return resu

    def _an_element_(self):
        r"""
        Construct some (unamed) tensor
        """
        return self.element_class(self.fmodule, self.tensor_type)
            
    #### End of methods required for any Parent 

    def _repr_(self):
        r"""
        String representation of the object.
        """
        description = "free module "
        if self.name is not None:
            description += self.name + " "
        description += "of type-(%s,%s)" % \
                           (str(self.tensor_type[0]), str(self.tensor_type[1]))
        description += " tensors on the " + str(self.fmodule)
        return description

    def _latex_(self):
        r"""
        LaTeX representation of the object.
        """
        if self.latex_name is None:
            return r'\mbox{' + str(self) + r'}'
        else:
           return self.latex_name

    def rank(self):
        r"""
        Return the rank of the free module ``self``.
        
        EXAMPLES:
        
        Rank of free modules over `\ZZ`::
        
            sage: M = FiniteFreeModule(ZZ, 3)
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
        
            sage: M = FiniteFreeModule(ZZ, 3, name='M')
            sage: M.zero()
            element zero of the rank-3 free module M over the Integer Ring
            sage: M.zero().parent() is M
            True
            sage: M.zero() is M(0)
            True
            sage: T = M.tensor_module(1,1)
            sage: T.zero()
            type-(1,1) tensor zero on the rank-3 free module M over the Integer Ring
            sage: T.zero().parent() is T
            True
            sage: T.zero() is T(0)
            True

        Components of the zero element with respect to some basis::
        
            sage: e = M.new_basis('e')
            sage: M.zero().comp(e)[:]
            [0, 0, 0]
            sage: for i in M.irange(): print M.zero().comp(e)[i] == M.base_ring().zero(),
            True True True
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

#******************************************************************************

class FiniteFreeModule(TensorFreeModule):
    r"""
    Free module of finite rank over a commutative ring `R`.

    This class inherits (via :class:`TensorFreeModule`) from the generic 
    class :class:`sage.modules.module.Module`. 
    
    .. NOTE::
    
        The class :class:`FiniteFreeModule` does not inherit from 
        :class:`sage.modules.free_module.FreeModule_generic` since the latter 
        is a derived class of :class:`sage.modules.module.Module_old`, 
        which does not conform to the new coercion model.
        Besides, the class :class:`FiniteFreeModule` does not inherit 
        from the class :class:`CombinatorialFreeModule` since the latter is
        devoted to modules *with a basis*. 

    The class :class:`FiniteFreeModule` is a Sage *Parent* class whose elements 
    belong to the class :class:`FreeModuleVector`. 

    INPUT:
    
    - ``ring`` -- commutative ring `R` over which the free module is 
      constructed.
    - ``rank`` -- (positive integer) rank of the free module
    - ``name`` -- (string; default: None) name given to the free module
    - ``latex_name`` -- (string; default: None) LaTeX symbol to denote the free 
      module; if none is provided, it is set to ``name``
    - ``start_index`` -- (integer; default: 0) lower bound of the range of 
      indices in bases defined on the free module
    - ``output_formatter`` -- (default: None) function or unbound 
      method called to format the output of the tensor components; 
      ``output_formatter`` must take 1 or 2 arguments: the 1st argument must be
      an element of the ring `R` and  the second one, if any, some format 
      specification.

    EXAMPLES:
    
    Free module of rank 3 over `\ZZ`::
    
        sage: M = FiniteFreeModule(ZZ, 3) ; M
        rank-3 free module over the Integer Ring
        sage: M = FiniteFreeModule(ZZ, 3, name='M') ; M  # declaration with a name
        rank-3 free module M over the Integer Ring
        sage: M.category()
        Category of modules over Integer Ring
        sage: M.base_ring()
        Integer Ring
        sage: M.rank()
        3
        
    The LaTeX output is adjusted via the parameter ``latex_name``::
    
        sage: latex(M)  # the default is the symbol provided in the string ``name``
        M
        sage: M = FiniteFreeModule(ZZ, 3, name='M', latex_name=r'\mathcal{M}')
        sage: latex(M)
        \mathcal{M}

    M is a *parent* object, whose elements are instances of 
    :class:`FreeModuleVector`::
    
        sage: v = M.an_element() ; v
        element of the rank-3 free module M over the Integer Ring
        sage: from sage.geometry.manifolds.free_module_tensor import FreeModuleVector
        sage: isinstance(v, FreeModuleVector)
        True        
        sage: v in M
        True
        sage: M.is_parent_of(v)
        True

    Elements can be constructed by means of the __call__ operator acting 
    on the parent; 0 yields the zero element::
        
        sage: M(0)
        element zero of the rank-3 free module M over the Integer Ring
        sage: M(0) is M.zero()
        True
        
    Non-zero elements are constructed by providing their components in 
    a given basis::
    
        sage: e = M.new_basis('e') ; e
        basis (e_0,e_1,e_2) on the rank-3 free module M over the Integer Ring
        sage: v = M([-1,0,3]) ; v  # components in the default basis (e)
        element of the rank-3 free module M over the Integer Ring
        sage: v.view()
        -e_0 + 3 e_2
        sage: f = M.new_basis('f')
        sage: v = M([-1,0,3], basis=f) ; v  # components in a specific basis
        element of the rank-3 free module M over the Integer Ring
        sage: v.view(f)
        -f_0 + 3 f_2
        sage: v = M([-1,0,3], basis=f, name='v') ; v
        element v of the rank-3 free module M over the Integer Ring
        sage: v.view(f)
        v = -f_0 + 3 f_2

    An alternative is to construct the element from an empty list of components
    and to set the nonzero components afterwards::
    
        sage: v = M([], name='v')
        sage: v.set_comp(e)[0] = -1
        sage: v.set_comp(e)[2] = 3
        sage: v.view(e)
        v = -e_0 + 3 e_2

    M is in the category of modules over `\ZZ`::

        sage: M.category()
        Category of modules over Integer Ring
        sage: M in Modules(ZZ)
        True

    Indices on the free module, such as indices labelling the element of a
    basis, are provided by the generator method :meth:`irange`. By default, 
    they range from 0 to the module's rank minus one::
    
        sage: for i in M.irange(): print i,
        0 1 2

    This can be changed via the parameter ``start_index`` in the module 
    construction::
    
        sage: M = FiniteFreeModule(ZZ, 3, name='M', start_index=1)
        sage: for i in M.irange(): print i,
        1 2 3

    The parameter ``output_formatter`` in the constructor of the free module
    is used to set the output format of tensor components::
    
        sage: M = FiniteFreeModule(QQ, 3, output_formatter=Rational.numerical_approx)
        sage: e = M.new_basis('e')
        sage: v = M([1/3, 0, -2], basis=e)
        sage: v.comp(e)[:]
        [0.333333333333333, 0.000000000000000, -2.00000000000000]
        sage: v.view(e)  # default format (53 bits of precision)
        0.333333333333333 e_0 - 2.00000000000000 e_2
        sage: v.view(e, format_spec=10)  # 10 bits of precision 
        0.33 e_0 - 2.0 e_2

    """
    
    Element = FreeModuleVector
    
    def __init__(self, ring, rank, name=None, latex_name=None, start_index=0,
                 output_formatter=None):
        self.ring = ring
        self._rank = rank 
        self.sindex = start_index
        self.output_formatter = output_formatter
        self.tensor_modules = {} # Dictionary of the tensor modules built on 
                                 # self (dict. keys = (k,l) --the tensor type)
        self.known_bases = []  # List of known bases on the free module
        self.def_basis = None # default basis
        self.basis_changes = {} # Dictionary of the changes of bases
        TensorFreeModule.__init__(self, self, (1,0), name, latex_name)

    #### Methods required for any Parent 
    def _element_constructor_(self, comp=[], basis=None, name=None, 
                              latex_name=None):
        r"""
        Construct an element of the module
        """
        if comp == 0:
            return self._zero_element
        resu = self.element_class(self, name=name, latex_name=latex_name)
        if comp != []:
            resu.set_comp(basis)[:] = comp
        return resu

    def _an_element_(self):
        r"""
        Construct some (unamed) element of the module
        """
        return self.element_class(self)
            
    #### End of methods required for any Parent 

    def _repr_(self):
        r"""
        String representation of the object.
        """
        description = "rank-" + str(self._rank) + " free module "
        if self.name is not None:
            description += self.name + " "
        description += "over the " + str(self.ring)
        return description
        
    def tensor_module(self, k, l):
        r"""
        Return the free module of all tensors of type (k,l) defined on 
        ``self``. 
        
        INPUT: 
        
        - ``k`` -- (non-negative integer) the contravariant rank, the tensor type 
          being (k,l)
        - ``l`` -- (non-negative integer) the covariant rank, the tensor type 
          being (k,l)
        
        OUTPUT:
        
        - instance of :class:`TensorFreeModule` representing the free module 
          `T^{(k,l)}(M)` of type-`(k,l)` tensors on the free module ``self``. 
        
        EXAMPLES:
        
        Tensor modules over a free module over `\ZZ`::
        
            sage: M = FiniteFreeModule(ZZ, 3, name='M')
            sage: T = M.tensor_module(1,2) ; T
            free module of type-(1,2) tensors on the rank-3 free module M over the Integer Ring
            sage: T.an_element()
            type-(1,2) tensor on the rank-3 free module M over the Integer Ring
            
        Tensor modules are unique::
        
            sage: M.tensor_module(1,2) is T
            True

        The base module is itself the module of all type-(1,0) tensors::
        
            sage: M.tensor_module(1,0) is M
            True
        
        """
        if (k,l) not in self.tensor_modules:
            self.tensor_modules[(k,l)] = TensorFreeModule(self, (k,l))
        return self.tensor_modules[(k,l)]

    def irange(self, start=None):
        r"""
        Single index generator, labelling the elements of a basis.
                
        INPUT:
        
        - ``start`` -- (integer; default: None) initial value of the index; if none is 
          provided, ``self.sindex`` is assumed

        OUTPUT:
        
        - an iterable index, starting from ``start`` and ending at
          ``self.sindex + self.rank() -1``

        EXAMPLES:
        
        Index range on a rank-3 module::
        
            sage: M = FiniteFreeModule(ZZ, 3)
            sage: for i in M.irange(): print i,
            0 1 2
            sage: for i in M.irange(start=1): print i,
            1 2

        The default starting value corresponds to the parameter ``start_index``
        provided at the module construction (the default value being 0)::
        
            sage: M1 = FiniteFreeModule(ZZ, 3, start_index=1)
            sage: for i in M1.irange(): print i,
            1 2 3
            sage: M2 = FiniteFreeModule(ZZ, 3, start_index=-4)
            sage: for i in M2.irange(): print i,
            -4 -3 -2

        """
        si = self.sindex
        imax = self._rank + si
        if start is None:
            i = si
        else:
            i = start
        while i < imax:
            yield i
            i += 1

    def new_basis(self, symbol, latex_symbol=None):
        r""" 
        Define a basis of the free module.
        
        INPUT:
        
        - ``symbol`` -- (string) a letter (of a few letters) to denote a 
          generic element of the basis
        - ``latex_symbol`` -- (string; default: None) symbol to denote a 
          generic element of the basis; if None, the value of ``symbol`` is 
          used. 

        OUTPUT:
        
        - instance of :class:`FreeModuleBasis` representing a basis on ``self``.
        
        EXAMPLES:
        
        Bases on a rank-3 free module::
        
            sage: M = FiniteFreeModule(ZZ, 3, name='M')
            sage: e = M.new_basis('e') ; e
            basis (e_0,e_1,e_2) on the rank-3 free module M over the Integer Ring
            sage: e[0]
            element e_0 of the rank-3 free module M over the Integer Ring
            sage: latex(e)
            \left(e_0,e_1,e_2\right)

        The LaTeX symbol can be set explicitely, as the second argument of
        :meth:`new_basis`::
        
            sage: eps = M.new_basis('eps', r'\epsilon') ; eps
            basis (eps_0,eps_1,eps_2) on the rank-3 free module M over the Integer Ring
            sage: latex(eps)
            \left(\epsilon_0,\epsilon_1,\epsilon_2\right)
            
        The individual elements of the basis are labelled according the 
        parameter ``start_index`` provided at the free module construction::
        
            sage: M = FiniteFreeModule(ZZ, 3, name='M', start_index=1)
            sage: e = M.new_basis('e') ; e
            basis (e_1,e_2,e_3) on the rank-3 free module M over the Integer Ring
            sage: e[1]
            element e_1 of the rank-3 free module M over the Integer Ring
    
        """
        from free_module_basis import FreeModuleBasis
        return FreeModuleBasis(self, symbol, latex_symbol)
    
    def tensor(self, tensor_type, name=None, latex_name=None, sym=None, 
               antisym=None):
        r"""
        Construct a tensor on the free module. 
        
        INPUT:
        
        - ``tensor_type`` -- pair (k,l) with k being the contravariant rank and l 
          the covariant rank
        - ``name`` -- (default: None) name given to the tensor
        - ``latex_name`` -- (default: None) LaTeX symbol to denote the tensor; 
          if none is provided, the LaTeX symbol is set to ``name``
        - ``sym`` -- (default: None) a symmetry or a list of symmetries among the 
          tensor arguments: each symmetry is described by a tuple containing 
          the positions of the involved arguments, with the convention position=0
          for the first argument. For instance:

          * sym=(0,1) for a symmetry between the 1st and 2nd arguments 
          * sym=[(0,2),(1,3,4)] for a symmetry between the 1st and 3rd
            arguments and a symmetry between the 2nd, 4th and 5th arguments.

        - ``antisym`` -- (default: None) antisymmetry or list of antisymmetries 
          among the arguments, with the same convention as for ``sym``. 
          
        OUTPUT:
        
        - instance of :class:`FreeModuleTensor` representing the tensor defined
          on ``self`` with the provided characteristics.
          
        EXAMPLES:
        
        Tensors on a rank-3 free module::
        
            sage: M = FiniteFreeModule(ZZ, 3, name='M')
            sage: t = M.tensor((1,0), name='t') ; t
            element t of the rank-3 free module M over the Integer Ring
            sage: t = M.tensor((0,1), name='t') ; t
            linear form t on the rank-3 free module M over the Integer Ring
            sage: t = M.tensor((1,1), name='t') ; t
            type-(1,1) tensor t on the rank-3 free module M over the Integer Ring
            sage: t = M.tensor((1,2), name='t') ; t
            type-(1,2) tensor t on the rank-3 free module M over the Integer Ring
            
        See :class:`FreeModuleTensor` for more examples and documentation.
                
        """
        from free_module_tensor import FreeModuleTensor, FreeModuleVector
        from free_module_alt_form import FreeModuleLinForm
        if tensor_type == (1,0):
            return FreeModuleVector(self, name=name, latex_name=latex_name)
        elif tensor_type == (0,1):
            return FreeModuleLinForm(self, name=name, latex_name=latex_name)
        else:
            return FreeModuleTensor(self, tensor_type, name=name, 
                                    latex_name=latex_name, sym=sym, 
                                    antisym=antisym) 
    
    
    
    
    
    
    
    
