""""""

from typing import override
from typing import Type as TYPE
from typing import Tuple as T
from typing import Self as K
from typing import Optional as O
from typing import List as L
from typing import Dict as D
from collections.abc import Generator as G
from collections.abc import Callable as C
import typing
import pathlib
import lzma
import io
import collections.abc
import importlib.abc
import importlib.machinery
import sys
import types


""""""


type Argument = typing.Any  # Import the real one.

type A = typing.Any
type B = bool
# type C = collections.abc.Callable
# type D = typing.Dict
type E = typing.Any  # Unused.  # ENUM?
type F = float
# Generator[YieldType, SendType, ReturnType]
# type G = collections.abc.Generator
type H = typing.Any  # Unused
type I = int
type J = object
# type K = typing.Self
# type L = typing.List
type M = types.ModuleType
type N = None
# type O = typing.Optional
type P = pathlib.Path
type Q = typing.Any  # Unused.  # Queue?
type R = typing.Any  # **star
type S = str
# type T = typing.Tuple
type U = typing.Any  # Unused.
type V = typing.Any  # Unused.
type W = typing.Any  # Unused.
type X = typing.Any  # Unused.
type Y = typing.Any  # Unused.
type Z = typing.Any  # Unused.

type GB = G[B, N, N]
type GF = G[F, N, N]
type GI = G[I, N, N]
type GP = G[P, N, N]
type GS = G[S, N, N]

type OB = O[B]
type OF = O[F]
type OI = O[I]
type OP = O[P]
type OS = O[S]

type LB = L[B]
type LF = L[F]
type LI = L[I]
type LP = L[P]
type LS = L[S]

type PATH = P | S

type FN = C[[N], N]
type AXIS = G[T[I, I], N, N]
type FILE = typing.IO[A]
type AT = D[S, A]
# type TYPE[X] = typing.Type
type IMAGE = A
type APD = D[A, A]
type LZMA = lzma.LZMAFile
type TABLE = D[S, S]
type BOX = T[I, I, I, I]
type PAIR = T[I, I]
type AD = D[S, Argument]  # session.argument
type AI = collections.abc.Iterable[T[S, Argument]]  # session.argument


def string(*characters: S) -> S:
    """"""
    buffer = io.StringIO()
    for character in characters:
        buffer.write(character)
    value = buffer.getvalue()
    return value


class Star(typing.TypedDict):
    """"""


class Fix:
    """"""

    def override(self) -> N:
        """"""


class ImportNotUsed(Fix):
    """"""

    @override
    def override(self) -> N:
        print(override)

    def self(self) -> K:
        """"""
        return self

    @staticmethod
    def type_() -> TYPE[int]:
        """"""
        return int


class DependencyInjectorLoader(importlib.abc.Loader):
    """"""

    _COMMON_PREFIX = "myapp.virtual."

    def __init__(self):
        self._services = {}
        # create a dummy module to return when Python attempts to import
        # myapp and myapp.virtual, the :-1 removes the last "." for
        # aesthetic reasons :)
        self._dummy_module = types.ModuleType(self._COMMON_PREFIX[:-1])
        # set __path__ so Python believes our dummy module is a package
        # this is important, since otherwise Python will believe our
        # dummy module can have no submodules
        self._dummy_module.__path__ = []

    def _truncate_name(self, fullname):
        """Strip off _COMMON_PREFIX from the given module name
        Convenience method when checking if a service is provided.
        """
        return fullname[len(self._COMMON_PREFIX):]

    def provide(self, service_name, module):
        """"""
        self._services[service_name] = module

    def provides(self, fullname):
        """"""
        if self._truncate_name(fullname) in self._services:
            return True

        # this checks if we should return the dummy module,
        # since this evaluates to True when importing myapp and
        # myapp.virtual
        return self._COMMON_PREFIX.startswith(fullname)

    def create_module(self, spec):
        """"""
        service_name = self._truncate_name(spec.name)
        if service_name not in self._services:
            # return our dummy module since at this point we're loading
            # *something* along the lines of "myapp.virtual" that's not
            # a service
            return self._dummy_module
        module = self._services[service_name]
        return module

    def exec_module(self, module):
        """Execute the given module in its own namespace
        This method is required to be present by importlib.abc.Loader,
        but since we know our module object is already fully-formed,
        this method merely no-ops.
        """


type SO = typing.Sequence[str] | None
type OM = types.ModuleType | None
type MS = importlib.machinery.ModuleSpec | None


class MetaPathFinder(importlib.abc.MetaPathFinder):
    """"""

    def __init__(self):
        loader = DependencyInjectorLoader()
        loader.provide("frontend", FrontendModule())

        self._loader = loader

    @override
    def find_spec(self, fullname: S, path: SO, target: OM = None) -> MS:
        """"""
        name = fullname
        loader = self._loader
        print("spec", fullname, path, target)
        if self._loader.provides(fullname):
            return importlib.machinery.ModuleSpec(name, loader)
        return None


class FrontendModule:
    """"""

    class Popup:
        """"""

        def __init__(self, message):
            self._message = message

        def display(self):
            """"""
            print("Popup:", self._message)


if __name__ == "__main__":

    sys.meta_path.insert(0, MetaPathFinder())

    # note that these last three lines could exist in any other
    # source file,
    # as long as injector.install() was called somewhere first

    import tkinter

    import myapp.virtual.frontend as frontend

    popup = frontend.Popup("Hello World!")
    popup.display()
