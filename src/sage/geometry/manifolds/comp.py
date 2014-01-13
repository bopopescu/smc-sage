r"""
Components

The class :class:`Components` takes in charge the storage of the components of 
a geometrical entity with respect to some "frame". The latter can be a 
vector-space basis or a vector frame on some manifold (i.e. a field of bases). 
The components can be of course components of tensors or tensor fields, 
but also  non-tensorial quantities, like connection coefficients or 
structure coefficients of a vector frame. 

Various subclasses of the class :class:`Components` are

* :class:`CompWithSym` for storing components with symmetries (symmetric and/or 
  antisymmetric indices)
* :class:`CompFullySym` for storing fully symmetric components.
* :class:`CompFullyAntiSym` for storing fully antisymmetric components.
* :class:`KroneckerDelta` for the Kronecker delta symbol. 

AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2014): initial version

EXAMPLES:

    Set of components with 2 indices on a 3-dimensional vector space, the frame
    being some basis of the vector space::
    
        sage: V = VectorSpace(QQ,3)
        sage: basis = V.basis() ; basis
        [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        ]
        sage: c = Components(QQ, basis, 2) ; c
        2-indices components w.r.t. [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        ]
    
    Actually, the frame can be any object that has some length, i.e. on which 
    the function :func:`len()` can be called::
    
        sage: basis1 = V.gens() ; basis1
        ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        sage: c1 = Components(QQ, basis1, 2) ; c1
        2-indices components w.r.t. ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        sage: basis2 = ['a', 'b' , 'c']
        sage: c2 = Components(QQ, basis2, 2) ; c2
        2-indices components w.r.t. ['a', 'b', 'c']
    
    A just created set of components is initialized to zero::
    
        sage: c.is_zero()
        True
        sage: c == 0
        True
    
    This can also be checked on the list of components, which is returned by
    the operator ``[:]``::
    
        sage: c[:]
        [0 0 0]
        [0 0 0]
        [0 0 0]
    
    Individual components are accessed by providing their indices inside 
    square brackets::
    
        sage: c[1,2] = -3
        sage: c[:]
        [ 0  0  0]
        [ 0  0 -3]
        [ 0  0  0]
        sage: v = Components(QQ, basis, 1)
        sage: v[:]
        [0, 0, 0]
        sage: v[0]
        0
        sage: v[:] = (-1,3,2)
        sage: v[:]
        [-1, 3, 2]
        sage: v[0]
        -1
    
    By default, the indices range from `0` to `n-1`, where `n` is the length
    of the frame. This can be changed via the argument ``start_index`` in
    the :class:`Components` constructor::
    
        sage: v1 = Components(QQ, basis, 1, start_index=1)
        sage: v1[:]
        [0, 0, 0]
        sage: v1[0]
        Traceback (most recent call last):
        ...
        IndexError: Index out of range: 0 not in [1,3]
        sage: v1[1]
        0
        sage: v1[:] = v[:]  # list copy of all components
        sage: v1[:]
        [-1, 3, 2]
        sage: v1[1], v1[2], v1[3]
        (-1, 3, 2)
        sage: v[0], v[1], v[2]
        (-1, 3, 2)

    If some formatter function or unbound method is provided via the argument
    ``output_formatter`` in the :class:`Components` constructor, it is used to 
    change the ouput of the access operator ``[...]``::
    
        sage: a = Components(QQ, basis, 2, output_formatter=Rational.numerical_approx)
        sage: a[1,2] = 1/3
        sage: a[1,2]
        0.333333333333333
        
    The format can be passed to the formatter as the last argument of the 
    access operator ``[...]``::
    
        sage: a[1,2,10] # here the format is 10, for 10 bits of precision
        0.33
        sage: a[1,2,100] 
        0.33333333333333333333333333333
        
    The raw (unformatted) components are then accessed by the double bracket 
    operator::
    
        sage: a[[1,2]]
        1/3
        
    For sets of components declared without any output formatter, there is no
    difference between ``[...]`` and ``[[...]]``::
    
        sage: c[1,2] = 1/3
        sage: c[1,2], c[[1,2]]
        (1/3, 1/3)

    The formatter is also used for the complete list of components::
    
        sage: a[:]
        [0.000000000000000 0.000000000000000 0.000000000000000]
        [0.000000000000000 0.000000000000000 0.333333333333333]
        [0.000000000000000 0.000000000000000 0.000000000000000]
        sage: a[:,10] # with a format different from the default one (53 bits)
        [0.00 0.00 0.00]
        [0.00 0.00 0.33]
        [0.00 0.00 0.00]
        
    The complete list of components in raw form can be recovered by the double
    bracket operator, replacing ``:`` by ``slice(None)`` (since ``a[[:]]`` 
    generates a Python syntax error)::
    
        sage: a[[slice(None)]]
        [  0   0   0]
        [  0   0 1/3]
        [  0   0   0]
        
    Internally, the components are stored as a dictionary (:attr:`_comp`) whose
    keys are the indices; only the non-zero components are stored::

        sage: a._comp
        {(1, 2): 1/3}
        sage: v[:] = (-1, 0, 3)
        sage: v._comp  # random output order of the dictionary elements
        {(0,): -1, (2,): 3}

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

from sage.structure.sage_object import SageObject
from sage.rings.integer import Integer

class Components(SageObject):
    r"""
    Class for storing components with respect to a given "frame".  
    
    The "frame" can be a basis of some vector space or a vector frame on some 
    manifold (i.e. a field of bases). 
    The stored quantities can be tensor components or non-tensorial quantities, 
    such as connection coefficients or structure coefficents. The symmetries 
    over some indices are dealt by subclasses of the class :class:`Components`.
     
    INPUT:
    
    - ``ring`` -- ring in which each component takes its value
    - ``frame`` -- frame with respect to which the components are defined; 
      whatever type ``frame`` is, it should have some method ``__len__()``
      implemented, so that ``len(frame)`` returns the dimension, i.e. the size
      of a single index range
    - ``nb_indices`` -- number of indices labeling the components
    - ``start_index`` -- (default: 0) first value of a single index; 
      accordingly a component index i must obey
      ``start_index <= i <= start_index + dim - 1``, where ``dim = len(frame)``. 
    - ``output_formatter`` -- (default: None) 2-argument function or unbound 
      method called to format the output of the component access 
      operator ``[...]`` (method __getitem__); the 1st argument of 
      ``output_formatter`` must be an instance of ``ring``, and the second some 
      format.
      
    EXAMPLES:

    Set of components with 2 indices on a 3-dimensional vector space, the frame
    being some basis of the vector space::

        sage: V = VectorSpace(QQ,3)
        sage: basis = V.basis() ; basis
        [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        ]
        sage: c = Components(QQ, basis, 2) ; c
        2-indices components w.r.t. [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        ]

    Actually, the frame can be any object that has some length, i.e. on which 
    the function :func:`len()` can be called::
    
        sage: basis1 = V.gens() ; basis1
        ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        sage: c1 = Components(QQ, basis1, 2) ; c1
        2-indices components w.r.t. ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        sage: basis2 = ['a', 'b' , 'c']
        sage: c2 = Components(QQ, basis2, 2) ; c2
        2-indices components w.r.t. ['a', 'b', 'c']

    By default, the indices range from `0` to `n-1`, where `n` is the length
    of the frame. This can be changed via the argument ``start_index``::
    
        sage: c1 = Components(QQ, basis, 2, start_index=1)
        sage: c1[0,1]
        Traceback (most recent call last):
        ...
        IndexError: Index out of range: 0 not in [1,3]
        sage: c[0,1]  # for c, the index 0 is OK
        0
        sage: c[0,1] = -3
        sage: c1[:] = c[:] # list copy of all components
        sage: c1[1,2]  # (1,2) = (0,1) shifted by 1
        -3

    If some formatter function or unbound method is provided via the argument
    ``output_formatter``, it is used to change the ouput of the access 
    operator ``[...]``::
    
        sage: a = Components(QQ, basis, 2, output_formatter=Rational.numerical_approx)
        sage: a[1,2] = 1/3
        sage: a[1,2]
        0.333333333333333
        
    The format can be passed to the formatter as the last argument of the 
    access operator ``[...]``::
    
        sage: a[1,2,10] # here the format is 10, for 10 bits of precision
        0.33
        sage: a[1,2,100] 
        0.33333333333333333333333333333
        
    The raw (unformatted) components are then accessed by the double bracket 
    operator::
    
        sage: a[[1,2]]
        1/3
        
    For sets of components declared without any output formatter, there is no
    difference between ``[...]`` and ``[[...]]``::
    
        sage: c[1,2] = 1/3
        sage: c[1,2], c[[1,2]]
        (1/3, 1/3)

    The formatter is also used for the complete list of components::
    
        sage: a[:]
        [0.000000000000000 0.000000000000000 0.000000000000000]
        [0.000000000000000 0.000000000000000 0.333333333333333]
        [0.000000000000000 0.000000000000000 0.000000000000000]
        sage: a[:,10] # with a format different from the default one (53 bits)
        [0.00 0.00 0.00]
        [0.00 0.00 0.33]
        [0.00 0.00 0.00]
        
    The complete list of components in raw form can be recovered by the double
    bracket operator, replacing ``:`` by ``slice(None)`` (since ``a[[:]]`` 
    generates a Python syntax error)::
    
        sage: a[[slice(None)]]
        [  0   0   0]
        [  0   0 1/3]
        [  0   0   0]
        
    Internally, the components are stored as a dictionary (:attr:`_comp`) whose
    keys are the indices; only the non-zero components are stored::

        sage: a._comp
        {(1, 2): 1/3}
        sage: v = Components(QQ, basis, 1)
        sage: v[:] = (-1, 0, 3)
        sage: v._comp  # random output order of the dictionary elements
        {(0,): -1, (2,): 3}
      
    ARITHMETIC EXAMPLES:

    Unary plus operator::
    
        sage: a = Components(QQ, basis, 1)
        sage: a[:] = (-1, 0, 3)
        sage: s = +a ; s[:]
        [-1, 0, 3]
        sage: +a == a
        True

    Unary minus operator::
    
        sage: s = -a ; s[:]
        [1, 0, -3]
        
    Addition::
    
        sage: b = Components(QQ, basis, 1)
        sage: b[:] = (2, 1, 4)
        sage: s = a + b ; s[:]
        [1, 1, 7]
        sage: a + b == b + a
        True
        sage: a + (-a) == 0
        True

    Subtraction::
    
        sage: s = a - b ; s[:]
        [-3, -1, -1]
        sage: s + b == a
        True
        sage: a - b == - (b - a)
        True
    
    Multiplication by a scalar::
    
        sage: s = 2*a ; s[:]
        [-2, 0, 6]

    Division by a scalar::
    
        sage: s = a/2 ; s[:]
        [-1/2, 0, 3/2]
        sage: 2*(a/2) == a
        True

    Tensor product (by means of the operator ``*``)::
    
        sage: c = a*b ; c
        2-indices components w.r.t. [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        ]
        sage: a[:], b[:]
        ([-1, 0, 3], [2, 1, 4])
        sage: c[:]
        [-2 -1 -4]
        [ 0  0  0]
        [ 6  3 12]
        sage: d = c*a ; d
        3-indices components w.r.t. [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
        ]
        sage: d[:]
        [[[2, 0, -6], [1, 0, -3], [4, 0, -12]],
         [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
         [[-6, 0, 18], [-3, 0, 9], [-12, 0, 36]]]
        sage: d[0,1,2] == a[0]*b[1]*a[2]
        True

    """
    def __init__(self, ring, frame, nb_indices, start_index=0, 
                 output_formatter=None):
        # For efficiency, no test is performed regarding the type and range of 
        # the arguments:
        self.ring = ring
        self.frame = frame
        self.nid = nb_indices
        self.dim = len(frame)
        self.sindex = start_index
        self.output_formatter = output_formatter
        self._comp = {} # the dictionary of components, with the indices as keys
        
    def _repr_(self):
        r"""
        String representation of the object.
        """
        description = str(self.nid)
        if self.nid == 1:
            description += "-index"
        else:
            description += "-indices"
        description += " components w.r.t. " + str(self.frame)
        return description
        
    def _new_instance(self):
        r"""
        Creates a :class:`Components` instance of the same number of indices 
        and w.r.t. the same frame.  

        This method must be redefined by derived classes of 
        :class:`Components`.
        
        """
        return Components(self.ring, self.frame, self.nid, self.sindex, 
                          self.output_formatter)

    def copy(self):
        r"""
        Returns an exact copy of ``self``.
        
        EXAMPLES:
        
        Copy of a set of components with a single index::

            sage: V = VectorSpace(QQ,3)
            sage: a = Components(QQ, V.basis(), 1)
            sage: a[:] = -2, 1, 5
            sage: b = a.copy() ; b
            1-index components w.r.t. [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
            ]
            sage: b[:]
            [-2, 1, 5]
            sage: b == a
            True
            sage: b is a  # b is a distinct object
            False

        """
        result = self._new_instance()
        for ind, val in self._comp.items():
            if hasattr(val, 'copy'):
                result._comp[ind] = val.copy()
            else:
                result._comp[ind] = val
        return result

    def _del_zeros(self):
        r"""
        Deletes all the zeros in the dictionary :attr:`_comp`
        
        """
        # The zeros are first searched; they are deleted in a second stage, to
        # avoid changing the dictionary while it is read
        zeros = []
        for ind, value in self._comp.items():
            if value == 0:
                zeros.append(ind)
        for ind in zeros:
            del self._comp[ind] 

    def _check_indices(self, indices):
        r"""
        Check the validity of a list of indices and returns a tuple from it
        
        INPUT:
        
        - ``indices`` -- list of indices (possibly a single integer if
          self is a 1-index object)
          
        OUTPUT:
        
        - a tuple containing valid indices
          
        """
        if isinstance(indices, (int, Integer)):
            ind = (indices,)
        else:
            ind = tuple(indices)
        if len(ind) != self.nid:
            raise TypeError("Wrong number of indices: " + str(self.nid) + 
                            " expected, while " + str(len(ind)) + 
                            " are provided.")
        si = self.sindex
        imax = self.dim - 1 + si
        for k in range(self.nid):
            i = ind[k]
            if i < si or i > imax: 
                raise IndexError("Index out of range: " 
                                  + str(i) + " not in [" + str(si) + ","
                                  + str(imax) + "]")
        return ind

    def __getitem__(self, args):
        r"""
        Returns the component corresponding to the given indices.

        INPUT:
        
        - ``args`` -- list of indices (possibly a single integer if
          self is a 1-index object) or the character ``:`` for the full list
          of components.

        OUTPUT:
        
        - the component corresponding to ``args`` or, if ``args`` = ``:``,
          the full list of components, in the form ``T[i][j]...`` for the components
          `T_{ij...}` (for a 2-indices object, a matrix is returned).
    
        """
        no_format = self.output_formatter is None
        format_type = None # default value, possibly redefined below
        if isinstance(args, list):  # case of [[...]] syntax
            no_format = True
            if isinstance(args[0], slice):
                indices = args[0]
            elif isinstance(args[0], tuple): # to ensure equivalence between
                indices = args[0]           # [[(i,j,...)]] and [[i,j,...]]
            else:
                indices = tuple(args)
        else:
            # Determining from the input the list of indices and the format
            if isinstance(args, (int, Integer)) or isinstance(args, slice):
                indices = args
            elif isinstance(args[0], slice):
                indices = args[0]
                format_type = args[1]
            elif len(args) == self.nid:
                indices = args
            else:
                format_type = args[-1]
                indices = args[:-1]
        if isinstance(indices, slice):
            return self._get_list(indices, no_format, format_type)
        else: 
            ind = self._check_indices(indices)
            if ind in self._comp:
                if no_format:
                    return self._comp[ind]
                else:
                    return self.output_formatter(self._comp[ind], format_type) 
            else:  # if the value is not stored in self._comp, it is zero:
                if no_format:
                    return self.ring.zero_element()
                else:
                    return self.output_formatter(self.ring.zero_element(), 
                                                 format_type) 

    def _get_list(self, ind_slice, no_format=True, format_type=None):
        r"""
        Return the list of components.
        
        INPUT:
        
        - ``ind_slice`` --  a slice object
        
        OUTPUT:
        
        - the full list of components if  ``ind_slice`` == ``[:]``, or a slice
          of it if ``ind_slice`` == ``[a:b]`` (1-D case), in the form
          ``T[i][j]...`` for the components `T_{ij...}` (for a 2-indices 
          object, a matrix is returned).
          
        """
        from sage.matrix.constructor import matrix
        si = self.sindex
        nsi = si + self.dim
        if self.nid == 1:
            if ind_slice.start is None: 
                start = si
            else:
                start = ind_slice.start
            if ind_slice.stop is None: 
                stop = nsi
            else:
                stop = ind_slice.stop
            if ind_slice.step is not None:
                raise NotImplementedError("Function [start:stop:step] " +
                                              "not implemented.")
            if no_format:
                return [self[[i]] for i in range(start, stop)]
            else:
                return [self[i, format_type] for i in range(start, stop)]
        if ind_slice.start is not None or ind_slice.stop is not None:
            raise NotImplementedError("Function [start:stop] not " +
                          "implemented for components with " + str(self.nid) + 
                          " indices.")
        resu = [self._gen_list([i], no_format, format_type)
                                                       for i in range(si, nsi)]
        if self.nid == 2:
            resu = matrix(resu)  # for a nicer output
        return resu

    def _gen_list(self, ind, no_format=True, format_type=None):
        r"""
        Recursive function to generate the list of values
        """
        if len(ind) == self.nid:
            if no_format:
                return self[ind]
            else:
                args = tuple(ind + [format_type])
                return self.__getitem__(args)
        else:
            si = self.sindex
            nsi = si + self.dim
            return [self._gen_list(ind + [i], no_format, format_type) 
                                                       for i in range(si, nsi)] 

    def __setitem__(self, indices, value):
        r"""
        Sets the component corresponding to the given indices.

        INPUT:
        
        - ``indices`` -- list of indices (possibly a single integer if
          self is a 1-index object) ; if [:] is provided, all the components 
          are set. 
        - ``value`` -- the value to be set or a list of values if ``args``
          == ``[:]``
    
        """
        if isinstance(indices, slice):
            self._set_list(indices, value)
        else:
            if isinstance(indices, list):    
            # to ensure equivalence between [i,j,...] and [[i,j,...]] or 
            # [[(i,j,...)]]
                if isinstance(indices[0], tuple):
                    indices = indices[0]
                else:
                    indices = tuple(indices)
            ind = self._check_indices(indices)
            if value == 0:
                # if the component has been set previously, it is deleted,
                # otherwise nothing is done:
                if ind in self._comp:
                    del self._comp[ind]
            else:
                self._comp[ind] = self.ring(value)

    def _set_list(self, ind_slice, values):
        r"""
        Set the components from a list.
        
        INPUT:
        
        - ``ind_slice`` --  a slice object
        - ``values`` -- list of values for the components : the full list if       
          ``ind_slice`` == ``[:]``, in the form ``T[i][j]...`` for the 
          component `T_{ij...}`. In the 1-D case, ``ind_slice`` can be
          a slice of the full list, in the form  ``[a:b]``
          
        """
        si = self.sindex
        nsi = si + self.dim
        if self.nid == 1:
            if ind_slice.start is None: 
                start = si
            else:
                start = ind_slice.start
            if ind_slice.stop is None: 
                stop = nsi
            else:
                stop = ind_slice.stop
            if ind_slice.step is not None:
                raise NotImplementedError("Function [start:stop:step] " +
                                              "not implemented.")
            for i in range(start, stop):
                self[i] = values[i-start]
        else:
            if ind_slice.start is not None or ind_slice.stop is not None:
                raise NotImplementedError("Function [start:stop] not " +
                          "implemented for components with " + str(self.nid) + 
                          " indices.")
            for i in range(si, nsi):
                self._set_value_list([i], values[i-si])

    def _set_value_list(self, ind, val):
        r"""
        Recursive function to set a list of values to self
        """
        if len(ind) == self.nid:
            self[ind] = val
        else:
            si = self.sindex
            nsi = si + self.dim
            for i in range(si, nsi):
                self._set_value_list(ind + [i], val[i-si])

    def swap_adjacent_indices(self, pos1, pos2, pos3):
        r"""
        Swap two adjacent sets of indices. 
        
        This method is essentially required to reorder the covariant and 
        contravariant indices in the computation of a tensor product. 
        
        INPUT:
        
        - ``pos1`` -- position of the first index of set 1
        - ``pos2`` -- position of the first index of set 2 = 1 + position of 
          the last index of set 1 (since the two sets are adjacent)
        - ``pos3`` -- 1 + position of the last index of set 2
        
        OUTPUT:
        
        - Components with index set 1 permuted with index set 2. 
        
        EXAMPLES:
        
        Swap of the two indices of a 2-indices set of components::
        
            
        Swap of two pairs of indices on a 4-indices set of components::
            

        """
        result = self._new_instance()
        for ind, val in self._comp.items():
            new_ind = ind[:pos1] + ind[pos2:pos3] + ind[pos1:pos2] + ind[pos3:]
            result._comp[new_ind] = val 
            # the above writing is more efficient than result[new_ind] = val 
            # it does not work for the derived class CompWithSym, but for the 
            # latter, the function CompWithSym.swap_adjacent_indices will be
            # called and not the present function. 
        return result
        
    def is_zero(self):
        r""" 
        Return True if all the components are zero and False otherwise.

        EXAMPLES:
        
        A just-created set of components is initialized to zero::
        
            sage: V = VectorSpace(QQ,3)
            sage: c = Components(QQ, V.basis(), 1)
            sage: c.is_zero()
            True
            sage: c[:]
            [0, 0, 0]
            sage: c[0] = 1 ; c[:]
            [1, 0, 0]
            sage: c.is_zero()
            False
            sage: c[0] = 0 ; c[:]
            [0, 0, 0]
            sage: c.is_zero()
            True

        It is equivalent to use the operator == to compare to zero::
        
            sage: c == 0
            True
            sage: c != 0
            False

        Comparing to a nonzero number is meaningless::
    
            sage: c == 1
            Traceback (most recent call last):
            ...
            TypeError: Cannot compare a set of components to a number.

        """
        if self._comp == {}:
            return True
        else:
            #!# What follows could be skipped since _comp should not contain
            # any zero value
            # In other words, the full method should be
            #   return self.comp == {}
            for val in self._comp.values():
                if val != 0:
                    return False
            return True

    def __eq__(self, other):
        r"""
        Comparison (equality) operator. 
        
        INPUT:
        
        - ``other`` -- a set of components or 0
        
        OUTPUT:
        
        - True if ``self`` is equal to ``other``,  or False otherwise
        
        """
        if isinstance(other, (int, Integer)): # other is 0
            if other == 0:
                return self.is_zero()
            else:
                raise TypeError("Cannot compare a set of components to a " + 
                                "number.")
        else: # other is another Components
            if not isinstance(other, Components):
                raise TypeError("An instance of Components is expected.")
            if other.frame != self.frame:
                return False
            if other.nid != self.nid:
                return False
            if other.sindex != self.sindex:
                return False
            if other.output_formatter != self.output_formatter:
                return False
            return (self - other).is_zero()

    def __ne__(self, other):
        r"""
        Inequality operator. 
        
        INPUT:
        
        - ``other`` -- a set of components or 0
        
        OUTPUT:
        
        - True if ``self`` is different from ``other``,  or False otherwise
        
        """
        return not self.__eq__(other)
        
    def __pos__(self):
        r"""
        Unary plus operator. 
        
        OUTPUT:
        
        - an exact copy of ``self``
    
        """
        return self.copy()

    def __neg__(self):
        r"""
        Unary minus operator. 
        
        OUTPUT:
        
        - the opposite of the components represented by ``self``
    
        """
        result = self._new_instance()
        for ind, val in self._comp.items():
             result._comp[ind] = - val
        return result

    def __add__(self, other):
        r"""
        Component addition. 
        
        INPUT:
        
        - ``other`` -- components of the same number of indices and defined
          on the same frame as ``self``
        
        OUTPUT:
        
        - components resulting from the addition of ``self`` and ``other``
        
        """
        if other == 0:
            return +self
        if not isinstance(other, Components):
            raise TypeError("The second argument for the addition must be " + 
                            "an instance of Components.")
        if isinstance(other, CompWithSym):
            return other + self     # to deal properly with symmetries
        if other.frame != self.frame:
            raise TypeError("The two sets of components are not defined on " +
                            "the same frame.")
        if other.nid != self.nid:
            raise TypeError("The two sets of components do not have the " + 
                            "same number of indices.")
        if other.sindex != self.sindex:
            raise TypeError("The two sets of components do not have the " + 
                            "same starting index.")
        result = self.copy()
        for ind, val in other._comp.items():
            result[[ind]] += val
        return result

    def __radd__(self, other):
        r"""
        Addition on the left with ``other``. 
        
        """
        return self.__add__(other)


    def __sub__(self, other):
        r"""
        Component subtraction. 
        
        INPUT:
        
        - ``other`` -- components, of the same type as ``self``
        
        OUTPUT:
        
        - components resulting from the subtraction of ``other`` from ``self``
        
        """
        if other == 0:
            return +self
        return self.__add__(-other)  #!# correct, deals properly with 
                                     # symmetries, but is probably not optimal

    def __rsub__(self, other):
        r"""
        Subtraction from ``other``. 
        
        """
        return (-self).__add__(other)


    def __mul__(self, other):
        r"""
        Component tensor product. 
        
        INPUT:
        
        - ``other`` -- components, on the same vector frame as ``self``
        
        OUTPUT: 
        
        - the tensor product of ``self`` by ``other``
        
        """
        if not isinstance(other, Components):
            raise TypeError("The second argument for the tensor product " + 
                            "must be an instance of Components.")
        if other.frame != self.frame:
            raise TypeError("The two sets of components are not defined on " +
                            "the same vector frame.")
        if other.sindex != self.sindex:
            raise TypeError("The two sets of components do not have the " + 
                            "same starting index.")
        if isinstance(other, CompWithSym):
            sym = []
            if other.sym != []:
                for s in other.sym:
                    ns = tuple(s[i]+self.nid for i in range(len(s)))
                    sym.append(ns)
            antisym = []
            if other.antisym != []:
                for s in other.antisym:
                    ns = tuple(s[i]+self.nid for i in range(len(s)))
                    antisym.append(ns)
            result = CompWithSym(self.ring, self.frame, self.nid + other.nid, 
                                 self.sindex, self.output_formatter, sym, 
                                 antisym)
        elif self.nid == 1 and other.nid == 1:
            if self is other:  # == would be dangerous here 
                # the result is symmetric:
                result = CompFullySym(self.ring, self.frame, 2, self.sindex, 
                                      self.output_formatter)
            else:
                result = Components(self.ring, self.frame, 2, self.sindex, 
                                    self.output_formatter)
        else:
            result = Components(self.ring, self.frame, self.nid + other.nid,
                                self.sindex, self.output_formatter)
        for ind_s, val_s in self._comp.items():
            for ind_o, val_o in other._comp.items():
                result._comp[ind_s + ind_o] = val_s * val_o
        return result
        

    def __rmul__(self, other):
        r"""
        Multiplication on the left by ``other``. 
        
        """
        if isinstance(other, Components):
            raise NotImplementedError("Left tensor product not implemented.")
        # Left multiplication by a "scalar": 
        result = self._new_instance()
        if other == 0:
            return result   # because a just created Components is zero
        for ind, val in self._comp.items():
            result._comp[ind] = other * val
        return result


    def __div__(self, other):
        r"""
        Division (by a scalar). 
        
        """
        if isinstance(other, Components):
            raise NotImplementedError("Division by an object of type " + 
                                      "Components not implemented.")
        result = self._new_instance()
        for ind, val in self._comp.items():
            result._comp[ind] = val / other
        return result

    def self_contract(self, pos1, pos2):
        r""" 
        Index contraction.
        
        INPUT:
            
        - ``pos1`` -- position of the first index for the contraction
        - ``pos2`` -- position of the second index for the contraction
          
        OUTPUT:
        
        - set of components resulting from the (pos1, pos2) contraction
       
        EXAMPLES:
        

        """
        if self.nid < 2:
            raise TypeError("Contraction can be perfomed only on " + 
                                "components with at least 2 indices.")
        if pos1 < 0 or pos1 > self.nid - 1:
            raise IndexError("pos1 out of range.")
        if pos2 < 0 or pos2 > self.nid - 1:
            raise IndexError("pos2 out of range.")
        if pos1 == pos2:
            raise IndexError("The two positions must differ for the " +
                                 "contraction to be meaningful.")
        si = self.manifold.sindex
        nsi = si + self.manifold.dim
        if self.nid == 2:
            res = 0 
            for i in range(si, nsi):
                res += self[[i,i]]
            return res
        else:
            # More than 2 indices
            result = Components(self.frame, self.nid - 2)
            if pos1 > pos2:
                pos1, pos2 = (pos2, pos1)
            for ind, val in self._comp.items():
                if ind[pos1] == ind[pos2]:
                    # there is a contribution to the contraction
                    ind_res = ind[:pos1] + ind[pos1+1:pos2] + ind[pos2+1:]
                    result[[ind_res]] += val
            return result


    def contract(self, pos1, other, pos2):
        r""" 
        Index contraction with another instance of :class:`Components`. 
        
        INPUT:
            
        - ``pos1`` -- position of the first index (in ``self``) for the 
          contraction
        - ``other`` -- the set of components to contract with
        - ``pos2`` -- position of the second index (in ``other``) for the 
          contraction
          
        OUTPUT:
        
        - set of components resulting from the (pos1, pos2) contraction
       
        EXAMPLES:


        """
        if not isinstance(other, Components):
            raise TypeError("For the contraction, other must be an instance " +
                            "of Components.")
        if pos1 < 0 or pos1 > self.nid - 1:
            raise IndexError("pos1 out of range.")
        if pos2 < 0 or pos2 > other.nid - 1:
            raise IndexError("pos2 out of range.")
        return (self*other).self_contract(pos1, 
                                          pos2+self.nid) #!# correct but not optimal

    def index_generator(self):
        r"""
        Generator of indices. 
                
        OUTPUT:
        
        - an iterable index

        EXAMPLES:
        
        Indices on a 3-dimensional vector space::
        
            sage: V = VectorSpace(QQ,3)
            sage: c = Components(QQ, V.basis(), 1)
            sage: for ind in c.index_generator(): print ind,
            (0,) (1,) (2,)
            sage: c = Components(QQ, V.basis(), 1, start_index=1)
            sage: for ind in c.index_generator(): print ind,
            (1,) (2,) (3,)
            sage: c = Components(QQ, V.basis(), 2)
            sage: for ind in c.index_generator(): print ind,
            (0, 0) (0, 1) (0, 2) (1, 0) (1, 1) (1, 2) (2, 0) (2, 1) (2, 2)

        """
        si = self.sindex
        imax = self.dim - 1 + si
        ind = [si for k in range(self.nid)]
        ind_end = [si for k in range(self.nid)]
        ind_end[0] = imax+1
        while ind != ind_end:
            yield tuple(ind)
            ret = 1
            for pos in range(self.nid-1,-1,-1):
                if ind[pos] != imax:
                    ind[pos] += ret
                    ret = 0
                elif ret == 1:
                    if pos == 0:
                        ind[pos] = imax + 1 # end point reached
                    else:
                        ind[pos] = si
                        ret = 1
                        
    def non_redundant_index_generator(self):
        r"""
        Generator of non redundant indices. 
        
        In the absence of declared symmetries, all possible indices are 
        generated. So this method is equivalent to :meth:`index_generator`. 
        Only versions for derived classes with symmetries or antisymmetries 
        are not trivial. 
        
        OUTPUT:
        
        - an iterable index

        EXAMPLES:
        
        Indices on a 3-dimensional vector space::
        
            sage: V = VectorSpace(QQ,3)
            sage: c = Components(QQ, V.basis(), 2)
            sage: for ind in c.non_redundant_index_generator(): print ind,
            (0, 0) (0, 1) (0, 2) (1, 0) (1, 1) (1, 2) (2, 0) (2, 1) (2, 2)

        """
        for ind in self.index_generator():
            yield ind


    def symmetrize(self, pos=None):
        r"""
        Symmetrization over the given index positions
        
        INPUT:
        
        - ``pos`` -- (default: None) list of index positions involved in the 
          symmetrization (with the convention position=0 for the first index); 
          if none, the symmetrization is performed over all the indices
          
        OUTPUT:
        
        - an instance of :class:`CompWithSym` describing the symmetrized 
          components. 
          
        EXAMPLES:
        
        Symmetrization of 2-indices components on a 3-dimensional manifold::
        
            
        Symmetrization of 3-indices components::
        

        Partial symmetrization of 3-indices components::
        
             

        """
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        if pos is None:
            pos = range(self.nid)
        else:
            if len(pos) < 2:
                raise TypeError("At least two index positions must be given.")
            if len(pos) > self.nid:
                raise TypeError("Number of index positions larger than the " \
                                "total number of indices.")
        n_sym = len(pos) # number of indices involved in the symmetry
        if n_sym == self.nid:
            result = CompFullySym(self.ring, self.frame, self.nid, self.sindex,
                                  self.output_formatter)
        else:
            result = CompWithSym(self.ring, self.frame, self.nid, self.sindex, 
                                 self.output_formatter, sym=pos)
        sym_group = SymmetricGroup(n_sym)
        for ind in result.non_redundant_index_generator():
            sum = 0
            for perm in sym_group.list():
                # action of the permutation on [0,1,...,n_sym-1]:
                perm_action = map(lambda x: x-1, perm.domain())
                ind_perm = list(ind)
                for k in range(n_sym):
                    ind_perm[pos[perm_action[k]]] = ind[pos[k]]
                sum += self[[ind_perm]]
            result[[ind]] = sum / sym_group.order()
        return result

            
    def antisymmetrize(self, pos=None):
        r"""
        Antisymmetrization over the given index positions
        
        INPUT:
        
        - ``pos`` -- (default: None) list of index positions involved in the 
          antisymmetrization (with the convention position=0 for the first 
          index); if none, the antisymmetrization is performed over all the 
          indices
          
        OUTPUT:
        
        - an instance of :class:`CompWithSym` describing the antisymmetrized 
          components. 
          
        EXAMPLES:
        
        Antisymmetrization of 2-indices components on a 3-dimensional manifold::
        
            
        Antisymmetrization of 3-indices components::
        

        Partial antisymmetrization of 3-indices components::
            

        """
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        if pos is None:
            pos = range(self.nid)
        else:
            if len(pos) < 2:
                raise TypeError("At least two index positions must be given.")
            if len(pos) > self.nid:
                raise TypeError("Number of index positions larger than the " \
                                "total number of indices.")
        n_sym = len(pos) # number of indices involved in the antisymmetry
        if n_sym == self.nid:
            result = CompFullyAntiSym(self.ring, self.frame, self.nid, 
                                      self.sindex, self.output_formatter)
        else:
            result = CompWithSym(self.ring, self.frame, self.nid, self.sindex, 
                                 self.output_formatter, antisym=pos)
        sym_group = SymmetricGroup(n_sym)
        for ind in result.non_redundant_index_generator():
            sum = 0 
            for perm in sym_group.list():
                # action of the permutation on [0,1,...,n_sym-1]:
                perm_action = map(lambda x: x-1, perm.domain())
                ind_perm = list(ind)
                for k in range(n_sym):
                    ind_perm[pos[perm_action[k]]] = ind[pos[k]]
                if perm.sign() == 1:
                    sum += self[[ind_perm]]
                else:
                    sum -= self[[ind_perm]]
            result[[ind]] = sum / sym_group.order()
        return result

            
#******************************************************************************

class CompWithSym(Components):
    r"""
    Class for storing components with respect to a given "frame", taking into 
    account symmetries or antisymmetries among the indices. 
    
    The "frame" can be a basis of some vector space or a vector frame on some 
    manifold (i.e. a field of bases). 
    The stored quantities can be tensor components or non-tensorial quantities, 
    such as connection coefficients or structure coefficents. 
    
    Subclasses of :class:`CompWithSym` are
    
    * :class:`CompFullySym` for storing fully symmetric components.
    * :class:`CompFullyAntiSym` for storing fully antisymmetric components.

    INPUT:
    
    - ``ring`` -- ring in which each component takes its value
    - ``frame`` -- frame with respect to which the components are defined; 
      whatever type ``frame`` is, it should have some method ``__len__()``
      implemented, so that ``len(frame)`` returns the dimension, i.e. the size
      of a single index range
    - ``nb_indices`` -- number of indices labeling the components
    - ``start_index`` -- (default: 0) first value of a single index; 
      accordingly a component index i must obey
      ``start_index <= i <= start_index + dim - 1``, where ``dim = len(frame)``. 
    - ``output_formatter`` -- (default: None) 2-argument function or unbound 
      method called to format the output of the component access 
      operator ``[...]`` (method __getitem__); the 1st argument of 
      ``output_formatter`` must be an instance of ``ring``, and the second some 
      format.
    - ``sym`` -- (default: None) a symmetry or a list of symmetries among the 
      indices: each symmetry is described by a tuple containing the positions 
      of the involved indices, with the convention position=0 for the first
      index. For instance:
        * sym=(0,1) for a symmetry between the 1st and 2nd indices 
        * sym=[(0,2),(1,3,4)] for a symmetry between the 1st and 3rd
          indices and a symmetry between the 2nd, 4th and 5th indices.
    - ``antisym`` -- (default: None) antisymmetry or list of antisymmetries 
      among the indices, with the same convention as for ``sym``. 
      
    EXAMPLES:

    Symmetric components with 2 indices::
    
        sage: V = VectorSpace(QQ,3)
        sage: c = CompWithSym(QQ, V.basis(), 2, sym=(0,1))  # for demonstration only: it is preferable to use CompFullySym in this case 
        sage: c[0,1] = 3  
        sage: c[:]  # note that c[1,0] has been set automatically
        [0 3 0]
        [3 0 0]
        [0 0 0]

    Antisymmetric components with 2 indices::
    
        sage: c = CompWithSym(QQ, V.basis(), 2, antisym=(0,1))  # for demonstration only: it is preferable to use CompFullyAntiSym in this case 
        sage: c[0,1] = 3
        sage: c[:]  # note that c[1,0] has been set automatically
        [ 0  3  0]
        [-3  0  0]
        [ 0  0  0]
        
    Internally, only non-redundant components are stored::
        
        sage: c._comp
        {(0, 1): 3}
        
    Components with 6 indices, symmetric among 3 indices (at position ((0,1,5))
    and antisymmetric among 2 indices (at position (2,4))::
    
        sage: c = CompWithSym(QQ, V.basis(), 6, sym=(0,1,5), antisym=(2,4))
        sage: c[0,1,2,0,1,2] = 3
        sage: c[1,0,2,0,1,2]  # symmetry between indices in position 0 and 1
        3
        sage: c[2,1,2,0,1,0]  # symmetry between indices in position 0 and 5
        3
        sage: c[0,2,2,0,1,1]  # symmetry between indices in position 1 and 5
        3
        sage: c[0,1,1,0,2,2]  # antisymmetry between indices in position 2 and 4
        -3

    Components with 4 indices, antisymmetric with respect to the first pair of
    indices as well as with the second pair of indices::
    
        sage: c = CompWithSym(QQ, V.basis(), 4, antisym=[(0,1),(2,3)])
        sage: c[0,1,0,1] = 3
        sage: c[1,0,0,1]  # antisymmetry on the first pair of indices
        -3
        sage: c[0,1,1,0]  # antisymmetry on the second pair of indices
        -3
        sage: c[1,0,1,0]  # consequence of the above
        3
        
    """
    def __init__(self, ring, frame, nb_indices, start_index=0, 
                 output_formatter=None, sym=None, antisym=None):
        Components.__init__(self, ring, frame, nb_indices, start_index, 
                            output_formatter)
        self.sym = []
        if sym is not None and sym != []:
            if isinstance(sym[0], (int, Integer)):  
                # a single symmetry is provided as a tuple -> 1-item list:
                sym = [tuple(sym)]
            for isym in sym:
                if len(isym) < 2:
                    raise IndexError("At least two index positions must be " + 
                                     "provided to define a symmetry.")
                for i in isym:
                    if i<0 or i>self.nid-1:
                        raise IndexError("Invalid index position: " + str(i) +
                                         " not in [0," + str(self.nid-1) + "]")
                self.sym.append(tuple(isym))       
        self.antisym = []
        if antisym is not None and antisym != []:
            if isinstance(antisym[0], (int, Integer)):  
                # a single antisymmetry is provided as a tuple -> 1-item list:
                antisym = [tuple(antisym)]
            for isym in antisym:
                if len(isym) < 2:
                    raise IndexError("At least two index positions must be " + 
                                     "provided to define an antisymmetry.")
                for i in isym:
                    if i<0 or i>self.nid-1:
                        raise IndexError("Invalid index position: " + str(i) +
                                         " not in [0," + str(self.nid-1) + "]")
                self.antisym.append(tuple(isym))
        # Final consistency check:
        index_list = []
        for isym in self.sym:
            index_list += isym
        for isym in self.antisym:
            index_list += isym
        if len(index_list) != len(set(index_list)):
            # There is a repeated index position:
            raise IndexError("Incompatible lists of symmetries: the same " + 
                             "index position appears more then once.")

    def _repr_(self):
        r"""
        String representation of the object.
        """
        description = str(self.nid)
        if self.nid == 1:
            description += "-index"
        else:
            description += "-indices"
        description += " components w.r.t. " + str(self.frame)
        for isym in self.sym:
            description += ", with symmetry on the index positions " + \
                           str(tuple(isym))
        for isym in self.antisym:
            description += ", with antisymmetry on the index positions " + \
                           str(tuple(isym))
        return description
    
    def _new_instance(self):
        r"""
        Creates a :class:`CompWithSym` instance w.r.t. the same vector frame,
        and with the same number of indices and the same symmetries
        
        """
        return CompWithSym(self.ring, self.frame, self.nid, self.sindex, 
                          self.output_formatter, self.sym, self.antisym)

    def _ordered_indices(self, indices):
        r"""
        Given a set of indices, returns a set of indices with the indices
        at the positions of symmetries or antisymmetries being ordered, 
        as well as some antisymmetry indicator.
 
        INPUT:
        
        - ``indices`` -- list of indices (possibly a single integer if
          self is a 1-index object)
        
        OUTPUT:
        
        - a pair `(s,ind)` where ind is a tuple that differs from the original 
          list of indices by a reordering at the positions of symmetries and
          antisymmetries and
            * `s=0` if the value corresponding to ``indices`` vanishes by 
              antisymmetry (repeated indices); `ind` is then set to None
            * `s=1` if the value corresponding to ``indices`` is the same as
              that corresponding to `ind`
            * `s=-1` if the value corresponding to ``indices`` is the opposite
              of that corresponding to `ind`
            
        """
        from sage.combinat.permutation import Permutation
        ind = list(self._check_indices(indices))
        for isym in self.sym:
            indsym = []
            for pos in isym:
                indsym.append(ind[pos])
            indsym_ordered = sorted(indsym)
            for k, pos in enumerate(isym):
                ind[pos] = indsym_ordered[k]
        sign = 1
        for isym in self.antisym:
            indsym = []
            for pos in isym:
                indsym.append(ind[pos])
            # Returns zero if some index appears twice:
            if len(indsym) != len(set(indsym)):
                return (0, None)
            # From here, all the indices in indsym are distinct and we need
            # to determine whether they form an even permutation of their 
            # ordered series
            indsym_ordered = sorted(indsym)
            for k, pos in enumerate(isym):
                ind[pos] = indsym_ordered[k]
            if indsym_ordered != indsym:
                # Permutation linking indsym_ordered to indsym:
                #  (the +1 is required to fulfill the convention of Permutation) 
                perm = [indsym.index(i) +1 for i in indsym_ordered]
                #c# print "indsym_ordered, indsym: ", indsym_ordered, indsym 
                #c# print "Permutation: ", Permutation(perm), " signature = ",  \
                #c#     Permutation(perm).signature()
                sign *= Permutation(perm).signature()
        ind = tuple(ind)
        return (sign, ind)

    def __getitem__(self, args):
        r"""
        Returns the component corresponding to the given indices.

        INPUT:
        
        - ``args`` -- list of indices (possibly a single integer if
          self is a 1-index object) or the character ``:`` for the full list
          of components.
          
        OUTPUT:
        
        - the component corresponding to ``args`` or, if ``args`` = ``:``,
          the full list of components, in the form ``T[i][j]...`` for the components
          `T_{ij...}` (for a 2-indices object, a matrix is returned).
    
        """
        no_format = self.output_formatter is None
        format_type = None # default value, possibly redefined below
        if isinstance(args, list):  # case of [[...]] syntax
            no_format = True
            if isinstance(args[0], slice):
                indices = args[0]
            elif isinstance(args[0], tuple): # to ensure equivalence between
                indices = args[0]           # [[(i,j,...)]] and [[i,j,...]]
            else:
                indices = tuple(args)
        else:
            # Determining from the input the list of indices and the format
            if isinstance(args, (int, Integer)) or isinstance(args, slice):
                indices = args
            elif isinstance(args[0], slice):
                indices = args[0]
                format_type = args[1]
            elif len(args) == self.nid:
                indices = args
            else:
                format_type = args[-1]
                indices = args[:-1]
        if isinstance(indices, slice):
            return self._get_list(indices, no_format, format_type)
        else: 
            sign, ind = self._ordered_indices(indices)
            if (sign == 0) or (ind not in self._comp): # the value is zero:
                if no_format:
                    return self.ring.zero_element()
                else:
                    return self.output_formatter(self.ring.zero_element(), 
                                                 format_type) 
            else: # non zero value
                if no_format:
                    if sign == 1:
                        return self._comp[ind]
                    else: # sign = -1
                        return -self._comp[ind]
                else:
                    if sign == 1:
                        return self._comp[ind].output_formatter(
                                              self._comp[ind], format_type)
                    else: # sign = -1
                        return -self._comp[ind].output_formatter(
                                              self._comp[ind], format_type)

    def __setitem__(self, indices, value):
        r"""
        Sets the component corresponding to the given indices.

        INPUT:
        
        - ``indices`` -- list of indices (possibly a single integer if
          self is a 1-index object) ; if [:] is provided, all the components 
          are set. 
        - ``value`` -- the value to be set or a list of values if ``args``
          == ``[:]``
    
        """
        if isinstance(indices, slice):
            self._set_list(indices, value)
        else:
            if isinstance(indices, list):    
            # to ensure equivalence between [i,j,...] and [[i,j,...]] or 
            # [[(i,j,...)]]
                if isinstance(indices[0], tuple):
                    indices = indices[0]
                else:
                    indices = tuple(indices)
            sign, ind = self._ordered_indices(indices)
            if sign == 0:
                if value != 0:
                    raise ValueError(
                            "By antisymmetry, the component cannot have a " + 
                            "nonzero value for the indices " + str(indices))
                if ind in self._comp:
                    del self._comp[ind]  # zero values are not stored
            elif value == 0:
                if ind in self._comp:
                    del self._comp[ind]  # zero values are not stored
            else:
                if sign == 1:
                    self._comp[ind] = self.ring(value)
                else:   # sign = -1
                    self._comp[ind] = -self.ring(value)


    def swap_adjacent_indices(self, pos1, pos2, pos3):
        r"""
        Swap two adjacent sets of indices. 
        
        This method is essentially required to reorder the covariant and 
        contravariant indices in the computation of a tensor product. 
        
        The symmetries are preserved and the corresponding indices are adjusted
        consequently. 
        
        INPUT:
        
        - ``pos1`` -- position of the first index of set 1
        - ``pos2`` -- position of the first index of set 2 = 1 + position of 
          the last index of set 1 (since the two sets are adjacent)
        - ``pos3`` -- 1 + position of the last index of set 2
        
        OUTPUT:
        
        - Components with index set 1 permuted with index set 2. 
        
        EXAMPLES:
        
        Swap of the index in position 0 with the pair of indices in position 
        (1,2) in a set of components antisymmetric with respect to the indices
        in position (1,2)::
        

        """
        result = self._new_instance()
        # The symmetries:
        lpos = range(self.nid)
        new_lpos = lpos[:pos1] + lpos[pos2:pos3] + lpos[pos1:pos2] + lpos[pos3:]
        result.sym = []
        for s in self.sym:
            new_s = [new_lpos.index(pos) for pos in s]
            result.sym.append(tuple(sorted(new_s)))
        result.antisym = []
        for s in self.antisym:
            new_s = [new_lpos.index(pos) for pos in s]
            result.antisym.append(tuple(sorted(new_s)))
        # The values:
        for ind, val in self._comp.items():
            new_ind = ind[:pos1] + ind[pos2:pos3] + ind[pos1:pos2] + ind[pos3:]
            result[new_ind] = val  
        return result

    def __add__(self, other):
        r"""
        Component addition. 
        
        INPUT:
        
        - ``other`` -- components of the same number of indices and defined
          on the same frame as ``self``
        
        OUTPUT:
        
        - components resulting from the addition of ``self`` and ``other``
        
        """
        if other == 0:
            return +self
        if not isinstance(other, Components):
            raise TypeError("The second argument for the addition must be a " + 
                            "an instance of Components.")
        if other.frame != self.frame:
            raise TypeError("The two sets of components are not defined on " +
                            "the same vector frame.")
        if other.nid != self.nid:
            raise TypeError("The two sets of components do not have the " + 
                            "same number of indices.")
        if other.sindex != self.sindex:
            raise TypeError("The two sets of components do not have the " + 
                            "same starting index.")
        if isinstance(other, CompWithSym):
            # Are the symmetries of the same type ?
            diff_sym = set(self.sym).symmetric_difference(set(other.sym))
            diff_antisym = \
                set(self.antisym).symmetric_difference(set(other.antisym))
            if diff_sym == set() and diff_antisym == set():
                # The symmetries/antisymmetries are identical:
                result = self.copy()
                for ind, val in other._comp.items():
                    result[[ind]] += val
                return result
            else:
                # The symmetries/antisymmetries are different: only the 
                # common ones are kept
                common_sym = []
                for isym in self.sym:
                    for osym in other.sym:
                        com = tuple(set(isym).intersection(set(osym)))
                        if len(com) > 1:
                            common_sym.append(com)
                common_antisym = []
                for isym in self.antisym:
                    for osym in other.antisym:
                        com = tuple(set(isym).intersection(set(osym)))
                        if len(com) > 1:
                            common_antisym.append(com)                           
                if common_sym != [] or common_antisym != []:
                    result = CompWithSym(self.ring, self.frame, self.nid, 
                                         self.sindex, self.output_formatter, 
                                         common_sym, common_antisym)
                else:
                    # no common symmetry -> the result is a generic Components:
                    result = Components(self.ring, self.frame, self.nid, 
                                        self.sindex, self.output_formatter)
        else:
            # other has no symmetry at all:
            result = Components(self.ring, self.frame, self.nid, 
                                self.sindex, self.output_formatter)
#!#       for ind in self.manifold.index_generator(self.nid):
        for ind in result.non_redundant_index_generator():
            result[[ind]] = self[[ind]] + other[[ind]]
        return result


    def __mul__(self, other):
        r"""
        Component tensor product. 
        
        INPUT:
        
        - ``other`` -- components, on the same vector frame as ``self``
        
        OUTPUT: 
        
        - the tensor product of ``self`` by ``other``
        
        """
        if not isinstance(other, Components):
            raise TypeError("The second argument for the tensor product " + 
                            "be an instance of Components.")
        if other.frame != self.frame:
            raise TypeError("The two sets of components are not defined on " +
                            "the same vector frame.")
        if other.sindex != self.sindex:
            raise TypeError("The two sets of components do not have the " + 
                            "same starting index.")
        sym = list(self.sym)
        antisym = list(self.antisym)
        if isinstance(other, CompWithSym):
            if other.sym != []:
                for s in other.sym:
                    ns = tuple(s[i]+self.nid for i in range(len(s)))
                    sym.append(ns)
            if other.antisym != []:
                for s in other.antisym:
                    ns = tuple(s[i]+self.nid for i in range(len(s)))
                    antisym.append(ns)
        result = CompWithSym(self.ring, self.frame, self.nid + other.nid, 
                             self.sindex, self.output_formatter, sym, antisym)
        for ind_s, val_s in self._comp.items():
            for ind_o, val_o in other._comp.items():
                result._comp[ind_s + ind_o] = val_s * val_o
        return result


    def self_contract(self, pos1, pos2):
        r""" 
        Index contraction, , taking care of the symmetries.
        
        INPUT:
            
        - ``pos1`` -- position of the first index for the contraction
        - ``pos2`` -- position of the second index for the contraction
          
        OUTPUT:
        
        - set of components resulting from the (pos1, pos2) contraction

        EXAMPLES:

        Self-contraction of symmetric 2-indices components::
        

        Self-contraction of antisymmetric 2-indices components::
        

        Self-contraction of 3-indices components with one symmetry::


        Self-contraction of 4-indices components with two symmetries::
        
        
        """ 
        if self.nid < 2:
            raise TypeError("Contraction can be perfomed only on " + 
                            "components with at least 2 indices.")
        if pos1 < 0 or pos1 > self.nid - 1:
            raise IndexError("pos1 out of range.")
        if pos2 < 0 or pos2 > self.nid - 1:
            raise IndexError("pos2 out of range.")
        if pos1 == pos2:
            raise IndexError("The two positions must differ for the " +
                                "contraction to take place.")
        si = self.manifold.sindex
        nsi = si + self.manifold.dim
        if self.nid == 2:
            res = 0 
            for i in range(si, nsi):
                res += self[[i,i]]
            return res
        else:
            # More than 2 indices
            if pos1 > pos2:
                pos1, pos2 = (pos2, pos1)
            # Determination of the remaining symmetries:
            sym_res = list(self.sym)
            for isym in self.sym:
                isym_res = list(isym)
                if pos1 in isym:
                    isym_res.remove(pos1)
                if pos2 in isym: 
                    isym_res.remove(pos2)
                if len(isym_res) < 2:       # the symmetry is lost
                    sym_res.remove(isym)
                else:
                    sym_res[sym_res.index(isym)] = tuple(isym_res)
            antisym_res = list(self.antisym)
            for isym in self.antisym:
                isym_res = list(isym)
                if pos1 in isym:
                    isym_res.remove(pos1)
                if pos2 in isym: 
                    isym_res.remove(pos2)
                if len(isym_res) < 2:       # the symmetry is lost
                    antisym_res.remove(isym)
                else:
                    antisym_res[antisym_res.index(isym)] = tuple(isym_res)
            # Shift of the index positions to take into account the
            # suppression of 2 indices:
            max_sym = 0
            for k in range(len(sym_res)):
                isym_res = []
                for pos in sym_res[k]:
                    if pos < pos1:
                        isym_res.append(pos)
                    elif pos < pos2:
                        isym_res.append(pos-1)
                    else:
                        isym_res.append(pos-2)
                max_sym = max(max_sym, len(isym_res))
                sym_res[k] = tuple(isym_res)        
            max_antisym = 0
            for k in range(len(antisym_res)):
                isym_res = []
                for pos in antisym_res[k]:
                    if pos < pos1:
                        isym_res.append(pos)
                    elif pos < pos2:
                        isym_res.append(pos-1)
                    else:
                        isym_res.append(pos-2)
                max_antisym = max(max_antisym, len(isym_res))
                antisym_res[k] = tuple(isym_res)
            # Construction of the appropriate object in view of the
            # remaining symmetries:
            nid_res = self.nid - 2
            if max_sym == 0 and max_antisym == 0:
                result = Components(self.ring, self.frame, nid_res, self.sindex,
                                    self.output_formatter)
            elif max_sym == nid_res:
                result = CompFullySym(self.ring, self.frame, nid_res,
                                      self.sindex, self.output_formatter)
            elif max_antisym == nid_res:
                result = CompFullyAntiSym(self.ring, self.frame, nid_res,
                                          self.sindex, self.output_formatter)
            else:
                result = CompWithSym(self.ring, self.frame, nid_res, 
                                     self.sindex, self.output_formatter, 
                                     sym=sym_res, antisym=antisym_res)
            # The contraction itself:
            for ind_res in result.index_generator():
                ind = list(ind_res)
                ind.insert(pos1, 0)
                ind.insert(pos2, 0)
                res = 0
                for i in range(si, nsi):
                    ind[pos1] = i
                    ind[pos2] = i 
                    res += self[[ind]]
                result[[ind_res]] = res
            return result


    def non_redundant_index_generator(self):
        r"""
        Generator of indices, with only ordered indices in case of symmetries, 
        so that only non-redundant indices are generated. 
                
        OUTPUT:
        
        - an iterable index

        EXAMPLES:
        
        Indices on a 3-dimensional manifold::
        

        """
        si = self.sindex
        imax = self.dim - 1 + si
        ind = [si for k in range(self.nid)]
        ind_end = [si for k in range(self.nid)]
        ind_end[0] = imax+1
        while ind != ind_end:
            ordered = True
            for isym in self.sym:
                for k in range(len(isym)-1):
                    if ind[isym[k+1]] < ind[isym[k]]:
                        ordered = False
                        break                
            for isym in self.antisym:
                for k in range(len(isym)-1):
                    if ind[isym[k+1]] <= ind[isym[k]]:
                        ordered = False
                        break
            if ordered:
                yield tuple(ind)
            ret = 1
            for pos in range(self.nid-1,-1,-1):
                if ind[pos] != imax:
                    ind[pos] += ret
                    ret = 0
                elif ret == 1:
                    if pos == 0:
                        ind[pos] = imax + 1 # end point reached
                    else:
                        ind[pos] = si
                        ret = 1

    def symmetrize(self, pos=None):
        r"""
        Symmetrization over the given index positions
        
        INPUT:
        
        - ``pos`` -- (default: None) list of index positions involved in the 
          symmetrization (with the convention position=0 for the first index); 
          if none, the symmetrization is performed over all the indices
          
        OUTPUT:
        
        - an instance of :class:`CompWithSym` describing the symmetrized 
          components. 
          
        EXAMPLES:
        
        Symmetrization of 3-indices components on a 3-dimensional manifold::
        
        
        Let us now start with a symmetry on the last two indices::

            
        Partial symmetrization of 4-indices components with an antisymmetry on
        the last two indices::
        

        Partial symmetrization of 4-indices components with an antisymmetry on
        the last three indices::


        """
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        if pos is None:
            pos = range(self.nid)
        else:
            if len(pos) < 2:
                raise TypeError("At least two index positions must be given.")
            if len(pos) > self.nid:
                raise TypeError("Number of index positions larger than the " \
                                "total number of indices.")
        pos = tuple(pos)
        pos_set = set(pos)
        # If the symmetry is already present, there is nothing to do:
        for isym in self.sym:
            if pos_set.issubset(set(isym)):
                return self.copy()
        #
        # Interference of the new symmetry with existing antisymmetries:
        # 
        antisym_res = []  # list of antisymmetries of the result
        for iasym in self.antisym:
            inter = pos_set.intersection(set(iasym))
            if len(inter) > 1: 
                # If at least two of the symmetry indices are already involved 
                # in the antisymmetry, the outcome is zero: 
                return CompFullySym(self.ring, self.frame, self.nid, 
                                    self.sindex, self.output_formatter)
                # (Note that a new instance of CompFullySym is initialized to zero)
            elif len(inter) == 1:
                # some piece of antisymmetry is lost
                k = inter.pop()  # the symmetry index position involved in the antisymmetry
                iasym_set = set(iasym)
                iasym_set.remove(k)
                if len(iasym_set) > 1:
                    iasym_res = tuple(iasym_set)
                    antisym_res.append(iasym_res)
                # len(iasym_set) = 1, the antisymmetry is fully lost, it is 
                # therefore not appended to antisym_res
            else:
                # case len(inter)=0: no interference: the antisymmetry is
                # added to the list of antisymmetries for the result:
                antisym_res.append(iasym)
        #
        # Does the new symmetry extend previous ones ? 
        #
        esym_set = pos_set
        index_esym = []
        for i, isym in enumerate(self.sym):
            if not esym_set.isdisjoint(set(isym)): # extension of a previous symmetry
                esym_set = esym_set.union(set(isym))
                index_esym.append(i)
        sym_res = [tuple(esym_set)]
        for i, isym in enumerate(self.sym):
            if i not in index_esym:
                sym_res.append(isym)
        # Creation of the result object:
        max_sym = 0
        for isym in sym_res:
            max_sym = max(max_sym, len(isym))
        if max_sym == self.nid:
            result = CompFullySym(self.ring, self.frame, self.nid, self.sindex,
                                  self.output_formatter)
        else:
            result = CompWithSym(self.ring, self.frame, self.nid, self.sindex,
                                 self.output_formatter, sym=sym_res, 
                                 antisym=antisym_res)
        # Symmetrization:
        n_sym = len(pos) # number of indices involved in the symmetry
        sym_group = SymmetricGroup(n_sym)
        for ind in result.non_redundant_index_generator():
            sum = 0 
            for perm in sym_group.list():
                # action of the permutation on [0,1,...,n_sym-1]:
                perm_action = map(lambda x: x-1, perm.domain())
                ind_perm = list(ind)
                for k in range(n_sym):
                    ind_perm[pos[perm_action[k]]] = ind[pos[k]]
                sum += self[[ind_perm]]
            result[[ind]] = sum / sym_group.order()
        return result


    def antisymmetrize(self, pos=None):
        r"""
        Antisymmetrization over the given index positions
        
        INPUT:
        
        - ``pos`` -- (default: None) list of index positions involved in the 
          antisymmetrization (with the convention position=0 for the first index); 
          if none, the antisymmetrization is performed over all the indices
          
        OUTPUT:
        
        - an instance of :class:`CompWithSym` describing the antisymmetrized 
          components. 
          
        EXAMPLES:
        
        Antisymmetrization of 3-indices components on a 3-dimensional manifold::
        
            
        Partial antisymmetrization::
        

        Partial antisymmetrization of 4-indices components with a symmetry on 
        the first two indices::
            

        The full antisymmetrization results in zero because of the symmetry on the 
        first two indices::
        
            
        Similarly, the partial antisymmetrization on the first two indices results in zero::
        
            
        The partial antisymmetrization on the positions (0,2) destroys the symmetry on (0,1)::
        

        """
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        if pos is None:
            pos = range(self.nid)
        else:
            if len(pos) < 2:
                raise TypeError("At least two index positions must be given.")
            if len(pos) > self.nid:
                raise TypeError("Number of index positions larger than the " \
                                "total number of indices.")
        pos = tuple(pos)
        pos_set = set(pos)
        # If the antisymmetry is already present, there is nothing to do:
        for iasym in self.antisym:
            if pos_set.issubset(set(iasym)):
                return self.copy()
        #
        # Interference of the new antisymmetry with existing symmetries:
        # 
        sym_res = []  # list of symmetries of the result
        for isym in self.sym:
            inter = pos_set.intersection(set(isym))
            if len(inter) > 1: 
                # If at least two of the antisymmetry indices are already involved 
                # in the symmetry, the outcome is zero: 
                return CompFullyAntiSym(self.ring, self.frame, self.nid, 
                                        self.sindex, self.output_formatter)
                # (Note that a new instance of CompFullyAntiSym is initialized to zero)
            elif len(inter) == 1:
                # some piece of the symmetry is lost
                k = inter.pop()  # the antisymmetry index position involved in the symmetry
                isym_set = set(isym)
                isym_set.remove(k)
                if len(isym_set) > 1:
                    isym_res = tuple(isym_set)
                    sym_res.append(isym_res)
                # len(isym_set) = 1, the symmetry is fully lost, it is 
                # therefore not appended to sym_res
            else:
                # case len(inter)=0: no interference: the symmetry is
                # added to the list of symmetries for the result:
                sym_res.append(isym)
        #
        # Does the new antisymmetry extend previous ones ?
        #
        esym_set = pos_set
        index_esym = []
        for i, isym in enumerate(self.antisym):
            if not esym_set.isdisjoint(set(isym)): # extension of a previous symmetry
                esym_set = esym_set.union(set(isym))
                index_esym.append(i)
        antisym_res = [tuple(esym_set)]
        for i, isym in enumerate(self.antisym):
            if i not in index_esym:
                antisym_res.append(isym)
        #
        # Creation of the result object:
        max_sym = 0
        for isym in antisym_res:
            max_sym = max(max_sym, len(isym))
        if max_sym == self.nid:
            result = CompFullyAntiSym(self.ring, self.frame, self.nid, 
                                      self.sindex, self.output_formatter)
        else:
            result = CompWithSym(self.ring, self.frame, self.nid, self.sindex,
                                 self.output_formatter, sym=sym_res, 
                                 antisym=antisym_res)
        # Antisymmetrization:
        n_sym = len(pos) # number of indices involved in the antisymmetry
        sym_group = SymmetricGroup(n_sym)
        for ind in result.non_redundant_index_generator():
            sum = 0 
            for perm in sym_group.list():
                # action of the permutation on [0,1,...,n_sym-1]:
                perm_action = map(lambda x: x-1, perm.domain())
                ind_perm = list(ind)
                for k in range(n_sym):
                    ind_perm[pos[perm_action[k]]] = ind[pos[k]]
                if perm.sign() == 1:
                    sum += self[[ind_perm]]
                else:
                    sum -= self[[ind_perm]]
            result[[ind]] = sum / sym_group.order()
        return result


#******************************************************************************

class CompFullySym(CompWithSym):
    r"""
    Class for storing fully symmetric components with respect to a given 
    "frame"`.
    
    The "frame" can be a basis of some vector space or a vector frame on some 
    manifold (i.e. a field of bases). 
    The stored quantities can be tensor components or non-tensorial quantities.
    
    INPUT:

    - ``ring`` -- ring in which each component takes its value
    - ``frame`` -- frame with respect to which the components are defined; 
      whatever type ``frame`` is, it should have some method ``__len__()``
      implemented, so that ``len(frame)`` returns the dimension, i.e. the size
      of a single index range
    - ``nb_indices`` -- number of indices labeling the components
    - ``start_index`` -- (default: 0) first value of a single index; 
      accordingly a component index i must obey
      ``start_index <= i <= start_index + dim - 1``, where ``dim = len(frame)``. 
    - ``output_formatter`` -- (default: None) 2-argument function or unbound 
      method called to format the output of the component access 
      operator ``[...]`` (method __getitem__); the 1st argument of 
      ``output_formatter`` must be an instance of ``ring``, and the second some 
      format.
      
    """
    def __init__(self, ring, frame, nb_indices, start_index=0, 
                 output_formatter=None):
        CompWithSym.__init__(self, ring, frame, nb_indices, start_index,
                             output_formatter, sym=range(nb_indices))

    def _repr_(self):
        r"""
        String representation of the object.
        """
        return "fully symmetric " + str(self.nid) + "-indices" + \
              " components w.r.t. " + str(self.frame)
    
    def _new_instance(self):
        r"""
        Creates a :class:`CompFullySym` instance w.r.t. the same frame,
        and with the same number of indices.
        
        """
        return CompFullySym(self.ring, self.frame, self.nid, self.sindex, 
                            self.output_formatter)

    def __getitem__(self, args):
        r"""
        Returns the component corresponding to the given indices.

        INPUT:
        
        - ``args`` -- list of indices (possibly a single integer if
          self is a 1-index object) or the character ``:`` for the full list
          of components.
          
        OUTPUT:
        
        - the component corresponding to ``args`` or, if ``args`` = ``:``,
          the full list of components, in the form ``T[i][j]...`` for the components
          `T_{ij...}` (for a 2-indices object, a matrix is returned).
    
        """
        no_format = self.output_formatter is None
        format_type = None # default value, possibly redefined below
        if isinstance(args, list):  # case of [[...]] syntax
            no_format = True
            if isinstance(args[0], slice):
                indices = args[0]
            elif isinstance(args[0], tuple): # to ensure equivalence between
                indices = args[0]           # [[(i,j,...)]] and [[i,j,...]]
            else:
                indices = tuple(args)
        else:
            # Determining from the input the list of indices and the format
            if isinstance(args, (int, Integer)) or isinstance(args, slice):
                indices = args
            elif isinstance(args[0], slice):
                indices = args[0]
                format_type = args[1]
            elif len(args) == self.nid:
                indices = args
            else:
                format_type = args[-1]
                indices = args[:-1]
        if isinstance(indices, slice):
            return self._get_list(indices, no_format, format_type)
        else:
            ind = self._ordered_indices(indices)[1]  # [0]=sign is not used
            if ind in self._comp: # non zero value
                if no_format:
                    return self._comp[ind]
                else:
                    return self._comp[ind].output_formatter(self._comp[ind], 
                                                            format_type)
            else: # the value is zero
                if no_format:
                    return self.ring.zero_element()
                else:
                    return self.output_formatter(self.ring.zero_element(), 
                                                 format_type) 

    def __setitem__(self, indices, value):
        r"""
        Sets the component corresponding to the given indices.

        INPUT:
        
        - ``indices`` -- list of indices (possibly a single integer if
          self is a 1-index object) ; if [:] is provided, all the components 
          are set. 
        - ``value`` -- the value to be set or a list of values if ``args``
          == ``[:]``
    
        """
        if isinstance(indices, slice):
            self._set_list(indices, value)
        else:
            if isinstance(indices, list):    
            # to ensure equivalence between [i,j,...] and [[i,j,...]] or 
            # [[(i,j,...)]]
                if isinstance(indices[0], tuple):
                    indices = indices[0]
                else:
                    indices = tuple(indices)
            ind = self._ordered_indices(indices)[1]  # [0]=sign is not used
            if value == 0:
                if ind in self._comp:
                    del self._comp[ind]  # zero values are not stored
            else:
                self._comp[ind] = self.ring(value)


    def __add__(self, other):
        r"""
        Component addition. 
        
        INPUT:
        
        - ``other`` -- components of the same number of indices and defined
          on the same frame as ``self``
        
        OUTPUT:
        
        - components resulting from the addition of ``self`` and ``other``
        
        """
        if other == 0:
            return +self
        if not isinstance(other, Components):
            raise TypeError("The second argument for the addition must be a " + 
                            "an instance of Components.")
        if isinstance(other, CompFullySym):
            if other.frame != self.frame:
                raise TypeError("The two sets of components are not defined " +
                                "on the same vector frame.")
            if other.nid != self.nid:
                raise TypeError("The two sets of components do not have the " + 
                                "same number of indices.")
            if other.sindex != self.sindex:
                raise TypeError("The two sets of components do not have the " + 
                                "same starting index.")
            result = self.copy()
            for ind, val in other._comp.items():
                result[[ind]] += val
            return result
        else:
            return CompWithSym.__add__(self, other)


#******************************************************************************

class CompFullyAntiSym(CompWithSym):
    r"""
    Class for storing fully antisymmetric components with respect to a given 
    "frame"`.
    
    The "frame" can be a basis of some vector space or a vector frame on some 
    manifold (i.e. a field of bases). 
    The stored quantities can be tensor components or non-tensorial quantities.
    
    INPUT:

    - ``ring`` -- ring in which each component takes its value
    - ``frame`` -- frame with respect to which the components are defined; 
      whatever type ``frame`` is, it should have some method ``__len__()``
      implemented, so that ``len(frame)`` returns the dimension, i.e. the size
      of a single index range
    - ``nb_indices`` -- number of indices labeling the components
    - ``start_index`` -- (default: 0) first value of a single index; 
      accordingly a component index i must obey
      ``start_index <= i <= start_index + dim - 1``, where ``dim = len(frame)``. 
    - ``output_formatter`` -- (default: None) 2-argument function or unbound 
      method called to format the output of the component access 
      operator ``[...]`` (method __getitem__); the 1st argument of 
      ``output_formatter`` must be an instance of ``ring``, and the second some 
      format.
      
    """
    def __init__(self, ring, frame, nb_indices, start_index=0, 
                 output_formatter=None):
        CompWithSym.__init__(self, ring, frame, nb_indices, start_index,
                             output_formatter, antisym=range(nb_indices))

    def _repr_(self):
        r"""
        String representation of the object.
        """
        return "fully antisymmetric " + str(self.nid) + "-indices" + \
               " components w.r.t. " + str(self.frame)
    
    def _new_instance(self):
        r"""
        Creates a :class:`CompFullyAntiSym` instance w.r.t. the same frame,
        and with the same number of indices.
        
        """
        return CompFullyAntiSym(self.ring, self.frame, self.nid, self.sindex, 
                                self.output_formatter)


    def __add__(self, other):
        r"""
        Component addition. 
        
        INPUT:
        
        - ``other`` -- components of the same number of indices and defined
          on the same frame as ``self``
        
        OUTPUT:
        
        - components resulting from the addition of ``self`` and ``other``
        
        """
        if other == 0:
            return +self
        if not isinstance(other, Components):
            raise TypeError("The second argument for the addition must be a " + 
                            "an instance of Components.")
        if isinstance(other, CompFullyAntiSym):
            if other.frame != self.frame:
                raise TypeError("The two sets of components are not defined " +
                                "on the same vector frame.")
            if other.nid != self.nid:
                raise TypeError("The two sets of components do not have the " + 
                                "same number of indices.")
            if other.sindex != self.sindex:
                raise TypeError("The two sets of components do not have the " + 
                                "same starting index.")
            result = self.copy()
            for ind, val in other._comp.items():
                result[[ind]] += val
            return result
        else:
            return CompWithSym.__add__(self, other)

            
#******************************************************************************

class KroneckerDelta(CompFullySym):
    r"""
    Kronecker delta `\delta_{ij}`.
            
    INPUT:

    - ``ring`` -- ring in which each component takes its value
    - ``frame`` -- frame with respect to which the components are defined; 
      whatever type ``frame`` is, it should have some method ``__len__()``
      implemented, so that ``len(frame)`` returns the dimension, i.e. the size
      of a single index range
    - ``start_index`` -- (default: 0) first value of a single index; 
      accordingly a component index i must obey
      ``start_index <= i <= start_index + dim - 1``, where ``dim = len(frame)``. 

    EXAMPLES:

    The Kronecker delta on a 3-dimensional manifold::
        
        
    One can read, but not set, the components of a Kronecker delta::
    

    """
    def __init__(self, frame):
        CompFullySym.__init__(self, frame, 2)
        from scalarfield import ScalarField
        chart = self.domain.def_chart
        for i in self.manifold.irange():
            self._comp[(i,i)] = ScalarField(self.domain, 1, chart)

    def _repr_(self):
        r"""
        String representation of the object.
        """
        n = str(self.manifold.dim)
        return "Kronecker delta of size " + n + "x" + n  
    
    def __setitem__(self, args, value):
        r"""
        Should not be used (the components of a Kronecker delta are constant)
        """
        raise NotImplementedError("The components of a Kronecker delta " + 
                                  "cannot be changed.")
