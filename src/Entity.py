from Coordinate import EType
class Entity:
     def __init__(self, primitives):
          self.primitives = primitives
          self.clockwise = False
     def determineClockwise(self):
          if self.primitives[0].type == EType.ARC:
               sp = self.primitives[0]
               mp = self.primitives[5]
               ep = self.primitives[-1]
               se = (ep.x - sp.x, ep.y - sp.y)
               sm = (mp.x - sp.x, mp.y - sp.y) 
               crossProduct = se[0] * sm[1] - se[1] * sm[0]
               if crossProduct <= 0:
                    self.clockwise = True
               else:
                    self.clockwise = False
     def start(self):
          if not self.clockwise:
               return self.primitives[0]
          else: return self.primitives[-1]
     def end(self):
          if not self.clockwise:
               return self.primitives[-1]
          else: return self.primitives[0]