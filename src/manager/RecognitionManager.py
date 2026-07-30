"""
Filename: RecognitionManager.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script is recognizing faces
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"

from os import listdir

import cv2
from keras_facenet import FaceNet
import numpy as np
from sklearn.preprocessing import LabelEncoder, Normalizer
from sklearn.svm import SVC
from src.other import constants as con

class RecognitionManager:
    """
    Summary:
        This class is for recognizing faces

    Fields:
        facenet_model: FaceNet
            The main facenet model that extract features into embedding
        normalizer: Normalizer
            The object to normalize the embedding
        label_encoder: LabelEncoder
            The object to convert to categorical label into numerical form for AI model
        svm_model: SVC
            This is our classifier
    Methods:
        recognize_users
        load_dataset_faces
    """
    def __init__(self,
                 identity_dir):
        self.facenet_model = FaceNet()
        self.normalizer = Normalizer(norm='l2')
        self.label_encoder = LabelEncoder()
        self.svm_model = SVC(kernel='linear', probability=True)

        
        
        train_faces, train_labels = self.load_dataset_faces(identity_dir)
        embeded_faces = list()
        embeded_faces = self.facenet_model.embeddings(train_faces)
        X = self.normalizer.transform(embeded_faces)
        self.label_encoder.fit(train_labels)
        Y = self.label_encoder.transform(train_labels)
        self.svm_model.fit(X,Y)
    
    def recognize_users(self, faces, ids):
        """
        Summary

        Args:
            faces: List[np.ndarray]
                List of faces
            ids: List[int]
                List of id

        Returns:
            recognized_faces: List[int,str]
                List of user id and user name
        """
        
        
        recognized_faces = []

        embbeddings = self.facenet_model.embeddings(faces)
        normalized_embeddings = self.normalizer.transform(embbeddings)
        predictions = self.svm_model.predict_proba(normalized_embeddings)
        best_class_idexs = np.argmax(predictions,axis=1)
    
        for i,(index,id) in enumerate(zip(best_class_idexs,ids)):
            probability = predictions[i][index] * 100
  
            if(probability > con.RECOGNITION_THRESHOLD ):
                user_name = self.label_encoder.inverse_transform([index])[0]
   
                recognized_faces.append((int(id),user_name))
                
        return recognized_faces
        
    def load_dataset_faces(self,directory):
        """
        Summary:
            load the dataset that store identities for the user

        Args:
            directory: str
                The path to the identity directory

        Returns:
            faces: List[np.ndarray]
                List of faces
            names: str
                List of names
        """
        
        faces = list()
        names = list()
        for filename in listdir(directory):
            
            path = directory + '\\'+ filename
            name = filename
            for img in listdir(path):
                face = cv2.imread(path + '\\' + img)
                faces.append(face)
                names.append(name)
        return faces, names