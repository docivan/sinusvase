import os
import numpy as np
import cv2
import math

# constant configs
r_top = 7
r_btm = 5
height = 15
r_xy_multiplier = 0.5
r_z_multiplier = 0.5
subdiv_xy = 60  # points per ring
subdiv_z = 60  # rings in total

#variable configs

abs_mode = (False, True)
func_xy = ("f_sin", "f_cos", "f_rct", "f_swt")
func_z = ("f_sin", "f_cos", "f_rct", "f_swt")

period_xy = np.arange(0,4)  # periods of func along each ring
period_z = np.arange(0,4)  # periods of func along vase edge
spiral_turns = np.arange(0,4,0.5)  # how many 360 deg turns around vase

# run
cnt = 0

frame_sz = 120
side_cnt = int(math.ceil(math.sqrt(len(abs_mode) * len(func_xy) * len(func_z) * len(period_xy) * len(period_z) * len(spiral_turns))))
img_sz = frame_sz * side_cnt
img = np.zeros((img_sz, img_sz, 3), np.uint8)

print("Creating image with size", img_sz, "x", img_sz)

for am in abs_mode:
    for fxy in func_xy:
        for fz in func_z:
            for pxy in period_xy:
                for pz in period_z:
                    for st in spiral_turns:
                        filename = "{:05}".format(cnt)
                        print("Processing", filename, "...")

                        with open("configs/" + filename + ".json", "w") as f:

                            #constants
                            f.write("{\n\"r_top\" : " + str(r_top) + ",\n")
                            f.write("\"r_btm\" : " + str(r_btm) + ",\n")
                            f.write("\"height\" : " + str(height) + ",\n")
                            f.write("\"r_xy_multiplier\" : " + str(r_xy_multiplier) + ",\n")
                            f.write("\"r_z_multiplier\" : " + str(r_z_multiplier) + ",\n")
                            f.write("\"subdiv_xy\" : " + str(subdiv_xy) + ",\n")
                            f.write("\"subdiv_z\" : " + str(subdiv_z) + ",\n")

                            #variables
                            f.write("\"abs_mode\" : \"" + str(am) + "\",\n")
                            f.write("\"func_xy\" : \"" + str(fxy) + "\",\n")
                            f.write("\"func_z\" : \"" + str(fz) + "\",\n")
                            f.write("\"period_xy\" : " + str(pxy) + ",\n")
                            f.write("\"period_z\" : " + str(pz) + ",\n")
                            f.write("\"spiral_turns\" : " + str(st) + "\n}\n")

                        os.system("python sinusvase.py configs/" + filename + ".json")
                        os.system("python stl2pov.py vase.stl vase.pov")
                        os.system("povray render.ini +Oout/" + filename + ".png")

                        frame = cv2.imread("out/" + filename + ".png")
                        cv2.transpose(frame, frame)
                        cv2.putText(frame, str(filename), (60, 117), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0,255,0), 2)
                        cv2.transpose(frame, frame)
                        cv2.flip(frame, 1, frame)

                        y = int(cnt / side_cnt)
                        x = cnt - y * side_cnt

                        img[(y*frame_sz):((y+1)*frame_sz), (x*frame_sz):((x+1)*frame_sz),:] = frame

                        cnt = cnt + 1

cv2.imwrite("batch.png", img)
