from Coordinate import *
from Code import *
from Shape import *
from Visualise import *
import copy
#I and J are determined by subtracting the center of the arc from start xy
#how flow rate is determined I am unsure.
outfile = open("./tests/OUT.CNC", "w")
global constMachine
global N
N = 0
constMachine = None
def generateLeadInOut(shape):
    #default tab location will be the leftmost highest point.
    if shape.children:
        for child in shape.children:
            generateLeadInOut(child)
    startX = shape.coordinates[0].primitives[0].x - .125
    startY = shape.coordinates[0].primitives[0].y - .125

    endX = shape.coordinates[0].primitives[0].x - .125
    endY = shape.coordinates[0].primitives[0].y + .125
    if shape.isChild:
        startX = shape.coordinates[0].primitives[0].x + .125
        startY = shape.coordinates[0].primitives[0].y - .125

        endX = shape.coordinates[0].primitives[0].x + .125
        endY = shape.coordinates[0].primitives[0].y + .125

    shape.coordinates[0].primitives.insert(0,Coordinate(EType.LINE, startX, startY))
    shape.coordinates[-1].primitives.append(Coordinate(EType.LINE, endX, endY))

def orderParts(method, shapes):
    #1 = center sort
    #2 = lowestX sort
    #3 = highestX sort
    final = []
    match method:
        case 1:
            final = sorted(shapes, key=lambda s: s.lowX.x)
    return final


def parseCoords(shapes, machine, fAcc):
    global constMachine
    global N
    constMachine = machine
    sortedShapes = orderParts(1, shapes)
    sortedLen = len(sortedShapes)
    nestedShapes = []
    #for each shape determine if a shape is inside by raycasting.
    for i in range(sortedLen):
        shape1 = sortedShapes[i]
        for j in range(sortedLen):
            if i == j:
                continue  
            shape2 = sortedShapes[j]
            if shape2.lowX.x > shape1.highX.x or shape2.highX.x < shape1.lowX.x or shape2.lowY.y > shape1.highY.y or shape2.highY.y < shape1.lowY.y:
                continue
            result = shape1.isInside(shape2.center)
            if ((result % 2) != 0):
                sortedShapes[j].isChild = True
                sortedShapes[i].children.append(copy.deepcopy(sortedShapes[j]))
                continue


    for shape in sortedShapes:
        if shape.isChild:
            continue
        else:
            nestedShapes.append(shape)
    
    plotXYIJ(nestedShapes)
    for shape in nestedShapes:
        generateLeadInOut(shape)
    
    match constMachine:
        case "burny":
            N = 18
        case "atr":
            N = 10
    preamble()
    for shape in nestedShapes:
        if (shape.children):
            for child in shape.children:
                handleShape(child)
        handleShape(shape)
    postamble()
    return

def handleShape(shape):
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
                outfile.write(f"N{incN()} G3 X{c.x} Y{c.y} I{c.center.x} J{c.center.y}\n")
            else:
                outfile.write(f"N{incN()} G2 X{c.x} Y{c.y} I{c.center.x} J{c.center.y}\n")
        case "atr":
            if isClockwise == True:
                outfile.write(f"N{incN()} G3 X{c.x} Y{c.y} I{c.center.x} J{c.center.y}\n")
            else:
                outfile.write(f"N{incN()} G2 X{c.x} Y{c.y} I{c.center.x} J{c.center.y}\n")
    return

def handleCircle(c):
    handleArc(False, c)


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