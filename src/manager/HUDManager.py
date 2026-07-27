import math

import cv2
import numpy as np

from src.enum import EItem
from src.entity import ItemList, Polygon, User
from src.utils import SAT
from src.other import constants as con


class HUDManager:
    def __init__(self,
                 selected_eitem: EItem,
                 item_list: ItemList,
                 main_user: User,
                 hud_top_left,
                 items_list_top_left,
                 open_item_list: bool):
        self.selected_eitem = selected_eitem
        self.item_list = item_list
        self.main_user = main_user
        self.hud_top_left = hud_top_left
        self.items_list_top_left = items_list_top_left
        self.open_item_list = open_item_list # True/False to open ItemList
        self.start_count = cv2.getTickCount()
        
        # I'm honest that I cheat it a little bit by making the hitbox bigger
        x,y = hud_top_left
        img_tl = (x+ con.ADDITIONAL_SIZE, 
                  y + con.ADDITIONAL_SIZE)
        img_tr = (img_tl[0] + con.MAIN_IMAGE_WIDTH + 4 * con.ADDITIONAL_SIZE,
                  img_tl[1])
        img_br = (img_tr[0], 
                  img_tr[1] + con.MAIN_IMAGE_HEIGHT + 4 * con.ADDITIONAL_SIZE)
        
        img_bl = (img_tl[0], img_tl[1] + con.MAIN_IMAGE_HEIGHT + 4 * con.ADDITIONAL_SIZE)
        
        self.img_hud_polygon = Polygon([img_tl,img_tr,img_br,img_bl]) 
    def get_image_hud_polygon(self):
        return self.img_hud_polygon
    def get_selected_eitem(self):
        return self.selected_eitem
    def get_item(self):
        return self.item_list.get_item(self.get_selected_eitem())
        
    def check_if_select_items_list(self, 
                                 current_gesture,
                                 if_polygon):
        items_polygon = self.item_list.get_items_polygons()
        if current_gesture == "click" and \
            if_polygon is not None and\
                self.open_item_list:
                    # item_position
            for item, item_polygon in zip(EItem, items_polygon):
  
                if SAT.check_collide(item_polygon,
                                    if_polygon):
                    self.selected_eitem = item
                    
    def check_if_click_item_hud(self,
                                 current_gesture,
                                 if_polygon:Polygon):
        img_polygon = self.get_image_hud_polygon()
        
        if current_gesture == "click" and if_polygon is not None:
                    # item_position
            time = (cv2.getTickCount() - self.start_count) * 1000 / cv2.getTickFrequency() 
            if SAT.check_collide(img_polygon,
                                if_polygon):
                if time > 500:
                    # Usually an click span for 3-4 frames, so this is to avoid 
                    # mis activate click again
                    status = self.open_item_list
                    self.start_count = cv2.getTickCount()
                    self.open_item_list = con.CLOSE_LIST \
                        if status == con.OPEN_LIST else con.OPEN_LIST 
    
    
    def draw_mu_hud(self, frame):
        main_user = self.main_user
        hud_top_left = self.hud_top_left
        
        rect_w =  con.MAIN_IMAGE_WIDTH + con.MAIN_HOR_BAR_LENGTH + 5 * con.ADDITIONAL_SIZE
        rect_h = con.MAIN_IMAGE_WIDTH + con.MAIN_HOR_BAR_THICK + 4 * con.ADDITIONAL_SIZE
        roi = frame[hud_top_left[1]: hud_top_left[1] + rect_h,
                    hud_top_left[0] : hud_top_left[0] + rect_w]
        
        img_tl = (con.ADDITIONAL_SIZE, con.ADDITIONAL_SIZE)
        img_br = (img_tl[0] + con.MAIN_IMAGE_WIDTH, 
                img_tl[1] + con.MAIN_IMAGE_HEIGHT)
        
        hp_p1 = (img_br[0] + 2 * con.ADDITIONAL_SIZE,
                img_tl[1] + 2 * con.ADDITIONAL_SIZE)
        hp_p2 = (hp_p1[0] + con.MAIN_HOR_BAR_LENGTH, hp_p1[1])
        
        mp_p1 = (hp_p1[0],
                img_br[1] - 2 * con.ADDITIONAL_SIZE)
        mp_p2 = (hp_p2[0], mp_p1[1])
        mask_neon = np.zeros_like(roi,dtype=np.uint8)
        cv2.rectangle(roi, img_tl,img_br, con.SEL_OUTER_BG_COLOR, -1)
        cv2.rectangle(roi, img_tl,img_br, con.SEL_OUTER_BD_COLOR, 1)
        img, mask = self.item_list.get_item(self.selected_eitem).get_hud_image()
        roi[img_tl[1]:img_br[1],img_tl[0]:img_br[0]] = \
            (1-mask) * roi[img_tl[1]:img_br[1],img_tl[0]:img_br[0]] +\
                mask * img
        
        # draw bar
        hp_ratio = main_user.get_hp() / con.FULL_HP
        mp_ratio = main_user.get_mp() / con.FULL_MP
        distance = math.dist(hp_p1, hp_p2)
        curr_hp_p2 = (hp_p1[0] + int(distance * hp_ratio), hp_p1[1] )
        curr_mp_p2 = (mp_p1[0] + int(distance * mp_ratio), mp_p1[1] )
        
        cv2.line(roi, hp_p1, hp_p2, con.DEFAULT_BAR_COLOR, con.MAIN_HOR_BAR_THICK)
        cv2.line(roi, mp_p1, mp_p2, con.DEFAULT_BAR_COLOR, con.MAIN_HOR_BAR_THICK)
        
        cv2.line(mask_neon, hp_p1, curr_hp_p2, con.HP_OUTER_COLOR, con.OTHER_BAR_THICK)
        cv2.line(mask_neon, mp_p1, curr_mp_p2, con.MP_OUTER_COLOR, con.OTHER_BAR_THICK)
            
            # Expand the by using dilation
        mask_neon = cv2.dilate(mask_neon,
                            con.DILATE_KERNEL,
                            iterations=con.DILATE_ITERATION)
            
            # Step 2: Apply Blur
        mask_neon = cv2.GaussianBlur(mask_neon,con.BLUR_KERNEL, 0)
        cv2.addWeighted(mask_neon,
                        con.DILATE_ALPHA, 
                        roi, 
                        con.DILATE_BETA,
                        con.DILATE_GAMMA,
                        roi)
        
        cv2.line(roi, hp_p1, curr_hp_p2, con.HP_INNER_COLOR, con.OTHER_BAR_THICK)
        cv2.line(roi, mp_p1, curr_mp_p2, con.MP_INNER_COLOR, con.OTHER_BAR_THICK)
        
        # Vertical EXP bar
        exp_tp = (con.MAIN_EXP_BAR[0],
                  con.MAIN_EXP_BAR[1] - con.MAIN_VER_BAR_LENGTH)
        x1 = exp_tp[0] - 2* con.ADDITIONAL_SIZE - con.MAIN_HOR_BAR_THICK
        x2 = con.MAIN_EXP_BAR[0] + 2* con.ADDITIONAL_SIZE + con.MAIN_VER_BAR_THICK
        y1 = exp_tp[1] - 2* con.ADDITIONAL_SIZE
        y2 = con.MAIN_EXP_BAR[1] + 2* con.ADDITIONAL_SIZE
        
        roi_exp = frame[y1:y2,x1:x2]
        mask_exp = np.zeros_like(roi_exp)
        exp_p2 = (2* con.ADDITIONAL_SIZE,2* con.ADDITIONAL_SIZE)
        exp_p1 = (exp_p2[0],exp_p2[1] + con.MAIN_VER_BAR_LENGTH)
        exp_ratio = main_user.get_exp() / con.FULL_EXP
        distance = math.dist(exp_p1, exp_p2)
        
        curr_exp_p2 = (exp_p1[0] , exp_p1[1]- int(distance * exp_ratio) )
        
        
        
        cv2.line(roi_exp, 
                 exp_p1, 
                 exp_p2, 
                 con.DEFAULT_BAR_COLOR, 
                 con.MAIN_VER_BAR_THICK)
        
        cv2.line(mask_exp, 
                 exp_p1, 
                 curr_exp_p2, 
                 con.EXP_OUTER_COLOR, 
                 con.MAIN_VER_BAR_THICK)
        mask_exp = cv2.dilate(mask_exp,
                              con.DILATE_KERNEL,
                              iterations=con.DILATE_ITERATION)
        mask_exp = cv2.GaussianBlur(mask_exp,(15, 15), 0)
        cv2.addWeighted(mask_exp,
                        con.DILATE_ALPHA, 
                        roi_exp, 
                        con.DILATE_BETA,
                        con.DILATE_GAMMA,
                        roi_exp)
        cv2.line(roi_exp, 
                 exp_p1, 
                 curr_exp_p2, 
                 con.EXP_INNER_COLOR, 
                 con.MAIN_VER_BAR_THICK)
                       
    def draw_sel_list(self, frame):
        if self.open_item_list:
            sel_item = self.selected_eitem
            
            img_h, img_w = self.item_list.get_item_size()
            
            list_h, list_w = self.item_list.get_items_list_size()
            x,y = self.items_list_top_left
            roi = frame[y:y+list_h, x:x+list_w]
            items_image, masks_image = self.item_list.get_items_image()
            overlay = roi.copy()
                
            for i in range(len(EItem)):
                bg_color = con.BG_SELECTED_RECTANGLE if i == sel_item.value else con.BG_REGULAR_RECTANGLE
                bd_color = con.BD_REGULAR_RECTANGLE
                cv2.rectangle(overlay,
                              (i*img_w,0),
                              ((i+1)*img_w,img_h),
                              bg_color,-1)
                cv2.rectangle(overlay,
                            (i*img_w,0),
                            ((i+1)*img_w,img_h),
                            bd_color,
                            con.ITEM_BAR_THICK)
                
            cv2.addWeighted(overlay,
                            con.TRANS_ALPHA, 
                            roi, 
                            con.TRANS_BETA,
                            con.TRANS_GAMMA,
                            roi)
            roi[:,:] = (1-masks_image) * roi + masks_image * items_image
            
            
     