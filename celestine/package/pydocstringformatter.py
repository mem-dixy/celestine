"""A tool to automatically format Python docstrings.

It tries to follow. recommendations from PEP 8 and PEP 257.
"""

from celestine.typed import MT

from . import Package as Package_


class Package(Package_):
    """"""

    def argument(self) -> list[str]:
        """"""
        return [
            "--beginning-quotes",
            "--capitalize-first-letter",
            "--closing-quotes",
            "--exclude = unicode.py",
            "--final-period",
            "--linewrap-full-docstring",
            "--max-summary-lines 1",
            "--max-line-length 72",
            "--no-numpydoc-name-type-spacing",
            "--no-numpydoc-section-hyphen-length",
            "--no-numpydoc-section-order",
            "--no-numpydoc-section-spacing",
            "--quotes-type",
            "--split-summary-body",
            "--strip-whitespaces",
            "--style pep257",
            "--write",
        ]

    def main(self, package: MT) -> None:
        """"""
        package.run_docstring_formatter()

    def name(self) -> str:
        """"""
        return "pydocstringformatter"
