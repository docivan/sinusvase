import math
import numpy as np

# CONFIG

# radii
r_top = 7
r_btm = 5
r_xy_multiplier = 0.3
r_z_multiplier = 0.3

subdiv_xy = 400  # points per ring
subdiv_z = 15  # rings in total

period_xy = 10  # periods of sinus func along each ring
period_z = 5 # periods of sinus func along vase edge
spiral_turns = 3  # how many 360 deg turns around vase

# GLOBALS

rings = []

# GENERATE VERTICES

radian_add_step = (2 * math.pi) * period_z / (subdiv_z * subdiv_xy)
radian_step_cnt = 0

for z in range(0, subdiv_z):
    print("Generating ring", z + 1, "out of", subdiv_z)

    this_ring = []

    for rd in np.arange(0, 2 * math.pi, 2 * math.pi / subdiv_xy):
        radians = rd + radian_add_step * radian_step_cnt
        radian_step_cnt += 1

        radius_base = r_btm + (r_top - r_btm) * (z / subdiv_z)
        radius_xy_add = r_xy_multiplier * math.sin(radians * period_xy)
        radius_z_add = r_z_multiplier * math.sin((2 * math.pi / subdiv_z) * z * period_z)

        radius = radius_base + radius_xy_add + radius_z_add

        x = radius * math.cos(rd)
        y = radius * math.sin(rd)
        this_ring.append((x, y, z))

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

    for z in range(1, subdiv_z):
        for idx in range(0, subdiv_xy):
            quad(rings[z][idx], rings[z][idx - 1], rings[z - 1][idx - 1], rings[z - 1][idx])

    # stitch bottom of the vase with triangles:
    for idx in range(0, subdiv_xy):
        triangle(rings[0][idx], rings[0][idx - 1], (0, 0, 0))

    # footer
    file.write("endsolid vase\n")
    file.close()
