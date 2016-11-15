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
    height = symbols("h")

    properties = ["ex", "ey", "ez", "radius", "diagonal"]

    towers = [
        Point(-sin(pi/3) * (radius), -cos(pi/3) * (radius)),
        Point(sin(pi/3) * (radius), -cos(pi/3) * (radius)),
        Point(0, (radius))
    ]

    x, y, z = symbols("x y z")
    a, b, c = symbols("a b c")

Model.ef_to_car = [
    Model.height + Model.endstops[i] - (Model.diagonal**2 - Point(Model.x, Model.y).distance(Model.towers[i])**2)**0.5 - Model.z
    for i in range(3)
]

a_eq = Model.ef_to_car[0] - Model.a
b_eq = Model.ef_to_car[1] - Model.b
c_eq = Model.ef_to_car[2] - Model.c
x_eq = solve(a_eq - b_eq, Model.y)
print(x_eq)
y_eq = solve(a_eq - b_eq, Model.y)
print(y_eq)
z_eq = c_eq.subs(Model.y, y_eq).subs(Model.x, x_eq)
print(z_eq)
Model.car_to_z = z_eq
