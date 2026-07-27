from collections import deque
import math

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from src.enum import EStatus
from src.entity import Item, Polygon, Projectile
from .ProjectileManager import ProjectileManager
from src.utils import SAT
from src.other import constants as con




class HandManager:
    def __init__(self, main_user, projectile_manager: ProjectileManager):
        self.main_user = main_user
        self.projectile_manager = projectile_manager
        
        base_options = python.BaseOptions(
            model_asset_path=con.MEDIAPIPE_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.timestamp = 0
        self.prev_frame = []
        self.landmarks = []
        self.world_landmarks = []
        self.processed_sequence = deque(maxlen=20)
        self.gun_counter = -1
        self.current_skill = ''
        self.gun = None
        self.hand_boundary_polygon = None
        self.hand_counter = 0

        
    def detect_landmarks(self,frame):
        h,w,_ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect_for_video(mp_image, self.timestamp)
        self.timestamp = self.timestamp + 1
        if detection_result.hand_landmarks:
            self.landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in detection_result.hand_landmarks[0]]
            self.world_landmarks = np.array([(lm.x, lm.y, lm.z) for lm in detection_result.hand_world_landmarks[0]])
        else:
            self.landmarks = []
            self.world_landmarks = []
            self.current_skill = ''
            self.reset_gun()
            self.reset_hand()
    
    def get_gun_pos_dir(self):
        pt8 = self.landmarks[8]
        pt11 = self.landmarks[11]
        pt12 = self.landmarks[12]
        center_point = ((pt8[0] + pt12[0]) // 2,
                            (pt8[1] + pt12[1]) // 2)

        direction = (pt12[0] - pt11[0], pt12[1] - pt11[1])
        return center_point, direction
    def get_index_finger_polygon(self):
        pts = self.landmarks
        if len(pts) > 0:
            return Polygon([pts[8],pts[7],pts[6]])
        return None
    def get_sequence(self):
        return self.processed_sequence
    
    def process_world_points(self):
        wpts = self.world_landmarks
        if len(wpts) > 0:
            wrist = wpts[0]
            middle_mcp = wpts[9]
            scale = max(math.dist(wrist, middle_mcp), 1e-6)
            
            normalized = (wpts - wrist) / scale
            deltas = normalized - self.prev_frame if len(self.prev_frame) > 0 else np.zeros_like(normalized)
            processed = np.concatenate([normalized, deltas], axis=1).flatten()
            self.prev_frame = normalized
            self.processed_sequence.append(processed)
        else:
            zero_frame = np.zeros(126, dtype=np.float32)
            self.processed_sequence.append(zero_frame)
            
            # Reset prev_frame so delta calculation starts fresh when hand re-appears
            self.prev_frame = []
    def reset_gun(self):
        if self.gun is not None:
            self.gun.update_status(EStatus.DYING)
            self.gun = None
            self.gun_counter = -1
    def reset_hand(self):
        self.hand_boundary_polygon = None
        self.hand_counter = 0
        
    def update_skill(self,frame, skill_item:Item, gesture, tracked_faces):
        self.current_skill = skill_item
        if len(self.landmarks) > 0 and self.main_user.get_mp()>=10:
            if self.current_skill.get_name() == "gun" :
                if gesture == "gun_pose":
        
                    if self.gun_counter == -1:
                        self.gun = Projectile(self.main_user, 
                                              skill_item, 
                                              con.GUN_STEP,
                                              con.GUN_IMAGE_LINK,
                                              (1,1))
                        self.gun_counter = 0
                        self.projectile_manager.add_projectile(self.gun)
                    if self.gun_counter >=0 and self.gun is not None:
                        
                        if self.gun_counter < 10:
                           
                            self.gun_counter = self.gun_counter + 1
                            self.gun.update_size(self.gun_counter * 4)
                        
                        pos, dir = self.get_gun_pos_dir()
                        self.gun.update_position(pos)
                        self.gun.update_direction(dir)
                elif gesture == "fire" and self.gun_counter == 10 :
                        self.gun.update_status(EStatus.MOVING)
                        self.main_user.update_mp(-10)
                        self.gun = None
                        self.gun_counter = -1
                else:
                    self.reset_gun()
                
            elif self.current_skill.get_name()== "hand":
                self.reset_gun()
                self.draw_glowing_haki_hand(frame)
                if self.hand_boundary_polygon is not None:
                    # for face,user in zip(faces,users):
                    # for face in faces:
                    #     collide = SAT.check_collide(Polygon(face),
                    #                                 self.hand_boundary_polygon)
                    #     if collide:
                            
                    #         cv2.fillPoly(frame, [np.array(face, dtype=np.int32)], DAMAGE_COLORS_BGR[self.hand_counter])
                    #         self.hand_counter = (self.hand_counter + 1) % 6
                    #         if users.get_hp() > 0:
                    #             users.update_hp(-skill_item.get_bonus_damage())
                    self.main_user.update_mp(-0.1)
                    for tracked_face in tracked_faces:
                        # [tl,br,id,crop,seg_face,user]
                        face = tracked_face[4]
                        user = tracked_face[5]
                        collide = SAT.check_collide(Polygon(face),
                                                     self.hand_boundary_polygon)
                        if collide:
                            cv2.fillPoly(frame, 
                                         [np.array(face, dtype=np.int32)], 
                                         con.DAMAGE_COLORS_BGR[self.hand_counter])
                            self.hand_counter = (self.hand_counter + 1) % 6
                            if user.get_hp() > 0:
                                user.update_hp(-skill_item.get_bonus_damage())
                            elif user.is_give_exp() == False:
                                self.main_user.update_lvl(36)
                                self.main_user.update_exp(20)
                                user.update_give_exp(True)
                                
                                
                
        else:
            self.reset_gun()
            self.reset_hand()
    
    def draw_land_mark(self,frame):
        pts = self.landmarks
        for start, end in con.HAND_CONNECTIONS:
            cv2.line(frame, pts[start], pts[end], con.HAND_LINE_COLOR, 2)
        for x, y in pts:
            cv2.circle(frame, (x, y), con.HAND_POINT_SCALE, con.HAND_POINT_COLOR, -1)
            
    def draw_glowing_haki_hand(self,image):
        """Applies a glowing dark purple aura to the detected hand."""
        h, w, c = image.shape
        
        # Create a binary mask of the hand (white=hand, black=background)
        mask_outer = np.zeros((h, w,3), dtype=np.uint8)
        mask_middle = np.zeros((h, w,3), dtype=np.uint8)
        points = self.landmarks
        # Fill the polygon defined by the hand landmarks

        for start, end in con.HAND_CONNECTIONS:
            cv2.line(mask_outer, points[start], points[end], con.HAKI_OUTER, 3)
            cv2.line(mask_middle, points[start], points[end], con.HAKI_MIDDLE, 15)
        poly_points = np.array([points[2],
                        points[5],
                        points[9],
                        points[13],
                        points[17],
                        points[0],
                        points[1],], np.int32)
        
                    
        # Expand the mask to create the area for the aura
        kernel_outer = np.ones((5, 5), np.uint8)
        mask_outer = cv2.dilate(mask_outer, kernel_outer, iterations=8)
        
        kernel_midle = np.ones((3, 3), np.uint8)
        mask_middle = cv2.dilate(mask_middle, kernel_midle, iterations=5)

        # Apply Gaussian blur to create the "soft glow" effect
        # blur_mask = cv2.GaussianBlur(dilated_mask, AURA_BLUR_KERNEL, 0)
        
        # Create a 3-channel BGR image of the desired purple color
        # Only where the blur_mask is bright will this color appear

        # Blend the resulting purple aura onto the original image
        # We use cv2.addWeighted to overlay the glow
        cv2.addWeighted(mask_middle, 1.0, mask_outer, con.AURA_INTENSITY,0, mask_outer)
        cv2.GaussianBlur(mask_outer,(5,5),3,mask_outer)
        for start, end in con.HAND_CONNECTIONS:
            cv2.line(mask_outer, points[start], points[end], con.HAKI_CORE, 10)
        cv2.fillPoly(mask_outer, [poly_points], con.HAKI_CORE)
        gray_mask = cv2.cvtColor(mask_outer, cv2.COLOR_BGR2GRAY)
        _, binary_mask = cv2.threshold(gray_mask, 1, 255, cv2.THRESH_BINARY)
        
        mask = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR)
        # we will determine the boundaries of the haki hand by using the countours
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # we know that there only one hand in the image so we flatter countours to acommodate noise
        contour = np.concatenate(contours, axis=0)
        # our contour could be anything, we would like to have a convexhull of it
        # convexhull or contours is something like [[[1,2]],[[2,3]]] which is (N,1,2)
        # sequeze remove that extra 1
        hand_boundary = np.squeeze(cv2.convexHull(contour))
        self.hand_boundary_polygon = Polygon(hand_boundary)
       
        
        inverse_hand_mask = cv2.bitwise_not(mask)
        
        
        image_no_hand = cv2.bitwise_and(image, inverse_hand_mask)
  
        image[:,:] = cv2.add(image_no_hand, mask_outer)
        # result = cv2.addWeighted(image, 1.0, mask_outer, AURA_INTENSITY, 0,image)
    
            