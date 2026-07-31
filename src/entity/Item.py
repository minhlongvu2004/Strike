"""
Filename: Item.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script is for Item Object
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"

import cv2
import numpy as np
from src.other import constants as con
class Item:
    def __init__(self, 
                 name,
                 bonus_damage, 
                 image_link,
                 image_size):
        self.name = name
        self.bonus_damage = bonus_damage
        self.image_link = image_link
        self.image_size = image_size
        image = cv2.imread(self.image_link,cv2.IMREAD_UNCHANGED)

        
        self.image = cv2.resize(image, self.image_size, interpolation=cv2.INTER_AREA)
        self.image_hud = cv2.resize(image, 
                                    (con.MAIN_IMAGE_HEIGHT, con.MAIN_IMAGE_WIDTH), 
                                    interpolation=cv2.INTER_AREA)
  
    def get_name(self):
        return self.name
    def get_bonus_damage(self):
        return self.bonus_damage
    def update_name(self, new_name):
        self.name = new_name
    def update_bonus_damage(self, bonus_damage):
        self.bonus_damage = bonus_damage
    def get_image_size(self):
        return self.image_size
    
    def get_image(self):
        b, g, r, a = cv2.split(self.image)
        bgr_item = cv2.merge((b, g, r))
        alpha_mask = a / 255.0  # Normalize to 0-1 range
        # mask now is only 2D array, we have to convert it to 3D
        # 
        alpha_mask = alpha_mask[:, :, np.newaxis]
        return bgr_item, alpha_mask
    def get_hud_image(self):
            b, g, r, a = cv2.split(self.image_hud)
            bgr_item = cv2.merge((b, g, r))
            alpha_mask = a / 255.0  # Normalize to 0-1 range
            # mask now is only 2D array, we have to convert it to 3D
            # 
            alpha_mask = alpha_mask[:, :, np.newaxis]
            return bgr_item, alpha_mask
        