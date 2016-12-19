from mpl_toolkits.mplot3d.axes3d import Axes3D
from scipy.optimize import curve_fit
from sympy import *
from model import Model
from settings import Settings
from matplotlib import pyplot
from matplotlib.widgets import Slider
import numpy

class Solver:
    def __init__(self, settings, optimize_for, probe_radius=60, n=10):
        settings.prepare()
        self.optimize_for = optimize_for
        self.probe_radius = probe_radius
        self.point_number = n
        self.settings = settings
        self.points = []

    def fixate(self, expr, leave=[]):
        if leave is None:
            leave = []
        for prop in Model.properties:
            if prop not in leave:
                expr = expr.subs(getattr(Model, prop), getattr(self.settings, prop))
        def f(*args):
            my = expr
            for arg, prop in zip(args, leave):
                my = my.subs(getattr(Model, prop), arg)
            return my.evalf()
        return lambdify([getattr(Model, prop) for prop in leave], expr)

    def generate_points(self, step):
        points = []
        for x in numpy.arange(-self.probe_radius, self.probe_radius, step):
            for y in numpy.arange(-self.probe_radius, self.probe_radius, step):
                if x**2 + y**2 < self.probe_radius**2 - 5:
                    points.append((x, y))
        return points


    def fill_points(self, points):
        self.source_points = numpy.array(points)
        f = self.fixate(Model.ef_to_car, ["position"])
        try:
            self.points = numpy.array([f([x, y, z]) for x, y, z in points])
        except ValueError:
            print "Unreachable point"

    def target_function(self):
        f = self.fixate(Model.car_to_z, ["state"]+self.optimize_for)
        def g(x, *args):
            return [f(el, *args) for el in x]
        return g

    def plot(self):
        plt = pyplot.subplot(1, 1, 1, projection="3d")
        plt.set_xlim(-60, 60)
        plt.set_ylim(-60, 60)
        plt.plot_trisurf(self.source_points[:, 0], self.source_points[:, 1], self.source_points[:,2])
        plt.plot_trisurf(self.source_points[:, 0], self.source_points[:, 1], [0]*len(self.source_points))
        pyplot.show()


    def target_jacobian(self):
        param = Matrix([[getattr(Model, prop) for prop in self.optimize_for]])
        f = self.fixate(Matrix([[Model.car_to_z]]).jacobian(param), ["state"]+self.optimize_for)
        def g(x, *args):
            return [f(el, *args)[0] for el in x]
        return g

    def optimize(self):
        param = [getattr(self.settings, prop) for prop in self.optimize_for]
        popt, pconv = curve_fit(self.target_function(), self.points, [0]*len(self.points), param, jac=self.target_jacobian()) 
        for prop, val in zip(self.optimize_for, popt):
            setattr(self.settings, prop, val)
        return numpy.diag(pconv)

    def interactive(self):
        #self.optimize()
        fig = pyplot.figure()
        plt = fig.add_subplot(1, 1, 1, projection="3d")
        plt.set_xlim(-60, 60)
        plt.set_ylim(-60, 60)
        pos = 0
        sliders = []
        axes = []
        def update(val):
            values = [el.val for el in sliders]
            for prop, val in zip(self.optimize_for, values):
                setattr(self.settings, prop, val)
            plt.clear()
            plt.plot_trisurf(self.source_points[:, 0], self.source_points[:, 1], [0]*len(self.source_points))
            plt.plot_trisurf(self.source_points[:, 0], self.source_points[:, 1], self.target_function()(self.points, *values))
            fig.canvas.draw_idle()
        for el in self.optimize_for:
            axis = pyplot.axes([0.85, pos, 0.15, 0.05])
            axes.append(axis)
            pos += 0.05
            val = getattr(self.settings, el)
            sliders.append(Slider(axis, el, val - 10, val + 10, val))
            sliders[-1].on_changed(update)
        def on_key(event):
            keys = {"left": -1, "right": 1, "up": 0.1, "down": -0.1}
            if event.key in keys:
                try:
                    sl = sliders[axes.index(event.inaxes)]
                    sl.set_val(sl.val + keys[event.key])
                except ValueError:
                    pass
        fig.canvas.mpl_connect('key_press_event', on_key)
        update(0)
        pyplot.show()

