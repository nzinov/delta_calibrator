#!/bin/python2
from sys import stdin, stdout
from time import sleep
from printrun.printcore import printcore
from reprapfirmware_lsq import Tuner
import re
OFFSET = -6.03
BASE_HEIGHT = 185.1 + OFFSET
core = printcore("/dev/kossel", 250000)
diagonal = 0
radius = 0
height = 0
xstop = 0
ystop = 0
zstop = 0
xadj = 0
yadj = 0
zadj = 0
probed_points = []


def log(x):
    if x.startswith("echo"):
        stdout.write(x[len("echo:"):])

m665 = re.compile("M665.*L([\d.-]+).*R([\d.-]+).*A([\d.-]+).*B([\d.-]+).*C([\d.-]+)")
m666 = re.compile("M666.*X([\d.-]+).*Y([\d.-]+).*Z([\d.-]+)")
m206 = re.compile("M206.*Z([\d.-]+)")
g30 = re.compile("Bed.*X: ([\d.-]+).*Y: ([\d.-]+).*Z: ([\d.-]+)")
probed = False

def parse_settings(x):
    global diagonal, radius, xadj, yadj, zadj, xstop, ystop, zstop, height, probed_points, probed
    x = x[:-1]
    print x
    m = m665.search(x)
    if m:
        diagonal = float(m.group(1))
        radius = float(m.group(2))
        xadj = float(m.group(3))
        yadj = float(m.group(4))
        zadj = float(m.group(5))
    m = m666.search(x)
    if m:
        xstop = float(m.group(1))
        ystop = float(m.group(2))
        zstop = float(m.group(3))
    m = m206.search(x)
    if m:
        height = BASE_HEIGHT + float(m.group(1))
    m = g30.search(x)
    if m:
        x = float(m.group(1))
        y = float(m.group(2))
        z = float(m.group(3))
        probed_points.append(-z)
        probed = True

core.recvcb = parse_settings
sleep(1)
try:
    core.send("M503")
    core.send("G28")
    sleep(1)
    print "Param:", diagonal, radius, height, xstop, ystop, zstop, xadj, yadj, zadj
    tuner = Tuner(diagonal, radius, height, xstop, ystop, zstop, xadj, yadj, zadj, num_factors=4, num_probe_points=12, base_height=BASE_HEIGHT)
    tuner.set_firmware("Marlin")
    points = tuner.get_probe_points()
    probed_points = []
    raw_input("Enter to go")
    for point in points:
        probed = False
        core.send("G30 X{} Y{} S0".format(point[0], point[1]))
        while not probed:
            sleep(1)
    res = []
    for point, z in zip(points, probed_points):
        res.append([point[0], point[1], z])
    print res
    tuner.set_probe_errors(res)
    commands, before, after = tuner.calc()
    print "Error before:", before, "Error after:", after
    for command in commands:
        print command
        core.send(command)
    core.send("M500")
except KeyboardInterrupt:
    print "Exiting"
finally:
    core.disconnect()

