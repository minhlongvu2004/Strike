<h1 align="center">🕵️‍♂️Face Recognition with YOLO, SORT, and FaceNet🕵️‍♂️</h1>

# Description

# Demo

<video src="https://github.com/user-attachments/assets/565989c3-f70e-46aa-980f-b0911cc4ff86" width="60%" controls></video>

# Tech Used

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


# Structure Folder


# Run script

- Step 1: clone the project
```
git clone https://github.com/minhlongvu2004/SRE-Strike.git
```
- Step 2: Create virtual enviroment
```
py -3.12 -m venv venv 
```
- Step 3: Open venv
```
venv\Scripts\activate
```
Make sure that your interpreter now is venv(3.12) like below
<img width="741" height="103" alt="Image" src="https://github.com/user-attachments/assets/6a115b27-5ee6-4cb2-9bc3-ab4a4f21eefa" />
- Step 4: install requirements txt
```
pip install -r requirements.txt
```
- Step 5: Run this small script to ensure that everythign work well
```
python -c "import torch; print(f'Is CUDA available? {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}')"
```
if you see True and GPU name then it is sucessful
<img width="682" height="62" alt="Image" src="https://github.com/user-attachments/assets/cf883b27-de5e-4bdc-82dd-23ab97f181c4" />

- Step 6: Run your application and enjoy
```
python main.py
```

# Futrue Improvement
- Adding LLM: This would create personality for our system.
- Using Game engine like unity or OpenGL: For now i just overlay those images to create effect. It doesn't look quite good. It would be great if we can use OpenGL to make it more 
- Increase the classes of LSTM: for now i only have 3-4 classes for LSTM. For a system game with many skills, it would be beneficial if we could train on more gestures to activate skills
- Improve the LSTM: The current LSTM accomdate for the normalized position and difference with previous frame for the speed. It work kind acceptable but I have to admit that it is somewhat overfit it to illstrate my idea. But we could accomadate feature like angles or more. We could even ultilize Ensemble learning such Bagging

# Troubleshoot

### 1. Mistmatch the name
So it display the wrong name like below. My name is *Minh Long Vu* but it display me as *Stephen Chow*

<img width="525" height="516" alt="Image" src="https://github.com/user-attachments/assets/97785f32-675f-4477-99d6-fd18b66d9444" />

the Facenet/SVM work well for recognizing the face so if it display wrong name for you, it is likely there are no or not enough images for SVM to learn

**Solution**: 
- Step 1: Create a folder with your name in /assets/identity
<img width="407" height="281" alt="Image" src="https://github.com/user-attachments/assets/ed714296-6757-4f9f-b55e-881396ea08d6" />

- Step 2: Gather around 20 images of yours and store it in the 
<img width="983" height="465" alt="Image" src="https://github.com/user-attachments/assets/113cc20f-bca2-44dd-b158-69dc58444dd4" />
Remember to crop your image so it contains only the face. This would significantly reduce the training time

- Step 3: In the *main.py*, create new user and register it to User Manager.

<img width="682" height="597" alt="Image" src="https://github.com/user-attachments/assets/e6657c9b-741e-40d2-9afc-48faa1e08943" />

Please note that user name in User Object must match with the user name in your folder 


### 2. List is out of index

<img width="1397" height="410" alt="Image" src="https://github.com/user-attachments/assets/f0c07a10-9f1f-47fd-9a10-fce79b012028" />

This is likely that you have image of your name but has not register it or misname it. For example my folder is "Minh Long" but the register name is "minh long vu"

<img width="1057" height="311" alt="Image" src="https://github.com/user-attachments/assets/99eb8559-6e17-4672-8704-d4c97398b2a2" />

*Solution*: Just try to match the *User* user name and the *folder* user name

<img width="940" height="257" alt="Image" src="https://github.com/user-attachments/assets/838593e5-8626-446f-bebc-91ffc7252f88" />
