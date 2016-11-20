#!/bin/python2
from sys import stdin, stdout
from time import sleep
from printrun.printcore import printcore
from settings import Settings
from solver import Solver
import re

g30 = re.compile("Bed.*X: ([\d.-]+).*Y: ([\d.-]+).*Z: ([\d.-]+)")

class Calibrator:
    def __init__(self, optimize_for=[]):
        self.core = printcore("/dev/kossel", 250000)
        self.probed_points = []
        self.settings = Settings()
        self.optimize_for = optimize_for
        sleep(1)

    def calibrate(self):
        self.core.recv = self.settings.parse
        core.send("M503")
        sleep(1)
        self.core.recv = self.parse_point
        try:
            for i in range(1):
                core.send("G28")
                sleep(1)
                solver = Solver(self.settings, self.optimize_for)
                points = Solver.generate_points(10)
                for point in points:
                    core.send("G30 X{} Y{} S0".format(point[0], point[1]))
                while not len(self.probed_points) == len(points):
                    sleep(1)
                res = []
                for point, z in zip(points, probed_points):
                    res.append([point[0], point[1], z])
                solver.fill_points(res)
                error = solver.optimize()
                print error
                raw_input("Enter to save")
                for command in solver.settings.dump():
                    print command
                    core.send(command)
                core.send("M500")
        except KeyboardInterrupt:
            print "Exiting"
        finally:
            core.disconnect()

    def parse_point(self, x):
        x = x[:-1]
        m = g30.search(x)
        if m:
            x = float(m.group(1))
            y = float(m.group(2))
            z = float(m.group(3))
            self.probed_points.append(-(z + self.probe_offset))
