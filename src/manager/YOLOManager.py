"""
Filename: YOLOManager.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script is for running the YOLO
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"

import math

import cv2
from ultralytics import YOLO

class YOLOManager:
    """
    Summary:
        The class is used to manage the user. The main focus is the register user where we replace
        the corresponding id based on user name
        
    Fields:
        segment_model: YOLO
            the YOLO segment model 
        detections: List[int,int,int,int,int]
            List of segment detection in the format [x1,y1,x2,y2,conf]
        face_segments: List[List[tuple[int,int]]]
            The list of face segment. Each face segment is the list of vertices of face polygon
        crop_faces: List[np.ndarray]
            The list of cropped face image
        
    Methods:
        get_detections_crops_segments
        detect_faces
    """   
    def __init__(self, model_path):
        self.segment_model = YOLO(model_path)
        self.segment_model.to('cuda')
        self.detections = []
        self.face_segments = []
        self.crop_faces = []
        
    def get_detections_crops_segments(self):
        return self.detections, self.crop_faces, self.face_segments
    
    def detect_faces(self, frame):
        self.detections = []
        self.face_segments = []
        self.crop_faces = []
        segment_results = self.segment_model(frame,verbose=False)
        for result in segment_results:
            if result.masks is not None:
                for points, box in zip(result.masks.xy,result.boxes):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = int(float(box.conf[0]) * 100)
                    self.face_segments.append(points)
                    self.detections.append([x1,y1,x2,y2,conf])
                    self.crop_faces.append(frame[y1:y2,x1:x2].copy())
                    
                    
                    
  
    