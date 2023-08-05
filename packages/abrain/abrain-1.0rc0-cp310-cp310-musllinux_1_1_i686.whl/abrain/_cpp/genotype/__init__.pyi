"""Docstring for genotype submodule"""
from __future__ import annotations
import _cpp.genotype
import typing

__all__ = [
    "CPPNData"
]


class CPPNData():
    """
    C++ supporting type for genomic data
    """
    class Link():
        """
        From-to relationship between two computational node
        """
        def __init__(self, arg0: int, arg1: int, arg2: int, arg3: float) -> None: ...
        def __repr__(self) -> str: ...
        @property
        def dst(self) -> int:
            """
            ID of the destination node

            :type: int
            """
        @dst.setter
        def dst(self, arg0: int) -> None:
            """
            ID of the destination node
            """
        @property
        def id(self) -> int:
            """
            Numerical identifier

            :type: int
            """
        @id.setter
        def id(self, arg0: int) -> None:
            """
            Numerical identifier
            """
        @property
        def src(self) -> int:
            """
            ID of the source node

            :type: int
            """
        @src.setter
        def src(self, arg0: int) -> None:
            """
            ID of the source node
            """
        @property
        def weight(self) -> float:
            """
            Connection weight

            :type: float
            """
        @weight.setter
        def weight(self, arg0: float) -> None:
            """
            Connection weight
            """
        pass
    class Links():
        """
        Collection of Links
        """
        def __bool__(self) -> bool: 
            """
            Check whether the list is nonempty
            """
        @typing.overload
        def __delitem__(self, arg0: int) -> None: 
            """
            Delete the list elements at index ``i``

            Delete list elements using a slice object
            """
        @typing.overload
        def __delitem__(self, arg0: slice) -> None: ...
        @typing.overload
        def __getitem__(self, arg0: int) -> CPPNData.Link: 
            """
            Retrieve list elements using a slice object
            """
        @typing.overload
        def __getitem__(self, s: slice) -> CPPNData.Links: ...
        @typing.overload
        def __init__(self) -> None: 
            """
            Copy constructor
            """
        @typing.overload
        def __init__(self, arg0: CPPNData.Links) -> None: ...
        @typing.overload
        def __init__(self, arg0: typing.Iterable) -> None: ...
        def __iter__(self) -> typing.Iterator: ...
        def __len__(self) -> int: ...
        @typing.overload
        def __setitem__(self, arg0: int, arg1: CPPNData.Link) -> None: 
            """
            Assign list elements using a slice object
            """
        @typing.overload
        def __setitem__(self, arg0: slice, arg1: CPPNData.Links) -> None: ...
        def append(self, x: CPPNData.Link) -> None: 
            """
            Add an item to the end of the list
            """
        def clear(self) -> None: 
            """
            Clear the contents
            """
        @typing.overload
        def extend(self, L: CPPNData.Links) -> None: 
            """
            Extend the list by appending all the items in the given list

            Extend the list by appending all the items in the given list
            """
        @typing.overload
        def extend(self, L: typing.Iterable) -> None: ...
        def insert(self, i: int, x: CPPNData.Link) -> None: 
            """
            Insert an item at a given position.
            """
        @typing.overload
        def pop(self) -> CPPNData.Link: 
            """
            Remove and return the last item

            Remove and return the item at index ``i``
            """
        @typing.overload
        def pop(self, i: int) -> CPPNData.Link: ...
        pass
    class Node():
        """
        Computational node of a CPPN
        """
        def __init__(self, arg0: int, arg1: str) -> None: ...
        def __repr__(self) -> str: ...
        @property
        def func(self) -> str:
            """
            Function used to compute

            :type: str
            """
        @func.setter
        def func(self, arg0: str) -> None:
            """
            Function used to compute
            """
        @property
        def id(self) -> int:
            """
            Numerical identifier

            :type: int
            """
        @id.setter
        def id(self, arg0: int) -> None:
            """
            Numerical identifier
            """
        pass
    class Nodes():
        """
        Collection of Nodes
        """
        def __bool__(self) -> bool: 
            """
            Check whether the list is nonempty
            """
        @typing.overload
        def __delitem__(self, arg0: int) -> None: 
            """
            Delete the list elements at index ``i``

            Delete list elements using a slice object
            """
        @typing.overload
        def __delitem__(self, arg0: slice) -> None: ...
        @typing.overload
        def __getitem__(self, arg0: int) -> CPPNData.Node: 
            """
            Retrieve list elements using a slice object
            """
        @typing.overload
        def __getitem__(self, s: slice) -> CPPNData.Nodes: ...
        @typing.overload
        def __init__(self) -> None: 
            """
            Copy constructor
            """
        @typing.overload
        def __init__(self, arg0: CPPNData.Nodes) -> None: ...
        @typing.overload
        def __init__(self, arg0: typing.Iterable) -> None: ...
        def __iter__(self) -> typing.Iterator: ...
        def __len__(self) -> int: ...
        @typing.overload
        def __setitem__(self, arg0: int, arg1: CPPNData.Node) -> None: 
            """
            Assign list elements using a slice object
            """
        @typing.overload
        def __setitem__(self, arg0: slice, arg1: CPPNData.Nodes) -> None: ...
        def append(self, x: CPPNData.Node) -> None: 
            """
            Add an item to the end of the list
            """
        def clear(self) -> None: 
            """
            Clear the contents
            """
        @typing.overload
        def extend(self, L: CPPNData.Nodes) -> None: 
            """
            Extend the list by appending all the items in the given list

            Extend the list by appending all the items in the given list
            """
        @typing.overload
        def extend(self, L: typing.Iterable) -> None: ...
        def insert(self, i: int, x: CPPNData.Node) -> None: 
            """
            Insert an item at a given position.
            """
        @typing.overload
        def pop(self) -> CPPNData.Node: 
            """
            Remove and return the last item

            Remove and return the item at index ``i``
            """
        @typing.overload
        def pop(self, i: int) -> CPPNData.Node: ...
        pass
    def __init__(self) -> None: ...
    @property
    def links(self) -> CPPNData.Links:
        """
        The collection of inter-node relationships

        :type: CPPNData.Links
        """
    @links.setter
    def links(self, arg0: CPPNData.Links) -> None:
        """
        The collection of inter-node relationships
        """
    @property
    def nextLinkID(self) -> int:
        """
        ID for the next random link (monotonic

        :type: int
        """
    @nextLinkID.setter
    def nextLinkID(self, arg0: int) -> None:
        """
        ID for the next random link (monotonic
        """
    @property
    def nextNodeID(self) -> int:
        """
        ID for the next random node (monotonic)

        :type: int
        """
    @nextNodeID.setter
    def nextNodeID(self, arg0: int) -> None:
        """
        ID for the next random node (monotonic)
        """
    @property
    def nodes(self) -> CPPNData.Nodes:
        """
        The collection of computing nodes

        :type: CPPNData.Nodes
        """
    @nodes.setter
    def nodes(self, arg0: CPPNData.Nodes) -> None:
        """
        The collection of computing nodes
        """
    INPUTS = 8
    OUTPUTS = 3
    _docstrings = {'INPUTS': 'Number of inputs for the CPPN', 'OUTPUTS': 'Number of outputs for the CPPN'}
    pass
