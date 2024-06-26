""""""

import math

import bpy

DEGREE_TO_RADIAN = math.pi / 180


class _imaginary:
    """Objects that only exist in spirit."""

    type_ = ""
    data = None

    @classmethod
    def new(cls, name):
        """"""
        if cls.type_:
            return cls.data.new(name, cls.type_)
        return cls.data.new(name)

    @classmethod
    def remove(cls, item):
        """"""
        cls.data.remove(
            item, do_unlink=True, do_id_user=True, do_ui_user=True
        )

    def __init__(self, name):
        soul = self.new(name)

        self.__dict__["name"] = name
        self.__dict__["soul"] = soul


class _real(_imaginary):
    """Objects that exist in the real world."""

    @classmethod
    def bind(cls, collection, name, soul):
        """Give an existing soul a body."""
        body = bpy.data.objects.new(name, soul)
        if collection:
            collection.objects.link(body)
        return cls(body, soul)

    def __init__(self, name, collection):
        soul = self.new(name)
        body = bpy.data.objects.new(name, soul)
        if collection:
            collection.objects.link(body)

        self.__dict__["name"] = name
        self.__dict__["body"] = body
        self.__dict__["soul"] = soul

    def __getattr__(self, name):
        match name:
            case "location":
                return getattr(self.body, name)
            case "parent":
                return getattr(self.body, name)
            case "rotation_euler":
                return getattr(self.body, name)
            case "scale":
                return getattr(self.body, name)
            case _:
                return getattr(self.soul, name)

    def __setattr__(self, name, value):
        match name:
            case "location":
                setattr(self.body, name, value)
            case "rotation":
                (x_dot, y_dot, z_dot) = value
                x_dot *= DEGREE_TO_RADIAN
                y_dot *= DEGREE_TO_RADIAN
                z_dot *= DEGREE_TO_RADIAN
                value = (x_dot, y_dot, z_dot)
                setattr(self.body, "rotation_euler", value)
            case "parent":
                setattr(self.body, name, value.body)
            case "rotation_euler":
                setattr(self.body, name, value)
            case "scale":
                setattr(self.body, name, value)
            case _:
                setattr(self.soul, name, value)


class _text(_real):
    @classmethod
    def new(cls, name, text):
        soul = super().new(name)
        soul.body = text
        return soul

    def __init__(self, name, collection, text):
        """Create a new soul and give it a body."""
        soul = self.new(name, text)
        body = bpy.data.objects.new(name, soul)
        if collection:
            collection.objects.link(body)

        self.__dict__["body"] = body
        self.__dict__["soul"] = soul
