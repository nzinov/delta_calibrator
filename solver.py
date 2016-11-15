from scipy.optimize import curve_fit
from sympy import *
from model import Model
from settings import Settings
import numpy

class Solver:
    def __init__(self, settings, optimize_for, probe_radius=90, n=10):
        self.optimize_for = optimize_for
        self.probe_radius = probe_radius
        self.point_number = n
        self.settings = settings
        self.points = []

    def fixate(self, expr, leave=None, var=[]):
        if leave is not None:
            leave = self.optimize_for
        for prop in Model.properties:
            if prop not in leave:
                expr = expr.subs(getattr(Model, prop), getattr(self.settings, prop))
        leave += var
        props = [getattr(Model, prop) for prop in leave]
        return lambdify(props, expr)

    def generate_points(self, step):
        points = [(0, 0)]
        radius = step
        while radius < self.probe_radius:
            for i in range(int(radius / step)):
                points.append((radius * numpy.sin(2 * numpy.pi * i * step / radius),
                               radius * numpy.cos(2 * numpy.pi * i * step / radius)))
            radius += step
        return points

    def fill_points(self, points):
        f = self.fixate(Model.ef_to_car, [], ["x", "y", "z"])
        self.points = [f(x, y, z) for x, y, z in points]

    def target_function(self):
        return self.fixate(Model.car_to_ef, var=["a", "b", "c"])

    def target_jacobian(self):
        return self.fixate(Model.car_to_ef.jacobian(Matrix(self.optimize_for)), var=["a", "b", "c"])

    def optimize(self):
        result = curve_fit(self.target_function(), self.points, [0]*len(self.points), jac=self.target_jacobian()) 
        return result
