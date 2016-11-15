import math
from sympy import *
from sympy.geometry import *
from sympy.matrices import *
import numpy
import scipy

class Model:
    endstops = symbols("ex ey ez")
    ex, ey, ez = endstops
    radius = symbols("r")
    diagonal = symbols("d")

    properties = ["ex", "ey", "ez", "radius", "diagonal"]

    towers = [
        Point(-sin(pi/3) * (radius), -cos(pi/3) * (radius)),
        Point(sin(pi/3) * (radius), -cos(pi/3) * (radius)),
        Point(0, (radius))
    ]

    x, y, z = symbols("x y z")
    a, b, c = symbols("a b c")

Model.ef_to_car = Matrix([
    Model.endstops[i] - (Model.diagonal**2 - Point(Model.x, Model.y).distance(Model.towers[i])**2)**0.5 - Model.z
    for i in range(3)
])

print([Model.ef_to_car[0] - Model.a, Model.ef_to_car[1] - Model.b, Model.ef_to_car[2] - Model.c])
Model.car_to_ef = Matrix(solve([Model.ef_to_car[0] - Model.a,
                                Model.ef_to_car[1] - Model.b,
                                Model.ef_to_car[2] - Model.c], (Model.x, Model.y, Model.z), check=False))
print(Model.car_to_ef)
