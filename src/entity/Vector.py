import math


class Vector:
    def __init__(self,
                 vertex1,
                 vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.vector = (vertex2[0] - vertex1[0],
                       vertex2[1] - vertex1[1])
        self.length = math.dist(vertex1, vertex2)
        
        if self.length != 0:
            self.unit = (self.vector[0] / self.length,
                        self.vector[1] / self.length)
        else:
            self.unit = (0,0)
    def get_unit(self):
        return self.unit