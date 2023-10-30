from numba import jit, njit
import numba
import numpy as np
from Entity import *
from Coordinate import *

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
    # def sortClockwise(self):
    #     global prevP
    #     prevP = False

    #     def angleAndDist(e):
    #         global prevP
    #         if (prevP == False):
    #             p = e.primitives[0]
    #             prevP = not prevP
    #         if (prevP):
    #             p = e.primitives[1]
    #             prevP = not prevP
    #             #determine which coordinate to sort by here.
    #             #scale everything to its own coordinates (Polar coordinates I think its called)
    #         relative = self.getRelativeCoord(p)
    #         #get each coord length and if 0 its a straight line.
    #         lengthOfCoord = math.hypot(relative.x, relative.y)
    #         if (lengthOfCoord == 0): return -math.pi, 0
    #         normalized = [relative.x/lengthOfCoord, relative.y/lengthOfCoord]
    #         dotProd = normalized[0]*self.ref[0] + normalized[1]*self.ref[1]
    #         diffProd = self.ref[1]*normalized[0] - self.ref[0]*normalized[1]
    #         #magic
    #         angle = math.atan2(diffProd, dotProd)
    #         if angle < 0:
    #             return 2*math.pi + angle, lengthOfCoord
    #         return angle, lengthOfCoord
        

    #     self.coordinates = sorted(self.coordinates, key=angleAndDist)


    def getAttribs(self):
        ##average all points
        x = 1
        y = 1
        highX = lowX = self.coordinates[0].primitives[0].x
        highY = lowY = self.coordinates[0].primitives[0].y

        for e in self.coordinates:
            for c in e.primitives:
                x += c.x
                y += c.y
                if (c.x > highX):
                    highX = c.x
                elif (c.x < lowX):
                    lowX = c.x
                if (c.y > highY):
                    highY = c.y
                elif (c.y < lowY):
                    lowY = c.y
        self.highY = highY
        self.highX = highX
        self.lowX = lowX
        self.lowY = lowY
        self.center =  (x / self.size, y / self.size)

    

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
        relativeP.x = (p.x - self.center[0])
        relativeP.y = (p.y - self.center[1])
        return relativeP
    
    def bubbleSort(self):
        swapped = False
        for i in range(self.size - 1):
            for j in range(0, self.size-i-1):
                if ((self.coordinates[j].primitives[1].x,self.coordinates[j].primitives[1].y) != (self.coordinates[j + 1].primitives[0].x,self.coordinates[j + 1].primitives[0].y)):
                    if ((self.coordinates[j].primitives[1].x, self.coordinates[j].primitives[1].y) == (self.coordinates[j + 1].primitives[1].x,self.coordinates[j + 1].primitives[1].y)):
                        self.coordinates[j+1].primitives[1], self.coordinates[j+1].primitives[0] = self.coordinates[j+1].primitives[0], self.coordinates[j+1].primitives[1]
                        self.coordinates[j + 1].clockwise = True
                    else:
                        swapped = True
                        self.coordinates[j], self.coordinates[j+1] = self.coordinates[j], self.coordinates[j+1]
            if not swapped:
                return
            
    def isInside(self, point):
        if (point.x >= self.highX or point.x <= self.lowX or point.y >= self.highY or point.y <= self.lowY):
            return False
        count = 0
        for edge in self.coordinates:
            (x1,y1) = edge.primitives[0].x, edge.primitives[0].y        
            (x2,y2) = edge.primitives[1].x, edge.primitives[1].y
            if (point.y < y1) != (point.y < y2) and  point.x < x1 + ((point.y-y1)/(y2-y1))*(x2-x1):
                    count+=1
        return count%2 == 1


