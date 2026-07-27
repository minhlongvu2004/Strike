# Run the script

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
- Step 4: install requirements txt
```
pip install -r requirements.txt
```

- Step 5: install cuda version
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --no-cache-dir
```
- Step 6: Run this small script to ensure that everythign work well
```
python -c "import torch; print(f'Is CUDA available? {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}')"
```
if you see True and GPU name then it is sucessful
<img width="682" height="62" alt="Image" src="https://github.com/user-attachments/assets/cf883b27-de5e-4bdc-82dd-23ab97f181c4" />
