"""
Filename: LSTMManager.py
Author: Minh Long Vu
Date: 2026-07-30
Description: This script is for LSTM model
"""

__author__ = "Minh Long Vu"
__license__ = "GPL"
__email__ = "minhlongvu626@gmail.com"
__status__ = "Prototype"


import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import TensorBoard
class LSTMManager:
    """
    Summary:
        This class is for LSTM model
    
    Fields:
        model: Sequential()
            The LSTM model
        current_pose: str
            the current pose after prediction
        conf: int
            The confident of the current pose
    
    Methods:
        fast_predict
        predict
        get_current_pose(
    """
    
    def __init__(self,
                 weight_file,label_map):
        self.weight_file = weight_file
        self.label_map = label_map
        model = Sequential([
            LSTM(128, return_sequences=True, activation='tanh', input_shape=(20, 126), dropout=0.2),
            LSTM(64, activation='tanh', dropout=0.2),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(len(label_map), activation='softmax')
        ])
        model.load_weights(weight_file)
        self.model = model
        self.current_pose = ""
        self.conf = 0
    def get_current_pose(self):
        return self.current_pose,self.conf
    
    
    @tf.function(experimental_relax_shapes=True)
    def fast_predict(self,x):
        """
        Summary:
            This is really fast inference function for LSTM

        Args:
            x: np.ndarray

        Returns:
            None
        """
        return self.model(x, training=False)
    
    def predict(self,frames_sequence):
        
        """
        Summary:
            Prepare the input and make a prediction using LSTM
        
        Args:
            frames_squence: deque(np.ndarray)
                The dequeue of 20 frames in np format
        Return:
            None
        """
        
        if len(frames_sequence) == 20:
            input_data = np.expand_dims(np.array(frames_sequence, dtype=np.float32), axis=0)
            res = self.fast_predict(input_data).numpy()[0]
            index = np.argmax(res)
            pose = self.label_map[index]
            self.current_pose = pose
            self.conf = res[index]
            

                