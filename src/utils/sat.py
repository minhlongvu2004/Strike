
from src.entity import Polygon


class SAT:
    # SAT: Seperating Axis Theorem
        
    @staticmethod
    def check_collide(polygon1: Polygon,
                      polygon2: Polygon):
        all_vectors = polygon1.get_vectors() + polygon2.get_vectors()
        for vector in all_vectors:
            unit = vector.get_unit()
            pro1 = SAT.project_axis(unit, polygon1)
            pro2 = SAT.project_axis(unit, polygon2)
            if pro1[1] < pro2[0] or pro2[1] < pro1[0]:
                return False
            
        return True
   

    @staticmethod
    def project_axis(unit, polygon: Polygon):
        
        '''
        project_axis: 
        
        unit: the target axis
        polygon: The polygon we want to project on the axis
        
        return: return a point (min, max) on that axis
        '''
        dot_products = []
        vertices = polygon.get_vertices()
        # each point (a,b) itself is a vecotr from (0,0) to (a,b)
        for vertex in vertices:
            dot_product = vertex[0] * unit[0] + vertex[1] * unit[1]
            dot_products.append(dot_product)
        # each product is the new coordiate on the axis, so we can
        # apply min max directly
        return (min(dot_products), max(dot_products))
        
        