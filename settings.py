import re


BASE_HEIGHT = 185.1


class Settings:
    commands = [
        "M665 L{diagonal} R{radius}",
        "M666 X{offset_x} Y{offset_y} Z{offset_z}",
        "M206 Z{height_offset}",
        "M851 Z{probe_offset}"
    ]

    def __init__(self, offset_x=0, offset_y=0, offset_z=0, radius=106, diagonal=215):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z
        self.height_offset = 0
        self.probe_offset = 0
        self.radius = radius
        self.diagonal = diagonal
        self.parsed = 0 #TODO: is it nessesary?

    def prepare(self):
        self.hx = BASE_HEIGHT + self.offset_x + self.height_offset
        self.hy = BASE_HEIGHT + self.offset_y + self.height_offset
        self.hz = BASE_HEIGHT + self.offset_z + self.height_offset
        self.homed = BASE_HEIGHT + self.height_offset

    def parse(self, message):
        for comm in self.commands:
            comm = re.sub(" ", r".*?", re.sub(r"\{(.*?)\}", r"(?P<\1>[\d.-]+)", comm))
            match = re.search(comm, message[:-1])
            if match:
                self.parsed += 1
                d = match.groupdict()
                for k, v in d.items():
                    d[k] = float(v)
                self.__dict__.update(d)

    def dump(self):
        self.height_offset = self.homed - BASE_HEIGHT
        self.offset_x = self.homed - self.hx
        self.offset_y = self.homed - self.hy
        self.offset_z = self.homed - self.hz
        d = max(self.offset_x, self.offset_y, self.offset_z)
        self.height_offset -= d
        self.offset_x -= d
        self.offset_y -= d
        self.offset_z -= d
        
        for comm in self.commands:
            yield re.sub(r"\{(.*?)\}", r"{\1:.2f}", comm).format(**self.__dict__)
