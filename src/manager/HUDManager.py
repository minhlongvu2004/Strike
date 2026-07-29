import math

import cv2
import numpy as np

from src.enum import EItem
from src.entity import ItemList, Polygon, User
from src.utils import SAT, LabelDrawer
from src.other import constants as con



class HUDManager:
    def __init__(self,
                 selected_eitem: EItem,
                 item_list: ItemList,
                 main_user: User,
                 hud_top_left,
                 items_list_top_left,
                 system_top_left,
                 system_top_right,
                 system_bottom_right,
                 system_bottom_left,
                 system_path,
                 open_item_list: bool,
                 open_system_status: bool):
        self.selected_eitem = selected_eitem
        self.item_list = item_list
        self.main_user = main_user
        self.hud_top_left = hud_top_left
        self.items_list_top_left = items_list_top_left
        self.open_item_list = open_item_list # True/False to open ItemList
        self.system_tl = system_top_left
        self.system_tr = system_top_right
        self.system_br = system_bottom_right
        self.system_bl = system_bottom_left
        self.open_system_status = open_system_status
        self.system_polygon = Polygon([self.system_tl,
                                       self.system_tr,
                                       self.system_br,
                                       self.system_bl])
        
        self.system_path = system_path
        self.sys_img = cv2.imread(self.system_path,cv2.IMREAD_UNCHANGED)
        
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
    def is_open_system_status(self):
        return self.open_system_status
    
    def is_open_item_list(self):
        return self.open_item_list
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
    def get_system_icon_polygon(self):
        return self.system_polygon   
    def check_if_click_item_hud(self,
                                 current_gesture,
                                 if_polygon:Polygon):
        img_polygon = self.get_image_hud_polygon()
        sys_polygon = self.get_system_icon_polygon()
        
        if current_gesture == "click" and if_polygon is not None:
                    # item_position
            time = (cv2.getTickCount() - self.start_count) * 1000 / cv2.getTickFrequency() 
            if SAT.check_collide(sys_polygon,
                                 if_polygon):
                if time > 1500:
                    # Usually an click span for 3-4 frames, so this is to avoid 
                    # mis activate click again
                    status = self.open_system_status
                    self.start_count = cv2.getTickCount()
    
                    self.open_system_status = con.CLOSE_SYS \
                                    if status == con.OPEN_SYS else con.OPEN_SYS 
                    self.open_item_list = con.CLOSE_LIST 
            
            elif SAT.check_collide(img_polygon,
                                if_polygon):
                if time > 1500:
                    # Usually an click span for 3-4 frames, so this is to avoid 
                    # mis activate click again
                    status = self.open_item_list
                    self.start_count = cv2.getTickCount()
                    self.open_item_list = con.CLOSE_LIST \
                        if status == con.OPEN_LIST else con.OPEN_LIST 
                    self.open_system_status = con.CLOSE_SYS 
    
    def draw_system_icon(self,frame):
        LabelDrawer.merge_tranparent_image(frame,
                                        self.sys_img, 
                                        self.system_tl,
                                        self.system_br,
                                        )
    
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
        
        
        # LV_OUTER_COLOR = (0, 215, 255)   # BGR (Gold)
        # LV_INNER_COLOR = (120, 255, 255)
       
        # LV_OUTER_COLOR = (220, 170, 0)
        # LV_INNER_COLOR = (255, 255, 170)
        LV_OUTER_COLOR = (0, 120, 220)
        LV_INNER_COLOR = (80, 190, 255)
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
                 LV_OUTER_COLOR, 
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
                 LV_INNER_COLOR, 
                 con.MAIN_VER_BAR_THICK)
        
        
        
        # Draw Level text above 
        level = f"Lv. {self.main_user.get_level()}"
        level_size,_ = cv2.getTextSize(level, cv2.FONT_HERSHEY_COMPLEX,0.6,2)
        # level text will be above the exp bar like 30 px and center
        pa = 10
        roi_tl = (exp_tp[0] - level_size[0]//2 - pa,
                    exp_tp[1] - 10 - level_size[1] - pa)
        roi_br = (roi_tl[0] + level_size[0] + 2*pa,
                    roi_tl[1] + level_size[1] + 2*pa)
        lvl_roi = frame[roi_tl[1]:roi_br[1],
                        roi_tl[0]:roi_br[0]]
        lvl_mask_neon = np.zeros_like(lvl_roi, dtype=np.uint8)
        lvl_br = (pa, pa+level_size[1])
        
        cv2.putText(lvl_mask_neon, level,lvl_br,cv2.FONT_HERSHEY_COMPLEX,0.6,LV_OUTER_COLOR,2)
        lvl_mask_neon = cv2.dilate(lvl_mask_neon,
                                    con.DILATE_KERNEL,
                                    iterations=con.DILATE_ITERATION)
                    
                    # Step 2: Apply Blur
        lvl_mask_neon = cv2.GaussianBlur(lvl_mask_neon,con.BLUR_KERNEL, 0)
     
        
        cv2.putText(lvl_roi, level,lvl_br,cv2.FONT_HERSHEY_COMPLEX,0.6,LV_INNER_COLOR,2)
        # cv2.rectangle(lvl_roi,(pa,pa),(pa+level_size[0],pa+level_size[1]),con.BD_INNER_COLOR,-1)

                       
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
            
    def draw_system_status_hud(self,
                           frame):
        if self.open_system_status:
            user = self.main_user
            img_h,img_w,_ = frame.shape
            header = "User Status"
            size = 0.7
            name = f"Name: {user.get_name()}"
            title = f"Title: {user.get_title()}"
            u_skill = f"Skill: {user.get_ultimate_skill()}"
            lvl = f"Level: {user.get_level()}"
            dmg = f"Damage: {user.get_dmg()}"
            
            # size = (height,width)
            header_size,_ = cv2.getTextSize(header, cv2.FONT_HERSHEY_COMPLEX, size,2)
            name_size,_ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, size,1)
            title_size,_ = cv2.getTextSize(title, cv2.FONT_HERSHEY_COMPLEX, size,1)
            u_skill_size,_ = cv2.getTextSize(u_skill, cv2.FONT_HERSHEY_COMPLEX, size,1)
            lvl_size,_ = cv2.getTextSize(lvl, cv2.FONT_HERSHEY_COMPLEX, size,1)
            dmg_size,_ = cv2.getTextSize(dmg, cv2.FONT_HERSHEY_COMPLEX, size,1)
    
            max_height = max(header_size[1],
                            name_size[1],
                            title_size[1],
                            u_skill_size[1],
                            lvl_size[1],
                            dmg_size[1])
            max_width = max(name_size[0],
                            title_size[0],
                            u_skill_size[0],
                            lvl_size[0],
                            dmg_size[0])
            rec_w = 2 * con.PADDING + max_width
            rec_h = 4 * con.PADDING + header_size[1]\
                + max_height * 5 + 5 * con.LINE_SPACE 
            hud_w = rec_w + 2 * con.ADDITIONAL_SIZE
            hud_h = rec_h + 2 * con.ADDITIONAL_SIZE
            
            
            hud_tl = ((img_w - hud_w)//2,
                    (img_h - hud_h)//2)
            hud_br = (hud_tl[0] + hud_w,
                    hud_tl[1] + hud_h)
            
            rec_tl = (con.ADDITIONAL_SIZE,
                    con.ADDITIONAL_SIZE)
            rec_br = (rec_tl[0] + rec_w,
                    rec_tl[1] + rec_h)
            roi = frame[hud_tl[1]:hud_br[1],
                        hud_tl[0]:hud_br[0]]
            
            hd_br = (rec_tl[0] + (rec_w-header_size[0])//2,
                    rec_tl[1] + con.PADDING + header_size[1])
            nm_br = (rec_tl[0] + con.PADDING,
                    hd_br[1] + con.LINE_SPACE + name_size[1])
            tle_br = (nm_br[0],
                    nm_br[1] + con.LINE_SPACE + title_size[1])
            us_br = (nm_br[0],
                    tle_br[1] + con.LINE_SPACE + u_skill_size[1])
            lv_br = (nm_br[0],
                    us_br[1] + con.LINE_SPACE + lvl_size[1])
            dmg_br = (nm_br[0],
                    lv_br[1] + con.LINE_SPACE + dmg_size[1])
            # Transparent
            overlay = roi.copy()
            cv2.rectangle(roi,rec_tl,rec_br,con.BG_COLOR,-1)
            cv2.addWeighted(overlay, 0.4, roi,0.6,0,roi)
            
            # Neon effect
            mask_neon = np.zeros_like(roi, dtype=np.uint8)
            
            cv2.putText(mask_neon, header, hd_br, con.FONT_FACE, size, con.TEXT_OUTER_COLOR, 2)
            cv2.putText(mask_neon, name, nm_br, con.FONT_FACE, size, con.TEXT_OUTER_COLOR, 1)
            cv2.putText(mask_neon, title, tle_br, con.FONT_FACE, size, con.TEXT_OUTER_COLOR, 1)
            cv2.putText(mask_neon, u_skill, us_br, con.FONT_FACE, size, con.TEXT_OUTER_COLOR, 1)
            cv2.putText(mask_neon, lvl, lv_br, con.FONT_FACE, size, con.TEXT_OUTER_COLOR, 1)
            cv2.putText(mask_neon, dmg, dmg_br, con.FONT_FACE, size, con.TEXT_OUTER_COLOR, 1)
            
            cv2.rectangle(mask_neon, rec_tl,rec_br,con.BD_OUTER_COLOR,1)
            mask_neon = cv2.dilate(mask_neon,
                                   con.DILATE_KERNEL,
                                   iterations=con.DILATE_ITERATION)
            mask_neon = cv2.GaussianBlur(mask_neon,con.BLUR_KERNEL, 0)  
            cv2.addWeighted(mask_neon,
                            con.DILATE_ALPHA, 
                            roi, 
                            con.DILATE_BETA,
                            con.DILATE_GAMMA,
                            roi)
            
            cv2.putText(roi, header, hd_br, con.FONT_FACE, size, con.TEXT_INNER_COLOR, 2)
            cv2.putText(roi, name, nm_br, con.FONT_FACE, size, con.TEXT_INNER_COLOR, 1)
            cv2.putText(roi, title, tle_br, con.FONT_FACE, size, con.TEXT_INNER_COLOR, 1)
            cv2.putText(roi, u_skill, us_br, con.FONT_FACE, size, con.TEXT_INNER_COLOR, 1)
            cv2.putText(roi, lvl, lv_br, con.FONT_FACE, size, con.TEXT_INNER_COLOR, 1)
            cv2.putText(roi, dmg, dmg_br, con.FONT_FACE, size, con.TEXT_INNER_COLOR, 1)
            cv2.rectangle(roi, rec_tl,rec_br,con.BD_OUTER_COLOR,1)
     