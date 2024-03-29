""""""


from celestine import load
from celestine.data.directory import (
    APPLICATION,
    DIRECTORY,
    INTERFACE,
    LANGUAGE,
    WHALE,
)
from celestine.session.argument import (
    Customization,
    InformationConfiguration,
    InformationHelp,
    InformationVersion,
    Optional,
    Positional,
)
from celestine.session.data import (
    Actions,
    Values,
)
from celestine.typed import (
    AD,
    AI,
    M,
    S,
)
from celestine.unicode import NONE

from . import default


class SuperSession:
    """"""

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return {}

    @classmethod
    def items(cls, core) -> AI:
        """"""
        dictionary = cls.dictionary(core)
        return dictionary.items()


class Information(SuperSession):
    """"""

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            Values.CONFIGURATION: InformationConfiguration(
                core.language.ARGUMENT_HELP_HELP,
            ),
            Actions.HELP: InformationHelp(
                core.language.ARGUMENT_HELP_HELP,
            ),
            Actions.VERSION: InformationVersion(
                core.language.ARGUMENT_VERSION_HELP,
            ),
        }


class Dictionary(SuperSession):
    """"""


class Application(Dictionary):
    """"""

    application: M

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            APPLICATION: Customization(
                default.application(),
                core.language.ARGUMENT_INTERFACE_HELP,
                load.argument(APPLICATION),
            ),
        }


# class Configuration(Dictionary):
#    """"""
#
#    configuration: M
#
#    @classmethod
#    def dictionary(cls, core) -> AD:
#        """"""
#        return super().dictionary(core) | {
#            CONFIGURATION: Customization(
#                default.application(),
#                core.language.ARGUMENT_INTERFACE_HELP,
#                load.argument(APPLICATION),
#            ),
#        }


class Whale(Dictionary):
    """"""

    whale: M

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            WHALE: Optional(
                "",
                "Path to configuration file.",
            ),
        }


class Directory(Dictionary):
    """"""

    directory: M

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            DIRECTORY: Customization(
                default.application(),
                core.language.ARGUMENT_INTERFACE_HELP,
                load.argument(APPLICATION),
            ),
        }


class Interface(Dictionary):
    """"""

    interface: M

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            INTERFACE: Customization(
                default.interface(),
                core.language.ARGUMENT_INTERFACE_HELP,
                load.argument(INTERFACE),
            ),
        }


class Language(Dictionary):
    """"""

    language: M

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            LANGUAGE: Customization(
                default.language(),
                core.language.ARGUMENT_LANGUAGE_HELP,
                load.argument(LANGUAGE),
            ),
        }


class Session(
    Application,
    Whale,
    Directory,
    Interface,
    Language,
):
    """"""

    main: S

    @classmethod
    def dictionary(cls, core) -> AD:
        """"""
        return super().dictionary(core) | {
            Values.MAIN: Positional(
                NONE,
                core.language.ARGUMENT_LANGUAGE_HELP,
                load.function_page(core.application),
            ),
        }
