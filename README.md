<h1 align="center">⚔️🛡️ SREL Strike: Simple AR Game 🛡️⚔️</h1>

# Table of Contents

<small>

- [1. Description](#1-description)
  - [1.1 Objective](#11-objective)
  - [1.2 Architecture](#12-architecture)
    - [1.2.1 Main Component Explanation](#121-main-component-explanation)
    - [1.2.2 Rationale for the threads](#122-rationale-for-the-threads)
- [2. Demo](#2-demo)
- [3. Tech Used](#3-tech-used)
- [4. Structure Folder](#4-structure-folder)
- [5. Run script](#5-run-script)
- [6. Future Improvement](#6-future-improvement)
- [7. Troubleshoot](#7-troubleshoot)
    - [7.1 Mismatch in the name](#71-mismatch-in-the-name)
    - [7.2 List is out of index](#72-list-is-out-of-index)

</small>

# 1 Description
## 1.1 Objective 
***For those who love novels***

If you’ve ever read Solo Leveling, Nano Machine, or Omniscient Reader’s Viewpoint, you know the dream: having a personal, real-time AI interface to guide your path to the peak. This project is a first step toward that reality—an exploration of how modern technology can bridge the gap between imagination and a functional Augmented Reality (AR) interface.

***For Practical Problem-Solvers***

Even if the concept of a "System" doesn't resonate with you, this project remains a powerful demonstration of hands-free technology. This AR interface enables you to access and interact with critical information on the fly, eliminating the need for a laptop or handheld computer.

This is particularly invaluable in high-stakes environments where carrying bulky equipment is impossible—such as navigating a structure fire or operating in darkness where you must instantly identify and retrieve crucial objects. By leveraging a high-quality camera and a robust server to handle heavy AI model inference, this project proves that we can extend human perception and decision-making capabilities exactly when it matters most.

## 1.2 Architecture
The project could be illustrated as below

<img width="828" height="415" alt="Image" src="https://github.com/user-attachments/assets/dd754829-ea16-4ffc-88a4-c86817fc25d9" />

#### 1.2.1 Main Component Explanation
The project mainly uses 4 AI models for separate tasks: Segmentation, Recognition, Estimation, and LSTM; thus the name SREL.

- ***Segmentation:*** Use the YOLO model to detect the face boundary to track the face and define the hitbox

- ***Recognition:*** Since YOLO works well in determining general classes but is poor at detailed features such as faces, the FaceNet+SVM is utilized to handle this complex task. Recognition is to determine who is who

- ***Estimation:*** It is also called Pose Estimation, more specifically in this project Hand Pose Estimation. This is to detect which finger is what and their position

- ***LSTM:*** The Estimation only shows where the fingers could be but doesn't show what gesture it is. The LSTM helps in determining not just what the current gesture is but also determines what action the hand is doing based on the temporal information(previous frames)

#### 1.2.2 Rationale for the threads
- ***Frame Thread:*** The reason why we need a separate thread for this is that ```cv2.imread```introduces around 5 ms latency. This means that it would block the main thread for that time. Fortunately, that function is written in C++, so it will release the GIL when it works in C++. Thus, a separate thread allows other operations during that time.

- ***SELU Thread:*** 
Theoretically, I should have separated SORT, MediaPipe, LSTM, and UI into separate threads. The documentation of MediaPipe states that the image mode would [block](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker) the main thread. Thus, it might make sense if we use streaming, which is non-blocking. However, doing that might lead to a mismatch between the actual hand and the landmarks. I don't want that. I want the landmarks to stay exactly where the hand should be. Thus, I just put all of them together into one thread. 


- ***Recognition Thread:*** This thread is to recognize the cropped faces sent by the SELU thread. We have a separate thread for it because we accept that an image could take multiple frames to process. Whenever it is done, just update the value of ID to its corresponding faces.


- ***Main Thread:*** The main thread here means the main program. The reason why we need a separate one with SELU is that we use the ``` cv2.imshow```. As explained by this [comment](https://stackoverflow.com/questions/49096804/cv2-image-show-doesnt-work-when-multithreading), anything related to UI should be on the main thread. Additionally, ```cv2.imrshow``` also introduces additional latency around 5 ms. Having a separate thread for both ***cv2.imshow*** and ***cap.read*** would save around 10 ms.

# 2 Demo

<video src="https://github.com/user-attachments/assets/565989c3-f70e-46aa-980f-b0911cc4ff86" width="60%" controls></video>

# 3 Tech Used

<p align="left">
  <img src="https://img.shields.io/badge/Python-111d27?style=for-the-badge&logo=python&logoColor=3776AB" />
  <img src="https://img.shields.io/badge/YOLO-111d27?style=for-the-badge&logo=ultralytics&logoColor=8A2BE2" />
  <img src="https://img.shields.io/badge/MediaPipe-111d27?style=for-the-badge&logo=mediapipe&logoColor=4285F4" />
  <img src="https://img.shields.io/badge/scikit--learn-111d27?style=for-the-badge&logo=scikitlearn&logoColor=F7931E" />
  <img src="https://img.shields.io/badge/FaceNet-111d27?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LSTM-111d27?style=for-the-badge" />
  <img src="https://img.shields.io/badge/SVM-111d27?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenCV-111d27?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/SORT-111d27?style=for-the-badge" />
</p>


# 4 Structure Folder
```text
SREL-Strike/
├── assets/             # Non-script files
│   ├── identity/             # User images trained for SVM
│   └── item/                 # Images for game items
├── my_notes/           # Project learnings and documentation
│   ├── knowledge/            # Theoretical research
│   └── tutorial/             # Step-by-step implementation guides
├── src/                # Core application source code
│   ├── entity/               # Base classes for objects
│   ├── enum/                 # Custom data types
│   ├── manager/              # Operations for entities
│   ├── other/                # Constants and configuration
│   └── utils/                # Static helper classes and utilities
├── train/              # Training scripts
│   ├── lstm/                 # Gesture sampling and model training
│   └── segmentation/         # Training scripts for Google Colab
├── weights/            # Model weights
│   ├── action.h5             # LSTM action weights
│   ├── hand_landmarker.task  # MediaPipe landmarks
│   └── segmentation.pt       # Segmentation model weights
├── .gitignore          # Files to ignore when stage commit
├── demo.mp4            # Project demonstration video
├── LICENSE             # GPL license
├── main.py             # Main application entry point
├── README.md           # Project description
└── requirements.txt    # Project dependencies
```
# 5 Run script

- Step 1: Clone the project
```
git clone https://github.com/minhlongvu2004/SREL-Strike.git
```
- Step 2: Create virtual environment
```
py -3.12 -m venv venv 
```
- Step 3: Open venv
```
venv\Scripts\activate
```
Make sure that your interpreter is now venv (3.12), like below

<img width="741" height="103" alt="Image" src="https://github.com/user-attachments/assets/6a115b27-5ee6-4cb2-9bc3-ab4a4f21eefa" />

- Step 4: Install requirements.txt
```
pip install -r requirements.txt
```
- Step 5: Run this small script to ensure that everything works well
```
python -c "import torch; print(f'Is CUDA available? {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}')"
```
If you see True and the GPU name, then it is successful

<img width="682" height="62" alt="Image" src="https://github.com/user-attachments/assets/cf883b27-de5e-4bdc-82dd-23ab97f181c4" />

- Step 6: Run your application and enjoy
```
python main.py
```

P/S: Not necessarily Python 3.12 just any stable version is fine

# 6 Future Improvement
- **Adding a fine-tuned LLM:** This would create personality for our system.

- **Adding RAG:** Further extension from above, RAG would allow us to monitor the status of all users and recommend to the main player what he should do

- **Using a game engine like Unity or OpenGL:** For now, I just overlay those images to create an effect. It doesn't look quite good. It would be great if we could use OpenGL to make it more 

- **Increase the classes of LSTM:** for now I only have 3-4 classes for LSTM. For a system game with many skills, it would be beneficial if we could train on more gestures to activate skills

- **Improve the LSTM:** The current LSTM accommodates the normalized position and difference with the previous frame for the speed. It works kind of acceptable, but I have to admit that it is somewhat overfitted to illustrate my idea. But we could accommodate features like angles or more. We could even utilize ensemble learning, such as as bagging

# 7 Troubleshoot

#### 7.1 Mismatch in the name
So it displays the wrong name, like below. My name is *Minh Long Vu*, but it displays me as *Stephen Chow*

<img width="525" height="516" alt="Image" src="https://github.com/user-attachments/assets/97785f32-675f-4477-99d6-fd18b66d9444" />

The Facenet/SVM works well for recognizing the face, so if it displays the wrong name for you, it is likely that there are no or not enough images for the SVM to learn.

**Solution**: 
- ***Step 1:*** Create a folder with your name in /assets/identity
<img width="407" height="281" alt="Image" src="https://github.com/user-attachments/assets/ed714296-6757-4f9f-b55e-881396ea08d6" />

- ***Step 2:*** Gather around 20 images of yours and store them in the 

<img width="983" height="465" alt="Image" src="https://github.com/user-attachments/assets/113cc20f-bca2-44dd-b158-69dc58444dd4" />

Remember to crop your image so it contains only the face. This would significantly reduce the training time

- ***Step 3:*** In *main.py*, create a new user and register it to the User Manager.

<img width="682" height="597" alt="Image" src="https://github.com/user-attachments/assets/e6657c9b-741e-40d2-9afc-48faa1e08943" />

Please note that the username in the User Object must match the username in your folder. 


#### 7.2 List is out of index

<img width="1397" height="410" alt="Image" src="https://github.com/user-attachments/assets/f0c07a10-9f1f-47fd-9a10-fce79b012028" />

It is likely that you have an image of your name but have not registered it or misnamed it. For example, my folder is "Minh Long" but the registered name is "minh long vu"

<img width="1057" height="311" alt="Image" src="https://github.com/user-attachments/assets/99eb8559-6e17-4672-8704-d4c97398b2a2" />

**Solution**: Just try to match the *User* user name and the *folder* user name

<img width="940" height="257" alt="Image" src="https://github.com/user-attachments/assets/838593e5-8626-446f-bebc-91ffc7252f88" />
