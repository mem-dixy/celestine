"""The View page."""


from celestine.data import (
    main,
    scene,
)
from celestine.typed import N
from celestine.window.element import View


@main
def trans(view: View) -> N:
    """"""
    with view.zone("main") as line:
        line.new(
            "main_A",
            text=view.hold.language.TRANSLATOR_MAIN_BUTTON,
            code="translate",
        )


# TODO: Add report functionality back in, and make it better.
@scene
def report(view: View) -> N:
    """"""
    with view.zone("head") as line:
        line.new("title", text="Page main")
    train = {}

    line.new(
        "main_action",
        text=view.hold.language.TRANSLATOR_REPORT_BUTTON,
        code="train",
        page=view.hold,
    )

    for tag, text in train.items():
        with view.zone("body") as line:
            line.new(tag, text=text)
