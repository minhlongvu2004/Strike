<h1 align="center"> 🖋️Segmentation & Estimation🖋️ </h1>


<small>

- [1. Plan of Training](#1-plan-of-training)
- [2. Segmentation](#2-segmentation)
  - [2.1 Type of Segmentation](#21-type-of-segmentation)
  - [2.2 Tutorial Annotation](#22-tutorial-annotation)
    - [Step 1: Sign in to CVAT](#step-1-sign-in-to-cvat)
    - [Step 2: Create new task](#step-2-create-new-task)
    - [Step 3: Open task](#step-3-open-task)
    - [Step 4: Draw the polygon](#step-4-draw-the)
    - [Step 5: Export](#step-5-export)
    - [Step 6: Examine the format](#step-6-examine-the-format)
- [3. Estimation Annotation](#3-estimation-annotation)
  - [Step 1: Setup & Skeleton](#step-1-do-similar-to-all-until-step-3)
  - [Step 2: Draw the estimation](#step-2-draw-the-estimation)
  - [Step 3: Export and download the dataset](#step-3-export-and-download-the-dataset)
  - [Step 4: Inspect the file format and config.yaml](#step-4-inspect-the-file-format-and-configyaml)

</small>

# 1 Plan of Training 
My initial plan was to use both YOLO segmentation for face and YOLO estimation for hand. The YOLO segmentation works kinda well, but the estimation didn't work as I expected. I thought my training was bad, but when I look at other people's [repo](https://github.com/chrismuntean/YOLO11n-pose-hands). They also have the same problem as me. Basically, it performs well on open palms but struggles when detecting other gestures like pinching or swiping. Thus, I use MediaPipe as an alternative. However, I still show the way to do the segmentation and estimation so future projects can benefit from this.


Detection, segmentation, and Estimation... what are those?
- ***Detection***: determine the bounding box of an object. The bounding box is defined by two points: the top left vertex and the bottom right vertex 
- ***Segmentation***: Determine the boundary of an object. The boundary is defined by a collection of points. This is really similar to a polygon
- ***Estimation***: Determine the locations of [keypoints](https://docs.ultralytics.com/tasks/pose). Those keypoints represent joints or unique features.

<img width="1256" height="465" alt="Image" src="https://github.com/user-attachments/assets/45e154f1-d8c5-42b3-b25a-4ef8c3d3b4fb" />

# 2 Segmentation
## 2.1 Type of Segmentation
There are generally 3 [types](https://www.geeksforgeeks.org/computer-vision/image-segmentation-techniques-and-applications/) of segmentation:
- ***Semantic segmentation:*** Divide the image into meaningful regions and assign a class to it
- ***Instance segmentation:*** Extend semantic segmentation by not only assigning a class to a region but also distinguishing between objects of the same class.
- ***Panoptic:*** Combination of Semantic and Instance segmentation

<img width="1118" height="371" alt="Image" src="https://github.com/user-attachments/assets/1fc980be-1f3f-4f46-b7c8-4d17cdb91a5e" /> 

For the sake of simplicity, I only want to segment the hands, so I will do ***Semantic Segmentation***
## 2.2 Tutorial Annotation
I will be using CVAT for this tutorial
### Step 1: Sign in to CVAT
Sign in to cvaat by using this https://www.cvat.ai/
### Step 2: Create new task
Go to *Task* section and click on the plus *+* sign and click on *Create new task*

<img width="1812" height="294" alt="Image" src="https://github.com/user-attachments/assets/7467be4a-dc40-4e18-bed7-94067c86dd2a" />

On the following page, name the task and then drag your image file into the red rectangle area. Then click on *Submit and Continue* and wait until it says that the task has been successfully pushed to the server.

### Step 3: Open task
Click on the *task* section again and click on *Open* for the task you just created.

<img width="1772" height="253" alt="Image" src="https://github.com/user-attachments/assets/abc304ba-1970-4506-9d4b-826ac13a8dbe" />

On the following page, click on *Add Label*

<img width="1412" height="747" alt="Image" src="https://github.com/user-attachments/assets/73185883-d983-48b3-9ca8-2d1ccaea7417" />

Next, type the name of the label. Here I use a hand image, so I simply type hand and then click on *Continue*

<img width="1292" height="466" alt="Image" src="https://github.com/user-attachments/assets/e977dfd0-0c16-4d98-bd8e-f3945e71910b" />

Next, click on the *Job #....* to open the new task

<img width="1462" height="760" alt="Image" src="https://github.com/user-attachments/assets/7f4537ea-663e-463f-8cc0-61e9d1885607" />

### Step 4: Draw the 

On the following page, click on the *draw polygon* and then click *shape*

<img width="1917" height="1011" alt="Image" src="https://github.com/user-attachments/assets/e7d36983-0f54-429e-bb7c-dcd2cc543d79" />

Now your mouse should be changed to a *+* sign. Now carefully click on the boundary of the hand.
- Left Click: Add a point
- Right Click: Remove the latest point

<img width="805" height="771" alt="Image" src="https://github.com/user-attachments/assets/26191dcd-73b3-49b5-b876-6a4592c2b5c6" />

Just be patient to complete it. When you think you have drawn enough and the polygon covers the region you want to segment. Then press *N* on your keyboard to complete it

<img width="800" height="802" alt="Image" src="https://github.com/user-attachments/assets/803e1bd9-bb1c-4393-a772-a5824b2f1fab" />

Next, press "Ctrl + S" to save the image
### Step 5: Export 
Click on the *Task* section, then click on the vertical three-dot *...* and click on Export. 

<img width="1875" height="602" alt="Image" src="https://github.com/user-attachments/assets/c08caa45-35ef-4771-a336-7c5701ece8bb" />

Since we are using YOLo, choose the YOLO segmentation format and name the file as anything you want. Then click OK.

<img width="517" height="361" alt="Image" src="https://github.com/user-attachments/assets/b07640a9-7ddc-4200-8b5c-49a549bb6081" />

Next, click on the *Request* section. You might need to wait some time for it to export the format. When it is done, click on the vertical three dots and **download*

<img width="1917" height="241" alt="Image" src="https://github.com/user-attachments/assets/e49bda04-ebe7-4403-85e4-4143f321a2a4" />

### Step 6: Examine the format
Go to your downloaded zip. Your label should be in the folder labels/train/*.txt. If you open it, you might see a lot of points. 

<img width="862" height="383" alt="Image" src="https://github.com/user-attachments/assets/ac930221-4c1a-4808-ade3-e831599777a9" />

YOLO segmentation has the [format](https://docs.ultralytics.com/datasets/segment#ultralytics-yolo-format) as 

\<class-index> \<x1> \<y1> \<x2> \<y2> ... \<xn> \<yn>

where \<class-index> is the index of the class (this is specified in the config.yaml), and each of the pairs (x1,y1) represents a point of that polygon. Overall, the polygon has *n* points.

Note that I only show how the annotation for segmentation works. The way to split and train it is the same as the [Train_YOLO.md](https://github.com/minhlongvu2004/Face_Recognition/blob/main/Tutorials/Train_Yolo.md) section *3. Organize image*. The train script is provided in */train* folder.


# 3 Estimation Annotation
### Step 1: do similar to all until step 3
Instead of choosing *Add Label*, choose* Set up skeleton* instead

<img width="1287" height="757" alt="Image" src="https://github.com/user-attachments/assets/17a50f77-a51d-4306-bd0e-19ce9754f3a1" />

Now type the name of the label, then click the second item on the left vertical bar. Since we only need to estimate 6 points: 5 tip fingers and one at the wrist, left-click to define each point as below.

<img width="1227" height="832" alt="Image" src="https://github.com/user-attachments/assets/a82b63bf-f882-466c-a33e-37b21257fbc6" />

Then click on *continue* and *back to the task*

### Step 2: Draw the estimation
Now open the task as in step 3 of segmentation. Click on the *draw new skeleton* and then *shape*

<img width="1482" height="922" alt="Image" src="https://github.com/user-attachments/assets/802b5e4b-0276-4ed2-9fd5-f988c6206d20" />

Now you need two left clicks, one for the top left and one for the bottom right, to carry out the template. Try to match it with the size of the hand.

<img width="786" height="736" alt="Image" src="https://github.com/user-attachments/assets/5533176d-a092-4a07-9f04-a8169e7a144f" />

After that, place the points on their corresponding finger or wrist.

<img width="792" height="692" alt="Image" src="https://github.com/user-attachments/assets/a3cb8415-7c8f-4961-87c7-afa9000447cb" />

---> Optionally
In case one point is missing or being obscured by the other hand, we can change the property of that point. Click on the  *Parts* on the right. Choose the point you want to target. For example, point one. The human icon is for an occluded point, and the eye is for a hidden point. Each of them has a number to represent the visibility flag
- hidden 0: it is not there and will not be trained during gradient descent
- occluded 1: it is still there but being hidden by another object and will also be trained during gradient descent
- Fully Visible 2: it is clearly visible, and we can see it
<img width="1461" height="690" alt="Image" src="https://github.com/user-attachments/assets/3c576d51-5bfa-4445-8a1b-10afcd5e67d8" />

### Step 3: Export and download the dataset

Same as above, but choose the pose format 

<img width="1287" height="653" alt="Image" src="https://github.com/user-attachments/assets/de722e9d-b9d3-4d32-b7f4-9fd68f09a511" />

### Step 4: Inspect the file format and config.yaml
#### File Format
Unlike the segmentation, the POSe follows the [format](https://docs.ultralytics.com/datasets/pose#faq)
```
<class-index> <x> <y> <width> <height> <px1> <py1> <p1-visibility> <px2> <py2> <p2-visibility> <pxn> <pyn> <pn-visibility>
```
For the first 4 points
- (x,y): this is the position of the center point of the object
(width, height): this is the width and height of the object
After that, we can see that for every two pairs of floats, there is an integer like 2 or 1
So those two numbers are
- (px1,py1): which represents the position of the point
- (p1-visibility): this is one of three properties we state above.
Since we have clear image data, all the points should have 2(fully visible)


<img width="871" height="257" alt="Image" src="https://github.com/user-attachments/assets/a3a33317-7b95-42e8-8b32-b3bab8e4bb62" />


#### config.yaml
The config.yaml of pose is a bit different from detection and segmentation
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

- kpt_shape: This is the key point shape \[a,b\] where a is the number of points and b is the dimension of each point. Since we have 6 points and each point has (x,y) and visibility, this means it is 3 in dimension. So we would have [6,3]
- kpt_names: keypoint names. Remember those points 1 and 2 above. Now we give it a name in here so we can later use it at inference time