import re
from sympy import *


BASE_HEIGHT = 185.1


class Settings:
    commands = [
        "M665 L{diagonal} R{radius}",
        "M666 X{ex} Y{ey} Z{ez}",
        "M206 Z{height_offset}",
        "M851 Z{probe_offset}"
    ]

    def __init__(self, ex=0, ey=0, ez=0, radius=106, height=185.1, diagonal=215):
        self.ex = ex
        self.ey = ey
        self.ez = ez
        self.height_offset = height - BASE_HEIGHT
        self.probe_offset = 0
        self.radius = height
        self.diagonal = diagonal

    def prepare(self):
        self.ex = BASE_HEIGHT + self.height_offset + self.ex
        self.ey = BASE_HEIGHT + self.height_offset + self.ey
        self.ez = BASE_HEIGHT + self.height_offset + self.ez

    def parse(self, message):
        for comm in self.commands:
            comm = re.sub("\{(.*?)\}", r"(?P<\1>[\d.-]+)", comm)
            match = re.search(comm, message[:-1])
            if match:
                self.__dict__.update(match.groupdict())

    def dump(self):
        self.ex = -BASE_HEIGHT - self.height_offset + self.ex
        self.ey = -BASE_HEIGHT - self.height_offset + self.ey
        self.ez = -BASE_HEIGHT - self.height_offset + self.ez
        for comm in self.commands:
            yield comm.format(self.__dict__)
