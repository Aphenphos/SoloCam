import ezdxf
import sys
import math

from ezdxf.math import Vec3
from Coordinate import *
from Shape import *
from Entity import *
from Visualise import *

global fPointAcc
def getCoords(dxfFile, machine, fAcc, quality):
    global coords
    global fPointAcc 
    fPointAcc= fAcc
    try:
        source = ezdxf.readfile(dxfFile)
    except IOError:
        print("Not a DXF file or generic IO Err")
    except ezdxf.DXFStructureError:
        print("Invalid or corrupt DXF File")
        sys.exit(2)
        
    coords = []
    count = 0
    for block in source.blocks:
        for e in block:
            match e.dxftype():
                case 'LWPOLYLINE' | 'POLYLINE':
                    count+=1
                    for p in e.virtual_entities():
                        getCoordsFromE(p)
                case 'CIRCLE' | 'LINE' | 'ARC':
                    getCoordsFromE(e)

    plotCoords(coords)
    offsetX, offsetY = offsetCoords()
    offsetAllXY(offsetX, offsetY, machine)
    #parse the shapes
    isOneShape()
    sortClockwise()
    out = open(f"{dxfFile}Out.txt", "w")
    for shape in coords:
        for e in shape.coordinates:
            for c in e.primitives:
                out.write(c.toFile())
                if c.end == True:
                    out.write("\n")
    out.close()
    return coords


#Find the lowest point and offset all coordinates by it and add 1 to ensure its
#in the positive plane
def offsetCoords():
    global coords
    lowestX = 0
    lowestY = 0
    for e in coords:
        for c in e.primitives:
            if c.x < lowestX:
                lowestX = c.x
            if c.y < lowestY:
                lowestY = c.y
            if c.type == EType.ARC or c.type == EType.CIRCLE:
                if c.center.x < lowestX:
                    lowestX = c.center.x
                if c.center.y < lowestY:
                    lowestY = c.center.y
    return (abs(lowestX), abs(lowestY))

def offsetAllXY(xOffset, yOffset, machine):
    global fPointAcc
    global coords
    for e in coords:
        for c in e.primitives:
            if c.type == EType.END:
                break
            c.x = round(c.x + xOffset + 1, 6)
            c.y = round(c.y + yOffset + 1, 6)
            if c.type == EType.ARC or c.type==EType.CIRCLE:
                c.center = Coordinate(EType.POINT, round(c.center.x + xOffset + 1, 6), round(c.center.y + yOffset + 1, 6))
    return


def getCoordsFromE(e):
    global coords
##  Step defines accuracy of an arc or circle (Lower is more accurate)
    match e.dxftype():
        case 'LINE':
            ent = Entity([])
            step = 5
            stepX = (e.dxf.end.x - e.dxf.start.x) / step
            stepY = (e.dxf.end.y - e.dxf.start.y) / step
        
            ent.primitives.append(Coordinate(
                EType.LINE,
                e.dxf.start.x,
                e.dxf.start.y, 
                start=True
            ))
            for s in range(1, step):
                ent.primitives.append(Coordinate(
                    EType.LINE,
                    x = e.dxf.start.x + (stepX * s),
                    y = e.dxf.start.y + (stepY * s)
                ))
            ent.primitives.append(Coordinate(
                EType.LINE,
                e.dxf.end.x,
                e.dxf.end.y,
                end=True
            ))
            coords.append(ent)
        case 'ARC':
            #Reverse arc entities order as arcs are inherently stored counterClockwise
            step = 10
            center = Coordinate(EType.POINT,e.dxf.center.x, e.dxf.center.y)
            ent = Entity([])
            ent.primitives.append(Coordinate(
                EType.ARC,
                e.start_point.x,
                e.start_point.y,
                e.dxf.radius,
                center=center,
                start=True,
                angle=e.dxf.start_angle
            )) 
            for angle in list(e.angles(step))[1:-1]:
                ent.primitives.append(Coordinate(
                    EType.ARC,
                    x = (Vec3.from_deg_angle(angle, e.dxf.radius) + [center.x, center.y]).x,
                    y = (Vec3.from_deg_angle(angle, e.dxf.radius) + [center.x, center.y]).y,
                    radius = e.dxf.radius,
                    center = center
                ))
            ent.primitives.append(Coordinate(
                EType.ARC,
                e.end_point.x,
                e.end_point.y,
                e.dxf.radius,
                center=center,
                end=True,
                angle=e.dxf.end_angle
            ))
            ent.primitives.reverse()
            ent.determineClockwise()
            coords.append(ent)
        case 'CIRCLE':
            ent = Entity([])
            center =  Coordinate(EType.POINT,e.dxf.center.x, e.dxf.center.y)
            step = 10
            ent.primitives.append(Coordinate(
                EType.CIRCLE,
                x = (Vec3.from_deg_angle(0, e.dxf.radius) + [center.x, center.y]).x,
                y = (Vec3.from_deg_angle(0, e.dxf.radius) + [center.x, center.y]).y,
                radius=e.dxf.radius,
                center = center,
                start=True
            ))   
            for s in range(1, step):
                x = (Vec3.from_deg_angle(s*36, e.dxf.radius) + [center.x, center.y]).x
                y = (Vec3.from_deg_angle(s*36, e.dxf.radius) + [center.x, center.y]).y
                ent.primitives.append(Coordinate(
                    EType.CIRCLE,
                    x,
                    y,
                    e.dxf.radius,
                    center = center,
                ))   
            ent.primitives.append(Coordinate(
                EType.CIRCLE,
                x = (Vec3.from_deg_angle(350, e.dxf.radius) + [center.x, center.y]).x,
                y = (Vec3.from_deg_angle(350, e.dxf.radius) + [center.x, center.y]).y,
                radius=e.dxf.radius,
                center = center,
                end=True
            ))   
            coords.append(ent)   
            return


#Parses through coordinates looking for connecting points if a "loop" is made 
#add the shape to the array
def isOneShape():
    global coords
    toShapes = []
    used = []
    shape = [None]
    i = 0
    length = len(coords)
    def isClose(p1, p2):
        if math.isclose(p1.x, p2.x) and math.isclose(p1.y, p2.y):
            return True
    def findNextEnt():
        for j in range(length):
            if j in used or coords[j].start().type == EType.CIRCLE:
                continue
            if (isClose(coords[j].start(), shape[-1].end()) or isClose(coords[j].end(), shape[-1].end())) or \
                (isClose(coords[j].start(), shape[-1].start()) or isClose(coords[j].end(), shape[-1].start())):
                used.append(j)
                shape.append(coords[j])
                return True
        print("Could not find next Entity.")
        quit()
    while (i < length):
        if coords[i].start().type == EType.CIRCLE:
            toShapes.append(Shape([coords[i]]))
            used.append(i)
            i+=1
            continue
        if shape[0] == None:
            shape[0] = coords[i]
            used.append(i)
            i+=1
        findNextEnt()
        i+=1
        if len(shape) > 2:
            if (isClose(shape[0].start(), shape[-1].end()) or isClose(shape[0].end(), shape[-1].end())) or \
                (isClose(shape[0].start(), shape[-1].start()) or isClose(shape[0].end(), shape[-1].start())):
                print("shape completed")
                toShapes.append(Shape(shape))
                shape = [None]
                continue
        if len(used) == length:
            break

    # for e in coords:

    #     if e.primitives[0].type == EType.CIRCLE:
    #         toShapes.append(Shape([e]))
    #         shape = []
    #         start = None
    #         continue

    #     shape.append(e)
    #     if start == None:
    #         start = e.primitives[0]
    #         e.primitives[0].start = True
    #         continue
    #     if isClose(e.primitives[0]):
    #         e.primitives[0].end = True
    #         toShapes.append(Shape(shape))
    #         start = None
    #         shape = []
    #         continue
    #     if isClose(e.primitives[-1]):
    #         e.primitives[-1].end = True
    #         toShapes.append(Shape(shape))
    #         start = None
    #         shape = []
    #         continue
    coords = toShapes
    # for f in coords:
    #     plotShapes([f])
    return

def sortClockwise():
    global coords
    for shape in coords:
        shape.bubbleSort()
    return
        

                
