from Coordinate import *
from Code import *
from Shape import *

#I and J are determined by subtracting the center of the arc from start xy
#how flow rate is determined I am unsure.
outfile = open("OUT.CNC", "w")
constMachine = None
def parseCoords(shapes, machine):
    constMachine = machine
    for shape in shapes:
        startShape()
        for e in shape.coordinates:
            for c in e.primitives:
                match (c.type):
                    case EType.LINE:
                        handleLine(c)
                        continue
                    case EType.ARC:
                        handleArc(False,c)
                        continue
                    case EType.CIRCLE:
                        handleCircle(c)
                        continue
                    case EType.END:
                        return
                    case _:
                        print("Undefined Type")
                        return
        endShape()
    return


def handleLine(c):
    outfile.write(f"G1 X{c.x} Y{c.y} F100\n")
    return
    

def handleArc(isClockwise, c):
    if isClockwise == True:
        outfile.write(f"G3 X{c.x} Y{c.y} I{c.center[0]} J{c.center[1]}\n")
    else:
        outfile.write(f"G2 X{c.x} Y{c.y} I{c.center[0]} J{c.center[1]}\n")
    return

def handleCircle(c):
    outfile.write(f"circle placeholder")



def startShape():
    outfile.write(f"M04\n")

def endShape():
    outfile.write(f"M03\n")
    