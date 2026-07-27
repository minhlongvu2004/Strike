
import cv2
import numpy as np
from src.enum import ERole
from src.other import constants as con

class User:
    def __init__(self,
                 name, 
                 health_point: int,
                 mana_point: int, 
                 experience_point: int,
                 attack_damage : int, 
                 role : ERole,
                 level: int,
                 main_title= "",
                 main_ultimate_skill= ""):
        self.name = name
        self.hp = health_point
        self.mp = mana_point
        self.exp = experience_point
        self.atk = attack_damage
        self.role = role
        self.level = level
        self.death_image = cv2.imread(con.DEATH_IMAGE,cv2.IMREAD_UNCHANGED)
        self.give_exp = False
        self.main_title = main_title
        self.main_ultimate_skill = main_ultimate_skill
        
    def update_give_exp(self, is_give):
        self.give_exp = is_give
    def is_give_exp(self):
        return self.give_exp

    def get_title(self):
        return self.main_title
    def get_ultimate_skill(self):
        return self.main_ultimate_skill
    
    def update_give_exp(self, is_give):
        self.give_exp = is_give
    def is_give_exp(self):
        return self.give_exp

    def get_death_image(self):
        return self.death_image
    
    def get_user_image(self):
        return self.image
    # def update_main_user_hud(self):    
    
    # def get_main_user_hud(self):
    #     return

    def get_name(self):
        return self.name
    def get_level(self):
        return self.level
    def get_hp(self):
        return self.hp
    def get_mp(self):
        return self.mp 
    def get_exp(self):
        return self.exp
    def get_dmg(self):
        return self.atk
    
    
    
    def update_name(self,new_name):
        self.name = new_name
    
    def update_hp(self,new_hp):
        updated_hp = self.hp + new_hp
        if updated_hp <= 0:
            self.hp = 0
        else:
            self.hp = updated_hp
    def update_mp(self,new_mp):
        updated_mp = self.mp + new_mp
        if updated_mp <= 0:
            self.mp = 0
        else:
            self.mp=updated_mp
    def update_exp(self,new_exp):
        updated_exp = self.exp + new_exp
        if updated_exp >= 100:
            self.exp = updated_exp - 100
            self.level = self.level + 1
        else:
            self.exp += new_exp
    def update_atk(self,new_atk):
        self.atk += new_atk
    def update_lvl(self, new_lvl):
        self.level += new_lvl