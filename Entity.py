class Entity:
     def __init__(self, c1, c2, primitives = []):
          self.primitives = [c1,c2]
     def addpoint(self, point):
          self.primitives.insert(1,point)