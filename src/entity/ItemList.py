
import numpy as np
from .Item import Item
from .Polygon import Polygon
from src.enum import EItem


class ItemList:
    def __init__(self,
                 top_left,
                 item1: Item,
                 item2: Item,
                 item3: Item,
                 item4: Item,
                 selected_item: EItem):
        self.top_left = top_left
        self.items = [item1, item2, item3, item4] 
        self.selected_item = selected_item
        self.img_h,self.img_w = self.items[0].get_image_size()
        img_h, img_w = self.items[0].get_image_size()
        
        
        bgr_items_image = np.zeros((img_h,4 * img_w, 3), dtype=np.uint8)
        alpha_masks_image = np.zeros((img_h,4 * img_w, 1),dtype=np.float32)
        for i, item in enumerate(self.items):
            bgr_item, alpha_mask = item.get_image()
            bgr_items_image[0:img_h,i*img_w:(i+1)*img_w] = bgr_item
            alpha_masks_image[0:img_h,i*img_w:(i+1)*img_w] = alpha_mask
        self.items_image = bgr_items_image, alpha_masks_image
        self.items_size = (img_h,4 * img_w)
        items_polygons = []
        x,y = self.top_left

        for i in range(len(self.items)):
            i_top_left = (x + i * img_w, y)
            i_top_right = (x + (i + 1) * img_w,y)
            i_bottom_right = (x + (i + 1) * img_w, y + img_h)
            i_bottom_left = (x + i * img_w, y + img_h)
            item_polygon = Polygon([i_top_left, i_top_right, i_bottom_right, i_bottom_left])
            items_polygons.append(item_polygon)
        self.items_polygons = items_polygons
        
    def get_items_list_size(self):
        return self.items_size  
    def get_item_size(self):
        return self.img_h, self.img_w
    def update_selected_item(self,new_item:EItem):
        self.selected_item = new_item
    
    def get_item(self, item: EItem):
        return self.items[item.value]
    def get_items_polygons(self):
        return self.items_polygons
    def get_items_image(self):
        return self.items_image
    
    

            
    
    
