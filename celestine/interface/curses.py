""""""

import io

from celestine import load
from celestine.package import pillow
from celestine.package.curses import package as curses
from celestine.unicode import LINE_FEED
from celestine.unicode.notational_systems import BRAILLE_PATTERNS
from celestine.window.element import Abstract as abstract
from celestine.window.element import Button as button
from celestine.window.element import Image as image
from celestine.window.element import Label as label
from celestine.window.window import Window as window

color_index = 8  # skip the 8 reserved colors
color_table = {}

COLORS = 15


def get_colors(image):
    """Fails after being called 16 times."""

    global color_index
    global color_table

    colors = image.getcolors()
    for color in colors:
        (count, pixel) = color
        (red, green, blue) = pixel

        red *= 1000
        green *= 1000
        blue *= 1000

        red //= 255
        green //= 255
        blue //= 255

        if red >= 920 or green >= 920 or blue >= 920:
            pass
            # print(red, green, blue)
        curses.init_color(color_index, red, green, blue)
        curses.init_pair(color_index, color_index, 0)

        color_table[pixel] = color_index
        color_index += 1


class Abstract(abstract):
    """"""

    def add_string(self, frame, x_dot, y_dot, text, *extra):
        """
        Curses swaps x and y.

        Also minus the window border to get local location.
        """
        frame.addstr(y_dot - 1, x_dot - 1, text, *extra)

    def origin(self):
        """"""
        x_dot = int(self.x_min)
        y_dot = int(self.y_min)
        return (x_dot, y_dot)

    def render(self, collection, item, **star):
        """"""
        text = item
        (x_dot, y_dot) = self.origin()
        self.add_string(collection, x_dot, y_dot, text)


class Button(Abstract, button):
    """"""

    def draw(self, collection, **star):
        """"""
        item = f"button:{self.data}"
        self.render(collection, item, **star)


class Image(Abstract, image):
    """"""

    def output(self):
        width, height = self.cache.size

        pixels = list(self.cache.getdata())
        string = io.StringIO()

        def shift(offset_x, offset_y):
            nonlocal braille
            nonlocal range_x
            nonlocal range_y

            index_x = range_x + offset_x
            index_y = range_y + offset_y

            index = index_y * width + index_x
            pixel = pixels[index] // 255

            braille <<= 1
            braille |= pixel

        for range_y in range(0, height, 4):
            for range_x in range(0, width, 2):
                braille = 0

                shift(0, 0)
                shift(1, 0)
                shift(0, 1)
                shift(1, 1)
                shift(0, 2)
                shift(1, 2)
                shift(0, 3)
                shift(1, 3)

                text = BRAILLE_PATTERNS[braille]
                string.write(text)

            string.write(LINE_FEED)

        value = string.getvalue()
        value = value[0:-1]
        return value.split(LINE_FEED)

    def render(self, collection, item, **star):
        """"""
        (x_dot, y_dot) = self.origin()

        color = list(self.color.getdata())

        index_y = 0
        for row_text in item:
            index_x = 0
            for col_text in row_text:
                width, height = self.color.size
                index = index_y * width + index_x

                (red, green, blue) = color[index]
                table = color_table[(red, green, blue)]
                extra = curses.color_pair(table)

                self.add_string(
                    collection,
                    x_dot + index_x,
                    y_dot + index_y,
                    col_text,
                    extra,
                )

                index_x += 1

            index_y += 1

    def draw(self, collection, **star):
        """"""
        path = self.image or load.asset("null.png")

        self.cache = pillow.Image.load(path)
        self.color = pillow.Image.clone(self.cache)

        # Crop box.
        source_length_x = self.cache.image.width
        source_length_y = self.cache.image.height

        length_x = self.x_max - self.x_min
        length_y = self.y_max - self.y_min

        target_length_x = length_x * 2
        target_length_y = length_y * 4

        source_length = (source_length_x, source_length_y)
        target_length = (target_length_x, target_length_y)

        box = self.crop(source_length, target_length)
        # Done.

        self.color.brightwing()

        self.cache.resize(target_length_x, target_length_y, box)
        self.color.resize(length_x, length_y, box)

        self.color.quantize()

        self.cache.convert_to_mono()
        self.color.convert_to_color()

        get_colors(self.color.image)

        item = self.output()
        self.render(collection, item, **star)


class Label(Abstract, label):
    """"""

    def draw(self, collection, **star):
        """"""
        item = f"label:{self.data}"
        self.render(collection, item, **star)


class Window(window):
    """"""

    def data(self, container):
        """"""
        data_box = (1, 1, self.width - 2, self.height - 2)
        container.data = curses.window(*data_box)

    def draw(self, **star):
        """"""
        # Do normal draw stuff.
        self.data(self.page)

        super().draw(**star)

        self.stdscr.noutrefresh()
        self.background.noutrefresh()
        self.page.data.noutrefresh()
        curses.doupdate()

        # Reset the global color counter.
        global color_index
        global color_table
        color_index = 8
        color_table = {}

    def view(self, name, function):
        """"""
        container = self.container.drop(name)
        self.data(container)
        function(container)
        container.spot(1, 1, self.width - 1, self.height - 1)
        self._view.set(name, container)

    def __enter__(self):
        super().__enter__()

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.start_color()

        self.background = curses.window(0, 0, self.width, self.height)
        self.background.box()

        header_box = (1, 0, self.width - 2, 1)
        header = curses.subwindow(self.background, *header_box)
        header.addstr(self.session.language.APPLICATION_TITLE)

        footer_box = (1, self.height - 1, self.width - 2, 1)
        footer = curses.subwindow(self.background, *footer_box)
        footer.addstr(self.session.language.CURSES_EXIT)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        while True:
            event = self.stdscr.getch()
            match event:
                case 258 | 259 | 260 | 261 as key:
                    match key:
                        case curses.KEY_UP:
                            self.cord_y -= 1
                        case curses.KEY_DOWN:
                            self.cord_y += 1
                        case curses.KEY_LEFT:
                            self.cord_x -= 1
                        case curses.KEY_RIGHT:
                            self.cord_x += 1

                    self.cord_x %= self.width
                    self.cord_y %= self.height
                    self.stdscr.move(self.cord_y, self.cord_x)
                case curses.KEY_EXIT:
                    break
                case curses.KEY_CLICK:
                    self.page.poke(self.cord_x, self.cord_y)

        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        return False

    def __init__(self, session, element, size, **star):
        super().__init__(session, element, size, **star)
        self.background = None
        self.cord_x = 0
        self.cord_y = 0
        self.frame = None
        self.stdscr = None


def image_format():
    """"""
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


def window(session, **star):
    """"""
    element = {
        "button": Button,
        "image": Image,
        "label": Label,
    }
    size = (80, 24)
    size = (122, 35)
    return Window(session, element, size, **star)
