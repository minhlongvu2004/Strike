# Description

# Demo

# Tech Used
<video src="https://github.com/user-attachments/assets/565989c3-f70e-46aa-980f-b0911cc4ff86" width="60%" controls></video>


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

## Mistmatch the name
the Facenet/SVM work well for recognizing the face so if it display wrong name for you, it is likely there are no or not enough images for SVM to learn

## List is out of index
This is likely that you have image of your name but has not register it or misname it. For example my folder is "Minh Long" but the register name is "Mnh Long"
