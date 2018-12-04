import math
import numpy as np

# CONFIG

# radii
r_top = 7
r_btm = 5

height = 15

r_xy_multiplier = 0.5
r_z_multiplier = 0.5

abs_mode = False

subdiv_xy = 60  # points per ring
subdiv_z = 60  # rings in total

period_xy = 2  # periods of sinus func along each ring
period_z = 2  # periods of sinus func along vase edge
spiral_turns = 2  # how many 360 deg turns around vase

# GLOBALS

rings = []

# GENERATE VERTICES

radian_add_step = 0
if spiral_turns > 0:
    radian_add_step = (2 * math.pi) * spiral_turns / subdiv_z
radian_step_cnt = 0

for ring_cnt in range(0, subdiv_z):
    print("Generating ring", ring_cnt + 1, "out of", subdiv_z)

    this_ring = []

    for rd in np.arange(0, 2 * math.pi, 2 * math.pi / subdiv_xy):
        radians = rd + radian_add_step * radian_step_cnt

        radius_base = r_btm + (r_top - r_btm) * (ring_cnt / subdiv_z)

        radius_xy_add = r_xy_multiplier * math.sin(radians * period_xy)
        if abs_mode:
            radius_xy_add = abs(radius_xy_add)


        radius_z_add = r_z_multiplier * math.sin((2 * math.pi / subdiv_z) * ring_cnt * period_z)
        if abs_mode:
            radius_z_add = abs(radius_z_add)

        radius = radius_base + radius_xy_add + radius_z_add

        x = radius * math.cos(rd)
        y = radius * math.sin(rd)
        z = height * ring_cnt / subdiv_z
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

    for z in range(1, subdiv_z):
        for idx in range(0, subdiv_xy):
            quad(rings[z][idx], rings[z][idx - 1], rings[z - 1][idx - 1], rings[z - 1][idx])

    # stitch top of the vase with triangles:
    for idx in range(0, subdiv_xy):
        triangle(rings[-1][idx - 1], rings[-1][idx], (0, 0, height))

    # stitch bottom of the vase with triangles:
    for idx in range(0, subdiv_xy):
        triangle(rings[0][idx], rings[0][idx - 1], (0, 0, 0))

    # footer
    file.write("endsolid vase\n")
    file.close()
