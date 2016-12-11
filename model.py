import math
from sympy import *
from sympy.geometry import *
from sympy.matrices import *
import numpy
import scipy
import dill

class Model:
    endstops = Matrix([symbols("hx hy hz")])
    hx, hy, hz = endstops
    radius = symbols("r")
    diagonal = symbols("d")
    homed = symbols("h")

    properties = ["hx", "hy", "hz", "radius", "diagonal", "homed"]

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
    #PrograsticPos -> State
    carriages = Model.towers + zeros(2, 3).col_join(ones(1, 3)*Model.homed - Model.state).T
    shifts = carriages - ones(3, 1) * Model.position
    equations = matrix2numpy(get_diag(shifts * shifts.T) - ones(3, 1) * Model.diagonal**2).flatten().tolist()
    Model.ef_to_car = solve(equations, (Model.state))[0]
    Model.ef_to_car = Matrix(Model.ef_to_car)
    #State -> RealPos
    carriages = Model.towers + zeros(2, 3).col_join(Model.endstops - Model.state).T
    shifts = carriages - ones(3, 1) * Model.position
    equations = matrix2numpy(get_diag(shifts * shifts.T) - ones(3, 1) * Model.diagonal**2).flatten().tolist()
    x_eq = solve(equations[0] - equations[1], Model.x)[0]
    y_eq = solve((equations[0] + equations[1] - 2*equations[2]).subs(Model.x, x_eq), Model.y)[0]
    Model.car_to_z = solve(equations[2].subs(Model.x, x_eq).subs(Model.y, y_eq), Model.z)[0]
    with open("model.dat", "w") as f:
        dill.dump(Model, f)
else:
    try:
        with open("model.dat") as f:
            Model = dill.load(f)
    except Exception:
        pass
