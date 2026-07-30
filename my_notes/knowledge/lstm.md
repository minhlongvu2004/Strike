I have to be honest that i don't quite understand how LSTM. In future I probably need more coures and researches to understand. For now, I will try to note down all the necessary information and how do I even make one. Yes it might be wrong but that is solid foundation to improve in the future
# RNN
### Definition of RNN
Recurrent Neural Network is a class of neural networks that process sequential data by retrieving information from previous steps.
A usual Neural Network has independent input and output. The RNN, on the other hand, [passes](https://www.ibm.com/think/topics/lstm) the previous state and current input to the nodes in the network. This allows it to get back information from the previous step. We could see that it works for sequential and temporal data
### Architecture
So for a simple RNN, it stores its long-term memory in the form of [weights](https://www.ibm.com/think/topics/lstm) and short-term in terms of activation(hidden state) from one node to its successor.

<img width="800" height="400" alt="Image" src="https://github.com/user-attachments/assets/9b124557-9975-4a83-9d66-2815ec15bbc1" />

As seen above, for a node, it receives input and hidden state from other nodes, then produces its own output and hidden state for the next node.

### Problem of RNN
Theoretically, RNN could handle long-term dependencies. However, in practice, it couldn't do [that](https://www.ibm.com/think/topics/lstm). There are two main issues.
- **Vanishing gradient:** During backpropagation, the gradient is so small that it doesn't make the calculation effective.
- **Exploding gradient:** Opposite to the above, the gradient is so big that it could step away from the optimal solution or, worse, overflow


# LSTM
Long Short-term Memory is an [improved](https://www.geeksforgeeks.org/deep-learning/deep-learning-introduction-to-long-short-term-memory/) version of RNN. Its improvement is to solve the problem above RNN. The general idea is still similiar to RNN about hidden state. The only difference is that each single reucrrent node is replaced with more complex object called memory cell.

<img width="800" height="400" alt="Image" src="https://github.com/user-attachments/assets/c814eb77-6520-4aee-8981-5355592b2938" />

In short, Each LSTM contains 3 gates and one cell state. It receive the cell state, hidden state from previous cell, and the input. It output the its own cell state,hidden state, and the output. This cell state is for the long term memory of past cells while the hidden state is for the immedtiately previous cell. The information flow from forget,  input and ouput gae
- Forget gate: Decide how much information should be kept or removed
- Input gate: decide how much information is added into the memory
- Output gate: Determine which part of internal state become visible as output and hidden state





# Stateful vs Stateless
**there is a question I was confused about: If I have 20 frames and input it to the machine to predict an action. Next I have another 20 frames to predict another action? Will the first 20 frames information carry to my current 20 frames? In other word, will the first prediction affect my second prediction?**
This turn out actually a fair question since it lead to the concept of stateless and stateful. As explained in [here](https://hackernoon.com/stateless-vs-stateful-lstms-in-machine-learning) and in [here](https://stackoverflow.com/questions/39681046/keras-stateful-vs-stateless-lstms). Each time we input 20 frames is called a batch. The batch 1 would initate state for the second batch but there are two strategy
- ***Stateful:*** Batch one send its hidden state to batch 2. This is what make predict 1 affect prediction 2
- ***Stateless:*** Batch one reset to zero all the time it initate states. This is waht make prediction 1 independent with prediction 2
FOr our application, we only want to define the window size of 20 which means only latest 20 counts. Anything before is irrelavant, thus each our prediction for 20 is totally independent. Therefore, we would go ***stateless*** for our project
# Train LSTM

### Sampling 
The Mediapipe hand landmarks provide two type of coordinates: landmark and word landmark. I chose to draw UI by using landmark but train lstm based world landmark. 

<img width="1543" height="538" alt="Image" src="https://github.com/user-attachments/assets/b2f0fa8b-4692-4134-a86e-1c3cddd6d20c" />

As show in the digram, I choose the wrist at my origin. Also I will normalize all the points by the distance between wrist-0 and middle mcp-9. Therefore, it would remove the dependent on the size and absolute position of points
```
 wrist = world_points[0]
middle_mcp = world_points[9]
scale = max(math.dist(wrist, middle_mcp), 1e-6) # Avoid division by zero
normalized = (world_points - wrist) / scale
```
Next, since my intention is to predict dynamic action so veclocity is an crucial factor. Thus I substract the current frame with previous frame to obtain velocity
```
deltas = normalized - prev_frame if len(prev_frame) > 0 else np.zeros_like(normalized)
```
Next I concatenate the coordinates with its corresponding vector. Axis = 1 means we target the columns and keep rows
```
ready_frame = np.concatenate([normalized, deltas], axis=1).flatten()
```

Next I wrote an program to automatically record 20 frames when you clicks S. Detailed is provided in ***lstm_sampling.py***

https://github.com/user-attachments/assets/33dac4f7-b094-4cce-b0c6-01b68514ec7b

As I experiment, each action should have at least 50 samples.
For each batch, we consider 20 frames. Each frame has 21 points. Each points has 3 elements for x,y,z and 3 for delta_x,delta_y,delta_z.
Since we flatten the whole, so each frame would have 21 * 6 = 126. So our shape would (20, 126)

# Train
I have to be honest i don't quite understand how training works, i simply follow youtube [tutorial](https://www.youtube.com/watch?v=doDUihpj6ro&t=6498s) with little twisted in architecture. In future when I have enough knowledge, I would come back here and make it better