import cv2
import numpy as np
from src.enum import EStatus
from src.utils import LabelDrawer, SAT
from src.entity import Polygon
from src.other import constants as con

class ProjectileManager:
    def __init__(self):
        self.projectiles = []
        # self.collide = False
    def add_projectile(self,projectile):
        self.projectiles.append(projectile)
    
    def update(self, img_shape, tracked_faces):
        
        '''
        faces: array of polygon vertices of a face. Each face is an array of
        vertices
        '''
        # [tl,br,id,crop,seg_face,user]
        faces = [u_face[4] for u_face in tracked_faces]
        users = [u_face[5] for u_face in tracked_faces]
        
        for pro in self.projectiles:

            if pro.get_status() == EStatus.MOVING:
                collide = False
                for face,user in zip(faces, users):
                    collide = SAT.check_collide(Polygon(face),
                                                Polygon(pro.get_coordinates()))
                    if collide:
                        pro.update_status(EStatus.COLLIDING)
                        pro.update_colliding_face(face)
                        pro.update_colliding_user(user)
                        # self.collide = True
                        pro.update_image(con.GUN_EXPLODE_LINK)
                if pro.get_status() == EStatus.MOVING:
                    pro.fire(img_shape)
            elif pro.status == EStatus.DYING:
                self.projectiles.remove(pro)
            elif pro.status == EStatus.COLLIDING:
                user = pro.get_colliding_user()
                item = pro.get_item()
                count = pro.get_count()
                size = pro.get_size()
                if count == 5:
                    pro.update_status(EStatus.DYING)
                    # self.collide = False
                else:
                    pro.update_count(count + 1)
                    pro.update_size(size + count*5)
                
                if user.get_hp() > 0:
                    user.update_hp(-item.get_bonus_damage())

    
    def draw(self, image):
        for pro in self.projectiles:
            status = pro.get_status()
            if status == EStatus.MOVING or\
                status == EStatus.STAYING or\
                status == EStatus.COLLIDING:
        
                tl,_,br,_ = pro.get_coordinates()
                # in case it is outside of the frame

                LabelDrawer.merge_tranparent_image(image,
                                    pro.get_image(),
                                    tl,
                                    br)
                if status == EStatus.COLLIDING:
                    colliding_face = pro.get_colliding_face()
                    count = pro.get_count()
                    cv2.fillPoly(image, [np.array(colliding_face, dtype=np.int32)], con.DAMAGE_COLORS_BGR[count])
                        
                    