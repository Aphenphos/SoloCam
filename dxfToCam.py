from Coordinate import *
from Code import *
from Shape import *

#I and J are determined by subtracting the center of the arc from start xy
#how flow rate is determined I am unsure.
outfile = open("OUT.CNC", "w")
global constMachine
global N
N = 0
constMachine = None
def generateLeadInOut(tab, customLoc):
    print("By default create the leadin/out on the top left corner of the part \
        this will not always be the best case and sometimes will require a custom lead in out location \
          or parameters. Solution to the custom ones are still up for debate \
          There is also the need for tabs which will be easily imlemented but again the location \
          will be difficult")
    pass

def quality(qual, shapes, fAcc):
    ##quality is determined by the distance between instructions as far as i can tell.
    for shape in shapes:
        shapeWithQuality = []
        for e in shape.coordinates:
            eDeltaX = e.primitives[1].x - e.primitives[0].x
            eDeltaY = e.primitives[1].y - e.primitives[0].y

            stepX = eDeltaX / (qual + 1) 
            stepY = eDeltaY / (qual + 1) 
            shapeWithQuality.append(e.primitives[0])
            for s in range(1, qual):
                shapeWithQuality.append(Coordinate(e.primitives[0].type,
                                                   round(e.primitives[0].x + stepX * s, fAcc),
                                                   round(e.primitives[0].y + stepY * s, fAcc), 
                                                   center=e.primitives[0].center))
            shapeWithQuality.append(Coordinate(e.primitives[1].type,
                                               round(e.primitives[1].x - stepX, fAcc),
                                               round(e.primitives[1].y - stepY, fAcc),
                                               center=e.primitives[1].center))
            e.primitives = shapeWithQuality
    return shapes



def orderParts(method, shapes):
    #1 = center sort
    #2 = lowestX sort
    #3 = highestX sort
    final = []
    match method:
        case 1:
            final = sorted(shapes, key=lambda s: s.lowX)
    return final


def parseCoords(shapes, machine, fAcc):
    global constMachine
    global N
    constMachine = machine
    sortedShapes = orderParts(1, shapes)
    for shape in sortedShapes:
        for shape2 in sortedShapes[:1]:
            if shape2.highX > shape.highX or shape2.lowX < shape.lowX or shape2.lowY < shape.lowY or shape2.highY < shape.highY:
                continue
            else : 
                for e in shape2.coordinates:
                    for c in e.primitives:
                        res = shape.isInside(c)
                        print(res)

    qualitiedShapes = quality(3, sortedShapes, fAcc)  
    match constMachine:
        case "burny":
            N = 18
        case "atr":
            N = 10
    preamble()
    for shape in qualitiedShapes:
        startShape()
        for e in shape.coordinates:
            for c in e.primitives:
                match (c.type):
                    case EType.LINE:
                        handleLine(c)
                        continue
                    case EType.ARC:
                        handleArc(e.clockwise,c)
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
    postamble()
    return


def handleLine(c):
    global constMachine
    match constMachine:
        case "burny":
            outfile.write(f"N{incN()} G1 X{c.x} Y{c.y} F100\n")
        case "atr":
            #unsure how to calculate flow rate still for ATR
            outfile.write(f"N{incN()} G1 X{c.x} Y{c.y} F0.55\n")

    return
    

def handleArc(isClockwise, c):
    global constMachine
    match constMachine:
        case "burny":
            if isClockwise == True:
                outfile.write(f"N{incN()} G3 X{c.x} Y{c.y} I{c.center[0]} J{c.center[1]}\n")
            else:
                outfile.write(f"N{incN()} G2 X{c.x} Y{c.y} I{c.center[0]} J{c.center[1]}\n")
        case "atr":
            if isClockwise == True:
                outfile.write(f"N{incN()} G3 X{c.x} Y{c.y} I{c.center[0]} J{c.center[1]}\n")
            else:
                outfile.write(f"N{incN()} G2 X{c.x} Y{c.y} I{c.center[0]} J{c.center[1]}\n")
    return

def handleCircle(c):
    outfile.write(f"circle placeholder")


def preamble():
    global constMachine
    match constMachine:
        case "burny":
            outfile.write(f"""N10 %
N11 (FILE: MAXTEST.NC)
N12 (MATR: Mild Steel/Standard/1.25)
N13 (DRAWING: MaxTesting) 
N14 (DATE: I CAN WRITE WHATEVER I WANT HERE)
N15 (MACHINE: AWJ-BURNY)
N16 G70
N17 G90\n
""")
        case "atr":
            outfile.write(f"""N{incN()} G90
N{incN()} G70
N{incN()} G40\n""")
def postamble():
    global constMachine
    match constMachine:
        case "burny":
            outfile.write(f"N{incN()} M246\n")
            outfile.write(f"N{incN()} G4F.5\n")
            outfile.write(f"N{incN()} M03\n")
            outfile.write(f"N{incN()} G04 F0.5\n")
            outfile.write(f"N{incN()} G40\n")
            outfile.write(f"N{incN()} M30\n")
            outfile.write(f"N{incN()} %\n")
        case "atr":
            outfile.write(f"N{incN()} M30\n")

def startShape():
    global constMachine
    match constMachine:
        case "burny":
            outfile.write(f"(PART NAME: I CAN WRITE WHATEVER HERE)\n")
            outfile.write(f"N{incN()} M04 (ALL JET ON)\n")
            outfile.write(f"N{incN()} M245 (ALL ABR ON)\n")
            outfile.write(f"N{incN()} G4f.5 (DWELL)\n")
        case "atr":
            outfile.write(f"(PART NAME: WHATEVER)\n")
            outfile.write(f"N{incN()} G0 X1 Y1\n")
            outfile.write(f"N{incN()} M50 (ALL JET ON)\n")
            outfile.write(f"N{incN()} G41\n")
            

def endShape():
    global constMachine
    match constMachine:
        case "burny":
            outfile.write(f"N{incN()} M246\n")
            outfile.write(f"N{incN()} G4F.5\n")
            outfile.write(f"N{incN()} M03\n")
            outfile.write(f"N{incN()} G04 F0.5\n")
            outfile.write(f"N{incN()} G40\n\n")
        case "atr":
            outfile.write(f"N{incN()} M51\n")
            outfile.write(f"N{incN()} G04 P0.5\n")
            outfile.write(f"N{incN()} G40\n")
    

def incN():
    global N
    curN = N
    N += 1
    return curN