import re


BASE_HEIGHT = 185.1


class Settings:
    commands = [
        "M665 L{delta_diagonal_rod} R{delta_radius}",
        "M666 X{ex} Y{ey} Z{ez}",
        "M206 Z{height_offset}",
        "M851 Z{probe_offset}"
    ]

    def __init__(self, ex, ey, ez, radius, height, diagonal):
        self.ex = ex
        self.ey = ey
        self.ez = ez
        self.height_offset = height - BASE_HEIGHT
        self.probe_offset = 0
        self.delta_radius = height
        self.delta_diagonal_rod = diagonal

    def parse(self, message):
        for comm in self.commands:
            comm = re.sub("\{(.*?)\}", r"(?P<\1>[\d.-]+)", comm)
            match = re.search(comm, message[:-1])
            if match:
                self.__dict__.update(match.groupdict())

    def dump(self):
        for comm in self.commands:
            yield comm.format(self.__dict__)
