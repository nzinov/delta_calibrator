from settings import Settings
from solver import Solver
from sympy import *
import inspect
import numpy
s1 = Settings()
s1.prepare()
solver = Solver(s1, ["ex", "ey", "ez", "radius"])
s = Settings(offset_x=10)
s.prepare()
mod = Solver(s, [])
probe = solver.generate_points(10)
mod.fill_points([(x, y, numpy.random.rand()*0.1) for x, y in probe])
solver.points = mod.points
z = solver.target_function()(mod.points, solver.settings.ex, solver.settings.ey, solver.settings.ez, solver.settings.radius)
solver.source_points = numpy.array([[x[0], x[1], z] for x, z in zip(probe, z)])
solver.plot()
print solver.optimize()
for el in solver.settings.dump():
    print el
