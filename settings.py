import re


BASE_HEIGHT = 185.1


class Settings:
    commands = [
        "M665 L{diagonal} R{radius}",
        "M666 X{offset_x} Y{offset_y} Z{offset_z}",
        "M206 Z{height_offset}",
        "M851 Z{probe_offset}"
    ]

    def __init__(self, offset_x=0, offset_y=0, offset_z=0, radius=106, height=185.1, diagonal=215):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z
        self.height_offset = 0
        self.probe_offset = 0
        self.radius = radius
        self.diagonal = diagonal
        self.parsed = 0

    def prepare(self):
        self.ex = BASE_HEIGHT + self.height_offset + self.offset_x
        self.ey = BASE_HEIGHT + self.height_offset + self.offset_y
        self.ez = BASE_HEIGHT + self.height_offset + self.offset_z
        print self.ex, self.ey, self.ez, self.height_offset

    def parse(self, message):
        for comm in self.commands:
            comm = re.sub(" ", r".*?", re.sub(r"\{(.*?)\}", r"(?P<\1>[\d.-]+)", comm))
            match = re.search(comm, message[:-1])
            if match:
                print comm
                self.parsed += 1
                d = match.groupdict()
                for k, v in d.items():
                    d[k] = float(v)
                self.__dict__.update(d)

    def dump(self):
        print self.ex, self.ey, self.ez
        self.offset_x = -BASE_HEIGHT - self.height_offset + self.ex
        self.offset_y = -BASE_HEIGHT - self.height_offset + self.ey
        self.offset_z = -BASE_HEIGHT - self.height_offset + self.ez
        d = max(self.offset_x, self.offset_y, self.offset_z)
        self.height_offset += d
        self.offset_x -= d
        self.offset_y -= d
        self.offset_z -= d
        print self.offset_x, self.offset_y, self.offset_z, self.height_offset
        
        for comm in self.commands:
            yield re.sub(r"\{(.*?)\}", r"{\1:.2f}", comm).format(**self.__dict__)
