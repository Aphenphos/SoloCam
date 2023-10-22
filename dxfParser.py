import ezdxf
import sys
import math
import statistics

from ezdxf.math import Vec3
from Coordinate import *
from Shape import *
from Entity import *

def getCoords(dxfFile):
    global coords
    try:
        source = ezdxf.readfile(dxfFile)
    except IOError:
        print("Not a DXF file or generic IO Err")
    except ezdxf.DXFStructureError:
        print("Invalid or corrupt DXF File")
        sys.exit(2)
        
    coords = []
    msp = source.modelspace()
    for e in msp:
        if e.dxftype() == 'LWPOLYLINE':
            e.explode()
        getCoordsFromE(e)

    offsetX, offsetY = offsetCoords()
    offsetAllXY(offsetX, offsetY)
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
                if c.center[0] < lowestX:
                    lowestX = c.center[0]
                if c.center[1] < lowestY:
                    lowestY = c.center[1]
    return (abs(lowestX), abs(lowestY))

def offsetAllXY(xOffset, yOffset):
    global coords
    for e in coords:
        for c in e.primitives:
            if c.type == EType.END:
                break
            c.x = round(c.x + xOffset, 3)
            c.y = round(c.y + yOffset, 3)
            if c.type == EType.ARC or c.type==EType.CIRCLE:
                c.center = [c.center[0] + xOffset, c.center[1] + yOffset]
    return

def getCoordsFromE(e):
    global coords
##  Step defines accuracy of an arc or circle (Lower is more accurate)
    step = 180
    match e.dxftype():
        case 'LINE':
##              Append start and end of line back to back
            coords.append(Entity(Coordinate(
                EType.LINE,
                e.dxf.start.x,
                e.dxf.start.y, 
            ), (Coordinate(
                EType.LINE,
                e.dxf.end.x,
                e.dxf.end.y,
            ))))
        case 'ARC':
            center = [e.dxf.center.x, e.dxf.center.y]
            radius = e.dxf.radius
            start = Vec3.from_deg_angle(e.dxf.start_angle, radius)
            end = Vec3.from_deg_angle(e.dxf.end_angle, radius)

            startPoint = start + center
            endPoint = end + center
            coords.append(Entity(Coordinate(
                EType.ARC,
                startPoint.x,
                startPoint.y,
                radius,
                center=center,
            ), (Coordinate(
                EType.ARC,
                endPoint.x,
                endPoint.y,
                radius,
                center=center,
            ))))
        case 'CIRCLE':
            ent = Entity(None,None)
            center = [e.dxf.center.x, e.dxf.center.y]
            radius = e.dxf.radius
            for a in range(2):
                if (a == 0):
                    x = center[0] + radius * math.cos(math.radians(a))
                    y = center[1] + radius * math.sin(math.radians(a))
                    ent.primitives[0] = (Coordinate(
                        EType.CIRCLE,
                        x,
                        y,
                        radius,
                        center = center,
                    ))

                if (a == 1):
                    ent.primitives.append((Coordinate(
                        EType.CIRCLE,
                        x,
                        y,
                        radius,
                        center = center,
                    )))    
                    coords.append(ent)   
                    break     
                ent.primitives[1] = Coordinate(
                    EType.CIRCLE,
                    x = center[0] + radius * math.cos(math.pi / 2),
                    y = center[1] + radius * math.sin(math.pi / 2),
                    radius = radius,
                    center = center
                )
            return

def isOneShape():
    global coords
    start = None
    #True for first False for second
    first = True
    end = False
    def isClose(coordinate):
        if math.isclose(start.x, coordinate.x, abs_tol=1e-3) and math.isclose(start.y, coordinate.y, abs_tol=1e-3):
            return True
    for e in coords:
        for c in e.primitives:
            if start == None:
                start = c
                c.start = True
                continue
            if end == True:
                start = None
                c.end = True
                end = False
                continue
            if c.type == EType.ARC:
                if first == True and isClose(c):
                    end = True
                    first = not first
                    continue
                elif first == False and isClose(c):
                    end = False
                    start = None
                    c.end = True
                    first = not first
                    continue
            if isClose(c):
                start = None
                c.end = True
                continue
    return

def sortClockwise():
    global coords
    shape = []
    sorted = []
    for e in coords:
        shape.append(e)
        for c in e.primitives:
            if c.end == True:
                shape = Shape(shape)
                shape.bubbleSort()
                sorted.append(shape)

                shape = []
                continue
        
    coords = sorted
        

                
