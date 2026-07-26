import numpy as np

from src.utils import Sort, iou_batch
from .UserManager import UserManager

class TrackerManager:
    
    def __init__(self, 
                 max_age,
                 min_hits,
                 iou_threshold,
                 user_manager:UserManager):
        self.tracker = Sort(max_age, min_hits,iou_threshold)
        self.user_manager = user_manager
        
        
    def reassociate_ids_faces(self,tracked_ids,detections,crops, face_segments):
        # bboxs is in format of [x1,y1,x2,y2,id]
        # sfaces is in format [x1,y1,x2,y2,sface] where 
        # x'1 is being noised by the Kalma filter. it might be
        # 10 pixels far away from origiona
        # the job is to associate id with sface.
        # basically the idea is to find the one that has bbbox that has
        # largest iou to corresponding sface
        # note that len(bboxs)<= len(sfaces)
        # bboxs is the row
        # sfaces is the columns
        # :4 means only take 0,1,2,3 and remove the last one
        # return [x1,y1,x2,y2,sface,id]
        ids_faces = []
        # bbox is row and sfaces is columns
        if not tracked_ids or not detections:
            return []
        tracked_data = np.array([item[:4] for item in tracked_ids])
        detection_data = np.array([item[:4] for item in detections])

        # 3. Now it is safe to call iou_batch
        iou_matrix = iou_batch(tracked_data, detection_data)
        # look maximum colum in a row
        # we want bbox so eliminate sfaces by stating axis=1
        best_face_indexs = np.argmax(iou_matrix,axis=1)

        for id_index, best_face_index in enumerate(best_face_indexs):
            score = iou_matrix[id_index, best_face_index]
         
            if score >= 0.8:
                x1 = detections[best_face_index][0]
                y1 = detections[best_face_index][1]
                x2 = detections[best_face_index][2]
                y2 = detections[best_face_index][3]
                face_segment = face_segments[best_face_index]
                crop = crops[best_face_index]
                top_left = (x1,y1)
                bottom_right = (x2,y2)
                id = int(tracked_ids[id_index][4])
                user = self.user_manager.get_user_by_id(id)
                
                
                ids_faces.append([top_left,
                                bottom_right,
                                id,
                                crop,
                                face_segment,
                                user])
        
        return ids_faces
        # it might be confusing but
        # assume we have a=[1,2,3,...,n] -> (n,) which is just a vector n
        # if we do expand(a,axis=0), this means that we add an dimension before it (1,n)
        # this result in [[1,2,3,4,...,n]]. Basically we wrap it in an []. This mean that we
        # increase one depth or convert it into a column
        # if we do expand(a,axis=1) we add dimension before it (n,1),
        # this mean that [[1],[2],[3],[4]]
        # so from vector convert to a column
        # Assume we have [[1,2,3...,N]_1,[1,2,3...N]_2,....,[]_M] which is (M,N)
        # when we do argmax(axis=0), we essetnial elimiate the first dimesnion it become (N,)
        # we see that it keep the same N or column so this find the max in column
        # if we do argmax(axis=1) we remove the second dimension so it become (M,)
        # think axis as layer and expand is add wraper and 
        # expand =0 means add wrapper at first layer, =1 means add wrapper at second layer
        # argmax means remove the first layer,
        

    def track_detections(self, detections):
        # [x1,y1,x2,y2,conf]
        # 
        # detection should be in the format [x1,y1,x2,y2,conf] where conf might be in scale of 100
        # 
        
        tracked_id = []
        untracked_id = []
        # crash when zero
        if len(detections) != 0:
            detections = np.array(detections)
         
            tracker_results = self.tracker.update(detections)
            for tracker_result in tracker_results:
                id = int(tracker_result[4])
                if self.user_manager.check_if_registered_id(id):
                    tracked_id.append(tracker_result)
                else:
                    untracked_id.append(tracker_result)
        id1 = [result[4] for result in tracked_id]
        id2 = [result[4] for result in untracked_id]
        print(f"track_id{id1} untrack_id{id2}")
        return tracked_id, untracked_id
            
            
            

    
    