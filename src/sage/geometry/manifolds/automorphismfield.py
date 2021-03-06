r"""
Tangent-space automorphism fields


AUTHORS:

- Eric Gourgoulhon (2015): initial version

"""

#******************************************************************************
#       Copyright (C) 2015 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.tensor.modules.free_module_tensor import FreeModuleTensor
from sage.tensor.modules.free_module_automorphism import FreeModuleAutomorphism
from tensorfield import TensorField, TensorFieldParal

#******************************************************************************

class AutomorphismField(TensorField):
    r"""
    Field of tangent-space automorphisms with values on a open
    subset of a differentiable manifold.

    Given an open subset `U` of a manifold `S` and a differentiable mapping
    `\Phi: U \rightarrow V`, where `V` is an open subset of a manifold `M`,
    an instance of this class is a field of tangent-space automorphisms
    along `U` with values in `V`.
    The standard case of a field of tangent-space automorphisms *on* a
    manifold corresponds to `S=M`, `U=V` and `\Phi = \mathrm{Id}_U`. Other
    common cases are `\Phi` being an immersion and `\Phi` being a curve in `V`
    (`U` is then an open interval of `\RR`).

    If `V` is parallelizable, the class :class:`AutomorphismFieldParal`
    must be used instead.

    This is a Sage *element* class, the corresponding *parent* class being
    :class:`~sage.geometry.manifolds.automorphismfield_group.AutomorphismFieldGroup`.

    INPUT:

    - ``vector_field_module`` -- module `\mathcal{X}(U,\Phi)` of vector
      fields along `U` with values on `V`
    - ``name`` -- (default: ``None``) name given to the field
    - ``latex_name`` -- (default: ``None``) LaTeX symbol to denote the field;
      if none is provided, the LaTeX symbol is set to ``name``
    - ``is_identity`` -- (default: ``False``) determines whether the
      constructed object is a field of identity automorphisms

    EXAMPLE:

    Field of tangent-space automorphisms on a non-parallelizable 2-dimensional
    manifold::

        sage: M = Manifold(2, 'M')
        sage: U = M.open_subset('U') ; V = M.open_subset('V')
        sage: M.declare_union(U,V)   # M is the union of U and V
        sage: c_xy.<x,y> = U.chart() ; c_uv.<u,v> = V.chart()
        sage: transf = c_xy.transition_map(c_uv, (x+y, x-y), intersection_name='W', restrictions1= x>0, restrictions2= u+v>0)
        sage: inv = transf.inverse()
        sage: a = M.automorphism_field('a') ; a
        field of tangent-space automorphisms 'a' on the 2-dimensional manifold 'M'
        sage: a.parent()
        General linear group of the module X(M) of vector fields on the
         2-dimensional manifold 'M'

    We first define the components of `a` w.r.t the coordinate frame on `U`::

        sage: eU = c_xy.frame() ; eV = c_uv.frame()
        sage: a[eU,:] = [[1,x], [0,2]]

    We then set the components w.r.t. the coordinate frame on `V` by extending
    the expressions of the components in the corresponding subframe on
    `W = U\cap V`::

        sage: W = U.intersection(V)
        sage: a.add_comp_by_continuation(eV, W, c_uv)

    At this stage, the automorphims field `a` is fully defined::

        sage: a.display(eU)
        a = d/dx*dx + x d/dx*dy + 2 d/dy*dy
        sage: a.display(eV)
        a = (1/4*u + 1/4*v + 3/2) d/du*du + (-1/4*u - 1/4*v - 1/2) d/du*dv + (1/4*u + 1/4*v - 1/2) d/dv*du + (-1/4*u - 1/4*v + 3/2) d/dv*dv

    In particular, we may ask for its inverse on the whole manifold `M`::

        sage: ia = a.inverse() ; ia
        field of tangent-space automorphisms 'a^(-1)' on the 2-dimensional manifold 'M'
        sage: ia.display(eU)
        a^(-1) = d/dx*dx - 1/2*x d/dx*dy + 1/2 d/dy*dy
        sage: ia.display(eV)
        a^(-1) = (-1/8*u - 1/8*v + 3/4) d/du*du + (1/8*u + 1/8*v + 1/4) d/du*dv + (-1/8*u - 1/8*v + 1/4) d/dv*du + (1/8*u + 1/8*v + 3/4) d/dv*dv

    """
    def __init__(self, vector_field_module, name=None, latex_name=None,
                 is_identity=False):
        if is_identity:
            if name is None:
                name = 'Id'
            if latex_name is None and name == 'Id':
                latex_name = r'\mathrm{Id}'
        TensorField.__init__(self, vector_field_module, (1,1), name=name,
                             latex_name=latex_name,
                             parent=vector_field_module.general_linear_group())
        self._is_identity = is_identity
        self._init_derived() # initialization of derived quantities
        # Specific initializations for the field of identity maps:
        if self._is_identity:
            self._inverse = self
            for dom in self._domain._subsets:
                if dom.is_manifestly_parallelizable():
                    fmodule = dom.vector_field_module()
                    self._restrictions[dom] = fmodule.identity_map(name=name,
                                                         latex_name=latex_name)

    def _repr_(self):
        r"""
        Return a string representation of ``self``.
        """
        description = "field of tangent-space "
        if self._is_identity:
            description += "identity maps "
        else:
            description += "automorphisms "
            if self._name is not None:
                description += "'%s' " % self._name
        return self._final_repr(description)

    def _init_derived(self):
        r"""
        Initialize the derived quantities
        """
        TensorField._init_derived(self)
        self._inverse = None  # inverse not set yet

    def _del_derived(self):
        r"""
        Delete the derived quantities.
        """
        # First delete the derived quantities pertaining to the mother class:
        TensorField._del_derived(self)
        # then deletes the inverse automorphism:
        self._inverse = None

    def __call__(self, *arg):
        r"""
        Redefinition of
        :meth:`~sage.geometry.manifolds.tensorfield.TensorField.__call__`
        to allow for a proper
        treatment of the identity map and of the call with a single argument
        """
        if self._is_identity:
            if len(arg) == 1:
                # The identity map acting as such, on a vector field:
                vector = arg[0]
                if vector._tensor_type != (1,0):
                    raise TypeError("the argument must be a vector field")
                dom = self._domain.intersection(vector._domain)
                return vector.restrict(dom)
            elif len(arg) == 2:
                # self acting as a type-(1,1) tensor on a pair
                # (1-form, vector field), returning a scalar field:
                oneform = arg[0]
                vector = arg[1]
                dom = self._domain.intersection(
                                  oneform._domain).intersection(vector._domain)
                return oneform.restrict(dom)(vector.restrict(dom))
            else:
                raise TypeError("wrong number of arguments")
        # Generic case
        if len(arg) == 1:
            raise NotImplementedError("__call__  with 1 arg not implemented yet")
        return TensorField.__call__(self, *arg)


    #### MultiplicativeGroupElement methods ####

    def __invert__(self):
        r"""
        Return the inverse automorphism.

        EXAMPLE:

        Inverse of a field of tangent-space automorphisms on a
        non-parallelizable 2-dimensional manifold::

            sage: M = Manifold(2, 'M')
            sage: U = M.open_subset('U') ; V = M.open_subset('V')
            sage: M.declare_union(U,V)   # M is the union of U and V
            sage: c_xy.<x,y> = U.chart() ; c_uv.<u,v> = V.chart()
            sage: transf = c_xy.transition_map(c_uv, (x+y, x-y), intersection_name='W', restrictions1= x>0, restrictions2= u+v>0)
            sage: inv = transf.inverse()
            sage: a = M.automorphism_field('a')
            sage: eU = c_xy.frame() ; eV = c_uv.frame()
            sage: a[eU,:] = [[1,x], [0,2]]
            sage: W = U.intersection(V)
            sage: a.add_comp_by_continuation(eV, W, c_uv)
            sage: ia = a.inverse() ; ia
            field of tangent-space automorphisms 'a^(-1)' on the 2-dimensional manifold 'M'
            sage: a[eU,:], ia[eU,:]
            (
            [1 x]  [     1 -1/2*x]
            [0 2], [     0    1/2]
            )
            sage: a[eV,:], ia[eV,:]
            (
            [ 1/4*u + 1/4*v + 3/2 -1/4*u - 1/4*v - 1/2]
            [ 1/4*u + 1/4*v - 1/2 -1/4*u - 1/4*v + 3/2],
            [-1/8*u - 1/8*v + 3/4  1/8*u + 1/8*v + 1/4]
            [-1/8*u - 1/8*v + 1/4  1/8*u + 1/8*v + 3/4]
            )

        Let us check that ia is indeed the inverse of a::

            sage: s = a.contract(ia)
            sage: s[eU,:], s[eV,:]
            (
            [1 0]  [1 0]
            [0 1], [0 1]
            )
            sage: s = ia.contract(a)
            sage: s[eU,:], s[eV,:]
            (
            [1 0]  [1 0]
            [0 1], [0 1]
            )

        """
        if self._is_identity:
            return self
        if self._inverse is None:
            if self._name is None:
                inv_name = None
            else:
                inv_name = self._name  + '^(-1)'
            if self._latex_name is None:
                inv_latex_name = None
            else:
                inv_latex_name = self._latex_name + r'^{-1}'
            self._inverse = self._vmodule.automorphism(name=inv_name,
                                                     latex_name=inv_latex_name)
            for dom, rst in self._restrictions.iteritems():
                self._inverse._restrictions[dom] = rst.inverse()
        return self._inverse

    inverse = __invert__

    def _mul_(self, other):
        r"""
        Automorphism composition.

        This implements the group law of GL(X(U,Phi)), X(U,Phi) being the
        module of ``self``.

        INPUT:

        - ``other`` -- an automorphism of the same module as ``self``

        OUPUT:

        - the automorphism resulting from the composition of ``other`` and
        ``self.``

        """
        # No need for consistency check since self and other are guaranted
        # to have the same parent. In particular, they are defined on the same
        # module.
        #
        # Special cases:
        if self._is_identity:
            return other
        if other._is_identity:
            return self
        if other is self._inverse or self is other._inverse:
            return self.parent().one()
        # General case:
        resu = self.__class__(self._vmodule)
        for dom in self._common_subdomains(other):
            resu._restrictions[dom] = self._restrictions[dom] * \
                                      other._restrictions[dom]
        return resu

    #### End of MultiplicativeGroupElement methods ####

    def __mul__(self, other):
        r"""
        Redefinition of
        :meth:`~sage.geometry.manifolds.tensorfield.TensorField.__mul__`
        so that * dispatches either to automorphism composition or to the
        tensor product.

        EXAMPLES:


        """
        if isinstance(other, AutomorphismField):
            return self._mul_(other)  # general linear group law
        else:
            return TensorField.__mul__(self, other)  # tensor product

    def __imul__(self, other):
        r"""
        Redefinition of
        :meth:`~sage.geometry.manifolds.tensorfield.TensorField.__imul__`

        TESTS::

        """
        return self.__mul__(other)

    def restrict(self, subdomain, dest_map=None):
        r"""
        Return the restriction of ``self`` to some subdomain.

        This is a redefinition of
        :meth:`sage.geometry.manifolds.tensorfield.TensorField.restrict`
        to take into account the identity map.

        INPUT:

        - ``subdomain`` -- open subset `U` of ``self._domain`` (must be an
          instance of :class:`~sage.geometry.manifolds.domain.ManifoldOpenSubset`)
        - ``dest_map`` -- (default: ``None``) destination map
          `\Phi:\ U \rightarrow V`, where `V` is a subdomain of
          ``self._codomain``
          (type: :class:`~sage.geometry.manifolds.diffmapping.DiffMapping`)
          If None, the restriction of ``self._vmodule._dest_map`` to `U` is
          used.

        OUTPUT:

        - instance of :class:`AutomorphismField` representing the restriction.

        EXAMPLES:

        Restrictions of an automorphism field on the 2-sphere::

            sage: M = Manifold(2, 'S^2', start_index=1)
            sage: U = M.open_subset('U') # the complement of the North pole
            sage: stereoN.<x,y> = U.chart()  # stereographic coordinates from the North pole
            sage: eN = stereoN.frame() # the associated vector frame
            sage: V =  M.open_subset('V') # the complement of the South pole
            sage: stereoS.<u,v> = V.chart()  # stereographic coordinates from the South pole
            sage: eS = stereoS.frame() # the associated vector frame
            sage: transf = stereoN.transition_map(stereoS, (x/(x^2+y^2), y/(x^2+y^2)), intersection_name='W', \
                                                  restrictions1= x^2+y^2!=0, restrictions2= u^2+v^2!=0)
            sage: inv = transf.inverse() # transformation from stereoS to stereoN
            sage: W = U.intersection(V) # the complement of the North and South poles
            sage: stereoN_W = W.atlas()[0]  # restriction of stereographic coord. from North pole to W
            sage: stereoS_W = W.atlas()[1]  # restriction of stereographic coord. from South pole to W
            sage: eN_W = stereoN_W.frame() ; eS_W = stereoS_W.frame()
            sage: a = M.automorphism_field(name='a') ; a
            field of tangent-space automorphisms 'a' on the 2-dimensional manifold 'S^2'
            sage: a[eN,:] = [[1, atan(x^2+y^2)], [0,3]]
            sage: a.add_comp_by_continuation(eS, W, chart=stereoS)
            sage: a.restrict(U)
            field of tangent-space automorphisms 'a' on the open subset 'U' of
             the 2-dimensional manifold 'S^2'
            sage: a.restrict(U)[eN,:]
            [                1 arctan(x^2 + y^2)]
            [                0                 3]
            sage: a.restrict(V)
            field of tangent-space automorphisms 'a' on the open subset 'V' of the 2-dimensional manifold 'S^2'
            sage: a.restrict(V)[eS,:]
            [   (u^4 + 10*u^2*v^2 + v^4 + 2*(u^3*v - u*v^3)*arctan(1/(u^2 + v^2)))/(u^4 + 2*u^2*v^2 + v^4)  -(4*u^3*v - 4*u*v^3 + (u^4 - 2*u^2*v^2 + v^4)*arctan(1/(u^2 + v^2)))/(u^4 + 2*u^2*v^2 + v^4)]
            [                    4*(u^2*v^2*arctan(1/(u^2 + v^2)) - u^3*v + u*v^3)/(u^4 + 2*u^2*v^2 + v^4) (3*u^4 - 2*u^2*v^2 + 3*v^4 - 2*(u^3*v - u*v^3)*arctan(1/(u^2 + v^2)))/(u^4 + 2*u^2*v^2 + v^4)]
            sage: a.restrict(W)
            field of tangent-space automorphisms 'a' on the open subset 'W' of the 2-dimensional manifold 'S^2'
            sage: a.restrict(W)[eN_W,:]
            [                1 arctan(x^2 + y^2)]
            [                0                 3]

        Restrictions of the field of tangent-space identity maps::

            sage: id = M.tangent_identity_field() ; id
            field of tangent-space identity maps on the 2-dimensional manifold 'S^2'
            sage: id.restrict(U)
            field of tangent-space identity maps on the open subset 'U' of the 2-dimensional manifold 'S^2'
            sage: id.restrict(U)[eN,:]
            [1 0]
            [0 1]
            sage: id.restrict(V)
            field of tangent-space identity maps on the open subset 'V' of the 2-dimensional manifold 'S^2'
            sage: id.restrict(V)[eS,:]
            [1 0]
            [0 1]
            sage: id.restrict(W)[eN_W,:]
            [1 0]
            [0 1]
            sage: id.restrict(W)[eS_W,:]
            [1 0]
            [0 1]

        """
        if subdomain == self._domain:
            return self
        if subdomain not in self._restrictions:
            if not self._is_identity:
                return TensorField.restrict(self, subdomain, dest_map=dest_map)
            # Special case of the identity map:
            if not subdomain.is_subset(self._domain):
                raise ValueError("The provided domain is not a subset of " +
                                 "the field's domain.")
            if dest_map is None:
                dest_map = self._vmodule._dest_map.restrict(subdomain)
            elif not dest_map._codomain.is_subset(self._ambient_domain):
                raise ValueError("Argument dest_map not compatible with " +
                                 "self._ambient_domain")
            smodule = subdomain.vector_field_module(dest_map=dest_map)
            self._restrictions[subdomain] = smodule.identity_map()
        return self._restrictions[subdomain]


#******************************************************************************

class AutomorphismFieldParal(FreeModuleAutomorphism, TensorFieldParal):
    r"""
    Field of tangent-space automorphisms with values on a parallelizable open
    subset of a differentiable manifold.

    Given an open subset `U` of a manifold `S` and a differentiable mapping
    `\Phi: U \rightarrow V`, where `V` is a parallelizable open subset of a
    manifold `M`, an instance of this class is a field of tangent-space
    automorphisms along `U` with values in `V`.
    The standard case of a field of tangent-space automorphisms *on* a
    manifold corresponds to `S=M`, `U=V` and `\Phi = \mathrm{Id}_U`. Other
    common cases are `\Phi` being an immersion and `\Phi` being a curve in `V`
    (`U` is then an open interval of `\RR`).

    If `V` is not parallelizable, the class :class:`AutomorphismField`
    must be used instead.

    This is a Sage *element* class, the corresponding *parent* class being
    :class:`~sage.geometry.manifolds.automorphismfield_group.AutomorphismFieldParalGroup`.

    INPUT:

    - ``vector_field_module`` -- free module `\mathcal{X}(U,\Phi)` of vector
      fields along `U` with values on `V`
    - ``name`` -- (default: ``None``) name given to the field
    - ``latex_name`` -- (default: ``None``) LaTeX symbol to denote the field;
      if none is provided, the LaTeX symbol is set to ``name``
    - ``is_identity`` -- (default: ``False``) determines whether the
      constructed object is a field of identity automorphisms

    EXAMPLES:

    A pi/3-rotation in the Euclidean 2-plane::

        sage: M = Manifold(2,'R^2')
        sage: c_xy.<x,y> = M.chart()
        sage: rot = M.automorphism_field('R') ; rot
        field of tangent-space automorphisms 'R' on the 2-dimensional manifold
         'R^2'
        sage: rot[:] = [[sqrt(3)/2, -1/2], [1/2, sqrt(3)/2]]
        sage: rot.parent()
        General linear group of the free module X(R^2) of vector fields on the
         2-dimensional manifold 'R^2'

    The inverse automorphism is obtained via the method :meth:`inverse`::

        sage: inv = rot.inverse() ; inv
        field of tangent-space automorphisms 'R^(-1)' on the 2-dimensional manifold 'R^2'
        sage: latex(inv)
        R^{-1}
        sage: inv[:]
        [1/2*sqrt(3)         1/2]
        [       -1/2 1/2*sqrt(3)]
        sage: rot[:]
        [1/2*sqrt(3)        -1/2]
        [        1/2 1/2*sqrt(3)]
        sage: inv[:] * rot[:]  # check
        [1 0]
        [0 1]

    """
    def __init__(self, vector_field_module, name=None, latex_name=None,
                 is_identity=False):
        r"""
        Construct a field of tangent-space automorphisms.

        TESTS::

            sage: Manifold._clear_cache_() # for doctests only
            sage: M = Manifold(2, 'M')
            sage: X.<x,y> = M.chart()
            sage: a = M.automorphism_field(name='a') ; a
            field of tangent-space automorphisms 'a' on the 2-dimensional manifold 'M'
            sage: a[:] = [[1+x^2, x*y], [0, 1+y^2]]
            sage: a.parent()
            General linear group of the free module X(M) of vector fields on
             the 2-dimensional manifold 'M'
            sage: a.parent() is M.automorphism_field_group()
            True
            sage: TestSuite(a).run()

        """
        FreeModuleAutomorphism.__init__(self, vector_field_module,
                                        name=name, latex_name=latex_name,
                                        is_identity=is_identity)
        # TensorFieldParal attributes:
        self._vmodule = vector_field_module
        self._domain = vector_field_module._domain
        self._ambient_domain = vector_field_module._ambient_domain
        # Initialization of derived quantities:
        TensorFieldParal._init_derived(self)

    def _repr_(self):
        r"""
        Return a string representation of ``self``.
        """
        description = "field of tangent-space "
        if self._is_identity:
            description += "identity maps "
        else:
            description += "automorphisms "
            if self._name is not None:
                description += "'%s' " % self._name
        return self._final_repr(description)

    def _del_derived(self, del_restrictions=True):
        r"""
        Delete the derived quantities

        INPUT:

        - ``del_restrictions`` -- (default: True) determines whether the
          restrictions of ``self`` to subdomains are deleted.

        """
        # Delete the derived quantities pertaining to the mother classes:
        FreeModuleAutomorphism._del_derived(self)
        TensorFieldParal._del_derived(self, del_restrictions=del_restrictions)

    def __call__(self, *arg):
        r"""
        Redefinition of
        :meth:`~sage.tensor.modules.free_module_automorphism.FreeModuleAutomorphism.__call__`
        to allow for domain treatment
        """
        if len(arg) == 1:
            # the automorphism acting as such (map of a vector field to a
            # vector field)
            vector = arg[0]
            dom = self._domain.intersection(vector._domain)
            return FreeModuleAutomorphism.__call__(self.restrict(dom),
                                                   vector.restrict(dom))
        elif len(arg) == 2:
            # the automorphism acting as a type (1,1) tensor on a pair
            # (1-form, vector field), returning a scalar field:
            oneform = arg[0]
            vector = arg[1]
            dom = self._domain.intersection(oneform._domain).intersection(
                                                                vector._domain)
            return FreeModuleAutomorphism.__call__(self.restrict(dom),
                                                   oneform.restrict(dom),
                                                   vector.restrict(dom))
        else:
            raise TypeError("wrong number of arguments")

    def __invert__(self):
        r"""
        Return the inverse automorphism.
        """
        from sage.matrix.constructor import matrix
        from sage.tensor.modules.comp import Components
        from vectorframe import CoordFrame
        from utilities import simplify_chain
        if self._is_identity:
            return self
        if self._inverse is None:
            if self._name is None:
                inv_name = None
            else:
                inv_name = self._name  + '^(-1)'
            if self._latex_name is None:
                inv_latex_name = None
            else:
                inv_latex_name = self._latex_name + r'^{-1}'
            fmodule = self._fmodule
            si = fmodule._sindex ; nsi = fmodule._rank + si
            self._inverse = fmodule.automorphism(name=inv_name,
                                                 latex_name=inv_latex_name)
            for frame in self._components:
                if isinstance(frame, CoordFrame):
                    chart = frame._chart
                else:
                    chart = self._domain._def_chart #!# to be improved
                try:
                    mat_self = matrix(
                              [[self.comp(frame)[i, j, chart]._express
                              for j in range(si, nsi)] for i in range(si, nsi)])
                except (KeyError, ValueError):
                    continue
                mat_inv = mat_self.inverse()
                cinv = Components(fmodule._ring, frame, 2, start_index=si,
                                  output_formatter=fmodule._output_formatter)
                for i in range(si, nsi):
                    for j in range(si, nsi):
                        cinv[i, j] = {chart: simplify_chain(mat_inv[i-si,j-si])}
                self._inverse._components[frame] = cinv
        return self._inverse

    inverse = __invert__

    def restrict(self, subdomain, dest_map=None):
        r"""
        Return the restriction of ``self`` to some subset of its domain.

        If such restriction has not been defined yet, it is constructed here.

        This is a redefinition of
        :meth:`sage.geometry.manifolds.tensorfield.TensorFieldParal.restrict`
        to take into account the identity map.

        INPUT:

        - ``subdomain`` -- open subset `U` of ``self._domain`` (must be an
          instance of :class:`~sage.geometry.manifolds.domain.ManifoldOpenSubset`)
        - ``dest_map`` -- (default: ``None``) destination map
          `\Phi:\ U \rightarrow V`, where `V` is a subset of
          ``self._codomain``
          (type: :class:`~sage.geometry.manifolds.diffmapping.DiffMapping`)
          If None, the restriction of ``self._vmodule._dest_map`` to `U` is
          used.

        OUTPUT:

        - instance of :class:`AutomorphismFieldParal` representing the
          restriction.

        EXAMPLES:

        Restriction of an automorphism field defined on `\RR^2` to a disk::

            sage: M = Manifold(2, 'R^2')
            sage: c_cart.<x,y> = M.chart() # Cartesian coordinates on R^2
            sage: D = M.open_subset('D') # the unit open disc
            sage: c_cart_D = c_cart.restrict(D, x^2+y^2<1)
            sage: a = M.automorphism_field(name='a') ; a
            field of tangent-space automorphisms 'a' on the 2-dimensional manifold 'R^2'
            sage: a[:] = [[1, x*y], [0, 3]]
            sage: a.restrict(D)
            field of tangent-space automorphisms 'a' on the open subset 'D' of the 2-dimensional manifold 'R^2'
            sage: a.restrict(D)[:]
            [  1 x*y]
            [  0   3]

        Restriction to the disk of the field of tangent-space identity maps::

            sage: id = M.tangent_identity_field() ; id
            field of tangent-space identity maps on the 2-dimensional manifold 'R^2'
            sage: id.restrict(D)
            field of tangent-space identity maps on the open subset 'D' of the 2-dimensional manifold 'R^2'
            sage: id.restrict(D)[:]
            [1 0]
            [0 1]
            sage: id.restrict(D) == D.tangent_identity_field()
            True

        """
        if subdomain == self._domain:
            return self
        if subdomain not in self._restrictions:
            if not self._is_identity:
                return TensorFieldParal.restrict(self, subdomain,
                                                 dest_map=dest_map)
            # Special case of the identity map:
            if not subdomain.is_subset(self._domain):
                raise ValueError("The provided domain is not a subset of " +
                                 "the field's domain.")
            if dest_map is None:
                dest_map = self._fmodule._dest_map.restrict(subdomain)
            elif not dest_map._codomain.is_subset(self._ambient_domain):
                raise ValueError("Argument dest_map not compatible with " +
                                 "self._ambient_domain")
            smodule = subdomain.vector_field_module(dest_map=dest_map)
            self._restrictions[subdomain] = smodule.identity_map()
        return self._restrictions[subdomain]

    def at(self, point):
        r"""
        Value of ``self`` at a given point on the manifold.

        The returned object is an automorphism of the tangent space at the
        given point.

        INPUT:

        - ``point`` -- (instance of
          :class:`~sage.geometry.manifolds.point.ManifoldPoint`) point `p` in
          the domain of ``self`` (denoted `a` hereafter)

        OUTPUT:

        - instance of
          :class:`~sage.tensor.modules.free_module_automorphism.FreeModuleAutomorphism`
          representing the automorphism `a(p)` of the tangent vector space
          `T_p M` (`M` being the manifold on which ``self`` is defined)

        EXAMPLES:

        Automorphism at some point of a tangent space of a 2-dimensional
        manifold::

            sage: Manifold._clear_cache_() # for doctests only
            sage: M = Manifold(2, 'M')
            sage: c_xy.<x,y> = M.chart()
            sage: a = M.automorphism_field(name='a')
            sage: a[:] = [[1+exp(y), x*y], [0, 1+x^2]]
            sage: a.display()
            a = (e^y + 1) d/dx*dx + x*y d/dx*dy + (x^2 + 1) d/dy*dy
            sage: p = M.point((-2,3), name='p') ; p
            point 'p' on 2-dimensional manifold 'M'
            sage: ap = a.at(p) ; ap
            Automorphism a of the tangent space at point 'p' on 2-dimensional
             manifold 'M'
            sage: ap.display()
            a = (e^3 + 1) d/dx*dx - 6 d/dx*dy + 5 d/dy*dy
            sage: ap.parent()
            General linear group of the tangent space at point 'p' on
             2-dimensional manifold 'M'

        The identity map of the tangent space at point ``p``::

            sage: id = M.tangent_identity_field() ; id
            field of tangent-space identity maps on the 2-dimensional manifold 'M'
            sage: idp = id.at(p) ; idp
            Identity map of the tangent space at point 'p' on
             2-dimensional manifold 'M'
            sage: idp is p.tangent_space().identity_map()
            True
            sage: idp.display()
            Id = d/dx*dx + d/dy*dy
            sage: idp.parent()
            General linear group of the tangent space at point 'p' on
             2-dimensional manifold 'M'
            sage: idp * ap == ap
            True

        """
        if point not in self._domain:
            raise TypeError("the {} is not a point in the domain of {}".format(
                                                                  point, self))
        ts = point.tangent_space()
        if self._is_identity:
            return ts.identity_map()
        resu = ts.automorphism(name=self._name, latex_name=self._latex_name)
        for frame, comp in self._components.iteritems():
            comp_resu = resu.add_comp(frame.at(point))
            for ind, val in comp._comp.iteritems():
                comp_resu._comp[ind] = val(point)
        return resu
