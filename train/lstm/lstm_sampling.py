'''
This file scrip is insteded to take the samples for training the LSTM

'''


import cv2
import os
import numpy as np
'''
how to write videox
'''
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
# 1. Initialize the HandLandmarker
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(options)

# 2. Define standard hand connections (these replace mp.solutions.hands.HAND_CONNECTIONS)
# Indices represent the 21 hand landmarks provided by MediaPipe
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8), # Index
    (5, 9), (9, 10), (10, 11), (11, 12), # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky/Palm
]

def draw_landmarks(image, detection_result):
    h, w, _ = image.shape
    # detection_result.hand_landmarks list of all hands
   
    if detection_result.hand_landmarks:
        
        for hand_landmarks,hand_world_landmarks in zip(detection_result.hand_landmarks,
                                                       detection_result.hand_world_landmarks):
            # hand_landmarks: list of all landmarks of a particular hand
            points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
   
            # world_points = [(int(lm.x * w), int(lm.y * h)) for lm in detection_result.hand_world_landmarks]
            # 1. Draw existing connections
            for start, end in HAND_CONNECTIONS:
                cv2.line(image, points[start], points[end], (0, 255, 0), 2)
            
            # 2. Draw existing points
            for x, y in points:
                cv2.circle(image, (x, y), 5, (255, 0, 0), -1)         
            # 3. Draw a rectangle between landmark 8 and 12
            # cv2.rectangle expects (top-left, bottom-right)
    # this logic fail because it trying to get coordination of a point of a hand. Remember that a hand has up to 21
    # points
    

    
# def analyze_result(detection_result):
#     intial_array = np.array([(lm.x, lm.y,lm.z) for lm in detection_result.hand_world_landmarks[0]]).flatten() if detection_result.hand_landmarks else np.zeros(21*3)
    
    
def get_world_points(detection_result):
    if detection_result.hand_world_landmarks:
        return np.array([(lm.x, lm.y, lm.z) for lm in detection_result.hand_world_landmarks[0]])
    return np.zeros((21,3), dtype=np.float32)


def process_world_points(world_points, prev_frame):
    wrist = world_points[0]
    middle_mcp = world_points[9]
    scale = max(math.dist(wrist, middle_mcp), 1e-6) # Avoid division by zero
    
    normalized = (world_points - wrist) / scale
    deltas = normalized - prev_frame if len(prev_frame) > 0 else np.zeros_like(normalized)
   
    
    # axis 1 so concatenate with correspond element
    return np.concatenate([normalized, deltas], axis=1).flatten(), normalized



FONT =  cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
THICKNESS = 2
PADDING = 20

def sample_video(label, 
                 frame_duration, 
                 start_label_counter, 
                 stop_label_counter):        
    label = label
    label_counter = start_label_counter
    clicked = False
    captured_video = []
    frame_counter = 0
    frames_duration = frame_duration 
    top_left = 640
    cap = cv2.VideoCapture(0)
    timestamp = 0
    prev_frame = []

    while cap.isOpened():
        success, frame = cap.read()
        h,w,_ = frame.shape
        h,w,_ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = detector.detect_for_video(mp_image, timestamp)
        timestamp += 1



    # Draw manually on the original BGR frame
        draw_landmarks(frame, detection_result)
        
        if clicked == False: 
            frame = draw_waiting_text(frame)
        else:
            # captured_video.append(frame)
            world_points = get_world_points(detection_result)
  
            processed, normalized = process_world_points(world_points,prev_frame)
            prev_frame = normalized
            directory_name = f"./{label}/{label_counter}"
            os.makedirs(directory_name, exist_ok=True)
            np.save(f'{directory_name}/{frame_counter}.npy', processed)
            frame_counter = (frame_counter + 1) % frames_duration
            
        draw_label(frame, label, label_counter)
            
        
        if frame_counter == 0 and clicked == True:
            label_counter = label_counter + 1
            clicked = False
            prev_frame = []
            
        
        
        if label_counter == stop_label_counter + 1:
            break
        if cv2.waitKey(1) & 0xFF == ord('s') :
            clicked = not clicked  # Set your flag to start recording
            
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        

    cap.release()
    cv2.destroyAllWindows()
    
def draw_waiting_text(frame):
    h,w,_ = frame.shape
    text = "Click S to start 1s Record"
    size, _ = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)
    width, height = size
    
    center = (w//2, h//2)
    top_left = (center[0] - width//2 - PADDING,
                center[1] - height//2 - PADDING)
    bottom_right = (center[0] + width//2 + PADDING,
                    center[1] + height//2 + PADDING)
    bottom_left = (center[0] - width//2, 
                center[1] + height//2)
    frame  = cv2.blur(frame,(20,20))
    cv2.rectangle(frame, top_left, bottom_right, (11, 12, 16), -1)
    
    cv2.putText(frame, text, bottom_left, FONT, FONT_SCALE, (102, 252, 241), THICKNESS)
    # we have to return because cv2.blur convert reference to local which break the link
    # if we don't do cv2.blur, we could apply rectangle and puttext directly
    return frame
def draw_label(frame, label, sample_counter):
    
    bottom_left = (30,30)
    text = f"{label}: {sample_counter}"
    cv2.putText(frame, text, bottom_left, FONT, FONT_SCALE, (102, 252, 241), THICKNESS)

# sample_video("./actions5/click", 20, 0, 40)
sample_video("./actions5/open_palm", 20, 0, 40)
# sample_video("./actions5/gun_pose", 20, 0, 40)
# sample_video("./actions5/fire", 20, 0, 40)
# sample_video("./actions5/any", 20, 0, 40)