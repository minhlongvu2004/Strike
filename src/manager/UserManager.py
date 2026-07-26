
from src.entity import User


class UserManager:
    def __init__(self,
                 all_users: list[User]):
        # for this set up of class, I assume that each frame only has
        # maximum a face for each user. This mean that no user would exist twice
        # this help in managing the continous increment of id. However it might not work
        # well if someone actually exit twice
        
        self.all_users = all_users
        self.ids = [-1] * len(all_users)
    
    def register_users(self,recognized_users):
        for (id,user_name) in recognized_users:
            index = self.get_index_by_user_name(user_name)
            self.ids[index] = id
    
    def check_if_registered_id(self,need_check_id):
        for id in self.ids:
  
            if need_check_id == id:
                return True
        return False
    
    def get_index_by_user_name(self, user_name):
        for index, user in enumerate(self.all_users):
            if user_name == user.get_name():
                return index
    def get_id_by_index(self,index):
        return self.ids[index]
    def get_user_by_index(self,index):
        return self.all_users[index]
    
    def get_user_by_id(self, user_id):
        for i,id in enumerate(self.ids):
            if user_id == id:
                return  self.all_users[i]
        return None