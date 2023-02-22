""""""

import math

from celestine.window.container import Container as container

from .button import Button
from .image import Image
from .label import Label


class Container(container):
    """"""

    def draw(self, collection, **star):
        """"""
        star.update(font=self.font)
        super().draw(collection, **star)

    def drop(self, tag, **kwargs):
        """"""
        return self.item_set(
            tag,
            Drop(
                self.session,
                tag,
                self.turn,
                self.font,
                **kwargs,
            )
        )

    def grid(self, tag, width, **kwargs):
        """"""
        return self.item_set(
            tag,
            Grid(
                self.session,
                tag,
                self.turn,
                self.font,
                width,
                **kwargs,
            )
        )

    def span(self, tag, **kwargs):
        """"""
        return self.item_set(
            tag,
            Span(
                self.session,
                tag,
                self.turn,
                self.font,
                **kwargs,
            )
        )

    def __init__(self, session, name, turn, font, **kwargs):
        self.font = font
        super().__init__(session, name, turn, **kwargs)
        super().ready(Button, Image, Label)


class Grid(Container):
    """"""

    def button(self, tag, text, action):
        """"""
        name = self._get_tag(tag)
        super().button(name, text, action)

    def image(self, tag, image):
        """"""
        name = self._get_tag(tag)
        super().image(name, image)

    def label(self, tag, text):
        """"""
        name = self._get_tag(tag)
        super().label(name, text)

    def items(self):
        """"""
        yield from [item for (_, item) in self.item.items()]

    def spot(self, x_min, y_min, x_max, y_max):
        """"""
        self.set(x_min, y_min, x_max, y_max)

        partition_x = self.width
        partition_y = math.ceil(len(self.item) / self.width)
        (axis_x, axis_y) = self.get(partition_x, partition_y)

        items = self.items()

        for _ in range(partition_y):
            (ymin, ymax) = next(axis_y)

            for _ in range(partition_x):
                (xmin, xmax) = next(axis_x)

                item = next(items)
                item.spot(xmin, ymin, xmax, ymax)

        axis_x.close()
        axis_y.close()

    def _get_tag(self, name):
        """"""
        length = len(self.item)
        index_x = length % self.width
        index_y = length // self.width

        return F"{name}_{index_x}-{index_y}"

    def __init__(self, session, name, turn, font, width, **kwargs):
        self.width = width
        super().__init__(session, name, turn, font, **kwargs)


class Drop(Container):
    """"""

    def spot(self, x_min, y_min, x_max, y_max):
        """"""
        self.set(x_min, y_min, x_max, y_max)

        partition_x = 1
        partition_y = len(self.item)
        (axis_x, axis_y) = self.get(partition_x, partition_y)

        for (_, item) in self.item.items():
            (xmin, xmax) = next(axis_x)
            (ymin, ymax) = next(axis_y)

            item.spot(xmin, ymin, xmax, ymax)

        axis_x.close()
        axis_y.close()


class Span(Container):
    """"""

    def spot(self, x_min, y_min, x_max, y_max):
        """"""
        self.set(x_min, y_min, x_max, y_max)

        partition_x = len(self.item)
        partition_y = 1
        (axis_x, axis_y) = self.get(partition_x, partition_y)

        for (_, item) in self.item.items():
            (xmin, xmax) = next(axis_x)
            (ymin, ymax) = next(axis_y)

            item.spot(xmin, ymin, xmax, ymax)

        axis_x.close()
        axis_y.close()
