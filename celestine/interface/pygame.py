""""""

from celestine import load
from celestine.interface import Abstract as Abstract_
from celestine.interface import Button as Button_
from celestine.interface import Image as Image_
from celestine.interface import Label as Label_
from celestine.interface import View as View_
from celestine.interface import Window as Window_
from celestine.typed import (
    LS,
    A,
    H,
    N,
    P,
    R,
    override,
)
from celestine.window.collection import (
    Plane,
    Point,
)
from celestine.window.container import Image as Mode


class Abstract(Abstract_):
    """"""

    def render(self, keep):
        """"""
        origin = (self.area.one.minimum, self.area.two.minimum)
        self.canvas.blit(keep, origin)


class Button(Abstract, Button_):
    """"""

    def draw(self, *, font, **star: R) -> N:
        """"""

        text = f"Button{self.data}"

        keep = font.render(text, True, (255, 255, 255))
        self.render(keep)


class Label(Abstract, Label_):
    """"""

    def draw(self, *, font, **star: R) -> N:
        """"""

        keep = font.render(self.data, True, (255, 255, 255))
        self.render(keep)


class Image(Abstract, Image_):
    """"""

    def make(self) -> N:
        """"""
        pillow = self.hold.package.pillow

        self.image = pillow.new(self.area.size.int)

    @override
    def update(self, path: P, **star: R) -> N:
        """"""
        pillow = self.hold.package.pillow

        self.path = path

        image = pillow.open(self.path)

        curent = Plane.make(image.image.width, image.image.height)
        target = Plane.make(*self.area.size.int)

        match self.mode:
            case Mode.FILL:
                result = curent.scale_to_min(target)
            case Mode.FULL:
                result = curent.scale_to_max(target)

        result.center(target)

        image.resize(result.size)
        self.image.paste(image, result)

    def draw(self, *, font, **star: R) -> N:
        """"""
        pygame = self.hold.package.pygame

        image = pygame.image.fromstring(
            self.image.image.tobytes(),
            self.image.image.size,
            self.image.image.mode,
        )

        self.render(image)


class View(Abstract, View_):
    """"""
    @override
    def hide(self) -> N:
        """"""
        super().hide()


    @override
    def show(self) -> N:
        """"""
        super().show()



class Window(Abstract, Window_):
    """"""

    @override
    def make(self, canvas: A) -> N:
        """"""
        pygame = self.hold.package.pygame

        canvas = pygame.display.set_mode(self.area.size.int)
        super().make(canvas)

    @override
    def draw(self, **star: R) -> N:
        """"""
        pygame = self.hold.package.pygame

        self.canvas.fill((0, 0, 0))

        super().draw(font=self.font, **star)

        pygame.display.flip()

    @override
    def extension(self) -> LS:
        return [
            ".bmp",
            ".sgi",
            ".rgb",
            ".bw",
            ".png",
            ".jpg",
            ".jpeg",
            ".jp2",
            ".j2c",
            ".tga",
            ".cin",
            ".dpx",
            ".exr",
            ".hdr",
            ".tif",
            ".tiff",
            ".webp",
            ".pbm",
            ".pgm",
            ".ppm",
            ".pnm",
            ".gif",
            ".png",
        ]

    @override
    def __enter__(self):
        super().__enter__()

        pygame = self.hold.package.pygame

        def set_caption():
            caption = self.hold.language.APPLICATION_TITLE
            pygame.display.set_caption(caption)

        def set_font():
            pygame.font.init()
            file_path = load.asset("cascadia_code_regular.otf")
            size = 40
            self.font = pygame.font.Font(file_path, size)

        set_caption()
        set_font()

        return self

    @override
    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

        pygame = self.hold.package.pygame

        def set_icon():
            path = "icon.png"
            asset = load.asset(path)
            image = pygame.image.load(asset)
            icon = image.convert_alpha()
            pygame.display.set_icon(icon)

        set_icon()

        while True:
            self.hold.dequeue()
            event = pygame.event.wait()
            match event.type:
                case pygame.QUIT:
                    break
                case pygame.MOUSEBUTTONDOWN:
                    # TODO: This triggers on all mouse buttons
                    # including scroll wheel! That is bad.

                    self.click(Point(*pygame.mouse.get_pos()))

        pygame.quit()
        return False

    @override
    def __init__(self, hold: H, **star: R) -> N:
        element = {
            "button": Button,
            "image": Image,
            "label": Label,
            "view": View,
            "window": Window,
        }
        super().__init__(hold, element, **star)
        self.area = Plane.make(1280, 960)
        self.font = None
