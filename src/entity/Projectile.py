import math
from src.enum import EStatus
import cv2
from .Item import Item
from .User import User


class Projectile:
    def __init__(self,
                 main_user: User, 
                 skill_item: Item,
                 step, 
                 image_path, 
                 size 
                 ):
        self.main_user = main_user
        self.skill_item = skill_item
        self.status = EStatus.STAYING
        self.image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        self.step = step
        self.size = size  
        self.count = 0
        self.colliding_face = 0
        self.colliding_user = None
        
        
    def update_colliding_user(self,colliding_user):
        self.colliding_user = colliding_user
    def update_colliding_face(self,colliding_face):
        self.colliding_face = colliding_face
    def get_colliding_face(self):
        return self.colliding_face
    def get_colliding_user(self):
            return self.colliding_user
        
        
    def get_item(self):
        return self.skill_item
    def get_user(self):
        return self.main_user
    def get_image(self):
        return self.image
    
    def update_count(self, new_count):
        self.count = new_count
        
    def get_count(self):
        return self.count
    
    def update_size(self,size):
        self.size = size
        
    def get_size(self):
        return self.size
    
    def get_status(self):
        return self.status
    
    def update_image(self,image_path):
        self.image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    def get_coordinates(self):
        x = self.position[0]
        y = self.position[1]
        s = self.size
        top_left = (x - s, y - s)
        top_right = (x + s, y- s)
        bottom_left = (x - s, y + s)
        bottom_right = (x + s, y + s)
        return [top_left, top_right, bottom_right, bottom_left]

    # setter
    def update_position(self, new_position):
        self.position = new_position
        
    def update_direction(self, new_direction):
        # only take the unit to remove the unexpected speed
        length = math.sqrt(new_direction[0]**2 + new_direction[1]**2)
        
        self.direction = (new_direction[0]/ length,
                            new_direction[1]/ length)
        
    def update_status(self, new_status):
        self.status = new_status
        
    def fire(self, img_shape):
        if self.status == EStatus.MOVING:
        # P(x_0,y_0) is the point of current position
        # assume vector position is OP and direction is d
        # new_position = OP + t * d = (x_0,y_0) + t(a,b) 
        # = (x_0+ta,y_0+tb)
        # where t is the step
     
            new_position = (round(self.position[0] + self.direction[0] * self.step),
                            round(self.position[1] + self.direction[1] * self.step))
        
            self.update_position(new_position)
            
            self.check_exceed_frame(img_shape)
        
    def check_exceed_frame(self,img_shape):
        
        '''
        check if the projectile is out of the frame
        '''
        h, w,_ = img_shape
        c_x, c_y = self.position
        s = self.size
        x_0 = c_x - s
        x_1 = c_x + s
        y_0 = c_y - s
        y_1 = c_y + s
        
        if x_1 <= 0 or y_1 <= 0 or x_0 >= w or y_0 >= h:
            self.status = EStatus.DYING
    