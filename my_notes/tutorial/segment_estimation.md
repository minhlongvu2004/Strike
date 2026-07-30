my initial plan was to use both YOLO semgnetaion for face and YOLO estimation for hand. The YOLO segmentation works kinda well but the estimation didn't work as I expected. I thought the my training was bad but when look at other people [repo](https://github.com/chrismuntean/YOLO11n-pose-hands). They also have the same problem as me. Basicly it perform well on open hand but struggle when detecting other gesture like pinching or swiping. Thus, I use MediaPipe as an alternative. However, I still show the way to do the segmentation and estimaation so future project can be benefited from this


Detection, segmentation, and Estimation... what are those?
- Detection: determine the bounding box of an object. The bounding box is define by two points top left verti and bottom right vertice 
- Segmentation: Determine the boundary of an object. The boundary is defined by collection of points. This is really similiar to a polygon
- Estimation: Determine the locations of [keypoins](https://docs.ultralytics.com/tasks/pose). Those keypoints represent joints or unique features.

<img width="1256" height="465" alt="Image" src="https://github.com/user-attachments/assets/45e154f1-d8c5-42b3-b25a-4ef8c3d3b4fb" />

# Segmentation
## Type of Segmentation
There are generally 3 [types](https://www.geeksforgeeks.org/computer-vision/image-segmentation-techniques-and-applications/) of segmentation:
- ***Semantic segmentation:*** Devide image into meaningful region and asisgn a class to it
- ***Instance segmentation:*** Extend semeantic segmentation by not only assign a class to a region but also distinguish between objects of the same class.
- ***Panoptic:*** Combination of Semantic and Instance segmentation

<img width="1118" height="371" alt="Image" src="https://github.com/user-attachments/assets/1fc980be-1f3f-4f46-b7c8-4d17cdb91a5e" /> 

Pro the sake of simplicity, I only want to segment the hands so I will do ***Semantic Segmentation***
## Tutorial Annotation
I will be using cvat for this tutorial
### Step 1: Sign in cvat
Sign in to cvaat by using this https://www.cvat.ai/
### Step 2: Create new task
Go to *Task* section amnd click on the the plust *+* sign and click on *Create new task*

<img width="1812" height="294" alt="Image" src="https://github.com/user-attachments/assets/7467be4a-dc40-4e18-bed7-94067c86dd2a" />

On the following page, Name the task and then drag your image file to in the red rectangle area. Then click on *Submit and Continue* and wait until it said that the task has been succesfully pushed to server.

### Step 3: Open task
Click on the *task* section again and click on *open* of the task you just created

<img width="1772" height="253" alt="Image" src="https://github.com/user-attachments/assets/abc304ba-1970-4506-9d4b-826ac13a8dbe" />

On following page, click on *Add Label*

<img width="1412" height="747" alt="Image" src="https://github.com/user-attachments/assets/73185883-d983-48b3-9ca8-2d1ccaea7417" />

Next, type the name of the label. In here I use hand image so I simply type hand and then click on *Continue*

<img width="1292" height="466" alt="Image" src="https://github.com/user-attachments/assets/e977dfd0-0c16-4d98-bd8e-f3945e71910b" />

Next click on the *Job #....* to open the new task

<img width="1462" height="760" alt="Image" src="https://github.com/user-attachments/assets/7f4537ea-663e-463f-8cc0-61e9d1885607" />

### Step 4: Draw the 

On the following page, click on the *draw polygon* and then click *shape*

<img width="1917" height="1011" alt="Image" src="https://github.com/user-attachments/assets/e7d36983-0f54-429e-bb7c-dcd2cc543d79" />

Now that your mouse should be changed to a *+* sign. Now carefuly click on the boundary of the hand.
- Left Click: Add a point
- Right Click: Remove the latest point

<img width="805" height="771" alt="Image" src="https://github.com/user-attachments/assets/26191dcd-73b3-49b5-b876-6a4592c2b5c6" />

Just be patient to complete it. When you think you have draw enough and the polygon cover the region you want to segment. Then press *N* on your keyboard to complete it

<img width="800" height="802" alt="Image" src="https://github.com/user-attachments/assets/803e1bd9-bb1c-4393-a772-a5824b2f1fab" />

Next press "Ctrl + S" to save the image
### Step 5: Export 
Click on the *Task* section, then click on the vertical three dot *...* and click on export 

<img width="1875" height="602" alt="Image" src="https://github.com/user-attachments/assets/c08caa45-35ef-4771-a336-7c5701ece8bb" />

Since we are using YOLo, choose the YOLO segmentation format and name the file as anything you want. Then click on OK

<img width="517" height="361" alt="Image" src="https://github.com/user-attachments/assets/b07640a9-7ddc-4200-8b5c-49a549bb6081" />

Next click on the *Request* section. You might need to wait sometime for it to export the format. When it is done, click on the vertical three dot and **download*

<img width="1917" height="241" alt="Image" src="https://github.com/user-attachments/assets/e49bda04-ebe7-4403-85e4-4143f321a2a4" />

### Step 6: Examine the format
Go to your downlaod zip, your label should be in the folder labels/train/*.txt. If you open it, you might see a lot of points 

<img width="862" height="383" alt="Image" src="https://github.com/user-attachments/assets/ac930221-4c1a-4808-ade3-e831599777a9" />

YOLO segmentation has the [format](https://docs.ultralytics.com/datasets/segment#ultralytics-yolo-format) as 

\<class-index> \<x1> \<y1> \<x2> \<y2> ... \<xn> \<yn>

where \<class-index> is the index of the class (this is specify in the config.yaml) and each of the pair (x1,y1) represent a point of that polygon. Overal the polygon has *n* points

Note that i only show how the annotation for segmentation works. The way to split and train it is the same as [Train_YOLO.md](https://github.com/minhlongvu2004/Face_Recognition/blob/main/Tutorials/Train_Yolo.md) section *3. Organize image*. The train script is provided in */train* folder


# Estimation
# Step 1: do similiar to all until step 3
Instead of choosing *Add Label*, Choose setup skeleton instead

<img width="1287" height="757" alt="Image" src="https://github.com/user-attachments/assets/17a50f77-a51d-4306-bd0e-19ce9754f3a1" />

Now type the name of label, then click the second item on the left vertical bar. Since we only need estimate 6 points: 5 tip fingers and one at wrist, left click to define each point as below

<img width="1227" height="832" alt="Image" src="https://github.com/user-attachments/assets/a82b63bf-f882-466c-a33e-37b21257fbc6" />

Then click on *continue* and *back to the task*

# Step 2: Draw the estimation
Now open the task as in step 3 of segmentation. Click on the *draw new skeleton* and then *shape*

<img width="1482" height="922" alt="Image" src="https://github.com/user-attachments/assets/802b5e4b-0276-4ed2-9fd5-f988c6206d20" />

Now you need two left clicks one for top left and bottom right to carry out the template. Try to match it with the size of hand

<img width="786" height="736" alt="Image" src="https://github.com/user-attachments/assets/5533176d-a092-4a07-9f04-a8169e7a144f" />

After that, place the points to its coresspond finger or wrist

<img width="792" height="692" alt="Image" src="https://github.com/user-attachments/assets/a3cb8415-7c8f-4961-87c7-afa9000447cb" />

---> Optionally
In case, if one point is missing or being obsucred by other hand, we can change its property of that point. Click on the  *Parts* on the right. Choose the point you want to target. For example point one. the human icon is for osculuded point and the eye is for hidden point. Each of them has a number to rpresent the visiblity flag
- hidden 0: it is not there and will not be trained during gradient descent
- osculuded 1 : it is still there but being hide by other object and will also be trained on durign gradient descent
- Fully Visible 2: it is clearcly visible and we can see it
<img width="1461" height="690" alt="Image" src="https://github.com/user-attachments/assets/3c576d51-5bfa-4445-8a1b-10afcd5e67d8" />

# Step 3: Export and download the dataset

Same as above, but choose the pose format 

<img width="1287" height="653" alt="Image" src="https://github.com/user-attachments/assets/de722e9d-b9d3-4d32-b7f4-9fd68f09a511" />

# Step 4: Inspect the file format and config.yaml
#### file Format
Unlike the segmentation, the POSe follow the [format](https://docs.ultralytics.com/datasets/pose#faq)
```
<class-index> <x> <y> <width> <height> <px1> <py1> <p1-visibility> <px2> <py2> <p2-visibility> <pxn> <pyn> <pn-visibility>
```
For first 4 points
- (x,y): this is the position of the center point of the object
(width,height): this the weidght and height of the object
After that we can see that for every two pairs of flaot, there is an integer like 2 or 1
so those two number are
- (px1,py1): which represent the position of the point
- (p1-visibility): this is one of three property we state above.
Since we have a clear image data, all the poitns should have 2(fully visible)


<img width="871" height="257" alt="Image" src="https://github.com/user-attachments/assets/a3a33317-7b95-42e8-8b32-b3bab8e4bb62" />


#### config.yaml
the config.yaml of pose is a bit different with detection and segmentation
```
path: /content/drive/MyDrive/Data/hand_estimation/data
train: train/images
val: val/images
test: test/images

kpt_shape: [6,3]
names:
  0: Hand

kpt_names:
  0:
    - wrist
    - pinky_tip
    - ring_tip
    - middle_tip
    - index_tip
    - thumb_tip
```

- kpt_shape: This is the key point shape \[a,b\] where a is the number of poitns and b is dimension of each point. Since we have 6 points and each point has (x,y) and visibility, this mean it is 3 in dimension. so we would have [6,3]
- kpt_names: keypoint names. Remeber those point 1 and point 2 above, now we give it a name in here so we can later use in inference time