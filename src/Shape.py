from Entity import *
from Coordinate import *
import numpy as np
class Shape:
    def __init__(self, coords):  
        self.coordinates = coords
        self.size = len(self.coordinates)
        self.isChild = False
        self.children = []
        self.center = 0
        self.highX = 0
        self.lowX = 0
        self.highY = 0
        self.lowY = 0
        self.topLeft = (self.lowX, self.highY)
        self.getAttribs()
        self.ref = self.getRef()

    def getAttribs(self):
        ##average all points
        x = y = count = 0
        highX = lowX = self.coordinates[0].primitives[0]
        highY = lowY = self.coordinates[0].primitives[0]

        for e in self.coordinates:
            for c in e.primitives:
                count += 1
                x += c.x
                y += c.y
                if (c.x > highX.x):
                    highX = c
                elif (c.x < lowX.x):
                    lowX = c
                if (c.y > highY.y):
                    highY = c
                elif (c.y < lowY.y):
                    lowY = c
        self.highY = highY
        self.highX = highX
        self.lowX = lowX
        self.lowY = lowY
        self.center = Coordinate(EType.POINT, x / count, y / count)
    
    def getRef(self):
        x = y = 0
        #get lowest x and highest y (top left coord of shape) then cut in half so its offset
        #to the top left but not in the top left
        for e in self.coordinates:
            for c in e.primitives:
                rel = self.getRelativeCoord(c)
                if rel.x < x: x = rel.x
                if rel.y > y: y = rel.y
        return (x ,y)
    
    def getRelativeCoord(self, p):
        relativeP = Coordinate(p.type,0,0,p.radius,p.start,p.end,p.center)
        relativeP.x = (p.x - self.center.x)
        relativeP.y = (p.y - self.center.y)
        return relativeP
    
    def bubbleSort(self):
        swapped = False
        for i in range(self.size - 1):
            for j in range(0, self.size-i-1):
                if ((self.coordinates[j].primitives[-1].x,self.coordinates[j].primitives[-1].y) != (self.coordinates[j + 1].primitives[0].x,self.coordinates[j + 1].primitives[0].y)):
                    if ((self.coordinates[j].primitives[-1].x, self.coordinates[j].primitives[-1].y) == (self.coordinates[j + 1].primitives[-1].x,self.coordinates[j + 1].primitives[-1].y)):
                        self.coordinates[j+1].primitives[-1], self.coordinates[j+1].primitives[0] = self.coordinates[j+1].primitives[0], self.coordinates[j+1].primitives[-1]
                        self.coordinates[j + 1].clockwise = True
                    else:
                        swapped = True
                        self.coordinates[j], self.coordinates[j+1] = self.coordinates[j], self.coordinates[j+1]
            if not swapped:
                return
            
    def isInside(self, point):
        #make this more robust by instead of only drawing lines from 0, -1 do all or maybe jst 2 or 3
        #using raycasting determine if a point (generally a shapes center) is within the bounds
        #of this shape
        def onLine(line1, p):
            if (p.x <= max(line1.primitives[0].x, line1.primitives[-1].x) 
                and p.x >= min(line1.primitives[0].x, line1.primitives[-1].x) 
                and (p.y <= max(line1.primitives[0].y, line1.primitives[-1].y) 
                and p.y >= min(line1.primitives[0].y, line1.primitives[-1].y))):
                    return 1
            return 0
        
        def direction(a,b,c):
            val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
            if val == 0:
                return 0
            elif val < 0:
                return 2
            return 1
        def intersects(line1, line2):
            dir1 = direction(line1.primitives[0],line1.primitives[-1],line2.primitives[0])
            dir2 = direction(line1.primitives[0],line1.primitives[-1],line2.primitives[-1])
            dir3 = direction(line2.primitives[0],line2.primitives[-1],line1.primitives[0])
            dir4 = direction(line2.primitives[0],line2.primitives[-1],line1.primitives[-1])
            if dir1 != dir2 and dir3 != dir4: return True
            if dir1 == 0 and onLine(line1, line2.primitives[0]): return True
            if dir2 == 0 and onLine(line1, line2.primitives[-1]): return True
            if dir3 == 0 and onLine(line2, line1.primitives[0]): return True
            if dir4 == 0 and onLine(line2, line1.primitives[-1]): return True
            return False
        
        lineProjected = Entity([])
        lineProjected.primitives.append(point)
        lineProjected.primitives.append(Coordinate(EType.POINT, 9999, point.y))
        count = 0
        i = 0
        while True:
            edge = self.coordinates[i]
            if (intersects(edge, lineProjected)):
                if (direction(edge.primitives[0], point, edge.primitives[-1]) == 0):
                    return onLine(edge, point)
                count += 1

            i += 1
            if i == len(self.coordinates):
                break
        return count & 1
