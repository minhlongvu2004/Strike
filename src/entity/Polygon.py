
"""
Filename: Polygon.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script is for Polygon Object
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"
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
    
