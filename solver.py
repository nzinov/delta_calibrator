from scipy.optimize import curve_fit
from sympy import *
from model import Model
from settings import Settings
import numpy

class Solver:
    def __init__(self, settings, optimize_for, probe_radius=10, n=10):
        self.optimize_for = optimize_for
        self.probe_radius = probe_radius
        self.point_number = n
        self.settings = settings
        self.points = []
        settings.prepare()

    def fixate(self, expr, leave=None):
        if leave is None:
            leave = []
        for prop in Model.properties:
            if prop not in leave:
                expr = expr.subs(getattr(Model, prop), getattr(self.settings, prop))
        props = [getattr(Model, prop) for prop in leave]
        print props, expr
        return lambdify(props, expr)

    def generate_points(self, step):
        points = []
        for x in numpy.arange(-self.probe_radius, self.probe_radius, step):
            for y in numpy.arange(-self.probe_radius, self.probe_radius, step):
                if x**2 + y**2 < self.probe_radius**2 - 5:
                    points.append((x, y))
        return points


    def fill_points(self, points):
        f = self.fixate(Model.ef_to_car, ["position"])
        try:
            self.points = [f((x, y, z)) for x, y, z in points]
        except ValueError:
            print "Unreachable point"

    def target_function(self):
        return self.fixate(Model.car_to_z, ["state"]+self.optimize_for)

    def target_jacobian(self):
        param = Matrix([[getattr(Model, prop) for prop in self.optimize_for]])
        print param
        return self.fixate(Matrix([[Model.car_to_z]]).jacobian(param), ["state"]+self.optimize_for)

    def optimize(self):
        popt, pcov = curve_fit(self.target_function(), self.points, [0]*len(self.points), jac=self.target_jacobian()) 
        for prop, val in zip(self.optimize_for, popt):
            setattr(self.settings, prop, val)
        return numpy.diag(pconv)
