<h1 align="center"> 📝Really Basic LSTM Note📝 </h1>

# Table of contents
<small>

- [1 RNN](#1-rnn)
  - [1.1 Definition of RNN](#11-definition-of-rnn)
  - [1.2 Architecture](#12-architecture)
  - [1.3 Problem of RNN](#13-problem-of-rnn)
- [2 LSTM](#2-lstm)
- [3 Stateful vs Stateless](#3-stateful-vs-stateless)
- [4 Train LSTM](#4-train-lstm)
  - [4.1 Sampling](#41-sampling)
  - [4.2 Training](#42-trainning)

</small>

I have to be honest that I don't quite understand LSTM. In the future, I probably need more courses and research to understand. For now, I will try to note down all the necessary information and how to make one. Yes, it might be wrong, but that is a solid foundation to improve in the future
# 1 RNN
### 1.1 Definition of RNN
Recurrent Neural Network is a class of neural networks that process sequential data by retrieving information from previous steps.
A usual Neural Network has independent input and output. The RNN, on the other hand, [passes](https://www.ibm.com/think/topics/lstm) the previous state and current input to the nodes in the network. This allows it to get back information from the previous step. We could see that it works for sequential and temporal data
### 1.2 Architecture
So for a simple RNN, it stores its long-term memory in the form of [weights](https://www.ibm.com/think/topics/lstm) and short-term in terms of activation(hidden state) from one node to its successor.

<img width="800" height="400" alt="Image" src="https://github.com/user-attachments/assets/9b124557-9975-4a83-9d66-2815ec15bbc1" />

As seen above, for a node, it receives input and hidden state from other nodes, then produces its own output and hidden state for the next node.

### 1.3 Problem of RNN
Theoretically, RNN could handle long-term dependencies. However, in practice, it couldn't do [that](https://www.ibm.com/think/topics/lstm). There are two main issues.
- **Vanishing gradient:** During backpropagation, the gradient is so small that it doesn't make the calculation effective.
- **Exploding gradient:** Opposite to the above, the gradient is so big that it could step away from the optimal solution or, worse, overflow


# 2 LSTM
Long Short-term Memory is an [improved](https://www.geeksforgeeks.org/deep-learning/deep-learning-introduction-to-long-short-term-memory/) version of RNN. Its improvement is to solve the problem above RNN. The general idea is still similar to RNN about hidden state. The only difference is that every single recurrent node is replaced with a more complex object called a memory cell.

<img width="800" height="400" alt="Image" src="https://github.com/user-attachments/assets/c814eb77-6520-4aee-8981-5355592b2938" />

In short, each LSTM cell contains 3 gates and one cell state. It receives the cell state and hidden state from the previous cell, and the input. It outputs its own cell state, hidden state, and the output. This cell state is for the long-term memory of past cells, while the hidden state is for the immediately previous cell. The information flow from the forget,  input, and output gates
- **Forget gate:** decides how much information should be kept or removed
- **Input gate:** decides how much information is added into the memory
- **Output gate:** determines which part of the internal state becomes visible as output and hidden state

# 3 Stateful vs Stateless
**There is a question I was confused about: If I have 20 frames and input them to the machine to predict an action.  Next, I have another 20 frames to predict another action? Will the first 20 frames' information carry over to my current 20 frames? In other words, will the first prediction affect my second prediction?**
This turns out to be a fair question since it led to the concept of stateless and stateful. As explained in [here](https://hackernoon.com/stateless-vs-stateful-lstms-in-machine-learning) and in [here](https://stackoverflow.com/questions/39681046/keras-stateful-vs-stateless-lstms). Each time we input 20 frames is called a batch. The first batch 1 would initiate state for the second batch, but there are two strategies
- ***Stateful:*** Batch one sends its hidden state to batch 2. This is what makes prediction 1 affect prediction 2

- ***Stateless:*** Batch one resets to zero all the time it initiates states. This is what makes prediction 1 independent of prediction 2

For our application, we only want to define the window size of 20, which means only the latest 20 counts. Anything before is irrelevant. Thus, each of our predictions for 20 is totally independent. Therefore, we would go ***stateless*** for our project
# 4 Train LSTM

### 4.1 Sampling 
The Mediapipe hand landmarks provide two types of coordinates: landmark and world landmark. I chose to draw the UI by using landmarks but train lstm based world landmarks. 

<img width="1543" height="538" alt="Image" src="https://github.com/user-attachments/assets/b2f0fa8b-4692-4134-a86e-1c3cddd6d20c" />

As shown in the diagram, I choose the wrist as my origin. Also, I will normalize all the points by the distance between wrist-0 and middle mcp-9. Therefore, it would remove the dependence on the size and absolute position of points.
```
 wrist = world_points[0]
middle_mcp = world_points[9]
scale = max(math.dist(wrist, middle_mcp), 1e-6) # Avoid division by zero
normalized = (world_points - wrist) / scale
```
Next, since my intention is to predict dynamic action, velocity is a crucial factor. Thus, I subtract the current frame from the previous frame to obtain velocity.
```
deltas = normalized - prev_frame if len(prev_frame) > 0 else np.zeros_like(normalized)
```
Next, I concatenate the coordinates with their corresponding vector. Axis = 1 means we target the columns and keep rows.
```
ready_frame = np.concatenate([normalized, deltas], axis=1).flatten()
```

Next, I wrote a program to automatically record 20 frames when you press S. Details are provided in ***lstm_sampling.py***

<video src="https://github.com/user-attachments/assets/33dac4f7-b094-4cce-b0c6-01b68514ec7b" width="60%" controls></video>

As I experiment, each action should have at least 50 samples.
For each batch, we consider 20 frames. Each frame has 21 points. Each point has 3 elements for x,y,z and 3 for delta_x,delta_y,delta_z.
Since we flatten the whole, each frame would have 21 * 6 = 126. So our shape would be (20, 126)

### 4.2 Trainning
I have to be honest, I don't quite understand how training works. I simply follow a YouTube [tutorial](https://www.youtube.com/watch?v=doDUihpj6ro&t=6498s) with a little twist in architecture. In the future, when I have enough knowledge, I will come back here and make it better.