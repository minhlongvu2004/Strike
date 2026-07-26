import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import TensorBoard
class LSTMManager:
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
        
    @tf.function(experimental_relax_shapes=True)
    def fast_predict(self,x):
        return self.model(x, training=False)
    
    def predict(self,frames_sequence):
        if len(frames_sequence) == 20:
            input_data = np.expand_dims(np.array(frames_sequence, dtype=np.float32), axis=0)
            res = self.fast_predict(input_data).numpy()[0]
            index = np.argmax(res)
            pose = self.label_map[index]
            self.current_pose = pose
            self.conf = res[index]
            
    def get_current_pose(self):
        return self.current_pose,self.conf
                