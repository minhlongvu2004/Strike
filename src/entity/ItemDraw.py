"""
Filename: ItemDraw.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script is an extension of Item Object
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"

import numpy as np
import cv2
from .Item import Item
class ItemDraw(Item):
    def __init__(self, 
                 name,
                 bonus_damage, 
                 image_link,
                 image_size,
                 border_thickness):
        super().__init__(name,
                         bonus_damage,
                         image_link,
                         image_size)
        self.thick = border_thickness
        self.associate_image()
        image = self.get_image()
        # for my experience, this make the gun brighter
        self.img_h, self.img_w, _ = image.shape
        self.container_h = self.img_h + 2 * self.thick
        self.container_w = self.img_w + 2 * self.thick
    
    def associate_rectangle_imge(self):
        lighter = 30
        reg_container = np.zeros( (self.container_h, self.container_w,3), dtype=np.uint8)
        sel_container = np.zeros( (self.container_h, self.container_w,3), dtype=np.uint8)
        
        top_left = (0,0)
        bottom_right = (self.container_w, self.container_h)
        
        # Regular rectangle
        cv2.rectangle(reg_container, top_left, bottom_right, (0,102,0), -1)
        
        reg_container[self.thick: self.thick + self.img_w,
                  self.thick: self.thick + self.img_h] = self.image + lighter
        self.rec_img = reg_container
        
        # selected rectangle
        
        cv2.rectangle(sel_container, top_left, bottom_right, (150, 255, 150), -1)
        
        sel_container[self.thick: self.thick + self.img_w,
                  self.thick: self.thick + self.img_h] = self.image+ lighter
        self.sel_img = sel_container
    
        
        
    def get_rec_img(self):
        return self.rec_img
    def get_sel_img(self):
        return self.sel_img
        
        
        