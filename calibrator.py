#!/bin/python2
from sys import stdin, stdout
from time import sleep
from printrun.printcore import printcore
from settings import Settings
from solver import Solver
import re

g30 = re.compile("Bed.*X: ([\d.-]+).*Y: ([\d.-]+).*Z: ([\d.-]+)")
OFFSET = (-3.6, -22.9)

class Calibrator:
    def __init__(self, optimize_for=[]):
        self.core = printcore("/dev/kossel", 250000)
        self.probed_points = []
        self.settings = Settings()
        self.optimize_for = optimize_for
        sleep(1)

    def calibrate(self):
        self.core.recvcb = self.settings.parse
        self.core.send("M503")
        while self.settings.parsed != len(self.settings.commands):
            sleep(1)
        self.settings.prepare()
        for command in self.settings.dump():
            print command
        self.core.recvcb = self.parse_point
        try:
            for i in range(1):
                self.core.send("G28")
                sleep(1)
                solver = Solver(self.settings, self.optimize_for)
                points = solver.generate_points(10)
                for point in points:
                    self.probed = False
                    self.core.send("G30 X{} Y{} S0".format(point[0], point[1]))
                    self.count = 0
                    while not self.probed and self.count < 30:
                        self.count += 1
                        sleep(0.1)
                solver.fill_points(self.probed_points)
                solver.plot()
                error = solver.optimize()
                print error
                solver.interactive()
                for command in solver.settings.dump():
                    print command
                raw_input("Enter to save")
                for command in solver.settings.dump():
                    print command
                    self.core.send(command)
                self.core.send("M500")
        except KeyboardInterrupt:
            print "Exiting"
        finally:
            self.core.disconnect()

    def parse_point(self, x):
        x = x[:-1]
        m = g30.search(x)
        if m:
            x = float(m.group(1))
            y = float(m.group(2))
            z = float(m.group(3))
            self.probed_points.append((x + OFFSET[0], y + OFFSET[1], (z + self.settings.probe_offset)))
            self.probed = True

if __name__ == "__main__":
    calibrator = Calibrator(["hx", "hy", "hz", "radius"])
    calibrator.calibrate()
