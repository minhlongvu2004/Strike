
from .Vector import Vector

class Polygon:
    def __init__(self,
                 vertices):
        self.vectors = []
        n = len(vertices)
        for i in range(n):
            self.vectors.append(Vector(vertices[i],vertices[(i+1)%n]))
        self.vertices = vertices
        
    def get_vectors(self):
        return self.vectors
    def get_vertices(self):
        return self.vertices
    
