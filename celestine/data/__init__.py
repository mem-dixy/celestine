""""""

from enum import Enum

from celestine.interface import View
from celestine.typed import (
    C,
    N,
    R,
)


class State(Enum):
    """"""

    CODE = 1
    VIEW = 2


def main(function: C[[View], N]) -> C[[View], N]:
    """"""

    def decorator(view: View) -> N:
        function(view)

    return decorator


def scene(function: C[[View], N]) -> C[[View], N]:
    """"""

    def decorator(view: View) -> N:
        function(view)

    return decorator


def code(function: C[[View], N]) -> C[[View], N]:
    """"""

    def decorator(**star: R) -> N:
        function(**star)

    return decorator
