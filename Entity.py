class Entity:
     def __init__(self, c1, c2, primitives = [], clockwise = False):
          self.primitives = [c1,c2]
          self.clockwise = clockwise
     def addpoint(self, point):
          self.primitives.insert(1,point)