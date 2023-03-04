""""""

from celestine.window.window import Window as master

from . import package
from .container import Container


class Window(master):
    def page(self, name, document):
        page = self.container.drop(name)
        page.frame = package.Frame(
            self.root,
            padx=5,
            pady=5,
            bg="skyblue",
        )
        page.frame.grid(row=0, column=0, sticky="nsew")
        document(page)
        page.draw(page.frame)
        self.item_set(name, page)

    def turn(self, page):
        frame = self.item_get(page)
        frame.frame.tkraise()

    def __enter__(self):
        super().__enter__()
        self.root.title(self.session.language.APPLICATION_TITLE)
        self.root.geometry("1920x1080")
        self.root.minsize(640, 480)
        self.root.maxsize(3840, 2160)
        self.root.config(bg="blue")

        self.container = Container(
            self.session,
            "window",
            self.turn,
            x_min=0,
            y_min=0,
            x_max=640,
            y_max=2160,
            offset_x=0,
            offset_y=0,
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.root.mainloop()
        return False

    def __init__(self, session, **kwargs):
        self.container = None
        super().__init__(session, **kwargs)
        self.root = package.Tk()
