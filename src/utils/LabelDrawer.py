import math

import cv2
import numpy as np
from src.entity import User
from src.other import constants as con


class LabelDrawer:
    @staticmethod
    def draw_labels(frame,
                   tracked_faces):
        # tracked_faces  is an array of [tl,br,id, crop,segment,user]
        # for bounding_box, user in (bounding_boxes, users):
        for tracked_face in tracked_faces:
            LabelDrawer.draw_label(frame,
                                   tracked_face[0],
                                   tracked_face[1],
                                   tracked_face[5])
    
    @staticmethod
    def draw_label(frame,
                   top_left,
                   bottom_right,
                   user:User):
        x1,y1 = top_left
        x2,y2 = bottom_right
        length = min(x2-x1,y2-y1) // 6
        r_s,_,_ = LabelDrawer.calculate_size_label(user)
        box_point, rect_point, top_left_label = LabelDrawer.get_points_for_connector(
                                                            frame, 
                                                            top_left,
                                                            bottom_right,
                                                            con.CONNECTOR_LENGTH,
                                                            r_s[1],
                                                            r_s[0])
        
        
        
        hp = user.get_hp()
        if hp >0:
            LabelDrawer.draw_neon_bounding_box(frame,
                                               top_left,
                                               bottom_right,
                                               length,
                                               con.BD_OUTER_COLOR,
                                               con.BD_INNER_COLOR)
            LabelDrawer.draw_line_connector(frame,
                                            box_point,
                                            rect_point,
                                            con.BD_OUTER_COLOR,
                                            con.BD_INNER_COLOR
                                            )
            
            LabelDrawer.draw_live_label(frame, top_left_label,user)
        else:
            LabelDrawer.draw_neon_bounding_box(frame,
                                            top_left,
                                            bottom_right,
                                            length,
                                            con.DEATH_OUTER_COLOR,
                                            con.DEATH_INNER_COLOR)
            LabelDrawer.draw_line_connector(frame,
                                            box_point,
                                            rect_point,
                                            con.DEATH_OUTER_COLOR,
                                            con.DEATH_INNER_COLOR
                                            )
            LabelDrawer.draw_death_label(frame, top_left_label, user)
    
    
    @staticmethod
    def draw_live_label(image,
               top_left,
               user: User):
    # rectangle, name and label sizes
        name = user.get_name()
        level = user.get_level()
        level = f"Lv. {level}"
        rec_s, n_s,l_s  = LabelDrawer.calculate_size_label(user)
        a = 5
        bottom_right = (top_left[0] + rec_s[1],
                        top_left[1] + rec_s[0])
        
        # this delta_x is to accomdate the fact when we go outside of the bound
        # we need it because we already use min max in ROI we remove information where the top left is
        # when it is < 0
        # so this delta_x keep that information and draw outside of the frame. 
        # Remember that drawing outside frame doesn't cause error but the zero dimension of input image does
        delta_x = top_left[0] if top_left[0] < 0 else 0
        delta_y = top_left[1] if top_left[1] <0 else 0
        name_p, level_p, hp_p1, hp_p2, mp_p1,mp_p2 = LabelDrawer.calculate_points((a +delta_x,a + delta_y),
                                                                    rec_s,
                                                                    n_s,
                                                                    l_s)
        
        # I know code below is kinda ugly but it is more efficient
        hp_ratio = user.get_hp() / con.FULL_HP
        mp_ratio = user.get_mp() / con.FULL_MP
        distance = math.dist(hp_p1, hp_p2)
        
        curr_hp_p2 = (hp_p1[0] + int(distance * hp_ratio), hp_p1[1] )
        curr_mp_p2 = (mp_p1[0] + int(distance * mp_ratio), mp_p1[1] )
        #### Transparent rectangle first
        y1 = max(0, min(480, top_left[1] - a))
        y2 = max(0, min(480, bottom_right[1] + a))

        x1 = max(0, min(640, top_left[0] - a))
        x2 = max(0, min(640, bottom_right[0] + a))
        
        rec_x1 = max(0, min(640, a + delta_x))
        rec_x2 = max(0, min(640, rec_s[1] + a + delta_x))

        rec_y1 = max(0, min(480, a + delta_y))
        rec_y2 = max(0, min(480, rec_s[0] + a + delta_y))
        
        # Now the slice is guaranteed to have valid dimensions
        if x1 != x2 and y1 != y2 and\
            rec_x1 != rec_x2 and rec_y1 != rec_y2:
            # print(())
            
            roi = image[y1:y2, x1:x2]
            overlay = roi.copy()
    
            cv2.rectangle(overlay,( rec_x1,rec_y1), 
                        (rec_x2,rec_y2), con.BG_COLOR, -1)
            # cv2.imshow()
            cv2.addWeighted(overlay, 0.6, roi,0.4,0,roi)
            
            
            cv2.line(roi, hp_p1, hp_p2, con.DEFAULT_BAR_COLOR, con.OTHER_BAR_THICK)
            cv2.line(roi, mp_p1, mp_p2, con.DEFAULT_BAR_COLOR, con.OTHER_BAR_THICK)
            
            
            # Step 1: draw the blurred bar and text
            mask_neon = np.zeros_like(roi, dtype=np.uint8)
            cv2.line(mask_neon, hp_p1, curr_hp_p2, con.HP_OUTER_COLOR, con.OTHER_BAR_THICK)
            cv2.line(mask_neon, mp_p1, curr_mp_p2, con.MP_OUTER_COLOR, con.OTHER_BAR_THICK)
            
            
            cv2.putText(mask_neon,
                        name, 
                        name_p,
                        con.FONT_FACE, 
                        con.NAME_SCALE, 
                        con.TEXT_OUTER_COLOR, 
                        con.NAME_THICKNESS)
            cv2.putText(mask_neon, 
                        level, 
                        level_p,
                        con.FONT_FACE, 
                        con.NAME_SCALE, 
                        con.TEXT_OUTER_COLOR, 
                        con.LEVEL_THICKNESS)
            cv2.rectangle(mask_neon, (rec_x1,rec_y1), (rec_x2,rec_y2), con.BD_OUTER_COLOR,1)
            
            # Expand the by using dilation
            mask_neon = cv2.dilate(mask_neon,
                                   con.DILATE_KERNEL,
                                   iterations = con.DILATE_ITERATION)
            
            # Step 2: Apply Blur
            mask_neon = cv2.GaussianBlur(mask_neon,con.BLUR_KERNEL, 0)   
            cv2.addWeighted(mask_neon,
                            con.DILATE_ALPHA, 
                            roi, 
                            con.DILATE_BETA,
                            con.DILATE_GAMMA,
                            roi)
            
            # Step 3: Add core light
            cv2.line(roi, 
                     hp_p1, 
                     curr_hp_p2, 
                     con.HP_INNER_COLOR, 
                     con.OTHER_BAR_THICK)
            cv2.line(roi, 
                     mp_p1, 
                     curr_mp_p2, 
                     con.MP_INNER_COLOR, 
                     con.OTHER_BAR_THICK)
            cv2.putText(roi, 
                        name, 
                        name_p,
                        con.FONT_FACE, 
                        con.NAME_SCALE, 
                        con.TEXT_INNER_COLOR, 
                        con.NAME_THICKNESS)
            cv2.putText(roi, 
                        level, 
                        level_p,
                        con.FONT_FACE, 
                        con.NAME_SCALE, 
                        con.TEXT_INNER_COLOR, 
                        con.LEVEL_THICKNESS)
            cv2.rectangle(roi, 
                          (rec_x1,rec_y1), 
                          (rec_x2,rec_y2), 
                          con.BD_INNER_COLOR,
                          1)
            cv2.rectangle(roi, 
                          (rec_x1,rec_y1), 
                          (rec_x2,rec_y2), 
                          con.BD_INNER_COLOR,1)
    
    @staticmethod
    def draw_neon_bounding_box(frame,
                               p1,
                               p2,
                               length,
                               outer_color,
                               inner_color):
        x1,y1 = p1
        x2,y2 = p2
        l = length
        # small trick to display full glooming, if at the edge don't do it
        a = con.ADDITIONAL_SIZE if min(x1,y1) > con.ADDITIONAL_SIZE \
            and min(640-x2,480-y2) > con.ADDITIONAL_SIZE else 0
        roi = frame[y1 - a:y2 + a, x1 - a:x2 + a]
        mask_neon = np.zeros_like(roi,dtype=np.uint8)
        delta_x = x2 - x1
        delta_y = y2 - y1
        # (x1,y1) = 0 0
        # (x2,y2) = delta_x delta_y
        # Step 2: Apply blurred text, the bigger the more blurred
        tl, tl_hor,tl_ver = (a, a),(l + a, a), (a,l + a)
        tr, tr_hor, tr_ver  = (delta_x + a, a),(delta_x - l + a, a), (delta_x + a, l + a)
        bl, bl_hor, bl_ver = (a, delta_y+ a), (l + a, delta_y + a), (a,delta_y - l + a)
        br, br_hor, br_ver = (delta_x + a, delta_y + a),(delta_x - l+ a,delta_y+ a), (delta_x+ a,delta_y - l+a)
            # top left
        cv2.line(mask_neon, tl, tl_hor, outer_color, con.CORNER_BAR_THICKNESS)
        cv2.line(mask_neon, tl, tl_ver, outer_color, con.CORNER_BAR_THICKNESS)
        # top right
        cv2.line(mask_neon, tr, tr_hor, outer_color, con.CORNER_BAR_THICKNESS)
        cv2.line(mask_neon, tr, tr_ver, outer_color, con.CORNER_BAR_THICKNESS)
        # bottom left
        cv2.line(mask_neon, bl, bl_hor, outer_color, con.CORNER_BAR_THICKNESS)
        cv2.line(mask_neon, bl, bl_ver, outer_color, con.CORNER_BAR_THICKNESS)
        
        # bottom right
        cv2.line(mask_neon, br, br_hor, outer_color,con.CORNER_BAR_THICKNESS)
        cv2.line(mask_neon, br, br_ver, outer_color,con.CORNER_BAR_THICKNESS)
            # at certain pixel, it will look at surrounding (x,y) the bigger x and y are, the more blurred it will be 
            
        # Step 3 - Blend with the image
        # why it need to be one?
        mask_neon = cv2.dilate(mask_neon,con.DILATE_KERNEL,iterations=con.DILATE_ITERATION)
        
        # Step 2: Apply Blur
        mask_neon = cv2.GaussianBlur(mask_neon,con.BLUR_KERNEL, 0) 
        cv2.addWeighted(mask_neon,
                        con.DILATE_ALPHA, 
                        roi, 
                        con.DILATE_BETA,
                        con.DILATE_GAMMA,
                        roi)
        # cv2.addWeighted(mask_neon,1, image, 1,0,image)
        # Step 4 - write the usual white text
        
        # Top left
        cv2.line(roi, tl, tl_hor, inner_color,con.CORNER_BAR_THICKNESS)
        cv2.line(roi, tl, tl_ver, inner_color,con.CORNER_BAR_THICKNESS)
        
        # Top Right
        cv2.line(roi, tr, tr_hor, inner_color,con.CORNER_BAR_THICKNESS)
        cv2.line(roi, tr, tr_ver, inner_color,con.CORNER_BAR_THICKNESS)
        # Bottom Left
        cv2.line(roi, bl, bl_hor, inner_color,con.CORNER_BAR_THICKNESS)
        cv2.line(roi, bl, bl_ver, inner_color,con.CORNER_BAR_THICKNESS)
        # Bottom Right
        cv2.line(roi, br, br_hor, inner_color,con.CORNER_BAR_THICKNESS)
        cv2.line(roi, br, br_ver, inner_color,con.CORNER_BAR_THICKNESS)
    @staticmethod
    def draw_line_connector(frame,box_point,rect_point,outer_color,inner_color):
        a = con.ADDITIONAL_SIZE
        x1, y1 = box_point
        x2, y2 = rect_point
        
        # contrain the value
        x1,x2 = LabelDrawer.contrain_coordinate([x1,x2], con.ADDITIONAL_SIZE,640)
        y1,y2 = LabelDrawer.contrain_coordinate([y1,y2], con.ADDITIONAL_SIZE,480)
        # Ensure that x1 < x2 and y1 < y2
   
        x_s, x_l = [x1,x2] if x1 <= x2 else [x2,x1]
        y_s,y_l = [y1,y2] if y1 <= y2 else [y2,y1]
        if x_s != x_l and y_s != y_l:
            
            roi = frame[y_s - a: y_l + a, x_s - a: x_l + a]
            r_tl = (x1 - x_s + a, y1 - y_s + a)
            r_br = (x2 - x_s + a, y2 - y_s + a)
            
            mask_neon = np.zeros_like(roi)
            cv2.line(mask_neon,r_tl,r_br,outer_color,con.CORNER_BAR_THICKNESS)
            mask_neon = cv2.dilate(mask_neon,con.DILATE_KERNEL,iterations=con.DILATE_ITERATION)
            mask_neon = cv2.GaussianBlur(mask_neon,con.BLUR_KERNEL,0)
            cv2.addWeighted(mask_neon,con.DILATE_ALPHA,roi,con.DILATE_BETA,con.DILATE_GAMMA, roi)
            cv2.line(roi,r_tl,r_br,inner_color,con.CORNER_BAR_THICKNESS)
        
        cv2.line(frame,box_point,rect_point,outer_color,1)
    @staticmethod
    def contrain_coordinate(coordinate_list,
                            additional_size,
                            height_or_width):
        a = additional_size
        contrained_coordinates = []
        for coor in coordinate_list:
            if coor - a < 0:
                coor = 0
            elif coor + a > height_or_width:
                coor = height_or_width - 1
                
            contrained_coordinates.append(coor)
        return contrained_coordinates
    
    @staticmethod
    def calculate_size_label(user:User):
        name = user.get_name()
        level = user.get_level()
        level = f"Lv. {level}"
        
        name_size,_ = cv2.getTextSize(name, con.FONT_FACE, con.NAME_SCALE, con.NAME_THICKNESS)
        n_w, n_h = name_size
        label_size, _ = cv2.getTextSize(level,con.FONT_FACE, con.LEVEL_SCALE,con.LEVEL_THICKNESS)
        l_w, l_h = label_size
        
        max_width = max(n_w, con.OTHER_BAR_LENGTH)
        rec_width = 2 * con.PADDING + max_width 
        rec_height = \
            2 * con.PADDING + 2 * con.OTHER_BAR_THICK + n_h+l_h + 3 * con.LINE_SPACE 
        return (rec_height, rec_width),(n_h,n_w),(l_h,l_w)
    
    @staticmethod
    def calculate_points(top_left,
                     rectangle_size,
                     name_size,
                     level_size):
    
        # Remember that the putText point is is the bottom left
        tl_x,tl_y = top_left
        rs_h,rs_w = rectangle_size
        ns_h,ns_w = name_size
        ls_h,ls_w = level_size
        
        # name point
        name_point = (tl_x + con.PADDING, tl_y + ns_h + con.PADDING)
        level_point = (tl_x + (rs_w - ls_w)//2 -2 ,
                    name_point[1] + con.LINE_SPACE + ls_h)
        # I don't knwo why there we have to give it for padding. I guess the putText already pad a little bit
        # if there is no padding, it will stick with the border
        hp_point1 = (name_point[0] + con.PADDING,
                    level_point[1] + con.LINE_SPACE)
        hp_point2 = (hp_point1[0] + ns_w - 2*  con.PADDING,
                    hp_point1[1] )
        
        mp_point1 = (hp_point1[0] ,
                    hp_point1[1] + con.OTHER_BAR_THICK +con.LINE_SPACE )
        
        mp_point2 = (mp_point1[0]+ ns_w - 2 * con.PADDING,
                    mp_point1[1])
        
        return name_point,level_point, hp_point1,hp_point2,mp_point1,mp_point2
    
    @staticmethod
    def draw_death_label(image,
                     top_left,
                     user:User):
        name = user.get_name()
        level = user.get_level()
        level = f"Lv. {level}"
        rec_s, n_s,l_s  = LabelDrawer.calculate_size_label(user)
        a = 5
        bottom_right = (top_left[0] + rec_s[1] ,
                        top_left[1] + rec_s[0]  )
        
        # this delta_x is to accomdate the fact when we go outside of the bound
        # we need it because we already use min max in ROI we remove information where the top left is
        # when it is < 0
        # so this delta_x keep that information and draw outside of the frame. 
        # Remember that drawing outside frame doesn't cause error but the zero dimension of input image does
        delta_x = top_left[0] if top_left[0] < 0 else 0
        delta_y = top_left[1] if top_left[1] <0 else 0
        name_p, level_p, hp_p1, hp_p2, mp_p1,mp_p2 = LabelDrawer.calculate_points((a +delta_x,a + delta_y),
                                                                    rec_s,
                                                                    n_s,
                                                                    l_s)
        
        # I know code below is kinda ugly but it is more efficient
        hp_ratio = user.get_hp() / con.FULL_HP
        mp_ratio = user.get_mp() / con.FULL_MP
        distance = math.dist(hp_p1, hp_p2)
        
        curr_hp_p2 = (hp_p1[0] + int(distance * hp_ratio), hp_p1[1] )
        curr_mp_p2 = (mp_p1[0] + int(distance * mp_ratio), mp_p1[1] )
        #### Transparent rectangle first
        # y1 = max(0, top_left[1] - a)
        # y1 = min(480, top_left[1] - a)
        # y2 = min(480, bottom_right[1] + a)
        # x1 = max(0, top_left[0] - a)
        # x2 = min(640, bottom_right[0] + a)
        y1 = max(0, min(480, top_left[1] - a))
        y2 = max(0, min(480, bottom_right[1] + a))

        x1 = max(0, min(640, top_left[0] - a))
        x2 = max(0, min(640, bottom_right[0] + a))
        
        
        # Assuming 'w' is frame width (e.g. 640) and 'h' is frame height (e.g. 480)

        rec_x1 = max(0, min(640, a + delta_x))
        rec_x2 = max(0, min(640, rec_s[1]  +a + delta_x))

        rec_y1 = max(0, min(480, a + delta_y))
        rec_y2 = max(0, min(480, rec_s[0]  +a+ delta_y))
        
        
        # Now the slice is guaranteed to have valid dimensions
        if x1 != x2 and y1 != y2 and\
            rec_x1 != rec_x2 and rec_y1 != rec_y2:
   
            
            roi = image[y1:y2, x1:x2]
            overlay = roi.copy()
        
            cv2.rectangle(overlay,( rec_x1,rec_y1), 
                        (rec_x2,rec_y2), con.BG_COLOR, -1)
            # cv2.imshow()
            cv2.addWeighted(overlay, 
                            con.TRANS_ALPHA, 
                            roi,
                            con.TRANS_BETA,
                            con.TRANS_GAMMA,
                            roi)
            
            
            cv2.line(roi, hp_p1, hp_p2, con.DEFAULT_BAR_COLOR, con.OTHER_BAR_THICK)
            cv2.line(roi, mp_p1, mp_p2, con.DEFAULT_BAR_COLOR, con.OTHER_BAR_THICK)
            
            
            # Step 1: draw the blurred bar and text
            mask_neon = np.zeros_like(roi, dtype=np.uint8)
            cv2.putText(mask_neon, name, name_p,con.FONT_FACE, con.NAME_SCALE, con.DEATH_OUTER_COLOR, con.NAME_THICKNESS)
            cv2.putText(mask_neon, level, level_p,con.FONT_FACE, con.NAME_SCALE, con.DEATH_OUTER_COLOR, con.LEVEL_THICKNESS)
            cv2.rectangle(mask_neon, (rec_x1,rec_y1), (rec_x2,rec_y2), con.DEATH_OUTER_COLOR, 1)
            
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
            
            # Step 3: Add core light
            cv2.putText(roi, name, name_p,con.FONT_FACE, con.NAME_SCALE, con.DEATH_INNER_COLOR, con.NAME_THICKNESS)
            cv2.putText(roi, level, level_p,con.FONT_FACE, con.NAME_SCALE, con.DEATH_INNER_COLOR, con.LEVEL_THICKNESS)
            cv2.rectangle(roi, (rec_x1,rec_y1), (rec_x2,rec_y2), con.DEATH_INNER_COLOR, 1)
            
            LabelDrawer.merge_tranparent_image(roi,
                                               user.get_death_image(), 
                                               (rec_x1,rec_y1), 
                                               (rec_x2,rec_y2))
    
    @staticmethod
    def merge_tranparent_image(frame,                   
                          item,
                          top_left,
                          bottem_right):
        '''
        lets call item is F for foreground
        and our image is B for background
        then we will base on the alpha channel for transparency
        if normalized alpha is 0, this mean we only take the background
        if it is 1, this mean we only take the foreground
        Therefore the math should be
        new_image = 
        '''
        hor_length = bottem_right[0] - top_left[0]
        ver_length = bottem_right[1] - top_left[1]
        
        resized_bgr_item = cv2.resize(item,(hor_length,ver_length))
        
        # this is to avoid crash when the image is outside of frame border
        new_tl, new_br, cut_item = LabelDrawer.cut_exceed_image(frame,
                                                    resized_bgr_item,
                                                    top_left,
                                                    bottem_right)
        x_0 = new_tl[0]
        x_1 = new_br[0]
        y_0 = new_tl[1]
        y_1 = new_br[1]
        ci = cut_item.shape
        fr = frame[y_0:y_1, x_0:x_1].shape
        if ci[0] != 0 and ci[1] != 0 and \
         fr[0] != 0 and fr[1] != 0:

            b, g, r, a = cv2.split(cut_item)
            bgr_item = cv2.merge((b, g, r)) + 20
            mask = a / 255.0  # Normalize to 0-1 range
            # mask now is only 2D array, we have to convert it to 3D
            # 
            mask = mask[:, :, np.newaxis]
            frame[y_0:y_1, x_0:x_1] = (1-mask) * frame[y_0:y_1, x_0:x_1] + mask*bgr_item
            
    @staticmethod
    def find_center_image(img):
        
            """
            find_center_image: calculate of the center of an images
            img: the numpy array of image
            return: Position tuple of center point
            """
            
            width = img.shape[0]
            height = img.shape[1]
            x_center = width // 2
            y_center = height // 2
            return (x_center, y_center)
    @staticmethod
    def get_points_for_connector(img,tl_p1,br_p2, length, rect_width, rect_height):
        """
        get_points_for_connector: get the two ends of connectors and bottom left of the label
        img: numpy array of the orgional image
        (x1,y1): Top left position of the detected face
        (x2,y2): Bottom right position of the detected face
        length: the length of the connector line
        rect_width: the width of the label rectangle 
        rect_height: the length of the label rectangle
        return: Return one connected to detected object, the other end connected to label 
        and bottom left of label
        """
        x1,y1 = tl_p1
        x2,y2 = br_p2
        
        
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        center = (x_center, y_center) # center of detected object
        delta_x = int(length * math.cos(math.pi /4 ))
        delta_y = int(length * math.sin(math.pi /4 ))
        
        
        img_center = LabelDrawer.find_center_image(img) # center of origional image
        # change from to top left
        """
        face_connect:  An end of connector connected to detected object
        label_connect: An end of connector connected to label rectangle
        bottom_left_label: bottom left of label rectangle
        """    
        if center[0] > img_center[0]  and center[1] > img_center[1]:
            face_connect = (x1,y1)
            # bottom right
            label_connect = (face_connect[0] - delta_x, face_connect[1] - delta_y)
            # bottom left
            bottom_left_label = (label_connect[0] - rect_width,label_connect[1] - rect_height)
        elif center[0] > img_center[0] and  center[1] < img_center[1]:
            face_connect = (x1,y2)
            # top right
            label_connect = (face_connect[0] - delta_x, face_connect[1] + delta_y)
            # bottom left
            bottom_left_label = (label_connect[0] - rect_width, label_connect[1])
            
        elif center[0] < img_center[0]  and center[1] > img_center[1] : 
            face_connect = (x2,y1)
            # bottom left
            label_connect = (face_connect[0] + delta_x, face_connect[1] - delta_y)
            # bottom left
            bottom_left_label = (label_connect[0],label_connect[1] - rect_height)
        else:
            face_connect = (x2, y2)
            # tio left
            label_connect = (face_connect[0] + delta_x, face_connect[1] + delta_y)
            # bottom left
            bottom_left_label = label_connect
        return face_connect, label_connect, bottom_left_label
    @staticmethod
    def calculate_size_label(user: User):
        name = user.get_name()
        level = user.get_level()
        level = f"Lv. {level}"
        
        name_size,_ = cv2.getTextSize(name, con.FONT_FACE, con.NAME_SCALE, con.NAME_THICKNESS)
        n_w, n_h = name_size
        label_size, _ = cv2.getTextSize(level,con.FONT_FACE, con.LEVEL_SCALE,con.LEVEL_THICKNESS)
        l_w, l_h = label_size
        
        max_width = max(n_w, con.OTHER_BAR_LENGTH)
        rec_width = 2 * con.PADDING + max_width 
        rec_height = \
            2 * con.PADDING + 2 * con.OTHER_BAR_THICK + n_h+l_h + 3 * con.LINE_SPACE 
        return (rec_height, rec_width),(n_h,n_w),(l_h,l_w)
    @staticmethod
    def cut_exceed_image(frame, 
                     image,
                     top_left,
                     bottom_right):
        f_h, f_w,_ = frame.shape
        
        i_h, i_w, _ = image.shape
        height_0 = 0
        height_1 = i_h
        width_0 = 0
        width_1 = i_w
        
        x_0 = top_left[0]
        x_1 = bottom_right[0]
        y_0 = top_left[1]
        y_1 = bottom_right[1]
        
        new_x_0 = x_0
        new_x_1 = x_1
        new_y_0 = y_0
        new_y_1 = y_1
        # Case 1: the image exceed the left frame
        if x_0 < 0 and x_1 > 0:
            width_0 = width_0 - x_0
            new_x_0 = 0
    
        # Case 2: the image exceed the right frame
        
        if x_1 > f_w and x_0 < f_w:
            width_1 =  width_1 - (x_1 - f_w)
            new_x_1 = f_w
        
        # Case 3: the image exceed top frame
        if y_0 <0 and y_1 > 0:
            height_0 = height_0 - y_0
            new_y_0 = 0
        if y_1 > f_h and y_0 < f_w:
            height_1 = height_1 - (y_1- f_h)
            new_y_1 = f_h
            
      

        cut_image = image[height_0:height_1,width_0:width_1]
        new_tl = (new_x_0,new_y_0)
        new_br = (new_x_1,new_y_1)
        return [new_tl,new_br,cut_image]