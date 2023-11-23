from Coordinate import *

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
def plotShapes(coords):
    x = []
    y = []
    for shape in coords:
        for child in shape.children:
            for e in child.coordinates:
                for c in e.primitives:
                    x.append(c.x)
                    y.append(c.y)
        for e in shape.coordinates:
            for c in e.primitives:
                x.append(c.x)
                y.append(c.y)
    plt.scatter(x,y)
    plt.show()

def plotCoords(coords, label=""):
    x = []
    y = []
    for e in coords:
        for c in e.primitives:
            x.append(c.x)
            y.append(c.y)
    plt.scatter(x,y)
    plt.xlabel(label)
    plt.show()
    
def plotEnts(e, label=""):
    x = []
    y = []
    for c in e.primitives:
        x.append(c.x)
        y.append(c.y)
    plt.scatter(x,y)
    plt.xlabel(label)
    plt.show()

def plotXYIJ(shapes):
    def plotAll(data):
        for ind in range(len(data)):
            p1 = data[ind].primitives[0]
            p2 = data[ind].primitives[-1]
            i = p1.center.x; j = p1.center.y
            startAngle = p1.angle
            endAngle = p2.angle
            rad = np.sqrt((i - p1.x)**2 + (j - p1.y)**2)
            startAngle = np.deg2rad(startAngle)
            endAngle = np.deg2rad(endAngle)
   

            theta = np.linspace(endAngle, startAngle, 100)
            arcX = i + rad * np.cos(theta)
            arcY = j + rad * np.sin(theta)
            plt.text(p1.x +.2, p1.y, ind, color="black")
            plt.text(p2.x +.7, p2.y, ind + .2, color="red")
            plt.plot(arcX, arcY, color ='green')
    xyij = []
    x = []
    y = []
    col = "blue"
    for shape in shapes:
        for e in shape.coordinates:
            for c in e.primitives:
                x.append(c.x)
                y.append(c.y)
            if e.primitives[0].type == EType.ARC:
                xyij.append(e)
                continue
            elif e.primitives[0].type == EType.CIRCLE:
                theta = np.linspace(0, 2*np.pi, 100)
                px = e.primitives[0].center.x + e.primitives[0].radius*np.cos(theta)
                py = e.primitives[0].center.y + e.primitives[0].radius*np.sin(theta)
                plt.plot(px, py, color=col)
            elif e.primitives[0].type == EType.LINE:
                px = [e.primitives[0].x, e.primitives[-1].x]
                py = [e.primitives[0].y, e.primitives[-1].y]
                plt.plot(px,py, color=col)
    col = "yellow"
    for shape in shapes:
        for child in shape.children:
            for e in child.coordinates:
                for c in e.primitives:
                    x.append(c.x)
                    y.append(c.y)
                if e.primitives[0].type == EType.ARC:
                    xyij.append(e)
                    continue
                elif e.primitives[0].type == EType.CIRCLE:
                    theta = np.linspace(0, 2*np.pi, 100)
                    px = e.primitives[0].center.x + e.primitives[0].radius*np.cos(theta)
                    py = e.primitives[0].center.y + e.primitives[0].radius*np.sin(theta)
                    plt.plot(px, py, color=col)
                elif e.primitives[0].type == EType.LINE:
                    px = [e.primitives[0].x, e.primitives[-1].x]
                    py = [e.primitives[0].y, e.primitives[-1].y]
                    plt.plot(px,py, color=col)
    plt.scatter(x, y, label='Points')
    plotAll(xyij)
    plt.show()
