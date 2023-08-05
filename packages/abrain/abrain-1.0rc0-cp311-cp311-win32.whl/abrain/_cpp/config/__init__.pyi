"""Docstring for config submodule"""
from __future__ import annotations
import _cpp.config
import typing

__all__ = [
    "Config",
    "FBounds",
    "MutationRates",
    "Strings"
]


class Config():
    """
    C++/Python configuration values for the ABrain library
    """
    @staticmethod
    def known_function(name: str) -> bool: 
        """
        Whether the requested function name is a built-in
        """
    _docstrings = {'activationFunc': 'The activation function used by all hidden/output neurons (inputs are passthrough)', 'annWeightsRange': 'Scaling factor `s` for the CPPN `w` output mapping :math:`[-1,1] \to [-s,s]`', 'bndThr': 'Minimal divergence threshold for discovering neurons', 'cppnInputNames': '``const`` Auto generated name of the CPPN inputs (based on dimensions and optional use of the connection length)', 'cppnOutputNames': '``const`` Auto generated name of the CPPN outputs', 'cppnWeightBounds': "Initial and maximal bounds for each of the CPPN's weights", 'divThr': 'Division threshold for a quad-/octtree cell/cube', 'functionSet': 'List of functions accessible to nodes via creation/mutation', 'initialDepth': 'Initial division depth for the underlying quad-/octtree', 'iterations': 'Maximal number of discovery steps for Hidden/Hidden connections. Can stop early in case of convergence (no new neurons discovered)', 'maxDepth': 'Maximal division depth for the underlying quad-/octtree', 'mutationRates': 'Probabilities for each point mutation (addition/deletion/alteration)\n\nGlossary:\n  - add_l: add a random link between two nodes (feedforward only)\n  - add_n: replace a link by creating a node\n  - del_l: delete a random link (never leaves unconnected nodes)\n  - del_n: replace a simple node by a direct link\n  - mut_f: change the function of a node\n  - mut_w: change the connection weight of a link\n\n', 'outputFunctions': 'Functions used for the CPPN output (same length as :attr:`cppnOutputNames`)', 'varThr': 'Variance threshold for exploring a quad-/octtree cell/cube'}
    _sections: dict # value = {'ANN': Strings[annWeightsRange, activationFunc], 'CPPN': Strings[functionSet, outputFunctions, mutationRates, cppnWeightBounds], 'ESHN': Strings[initialDepth, maxDepth, iterations, divThr, varThr, bndThr]}
    activationFunc = 'ssgn'
    annWeightsRange = 3.0
    bndThr = 0.15000000596046448
    cppnInputNames: _cpp.config.Strings # value = Strings[x_0, y_0, z_0, x_1, y_1, z_1, l, b]
    cppnOutputNames: _cpp.config.Strings # value = Strings[w, l, b]
    cppnWeightBounds: _cpp.config.FBounds # value = Bounds(-3, -1, 1, 3, 0.01)
    divThr = 0.30000001192092896
    functionSet: _cpp.config.Strings # value = Strings[abs, gaus, id, bsgm, sin, step]
    initialDepth = 2
    iterations = 10
    maxDepth = 3
    mutationRates: _cpp.config.MutationRates # value = MutationRates{add_l: 0.0681818, add_n: 0.0454545, del_l: 0.0909091, del_n: 0.0681818, mut_f: 0.227273, mut_w: 0.5}
    outputFunctions: _cpp.config.Strings # value = Strings[bsgm, step, id]
    varThr = 0.30000001192092896
    pass
class FBounds():
    def __eq__(self, arg0: FBounds) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: float) -> None: ...
    def __repr__(self) -> str: ...
    @staticmethod
    def ccpParseString(arg0: str) -> FBounds: 
        """
        Try to parse the provided string into a mutation bounds object
        """
    @staticmethod
    def isValid(arg0: FBounds) -> bool: 
        """
        Whether this is a valid mutation bounds object
        """
    @property
    def max(self) -> float:
        """
        :type: float
        """
    @max.setter
    def max(self, arg0: float) -> None:
        pass
    @property
    def min(self) -> float:
        """
        :type: float
        """
    @min.setter
    def min(self, arg0: float) -> None:
        pass
    @property
    def rndMax(self) -> float:
        """
        :type: float
        """
    @rndMax.setter
    def rndMax(self, arg0: float) -> None:
        pass
    @property
    def rndMin(self) -> float:
        """
        :type: float
        """
    @rndMin.setter
    def rndMin(self, arg0: float) -> None:
        pass
    @property
    def stddev(self) -> float:
        """
        :type: float
        """
    @stddev.setter
    def stddev(self, arg0: float) -> None:
        pass
    __hash__ = None
    pass
class MutationRates():
    def __bool__(self) -> bool: 
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: object) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: str) -> bool: ...
    def __delitem__(self, arg0: str) -> None: ...
    def __getitem__(self, arg0: str) -> float: ...
    def __init__(self) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: 
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: str, arg1: float) -> None: ...
    @staticmethod
    def ccpParseString(arg0: str) -> MutationRates: 
        """
        Try to parse the provided string into a dictionary of mutation rates
        """
    @staticmethod
    def isValid(arg0: MutationRates) -> bool: 
        """
        Whether this is a valid dictionary of mutation rates
        """
    def items(self) -> typing.ItemsView[str, float]: ...
    def keys(self) -> typing.KeysView[str]: ...
    def values(self) -> typing.ValuesView[float]: ...
    pass
class Strings():
    def __bool__(self) -> bool: 
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: str) -> bool: 
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None: 
        """
        Delete the list elements at index ``i``

        Delete list elements using a slice object
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None: ...
    def __eq__(self, arg0: Strings) -> bool: ...
    @typing.overload
    def __getitem__(self, arg0: int) -> str: 
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, s: slice) -> Strings: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: Strings) -> None: ...
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, arg0: Strings) -> bool: ...
    def __repr__(self) -> str: 
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: str) -> None: 
        """
        Assign list elements using a slice object
        """
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: Strings) -> None: ...
    def append(self, x: str) -> None: 
        """
        Add an item to the end of the list
        """
    @staticmethod
    def ccpParseString(arg0: str) -> Strings: 
        """
        Try to parse the provided string into a strings collection
        """
    def clear(self) -> None: 
        """
        Clear the contents
        """
    def count(self, x: str) -> int: 
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: Strings) -> None: 
        """
        Extend the list by appending all the items in the given list

        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None: ...
    def insert(self, i: int, x: str) -> None: 
        """
        Insert an item at a given position.
        """
    @staticmethod
    def isValid(arg0: Strings) -> bool: 
        """
        Whether this is a valid strings colleciton (not empty)
        """
    @typing.overload
    def pop(self) -> str: 
        """
        Remove and return the last item

        Remove and return the item at index ``i``
        """
    @typing.overload
    def pop(self, i: int) -> str: ...
    def remove(self, x: str) -> None: 
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    __hash__ = None
    pass
