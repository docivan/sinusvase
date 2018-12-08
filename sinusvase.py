import math
import numpy as np
import sys
import json

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0],"config.json")
    quit()

# CONFIG

config = None
with open(sys.argv[1], "r") as f:
    # NB! this will fail if // is contained within a comment
    config = json.loads("\n".join(line.split("//")[0].replace("\n", "") for line in f.readlines()))

# GLOBALS

rings = []

def norm_rad(rad):
    if rad > math.pi * 2:
        n = math.floor(rad / (math.pi * 2))
        return rad - n * math.pi * 2

    return rad


def f_rect(rad):
    rad = norm_rad(rad)

    if rad < math.pi:
        return 0
    return 1


def f_swt(rad):
    rad = norm_rad(rad)

    if rad < math.pi:
        return rad / math.pi
    else:
        return 1 - (rad - math.pi) / math.pi


f_map = {
    "f_sin": math.sin,
    "f_cos": math.cos,
    "f_rct": f_rect,
    "f_swt": f_swt
}

# GENERATE VERTICES

radian_add_step = 0
if config["spiral_turns"] > 0:
    radian_add_step = (2 * math.pi) * config["spiral_turns"] / config["subdiv_z"]
radian_step_cnt = 0

for ring_cnt in range(0, config["subdiv_z"]):
    print("Generating ring", ring_cnt + 1, "out of", config["subdiv_z"])

    this_ring = []

    for rd in np.arange(0, 2 * math.pi, 2 * math.pi / config["subdiv_xy"]):
        radians = rd + radian_add_step * radian_step_cnt

        radius_base = config["r_btm"] + (config["r_top"] - config["r_btm"]) * (ring_cnt / config["subdiv_z"])

        radius_xy_add = config["r_xy_multiplier"] * f_map[config["func_xy"]](radians * config["period_xy"])
        if config["abs_mode"]:
            radius_xy_add = abs(radius_xy_add)

        radius_z_add = config["r_z_multiplier"] * f_map[config["func_z"]]((2 * math.pi / config["subdiv_z"]) * ring_cnt * config["period_z"])
        if config["abs_mode"]:
            radius_z_add = abs(radius_z_add)

        radius = radius_base + radius_xy_add + radius_z_add

        x = radius * math.cos(rd)
        y = radius * math.sin(rd)
        z = config["height"] * ring_cnt / config["subdiv_z"]
        this_ring.append((x, y, z))

    radian_step_cnt += 1
    rings.append(this_ring)


# GENERATE STL
def calc_normal(v1, v2, v3):
    u = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    v = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


with open("vase.stl", "w") as file:
    def triangle(v1, v2, v3):
        normal = calc_normal(v1, v2, v3)
        file.write("facet normal {} {} {}\n".format(normal[0], normal[1], normal[2]))
        file.write("\touter loop\n")
        file.write("\t\tvertex {} {} {}\n".format(v1[0], v1[1], v1[2]))
        file.write("\t\tvertex {} {} {}\n".format(v2[0], v2[1], v2[2]))
        file.write("\t\tvertex {} {} {}\n".format(v3[0], v3[1], v3[2]))
        file.write("\tendloop\n")
        file.write("endfacet\n")


    def quad(v1, v2, v3, v4):
        triangle(v1, v2, v3)
        triangle(v1, v3, v4)


    # header
    file.write("solid vase\n")

    for z in range(1, config["subdiv_z"]):
        for idx in range(0, config["subdiv_xy"]):
            quad(rings[z][idx], rings[z][idx - 1], rings[z - 1][idx - 1], rings[z - 1][idx])

    # stitch top of the vase with triangles:
    for idx in range(0, config["subdiv_xy"]):
        triangle(rings[-1][idx - 1], rings[-1][idx], (0, 0, config["height"]))

    # stitch bottom of the vase with triangles:
    for idx in range(0, config["subdiv_xy"]):
        triangle(rings[0][idx], rings[0][idx - 1], (0, 0, 0))

    # footer
    file.write("endsolid vase\n")
    file.close()
