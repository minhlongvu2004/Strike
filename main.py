from collections import deque
import queue
import threading
import time
from src.enum import ERole, EItem

from src.utils import LabelDrawer
from src.other import constants as con
from src.manager import HandManager,HUDManager,LSTMManager,ProjectileManager,\
    RecognitionManager,TrackerManager,UserManager,YOLOManager
from src.entity import User, Item, ItemList
import cv2

import numpy as np

QUEUE_MAX_SIZE = 1


def FrameCaptureThread(frame_queue: queue.Queue):
    # remember to set the max size for queue
    
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if success == False:
            continue
        frame_queue.put(frame)
        
def FaceRecognitionThread(recognition_manager: RecognitionManager,
                          user_manager: UserManager,
                          recognition_queue: queue.Queue):
    
        # this recognition queue is a list of tuple 
        # (faces,id)
        # we have to run FaceNet and SVM based on this
        # if the prob is more than 50 then we will register it to 
        # a dictionary. This dictionary should have something like
        # id:class
        while True:
            # [tl,br,id,face,user]
            untracked_faces = recognition_queue.get()
            faces = [u_face[3] for u_face in untracked_faces]
            ids = [u_face[2] for u_face in untracked_faces]
            recognize_users = recognition_manager.recognize_users(faces,ids)
            user_manager.register_users(recognize_users)
        
def SELUThread(frame_queue:queue.Queue,
               read_queue: queue.Queue,
               recognition_queue: queue.Queue,
               yolo_manager: YOLOManager,
               main_user: User,
               hand_manager: HandManager,
               lstm_manager: LSTMManager,
               hud_manager: HUDManager,
               projectile_manager: ProjectileManager,
               track_manager: TrackerManager):
    frame_counter = 0
    while True:
        frame = frame_queue.get()
        yolo_manager.detect_faces(frame)
        end1 =  cv2.getTickCount()
        detections, crops,face_segments= yolo_manager.get_detections_crops_segments()
        tracked_ids,untracked_ids = track_manager.track_detections(detections)
        # at this point we loose information about tracked_id
        tracked_faces = track_manager.reassociate_ids_faces(tracked_ids, detections,crops,face_segments)
        # untrack face will have user = None
        untracked_faces = track_manager.reassociate_ids_faces(untracked_ids, detections,crops,face_segments)
        
        
        
        
        LabelDrawer.draw_labels(frame, tracked_faces)
        
        
        # Detect Hand LandMark
        hand_manager.detect_landmarks(frame)
        hand_manager.process_world_points()
        lstm_manager.predict(hand_manager.get_sequence())
        current_pose,_ = lstm_manager.get_current_pose()
    
        index_polygon = hand_manager.get_index_finger_polygon()
        hud_manager.check_if_click_item_hud(current_pose,index_polygon)
        hud_manager.check_if_select_items_list(current_pose,index_polygon)
        current_skill_item = hud_manager.get_item()
        is_open_list = hud_manager.is_open_item_list()
        is_open_system_status = hud_manager.is_open_system_status()
        is_open_list_system = is_open_list or is_open_system_status
        # detect collision
        
        
        # Draw
        hud_manager.draw_system_icon(frame)
        hud_manager.draw_mu_hud(frame)
        hud_manager.draw_system_status_hud(frame)
        hud_manager.draw_sel_list(frame)
        # 
        hand_manager.update_skill(frame, 
                                  current_skill_item, 
                                  current_pose,
                                  tracked_faces,
                                  is_open_list_system)
        
        
        projectile_manager.update(frame.shape, tracked_faces)
        projectile_manager.draw(frame)
        
        
        read_queue.put(frame)
        if len(untracked_faces) >0 and frame_counter == 0:
                recognition_queue.put(untracked_faces)
        frame_counter = (frame_counter + 1) % con.RECOGNITION_INTERVAL



def main():
    main_user = User(con.MAIN_USER_NAME,
            con.FULL_HP,
             con.FULL_MP,
             con.FULL_EXP // 2,
             con.FULL_ATTACK,
             ERole.MAIN_USER,
             1,
            "True Dragon, Dream Creator, Greedy Dreamer",
            "Hand Of Death, World of Dreamers")
    gun = Item(con.GUN_NAME, 
               con.GUN_DAMAGE, 
               con.GUN_IMAGE_LINK, 
               con.LIST_ITEM__SIZE)
    katana = Item(con.KATANA_NAME, 
                  con.KATANA_DAMAGE, 
                  con.KATANA_IMAGE_LINK, 
                  con.LIST_ITEM__SIZE)
    hand = Item(con.HAND_NAME, 
                con.HAND_DAMAGE, 
                con.HAND_IMAGE_LINK, 
                con.LIST_ITEM__SIZE)
    potion = Item(con.POTION_NAME, 
                  con.POTION_DAMAGE, 
                  con.POTION_IMAGE_LINK, 
                  con.LIST_ITEM__SIZE)
    item_list = ItemList(con.TOP_LEFT_ITEMS_LIST,
                         katana, 
                         potion,
                         gun, 
                        hand, 
                         EItem.First)
    
    
    
    obama = User("Barack Obama",
                 con.FULL_HP,
                 con.FULL_MP,
                 con.FULL_EXP,
                 0,
                 ERole.OTHER_USER, 
                 99)
    trump = User("Donal Trump",
                 con.FULL_HP,
                 con.FULL_MP,
                 con.FULL_EXP,
                 0,
                 ERole.OTHER_USER, 
                 99)
    musk = User("Elon Musk",
                con.FULL_HP,
                con.FULL_MP,
                con.FULL_EXP,
                0,
                ERole.OTHER_USER, 
                999)
    ishowspeed = User("ishowspeed",
                      con.FULL_HP,
                      con.FULL_MP,
                      con.FULL_EXP,
                      0,
                      ERole.OTHER_USER, 
                      999)
    long = User("Minh Long Vu",
                con.FULL_HP,
                con.FULL_MP,
                con.FULL_EXP,
                0,
                ERole.OTHER_USER, 
                2026)
    chow = User("Stephen Chow",
                con.FULL_HP,
                con.FULL_MP,
                con.FULL_EXP,
                0,
                ERole.OTHER_USER,999)

    user_manager = UserManager([obama,
                                trump,
                                musk,
                                ishowspeed,
                                long,
                                chow])
    hud_manager = HUDManager(EItem.First, 
                                item_list,
                                main_user,
                                con.MAIN_HUD_TOP_LEFT,
                                con.TOP_LEFT_ITEMS_LIST,
                                con.SYSTEM_ICON_TOP_LEFT,
                                con.SYSTEM_ICON_TOP_RIGHT,
                                con.SYSTEM_ICON_BOTTOM_RIGHT,
                                con.SYSTEM_ICON_BOTTOM_LEFT,
                                con.SYSTEM_ICON_PATH,
                                con.CLOSE_LIST,
                                con.CLOSE_SYS)
    
        
    recognition_manager = RecognitionManager(con.RECOGNITION_IMAGES_PATH)

    # 3. ------ LSTM Manager ------------
    lstm_manager = LSTMManager(con.LSTM_WEIGHT_FILE, con.LSTM_LABEL_MAP)

    # 4. ------ Projectile Manager ------------
    projectile_manager = ProjectileManager()

    # 2. ------ Hand Manager ------------
    hand_manager = HandManager(main_user,projectile_manager)

    # 5. ------ YOLO Model
    yolo_manager = YOLOManager(con.YOLO_MODEL_PATH)
    # 6 ------- Track Manager
    track_manager =TrackerManager(con.MAX_AGE,
                                  con.MIN_HITS,
                                  con.IOU_THRESHOLD,
                                  user_manager)
    
    frame_queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)
    ready_queue = queue.Queue()
    recognition_queue = queue.Queue()
    capture_worker = threading.Thread(target = FrameCaptureThread,
                                    args=(frame_queue,),
                                    daemon=True)
    main_worker = threading.Thread(target = SELUThread,
                                    args=(frame_queue,
                                          ready_queue,
                                          recognition_queue,
                                          yolo_manager,
                                          main_user,
                                          hand_manager,
                                          lstm_manager,
                                          hud_manager,
                                          projectile_manager,
                                          track_manager),
                                    daemon=True)
    face_recognition_worker = threading.Thread(target = FaceRecognitionThread,
                                               args=(recognition_manager,
                                                     user_manager,
                                                     recognition_queue),
                                               daemon = True)
    
    capture_worker.start()
    main_worker.start()
    face_recognition_worker.start()
    
    time_buffer = deque(maxlen=20)
    last_time = -1
    
    while True:
        
        ready_frame = ready_queue.get()
        end = time.time()
        if last_time == -1:
            last_time = end
        else:
            delta = end - last_time
            time_buffer.append(delta)
            last_time = end
        if len(time_buffer) == 20:
            moving_average = len(time_buffer)/ sum(time_buffer)
            cv2.putText(ready_frame,f"FPS: {moving_average:.0f}",(10,10),cv2.FONT_HERSHEY_COMPLEX,0.4,(123,123,123),1)
        cv2.imshow("SREL Strike", ready_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()