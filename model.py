import math
from sympy import *
from sympy.geometry import *
from sympy.matrices import *
import numpy
import scipy
import dill

class Model:
    endstops = Matrix([symbols("ex ey ez")])
    ex, ey, ez = endstops
    radius = symbols("r")
    diagonal = symbols("d")

    properties = ["ex", "ey", "ez", "radius", "diagonal"]

    towers = Matrix([
        [-sin(pi/3) * radius, -cos(pi/3) * radius, 0],
        [sin(pi/3) * radius, -cos(pi/3) * radius, 0],
        [0, radius, 0]
    ])

    position = Matrix([symbols("x y z")])
    x, y, z = position
    state = Matrix([symbols("a b c")])

def get_diag(matrix):
    return Matrix(matrix2numpy(matrix)[(0, 1, 2),(0, 1, 2)])

if __name__=="__main__":
    carriages = Model.towers + zeros(2, 3).col_join(Model.endstops - Model.state).T
    shifts = carriages - ones(3, 1) * Model.position
    equations = matrix2numpy(expand(get_diag(shifts * shifts.T) - ones(3, 1) * Model.diagonal**2)).flatten().tolist()
    Model.ef_to_car = solve(equations, (Model.state))[0]
    x_eq = solve(equations[0] - equations[1], Model.x)[0]
    print(x_eq)
    y_eq = solve((equations[0] + equations[1] - 2*equations[2]).subs(Model.x, x_eq), Model.y)[0]
    print(y_eq)
    Model.car_to_z = solve(equations[2].subs(Model.x, x_eq).subs(Model.y, y_eq), Model.z)[0]
    print(Model.car_to_z)
    Model.ef_to_car = Matrix(Model.ef_to_car)
    with open("model.dat", "w") as f:
        dill.dump(Model, f)
else:
    try:
        with open("model.dat") as f:
            Model = dill.load(f)
    except Exception:
        pass
