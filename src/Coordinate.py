from enum import Enum


class EType(Enum):
    END = 0
    POINT = 1
    LINE = 2
    LWPOLYLINE = 3
    ARC = 4
    CIRCLE = 5


class Coordinate:
    def __init__(self, type, x, y, radius = None, start = None, end = None, center=None, angle=None):
        self.type = type
        self.x = x
        self.y = y
        self.radius = radius
        self.start = start
        self.end = end
        self.center = center
        self.angle = angle
    
    def toFile(self):
        match (self.type):
            case EType.LINE:
                if (self.isStart()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} START\n"
                if (self.isEnd()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} END\n"
                return f"TYPE:{self.type.name} X:{self.x} Y:{self.y}\n"
            case EType.LWPOLYLINE:
                if (self.isStart()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} START\n"
                if (self.isEnd()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} END\n"
                return f"TYPE:{self.type.name} X:{self.x} Y:{self.y}\n"
            case EType.ARC:
                if (self.isStart()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} RADIUS:{self.radius} CENTER {self.center} START\n"
                if (self.isEnd()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} RADIUS:{self.radius} CENTER {self.center} END\n"
                return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} RADIUS:{self.radius} CENTER {self.center} \n"
            case EType.CIRCLE:
                if (self.isStart()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} RADIUS:{self.radius} CENTER{self.center} START\n"
                if (self.isEnd()):
                    return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} RADIUS:{self.radius} CENTER{self.center} END\n"
                return f"TYPE:{self.type.name} X:{self.x} Y:{self.y} RADIUS:{self.radius} CENTER{self.center}\n"                
            case EType.END:
                return "TYPE:END"
    def isStart(self):
                return self.start == True
    def isEnd(self):
                return self.end == True