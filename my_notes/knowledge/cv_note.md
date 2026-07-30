# Dialation
So basically the way we make a gloom effect by using a thicker text, blurring and placing the brigther 
in middle is kinda obsolte. This can be seen below
![misalign](<Screenshot 2026-07-16 204948.png>)
I don't the exact reason but might be the conflict version. 
Thanks to gemini, I figure another way to make by using [dialation](https://www.jeremymorgan.com/tutorials/opencv/dilate-opencv-python/). So dialation algorithm basically compare the all the neighbor with the central pixel (Neighbors are define as matrix in kernel). And replace the maximum value to the central. You might think that it might cause chain reaction to fill the whole thing. Valid question and turn out that for every pixel it only look at the origional input and draw it to other output. Thus it wont affect
the input data so no chain reaction would be made
```python
kernel =  np.ones((3, 3), np.uint8)
mask_neon = cv2.dilate(mask_neon, kernel, iterations=3)
```
as you can see here we have reassign it if we want it affect orgional variable
This mean that if we define a neighbor as [3,3]. Then the central pixel can only look at one pixel around it. So we maximum can only increase one pixel from the border. If we are two make a second iteration, we would look further 1 pixel. So assume we have odd kernel MxM, then number of line of pixel we could add from a border is 
$$\left\lfloor \frac{M}{2} \right\rfloor \cdot iteration$$

# Save time with ROI instead of full frame
### Measurement
In my previous project "Face Recognition", I used something like 
```
success, frame = cap.read()
cv2.GaussianBlur(frame,...)
```
Basically I use the Gausian Blur for the whole frame how its effect only take place in single small area. This drastically reduce the speed performance.
For example: to draw a small neon text like below. I define two variant of functions
<img width="788" height="627" alt="Image" src="https://github.com/user-attachments/assets/fb14ded2-4670-4ebb-a00c-669bd5f4279a" />

First one is as usual, where i use all the frame
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
Avergae for 100 frames: 3.82
Avergae for 100 frames: 3.79
Avergae for 100 frames: 3.78
Avergae for 100 frames: 3.80
Avergae for 100 frames: 3.81
Avergae for 100 frames: 3.83
Avergae for 100 frames: 3.86
```
So it take around 3.5 ms to complete single small neon text. This is quite expensive operation because if we draw ten line like this, it would take 35ms. This is equiavalent to run another YOLO model. In order to improve this, I introduce the *ROI* or region of interest. Basiclly only interact with area that we intend to do.

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
Avergae for 100 frames: 1.20
Avergae for 100 frames: 1.22
Avergae for 100 frames: 1.21
Avergae for 100 frames: 1.20
Avergae for 100 frames: 1.19
Avergae for 100 frames: 1.20
Avergae for 100 frames: 1.20
Avergae for 100 frames: 1.21
Avergae for 100 frames: 1.24
Avergae for 100 frames: 1.24
Avergae for 100 frames: 1.24
Avergae for 100 frames: 1.26
Avergae for 100 frames: 1.27
Avergae for 100 frames: 1.28
Avergae for 100 frames: 1.28
Avergae for 100 frames: 1.27
Avergae for 100 frames: 1.28
```
As you can see here the neon text only take around ***1.2 ms***. The difference is ***2.3 ms***.
Let take an example of calculation:
*Full frame*:
Assume we were to draw 10 line of neons. So take us 35 ms
Remember that the cv2.read() it self introduce latency around 5ms. 
The yolo model is around 30 ms
So our FPS would 
$$\frac{1000}{35+5+30} \approx 14.3 FPS$$
This is quite slow since the bare minimum goal is 20 FPS and good one is 30 FPS
*ROI*
10 lines of neons -> 12 ms
So our FPS would 
$$\frac{1000}{12+5+30} \approx 21 FPS$$
You see! significantly improve the FPS

### How do I optimize it
Assume we want to take an ROI region out of image

<img width="561" height="495" alt="Image" src="https://github.com/user-attachments/assets/f4daf442-a950-461a-b286-c270b3ab49c3" />

Since the image itself is just numpy array, to take the ROI we basically slice the image in both axis. Let say that (x1,y1) and (x2,y2) are top left and bottom right of the ROI, respectively

<img width="1003" height="562" alt="Image" src="https://github.com/user-attachments/assets/e25717a2-c56b-4958-8be1-af3e450389a2" /> 

Then to take roi we simply need

$$roi = img[y1:y2,x1:x2]$$

Now that we have our ROI.

<img width="676" height="566" alt="Image" src="https://github.com/user-attachments/assets/a8895770-274b-41ff-aa2b-c911153a5030" />

It is still just an reference to our origional frame, however, operation on this roi require the index start from zero (not from the topleft of itself). To allow the the neon effect spread out. We might need some extra space from the text to the roi. so we padding *pad*

<img width="637" height="541" alt="Image" src="https://github.com/user-attachments/assets/ecf29104-74bc-46f9-9144-370593ddd4b7" />

Not our last job is to calculate the width and height of the text content 
```
(txt_w,txt_h),_ = cv2.getTexSize()
```

<img width="650" height="537" alt="Image" src="https://github.com/user-attachments/assets/623a5055-02a4-4cdc-a203-12856295db19" />

so our new coordinates for text is

```
txt_top_left = (pad,pad)
txt_bottom_right = (pad+txt_w,pad+txt_h)
```

However, since we only need bottom left for drawing text
```
txt_bl = (pad,pad + txt_h)
```

Now just treat it the ROI the same way as Full frame on your operations. This is really efficient

# Problem with image slicing
Assume that we have an image ***img***. There is a problem with the code below
```python
roi = image[y1:y2,x1:x2]
cv2.rectangle(roi, P1, P2, thick) # same for other like line
```
The problem is mthat whenever the (x1,y1), (x2,y2) exeed the image frame, it result in an zero in one dimension of roi. This is what cause error for funtion like cv2.rectangle
![alt text](image.png)
However, it doesn't cause any error even P1 and P2 exceed the frame of image
![alt text](image-1.png)
This will create an illusion as if the image still exist outside of the frame. 
> [!NOTE]
> Doesn't matter which points we are drawing, as long as we making sure that the input ROI doesn't have any zero dimension, then it is totally okay 


# Transparent image
Let say that you want to load an image but don't want the rectangle around. You just want a single object like the left object below

<img width="227" height="111" alt="Image" src="https://github.com/user-attachments/assets/550921fb-d437-4b9a-81ae-dc7eb5516852" />

Step 1: Make sure to convert it to real unbackground object. You could go [here](https://www.remove.bg/). Simply load your object and then downlaod transparent back

Step 2: Load the object to app using unchanged flag
```
img = cv2.imread(<path_to_ur_img>,cv2.IMREAD_UNCHANGED)
```
By specifing this flag, your img doesn't just have 3 dimension as usual but 4 with the extra is alpha for transparency

Step 3: Define your ROI as above
```
roi = image[y1:y2,x1:x2]
```
Step 4: resize your image to the same size as your roi
```
resized_img = cv2.resize(item,(x2-x1,y2-y1))
```

As explained above, your object and your roi has different dimensions. Our plan is to reduce the resized_img from 4 to 3

Step 5: Split dimensions
```
b, g, r, a = cv2.split(resized_img)
```
Step 6: Merge BGR dimension
```
bgr_item = cv2.merge((b, g, r))
```
Step 7: Normalize the alpha
Latter we will use alpha as a gate to filter or keep the image. Because we already define what is tranparency what is not. when we normalize it only take between 0 and 1
```
mask = a / 255.0
```
Step 8: Convert to 3 array
Problem with mask it is 2D array where roi and object are 3D. So we add another dimesion to it
```
mask = mask[:, :, np.newaxis]
```
Step 9: Now merge between roi and your object
```
roi[:,:] = (1-mask) * roi + mask * bgr_item
```
specify [:,:] to state that we replace back to the origional frame not just rename. The operation basically means that keep the origional pixel if it is transparent (background) otherwise replace with object content.

Not that you have an object without black bounding box 

# Draw dark haki hand (Need Improvement)

<img width="383" height="437" alt="Image" src="https://github.com/user-attachments/assets/228216fd-8f43-4ebe-97f6-c01b0060b311" />

It is so funny that above image is the problem I stated. I even wrote detail what the problem was and then I just solved while writing this.
**step 1: Lets define roi**
Let first define the roi to reduce the cost of operation. we need to find the the posible top left so we will use np.min(,axis=0). axis = 0 means target row so it will collapse all rows and return the min/max of that column
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
This basically we find the top left and bottom right. We leave the padding 40 because we need space for really strong dilation
**Step 2: Redefine relative point**
The *points* above is for the original frame. However, as mention in section above, we have to recalculate the coordinate when we do the roi. Thankfully, we only to extract the vector top left
```python
rel_points = points - [x_min, y_min]
```

**Step 3: Make two maskes**
So in order to do this. I define two mask, one for the inner purple and one for outer purple
```python
mask_outer = np.zeros_like(roi,dtype=np.uint8)
mask_middle = np.zeros_like(roi,dtype=np.uint8)
```

**Step 4: Connect all the points**
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
You can consult with below landmark image

<img width="1543" height="538" alt="Image" src="https://github.com/user-attachments/assets/3efec22a-f08a-4e09-861c-b8a925d2ea42" />

**Step 5: Apply dilation for both mask**
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
Notice that the outer mask has higer iteration and kernel so it would draw a bigger hand
**Step 5: blend them into single mask**
Combine them together and then apply Gasussian blurred
```python
# Blend the resulting purple aura onto the original image
        # We use cv2.addWeighted to overlay the glow
cv2.addWeighted(mask_middle, 1.0, mask_outer, con.AURA_INTENSITY,0, mask_outer)
cv2.GaussianBlur(mask_outer,(5,5),3,mask_outer)
```
we now have a mask with two layers of neon effect
**step 6: Draw the haki core**
Now we draw the hand again and fill the palm
```python
for start, end in con.HAND_CONNECTIONS:
    cv2.line(mask_outer, rel_points[start], rel_points[end], con.HAKI_CORE, 10)
    cv2.fillPoly(mask_outer, [poly_points], con.HAKI_CORE)
```
we now have haki style hand. However as you can see that we are using mask_outer not the ROI. how can we blend it back. 
My idea is to make the transparent variable alpha like what we did to transparent image. 
So how to make this variable?
Since we are using the black, we can set the condition where a pixel is black has transparent of 0 whereas anything above is 1
**step 7: make alpha mask**
```python
# convert to 2D gray color
gray_mask = cv2.cvtColor(mask_outer, cv2.COLOR_BGR2GRAY) 
# any pixel that has intensity greater than 1 will be convert to 255 
_, binary_mask = cv2.threshold(gray_mask, 50, 255, cv2.THRESH_BINARY) 
alpha = binary_mask / 255
alpha = alpha[:, :, np.newaxis]
```
if we set threshold as 1, we might see the black boundary. This make sense though since those black boundary is not completely black. So to mitigate it, it set the threshold 50
**step 9: Blend to our roi **

```python
roi[:,:] = (1-alpha) * roi + alpha * mask_outer
```

**Step 10: Find the boundary for the haki hand**
we pretty much done with drawing, however we need the polygon of the haki hand so we could detect collision. FIrst of all, we will find the contour
```python
contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
This will return a list of contours. However, for simplicity, I assume that we only have single hand displayed in the image. So there is only one contour
```python
contour = contours[0]
```
Well this is not good and in future we need to associate contour to the hand.

**Step 11: Find the Polygon**
So the contour we having now is somewhat arbtirary. We need to find the smallest convex polygon to repsrent the hit box area for us
```python
hand_boundary = np.squeeze(cv2.convexHull(contour))
```
the return type of convexHull is some kind of weird (N,1,2). We need to remove those extra 1 dimension. np.sequeeze help us doing that

**step 12: convert to original coordinate**
Remember that we are using coordinates inside the roi. To go back to origional world, simply add the vector top left
```python
hand_boundary = hand_boundary + [x_min, y_min]
```