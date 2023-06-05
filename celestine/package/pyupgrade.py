"""Removes unused imports and unused variables."""


from celestine.load import directory
from celestine.typed import (
    MT,
    L,
    N,
    S,
)

from . import Package as Package_


class Package(Package_):
    """"""

    def main(self, package: MT, path: S) -> N:
        """
        This package has no configuration file options.

        Since no way to configure exclude files, we do it ourself.
        """
        files = directory.python(path, [], ["unicode"])

        file = map(str, files)
        argv = [*file, "--py311-plus"]
        package.main(argv)

    def module(self) -> L[S]:
        """"""
        return ["_main"]
