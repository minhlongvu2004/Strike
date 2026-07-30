<h1 align="center"> 📝OpenCV Note📝 </h1>

# Table of Contents

<small>

- [1. Dilation](#1-dilation)
- [2. Save time with ROI instead of full frame](#2-save-time-with-roi-instead-of-full-frame)
  - [2.1 Measurement](#21-measurement)
  - [2.2 How do I optimize it?](#22-how-do-i-optimize-it)
- [3. Problem with image slicing](#3-problem-with-image-slicing)
- [4. Transparent image](#4-transparent-image)
- [5. Draw dark haki hand](#5-draw-dark-haki-hand)

</small>

# 1 Dilation
So basically, the way we make a gloom effect by using thicker text, blurring, and placing the brighter 
in the middle is kinda obsolete. This can be seen below.

<img width="250" height="212" alt="Image" src="https://github.com/user-attachments/assets/333de9c8-dc5d-42b2-9d9c-b42a3ea03bad" />

I don't know the exact reason, but it might be that OpenCV changed its text engine. Thankfully, I figured out another way to do it by using [dilation](https://www.jeremymorgan.com/tutorials/opencv/dilate-opencv-python/). 
So the dilation algorithm basically compares all the neighbors against the central pixel (Neighbors are defined as a matrix in the kernel). And replaces the central pixel with the neighbor maximum value. You might think that it might cause a chain reaction to fill the whole thing. Valid question! It turns out that for every pixel, it only looks at the original input and draws it to the other output. Thus it won't affect
the input data, so no chain reaction would be made
```python
kernel =  np.ones((3, 3), np.uint8)
mask_neon = cv2.dilate(mask_neon, kernel, iterations=3)
```
As you can see here, we have re-assigned it if we want it to affect the original variable
This means that if we define a neighbor as [3,3]. Then the central pixel can only look at one pixel around it. So we can only increase one pixel from the border. If we make a second iteration, we would look 1 pixel further. So assume we have an odd kernel MxM, then the number of lines of pixels we could add from the border is 
$$\left\lfloor \frac{M}{2} \right\rfloor \cdot iteration$$

# 2 Save time with ROI instead of full frame
### 2.1 Measurement
In my previous project "Face Recognition", I used something like 
```
success, frame = cap.read()
cv2.GaussianBlur(frame,...)
```
Basically, I used Gaussian Blur for the whole frame, but its effect only takes place in a single small area. This drastically reduces the speed performance.
For example: to draw a small neon text like below. I define two variants of functions.

<img width="788" height="627" alt="Image" src="https://github.com/user-attachments/assets/fb14ded2-4670-4ebb-a00c-669bd5f4279a" />

The first one is, as usual, where I use the whole frame
```python
def draw_neon_text(frame, text):
    
 mask_neon = np.zeros_like(frame,dtype=np.uint8)
 cv2.putText(mask_neon, text, (50,50),cv2.FONT_HERSHEY_COMPLEX,0.6,TEXT_OUTER_COLOR,1)
 mask_neon = cv2.dilate(mask_neon,DILATE_KERNEL,iterations=1)
 mask_neon = cv2.GaussianBlur(mask_neon,BLUR_KERNEL,0)
 cv2.addWeighted(mask_neon,0.6,frame,0.4,0,frame)
 cv2.putText(frame, text, (50,50),cv2.FONT_HERSHEY_COMPLEX,0.6,TEXT_INNER_COLOR,1)
```
And the result below
```
Average for 100 frames: 3.82
Average for 100 frames: 3.79
Average for 100 frames: 3.78
Average for 100 frames: 3.80
Average for 100 frames: 3.81
Average for 100 frames: 3.83
Average for 100 frames: 3.86
```
So it takes around 3.5 ms to complete a single small neon text. This is quite an expensive operation because if we draw ten lines like this, it would take 35ms. This is equivalent to running another YOLO model. In order to improve this, I introduce the *ROI* or region of interest. Basically, only interact with the area that we intend to.

```python
def draw_neon_text(frame, text, top_left):
    
 txt_size, _ = cv2.getTextSize(text,cv2.FONT_HERSHEY_COMPLEX,0.6,1)
 t_w, t_h = txt_size
 padding = 5

 roi_w = t_w + 2 * padding
 roi_h = t_h + 2 * padding
        
 roi_tl = top_left
 roi_br = (top_left[0] + roi_w,
 top_left[1] + roi_h)
    
 roi = frame[roi_tl[1]:roi_br[1],
 roi_tl[0]:roi_br[0]]
    
 txt_tl = (padding, padding)
 txt_bl = (txt_tl[0],
 txt_tl[1] + t_h)
    
 mask_neon = np.zeros_like(roi,dtype=np.uint8)
 cv2.putText(mask_neon, text, txt_bl,cv2.FONT_HERSHEY_COMPLEX,0.6,TEXT_OUTER_COLOR,1)
 mask_neon = cv2.dilate(mask_neon,DILATE_KERNEL,iterations=1)
 mask_neon = cv2.GaussianBlur(mask_neon,BLUR_KERNEL,0)
    
 cv2.addWeighted(mask_neon,0.6,roi,1,0,roi)
    
 cv2.putText(roi, text, txt_bl,cv2.FONT_HERSHEY_COMPLEX,0.6,TEXT_INNER_COLOR,1)
```


and the result below
```
Average for 100 frames: 1.20
Average for 100 frames: 1.22
Average for 100 frames: 1.21
Average for 100 frames: 1.20
```
As you can see here, the neon text only takes around ***1.2 ms***. The difference is ***2.3 ms***.
Let's take an example of calculation:
*Full frame*:
Assume we were to draw 10 lines of neon. So it takes us 35 ms
Remember that the cv2.read() itself introduces latency around 5ms. 
The yolo model is around 30 ms
So our FPS would be 
$$\frac{1000}{35+5+30} \approx 14.3 FPS$$
This is quite slow since the bare minimum goal is 20 FPS and a good one is 30 FPS
*ROI*
10 lines of neons -> 12 ms
So our FPS would be 
$$\frac{1000}{12+5+30} \approx 21 FPS$$
You see! significantly improve the FPS

### 2.2 How do I optimize it?
Assume we want to take a small ROI region out of an image.

<img width="561" height="495" alt="Image" src="https://github.com/user-attachments/assets/f4daf442-a950-461a-b286-c270b3ab49c3" />

Since the image itself is just a numpy array, to take the ROI we basically slice the image along both axes. Let's say that (x1,y1) and (x2,y2) are the top left and bottom right of the ROI, respectively.

<img width="1003" height="562" alt="Image" src="https://github.com/user-attachments/assets/e25717a2-c56b-4958-8be1-af3e450389a2" /> 

Then, to take roi we simply need

$$roi = img[y1:y2,x1:x2]$$

Now that we have our ROI.

<img width="676" height="566" alt="Image" src="https://github.com/user-attachments/assets/a8895770-274b-41ff-aa2b-c911153a5030" />

It is still just a reference to our original frame, however, operations on this roi require the index to start from zero (not from the top-left of itself). To allow the neon effect to spread out. We might need some extra space from the text to the roi. So we need padding *pad*

<img width="637" height="541" alt="Image" src="https://github.com/user-attachments/assets/ecf29104-74bc-46f9-9144-370593ddd4b7" />

Not our last job is to calculate the width and height of the text content. 
```
(txt_w,txt_h),_ = cv2.getTexSize()
```

<img width="650" height="537" alt="Image" src="https://github.com/user-attachments/assets/623a5055-02a4-4cdc-a203-12856295db19" />

So our new coordinates for text are

```
txt_top_left = (pad, pad)
txt_bottom_right = (pad+txt_w,pad+txt_h)
```

However, since we only need bottom left for drawing text
```
txt_bl = (pad,pad + txt_h)
```

Now just treat it as the ROI the same way as the full frame in your operations. This is really efficient.

# 3 Problem with image slicing
Assume that we have an image ***img***. There is a problem with the code below.

```python
roi = image[y1:y2,x1:x2]
cv2.rectangle(roi, P1, P2, thick) # same for other like line
```
The problem is that whenever the (x1,y1), (x2,y2) exceed the image frame during slicing, it results in a zero in one dimension of ***ROI***. This is what causes an error for functions like cv2.rectangle
Example: Running this script
```python
import cv2
import numpy as np

image = np.zeros((500,500,3), dtype=np.uint8)
roi = image[-50:100,-50:200]
mask_neon = np.zeros_like(roi,dtype=np.uint8)
print(f"Shape of ROI:{roi.shape}")
print(f"Shape of Mask:{mask_neon.shape}")
cv2.rectangle(mask_neon, (50,50),(150,150),(123,123,123),-1)
cv2.addWeighted(mask_neon,0.6,roi,0.4,0,roi)
cv2.imshow("asd", image)
cv2.waitKey(0)
```
Then it would crash, stating that it is a bad argument.

<img width="1002" height="340" alt="Image" src="https://github.com/user-attachments/assets/14e46be6-3271-420b-9ca3-7fcbb2f8876a" />

However, it doesn't cause errors P1 and P2 exceeding the image frame
Example 2: Twists the ROI a bit where
```python
import cv2
import numpy as np

image = np.zeros((500,500,3), dtype=np.uint8)
roi = image[0:100,0:200]
mask_neon = np.zeros_like(roi,dtype=np.uint8)
print(f"Shape of ROI:{roi.shape}")
print(f"Shape of Mask:{mask_neon.shape}")
cv2.rectangle(mask_neon, (-50,-50),(50,50),(123,123,123),-1)
cv2.addWeighted(mask_neon,0.6,roi,0.4,0,roi)
cv2.imshow("asd", image)
cv2.waitKey(0)
```


<img width="622" height="207" alt="Image" src="https://github.com/user-attachments/assets/0d1a27f9-3e08-4871-8268-cabff53b478c" />

This will create an illusion as if the object still exists outside of the image. 
> [!NOTE]
> Doesn't matter where the points we are drawing are, as long as we are making sure that the input ROI doesn't have any zero dimensions; then it is totally okay even if we have negative drawing points
This note is what we need ot keep in mind when doing the slicing and drawing


# 4 Transparent image
Let's say that you want to load an image but don't want the rectangle around it. You just want a single object like the left object below.

<img width="227" height="111" alt="Image" src="https://github.com/user-attachments/assets/550921fb-d437-4b9a-81ae-dc7eb5516852" />

- **Step 1:** Make sure to convert it to a real unbackgrounded object. You could go [here](https://www.remove.bg/). Simply load your object and then download the transparent background.

- **Step 2:** Load the object into the app using the unchanged flag
```
img = cv2.imread(<path_to_ur_img>,cv2.IMREAD_UNCHANGED)
```
By specifying this flag, your img doesn't just have 3 dimensions as usual, but 4, with the extra being alpha for transparency

- **Step 3:** Define your ROI as above
```
roi = image[y1:y2,x1:x2]
```
- **Step 4:** Resize your image to the same size as your roi
```
resized_img = cv2.resize(item,(x2-x1,y2-y1))
```

As explained above, your object and your roi has different dimensions. Our plan is to reduce the resized_img from 4 to 3

- **Step 5:** Split dimensions
```
b, g, r, a = cv2.split(resized_img)
```
- **Step 6:** Merge BGR dimension
```
bgr_item = cv2.merge((b, g, r))
```
- **Step 7:** Normalize the alpha
Later, we will use alpha as a gate to filter or keep the image. Because we already defined what is and what is not. When we normalize it, it only takes values between 0 and 1
```
mask = a / 255.0
```
- **Step 8:** Convert to 3 array
Problem with mask: it is a 2D array where roi and object are 3D. So we add another dimension to it.
```
mask = mask[:, :, np.newaxis]
```
- **Step 9:** Now merge between roi and your object
```
roi[:,:] = (1-mask) * roi + mask * bgr_item
```
Specify [:,:] to state that we replace back to the original frame, not just rename. The operation basically means that we keep the original pixel if it is transparent (background), otherwise replace it with object content.

Note that you have an object without a black bounding box 

# 5 Draw dark haki hand 

<img width="383" height="437" alt="Image" src="https://github.com/user-attachments/assets/228216fd-8f43-4ebe-97f6-c01b0060b311" />

It is so funny that the above image is the problem I stated when I was writing the draft. I even wrote detail what the problem was, and then I just solved it while writing that.

#### Step 1: Define  the ROI
Let's first define the roi to reduce the cost of operation. We need to find the possible top left, so we will use np.min(axis=0). **axis = 0** means it targets the row, so all rows will be aggregated into a single row and return the min/max of that column
```python
points = np.array(self.landmarks)
x_min, y_min = np.min(points, axis=0) - 40
x_max, y_max = np.max(points, axis=0) + 40
x_min, y_min = max(0, x_min), max(0, y_min)
x_max, y_max = min(w, x_max), min(h, y_max)
if x_max - x_min <= 0 or y_max - y_min <= 0: return 
# above is to prevent crash
roi = image[y_min:y_max, x_min:x_max]
```
Basically, we find the top left and bottom right. We leave the padding at 40 because we need space for really strong dilation
#### Step 2: Redefine relative point
The *points* above are for the original frame. However, as mentioned in the section above, we have to recalculate the coordinates when we do the roi. Thankfully, we only need to extract the vector top left
```python
rel_points = points - [x_min, y_min]
```

#### Step 3: Make two masks
So in order to do this. I define two masks, one for the inner purple and one for the outer purple
```python
mask_outer = np.zeros_like(roi,dtype=np.uint8)
mask_middle = np.zeros_like(roi,dtype=np.uint8)
```

#### Step 4: Connect all the points
```python
HAND_CONNECTIONS = [
 (0, 1), (1, 2), (2, 3), (3, 4), 
 (0, 5), (5, 6), (6, 7), (7, 8), 
 (5, 9), (9, 10), (10, 11), (11, 12), 
 (9, 13), (13, 14), (14, 15), (15, 16), 
 (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
]
for start, end in con.HAND_CONNECTIONS:
 cv2.line(mask_outer, rel_points[start], rel_points[end], con.HAKI_OUTER, 3)
 cv2.line(mask_middle, rel_points[start], rel_points[end], con.HAKI_MIDDLE, 15)

poly_points = np.array([rel_points[2],
 rel_points[5],
 rel_points[9],
 rel_points[13],
 rel_points[17],
 rel_points[0],
 rel_points[1],], np.int32)
```
You can consult the landmark image below.

<img width="1543" height="538" alt="Image" src="https://github.com/user-attachments/assets/3efec22a-f08a-4e09-861c-b8a925d2ea42" />

#### Step 5: Apply dilation to both mask
```python
kernel_outer = np.ones((5, 5), np.uint8)
mask_outer = cv2.dilate(mask_outer, kernel_outer, iterations=8)

kernel_midle = np.ones((3, 3), np.uint8)
mask_middle = cv2.dilate(mask_middle, kernel_midle, iterations=5)

# Apply Gaussian blur to create the "soft glow" effect
# blur_mask = cv2.GaussianBlur(dilated_mask, AURA_BLUR_KERNEL, 0)

# Create a 3-channel BGR image of the desired purple color
# Only where the blur_mask is bright will this color appear
```
Notice that the outer mask has higher iterations and kernel, so it would draw a bigger hand
#### Step 6: Blend them into a single mask
Combine them together and then apply Gaussian blur
```python
# Blend the resulting purple aura onto the original image
        # We use cv2.addWeighted to overlay the glow
cv2.addWeighted(mask_middle, 1.0, mask_outer, con.AURA_INTENSITY,0, mask_outer)
cv2.GaussianBlur(mask_outer,(5,5),3,mask_outer)
```
We now have a mask with two layers of neon effect
- **step 7: Draw the haki core**
Now we draw the hand again and fill the palm
```python
for start, end in con.HAND_CONNECTIONS:
 cv2.line(mask_outer, rel_points[start], rel_points[end], con.HAKI_CORE, 10)
 cv2.fillPoly(mask_outer, [poly_points], con.HAKI_CORE)
```
We now have a haki-style hand. However, as you can see, we are using mask_outer, not the ROI. How can we blend it back? 
My idea is to make the transparent variable alpha like what we did to a transparent image. 
So how do we make this variable?
Since we are using black, we can set the condition where a pixel is black to have a transparency of 0, whereas anything above is 1
#### step 8: Make alpha mask
```python
# convert to 2D gray color
gray_mask = cv2.cvtColor(mask_outer, cv2.COLOR_BGR2GRAY) 
# any pixel that has intensity greater than 1 will be converted to 255 
_, binary_mask = cv2.threshold(gray_mask, 50, 255, cv2.THRESH_BINARY) 
alpha = binary_mask / 255
alpha = alpha[:, :, np.newaxis]
```
If we set the threshold as 1, we might see the thick black boundary. This makes sense, though, since those black boundaries are not completely black. It could be something like (3,3,3). So to mitigate it, we set the threshold to 50
#### Step 9: Blend to our roi

```python
roi[:,:] = (1-alpha) * roi + alpha * mask_outer
```

#### Step 10: Find the boundary for the haki hand
We're pretty much done with drawing. However, we need the polygon of the haki hand so we can detect collision. First of all, we will find the contour
```python
contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
This will return a list of contours. However, for simplicity, I assume that we only have a single hand displayed in the image. So there is only one contour
```python
contour = contours[0]
```
Well, this is not good, and in the future we need to associate the contour with the hand.

#### Step 11: Find the Polygon
So the contour we have now is somewhat arbitrary. We need to find the smallest convex polygon to represent the hit box area for us
```python
hand_boundary = np.squeeze(cv2.convexHull(contour))
```
The return type of convexHull is some kind of weird (N,1,2). We need to remove that extra 1 dimension. **np.squeeze** helps us do that

#### step 12: convert to original coordinate
Remember that we are using coordinates inside the roi. To go back to the original world, simply add the vector to the top left
```python
hand_boundary = hand_boundary + [x_min, y_min]
```
