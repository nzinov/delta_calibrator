from settings import Settings
from solver import Solver
from sympy import *
import inspect
import numpy

class Printer:
    def __init__(self, real_settings, prog_settings):
        self.real = Solver(real_settings, [])
        self.prog = Solver(prog_settings, [])

    def probe(self, x, y):
        self.real.fill_points([[x, y, 0]])
        return self.prog.target_function()(self.real.points)[0]

    def dump(self):
        print "Real settings"
        for el in self.real.settings.dump():
            print el
        print "Prog settings"
        for el in self.prog.settings.dump():
            print el

p = Printer(Settings(), Settings(-1, -1, 0))
solver = Solver(p.prog.settings, ["hx", "hy", "hx"])
solver.fill_points([(x, y, p.probe(x, y)) for x, y in solver.generate_points(10)])
solver.optimize()
for el in solver.settings.dump():
    print el
