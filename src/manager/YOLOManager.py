import math

import cv2
from ultralytics import YOLO

class YOLOManager:
    def __init__(self, model_path):
        self.segment_model = YOLO(model_path)
        self.segment_model.to('cuda')
        self.detections = []
        self.face_segments = []
        self.crop_face = []
        
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
                    
                    
                    
  
    