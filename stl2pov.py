import sys

if len(sys.argv) != 3:
    print("Usage: stl2pov file.stl file.pov")
    quit()


with open(sys.argv[1], "r") as infile:
    with open(sys.argv[2], "w") as outfile:
        outfile.write("mesh{")
        buffer = []

        for line in infile:
            if line.find("vertex") != -1:
                buffer.append([float(i) for i in line.split()[1:4]])

                #buffer full
                if len(buffer) == 3:
                    outfile.write("triangle{")
                    outfile.write("<{}, {}, {}>,".format(buffer[0][0], buffer[0][1], buffer[0][2]))
                    outfile.write("<{}, {}, {}>,".format(buffer[1][0], buffer[1][1], buffer[1][2]))
                    outfile.write("<{}, {}, {}>".format(buffer[2][0], buffer[2][1], buffer[2][2]))
                    outfile.write("}\n")
                    buffer = []
        outfile.write("}\n")
