"""Docstring for phenotype submodule"""
from __future__ import annotations
import _cpp.phenotype
import typing
import _cpp.genotype

__all__ = [
    "ANN",
    "CPPN",
    "Point"
]


class ANN():
    """
    3D Artificial Neural Network produced through Evolvable Substrate Hyper-NEAT
    """
    class IBuffer():
        """
        Specialized, fixed-size buffer for the neural inputs (write-only)
        """
        def __len__(self) -> int: 
            """
            Return the number of expected inputs
            """
        @typing.overload
        def __setitem__(self, arg0: int, arg1: float) -> None: 
            """
            Assign an element
            """
        @typing.overload
        def __setitem__(self, arg0: slice, arg1: typing.Iterable) -> None: ...
        pass
    class Neuron():
        """
        Atomic computational unit of an ANN
        """
        class Link():
            """
            An incoming neural connection
            """
            def src(self) -> ANN.Neuron: 
                """
                Return a reference to the source neuron
                """
            @property
            def weight(self) -> float:
                """
                Connection weight (see attr:`Config.annWeightScale`)

                :type: float
                """
            pass
        class Type():
            """
            Members:

              I : Input (receiving data)

              H : Hidden (processing data)

              O : Output (producing data)
            """
            def __eq__(self, other: object) -> bool: ...
            def __getstate__(self) -> int: ...
            def __hash__(self) -> int: ...
            def __index__(self) -> int: ...
            def __init__(self, value: int) -> None: ...
            def __int__(self) -> int: ...
            def __ne__(self, other: object) -> bool: ...
            def __repr__(self) -> str: ...
            def __setstate__(self, state: int) -> None: ...
            @property
            def name(self) -> str:
                """
                :type: str
                """
            @property
            def value(self) -> int:
                """
                :type: int
                """
            H: _cpp.phenotype.ANN.Neuron.Type # value = <Type.H: 2>
            I: _cpp.phenotype.ANN.Neuron.Type # value = <Type.I: 0>
            O: _cpp.phenotype.ANN.Neuron.Type # value = <Type.O: 1>
            __members__: dict # value = {'I': <Type.I: 0>, 'H': <Type.H: 2>, 'O': <Type.O: 1>}
            pass
        def links(self) -> typing.List[ANN.Neuron.Link]: 
            """
            Return the list of inputs connections
            """
        @property
        def bias(self) -> float:
            """
            Neural bias

            :type: float
            """
        @property
        def depth(self) -> int:
            """
            Depth in the neural network

            :type: int
            """
        @property
        def flags(self) -> int:
            """
            Stimuli-dependent flags (for modularization)

            :type: int
            """
        @property
        def pos(self) -> Point:
            """
            Position in the 3D substrate

            :type: Point
            """
        @property
        def type(self) -> ANN.Neuron.Type:
            """
            Neuron role (see :class:`Type`)

            :type: ANN.Neuron.Type
            """
        @property
        def value(self) -> float:
            """
            Current activation value

            :type: float
            """
        pass
    class Neurons():
        """
        Wrapper for the C++ neurons container
        """
        def __iter__(self) -> typing.Iterator: ...
        def __len__(self) -> int: ...
        pass
    class OBuffer():
        """
        Specialized, fixed-size buffer for the neural outputs (read-only)
        """
        @typing.overload
        def __getitem__(self, arg0: int) -> float: 
            """
            Access an element
            """
        @typing.overload
        def __getitem__(self, arg0: slice) -> list: ...
        def __len__(self) -> int: 
            """
            Return the number of expected outputs
            """
        @property
        def __iter__(self) -> None:
            """
            Cannot be iterated. Use direct access instead.

            :type: None
            """
        pass
    class Stats():
        """
        Contains various statistics about an ANN
        """
        @property
        def axons(self) -> float:
            """
            Total length of the connections

            :type: float
            """
        @property
        def depth(self) -> int:
            """
            Maximal depth of the neural network

            :type: int
            """
        @property
        def edges(self) -> int:
            """
            Number of connections

            :type: int
            """
        pass
    def __call__(self, inputs: ANN.IBuffer, outputs: ANN.OBuffer, substeps: int = 1) -> None: 
        """
        Execute a computational step

        Assigns provided input values to corresponding input neurons in the same order
        as when created (see build). Returns output values as computed.
        If not otherwise specified, a single computational substep is executed. If need
        be (e.g. large network, fast response required) you can requested for multiple
        sequential execution in one call

        :param inputs: provided analog values for the input neurons
        :param outputs: computed analog values for the output neurons
        :param substeps: number of sequential executions

        .. seealso:: :ref:`usage-basics-ann`
                   
        """
    def __init__(self) -> None: ...
    def buffers(self) -> typing.Tuple[ANN.IBuffer, ANN.OBuffer]: 
        """
        Return the ann's I/O buffers as a tuple
        """
    @staticmethod
    def build(inputs: typing.List[Point], outputs: typing.List[Point], genome: _cpp.genotype.CPPNData) -> ANN: 
        """
        Create an ANN via ES-HyperNEAT

        The ANN has inputs/outputs at specified coordinates.
        A CPPN is instantiated from the provided genome and used
        to query connections weight, existence and to discover
        hidden neurons locations

        :param inputs: coordinates of the input neurons on the substrate
        :param outputs: coordinates of the output neurons on the substrate
        :param genome: genome describing a cppn (see :class:`abrain.Genome`,
                                                :class:`CPPN`)

        .. seealso:: :ref:`usage-basics-ann`
                          
        """
    def empty(self) -> bool: 
        """
        Whether the ANN contains neurons/connections
        """
    def ibuffer(self) -> ANN.IBuffer: 
        """
        Return a reference to the neural inputs buffer
        """
    def neuronAt(self, pos: Point) -> ANN.Neuron: 
        """
        Query an individual neuron
        """
    def neurons(self) -> ANN.Neurons: 
        """
        Provide read-only access to the underlying neurons
        """
    def obuffer(self) -> ANN.OBuffer: 
        """
        Return a reference to the neural outputs buffer
        """
    def stats(self) -> ANN.Stats: 
        """
        Return associated stats (connections, depth...)
        """
    pass
class CPPN():
    """
    Middle-man between the descriptive :class:`Genome` and the callable :class:`ANN`
    """
    class Output():
        """
        Members:

          Weight

          LEO

          Bias
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Bias: _cpp.phenotype.CPPN.Output # value = <Output.Bias: 2>
        LEO: _cpp.phenotype.CPPN.Output # value = <Output.LEO: 1>
        Weight: _cpp.phenotype.CPPN.Output # value = <Output.Weight: 0>
        __members__: dict # value = {'Weight': <Output.Weight: 0>, 'LEO': <Output.LEO: 1>, 'Bias': <Output.Bias: 2>}
        pass
    class Outputs():
        """
        Output communication buffer for the CPPN
        """
        def __getitem__(self, arg0: int) -> float: ...
        def __init__(self) -> None: ...
        def __len__(self) -> int: ...
        @property
        def __iter__(self) -> None:
            """
            Cannot be iterated. Use direct access instead.

            :type: None
            """
        pass
    @typing.overload
    def __call__(self, src: Point, dst: Point, buffer: CPPN.Outputs) -> None: 
        """
        Evaluates on provided coordinates and retrieve all outputs

        Evaluates on provided coordinates for the requested output

        .. note: due to an i686 bug this function is unoptimized on said platforms

        Evaluates on provided coordinates for the requested outputs
        """
    @typing.overload
    def __call__(self, src: Point, dst: Point, buffer: CPPN.Outputs, subset: typing.Set[CPPN.Output]) -> None: ...
    @typing.overload
    def __call__(self, src: Point, dst: Point, type: CPPN.Output) -> float: ...
    def __init__(self, arg0: _cpp.genotype.CPPNData) -> None: ...
    @staticmethod
    def functions() -> typing.Dict[str, typing.Callable[[float], float]]: 
        """
        Return a copy of the C++ built-in function set
        """
    @staticmethod
    def outputs() -> CPPN.Outputs: 
        """
        Return a buffer in which the CPPN can store output data
        """
    DIMENSIONS = 3
    INPUTS = 8
    OUTPUTS = 3
    OUTPUTS_LIST: list # value = [<Output.Weight: 0>, <Output.LEO: 1>, <Output.Bias: 2>]
    _docstrings = {'DIMENSIONS': 'for the I/O coordinates', 'INPUTS': 'Number of inputs', 'OUTPUTS': 'Number of outputs', 'OUTPUTS_LIST': 'The list of output types the CPPN can produce'}
    pass
class Point():
    """
    3D coordinate using fixed point notation with 3 decimals
    """
    def __init__(self, x: float, y: float, z: float) -> None: 
        """
        Create a point with the specified coordinates

        Args:
          x, y, z (float): x, y, z coordinate
        """
    def __repr__(self) -> str: ...
    def tuple(self) -> typing.Tuple[float, float, float]: 
        """
        Return a tuple for easy unpacking in python
        """
    pass
