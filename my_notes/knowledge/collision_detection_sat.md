
<h1 align="center"> 💥Detection Collision with Seperating Axis Theorem💥 </h1>

# Table of Contents

<small>

- [1. Polygon](#1-polygon)
  - [1.1 Convex polygon](#11-convex-polygon)
  - [1.2 Concave Polygon](#12-concave-polygon)
- [3. Separating axis theorem](#3-separating-axis-theorem)
- [4. Projection with dot product](#4-projection-with-dot-product)
- [5. General algorithm](#5-general-algorithm)
- [6. Example of triangle and rectangle](#6-example-of-triangle-and-rectangle)
  - [6.1 No collision](#61-no-collision)
  - [6.2 Collision](#62-collision)

</small>

In short, the Separating Axis Theorem SAD is used to detect whether there is a collision between two shapes
# 1 Polygon
In Greek, [Polygon] contains **Poly** and **gon**, meaning **many** and **angle**, respectively. As the name suggests, it is a shape that contains many line segments to [form](https://en.wikipedia.org/wiki/Polygon) a closed chain. 
- Each line-segment is called an *edge*
- Each intersection point of two edges is are call *vertice*
The polygon is usually represented as a circular list of vertices 
$$P_0(x_0,x_0), P_1(x_1,y_1), P_2(x_2,y_2)...,P_{n-1}(x_{n-1},y_{n-1}) $$
where any two adjacent vertices could form an edge. Since it is a circular list, $P_0, P_n$ also form an edge to close the shape.
There are two types of angles for each intersection between 
- **Interior angle:** the angle inside the shape
- **Exterior angle:** the angle outside of the shape

There could be many types of polygons. For simplicity, we could divide into two basic types: convex and concave. 
## 1.1 convex polygon
**convex**: A polygon where all the interior angles are below 180 degrees. If there is a line that intersects the polygon, it doesn't intersect its edges more than twice. This is our main focus for the SAD algorithm
## 1.2 Concave Polygon
**concave**: Opposite to convex, there is at least one interior angle that is more than 180 degrees. A line could intersect its shape more than twice.

# 3 Separating axis theorem
**Separating axis theorem**: two convex objects don't collide if there exists a line that could separate the two shapes.

It only works for the two convex shapes but fails for the concave ones. However, if we think of concave as a collection of convex shapes and consider each convex shape separately. Then it still works.

This is a really efficient algorithm for detecting no collision since we don't have to check for all.
***You might wonder how many axes we might have to check if there exists a collision***
Well, good catch! The above theorem is kinda general and implies that we could have to check an infinite number of axes. Thankfully, we actually have a [stronger](https://math.stackexchange.com/questions/2106402/proof-of-separating-axis-theorem-for-polygons) version of this in the case of 2D.
**2D Collision Detection:** If there exists a straight line that is parallel to one of those shape edges and separates two shapes, then they don't collide
This stronger version gives us a hint that we only need to check for those edges.
**Okay, I know how many lines to check, but how do we actually check if a line separates two shapes?**
Well, there is a bit of confusion here in the name. The theory is based on the line, but the name is on the axis, which is **not** the same thing.
- **seperating line**: Just any [line]((https://www.maxthomarino.com/blog/sat-collision-detection-separating-axis-theorem-how-it-works-why-it-works-and-how-to-implement-it) in the 2D space
-  **Separating axis:** The normal direction of the separating line
If we think about it, it is kinda intuitive. If we are to draw a line to separate between two shapes, how do we know if it is even separated? We look at the distance between the closest point of each shape. 
<img width="903" height="711" alt="Image" src="https://github.com/user-attachments/assets/31a64f1a-5ce6-42ee-84ed-f2707cc10007" />

As we are talking about the distance, the smallest one that can be used to measure is the perpendicular line from that point to the separating line. Yes, we did mention the perpendicular line. So to automate the process, we basically project the whole shape onto the perpendicular line. Do the same thing for the other shape. If there is a gap between the maximum and minimum of both shapes, then there is a space, which means we could draw a separating line. Thus, that is the whole idea of the separating axis theorem
# 4 Projection with dot product
As stated above, we have to project all the shapes onto the separating axis. But how can we do this?
When we talk about projection, we usually mention the dot product. The dot product is defined as
$$\vec{m} \cdot \vec{n} = |m|*|n|*\cos{\theta}$$

<img width="410" height="312" alt="Image" src="https://github.com/user-attachments/assets/7c73bc21-a3b3-406a-b946-bb4d1b127aa2" />

If $n$ is a unit vector where its length is 1, $|\vec{n}| = 1$, then the dot product basically becomes a projection onto that direction

<img width="450" height="383" alt="Image" src="https://github.com/user-attachments/assets/6bd2a970-2132-48bb-b70b-177884194c04" />

# 5 General algorithm
- ***Step 1:*** Form the list of edge vectors to represent the polygon
- ***Step 2:*** For each edge, calculate the normal unit vector by using the following formula
$$normal\_unit((x,y)) = \frac{(-y,x)}{\sqrt{x^2 + y^2}}$$
Repeatedly do the same thing for all edges and store them in a list. If shape A has $n_a$ edges and shape B has $n_b$, then the length of the list is $n_a+n_b$
- ***Step 3:*** (This step can be done along with step 2, but I separate it for understandability)
Loop through all unit vectors. For each unit vector, project an entire shape on that vector by using the dot product for each pair of edge and normal. Then take the maximum and minimum values of projection for each shape
- ***step 4:*** (this is done during each iteration of unit vector)Now we simply compare the maximum and minimum between shapes. We see that the possible intersection is between the minimum of one shape and the maximum of the other. So we could check 
If 
$$\max(A) < \min(B) \lor \min(A) > \max(B)$$
<img width="751" height="280" alt="Image" src="https://github.com/user-attachments/assets/d2bed94b-0c91-4d83-a8db-1abf41bf411e" />
This basically means that if the maximum of a shape is smaller than the minimum of the other, then the entire shape is smaller than the other shape, which results in a gap. There are two cases that could happen as shown above. We only need it to be true for one case, so we use the *or* operator for two cases. If the statement is false for **all** the unit vectors, then there exists a collision, and we could exit the loop early. However, if it is false for all unit vectors, that means we have detected a collision.


# 6 Example of triangle and rectangle
It is better to illustrate how we can apply it on paper before we even code. For simplicity, I only do a bare example for the case of a triangle and rectangle. It should be the same for other shapes
## 6.1 No collision
Given the triangle and rectangle below, determine whether there is a collision using the Separating Axis Theorem
. <img width="586" height="462" alt="Image" src="https://github.com/user-attachments/assets/39ba15d7-efce-46aa-85ea-ac2decabf9a5" />
Let's call the triangle A and the rectangle B.
**Step 1**: Calculate the edge vectors list for each shape
Edges of A: {(1,2), (-1,0),(-2,-2)}
Edges of B: {(1,0), (1,0.5), (1.5,0.5), (1.5,0)}
(0,0.5) (0.5,0) (0,-0.5) (-0.5,0)
**Step 2**: for each edge vector calculate the normal unit
**Shape A**
$$(1,2)->(-0.894, 0.447)$$

$$(-1,0)->(0,1)$$

$$(-2,-2)->(0.707, -0.707)$$

**Shape B**
$$(0,0.5) -> (-1,0)$$

$$(0.5,0) -> (0,1)$$

$$(0,-0.5) -> (1,0)$$

$$(-0.5,0) -> (0,-1)$$

So we have
Normal units of A: (-0.894, 0.447) (0,1) (0.707, -0.707)
Normal units of B: (-1,0) (0,1) (1,0) (0,-1)
Combined, we have a list of normal vectors
(-0.894, 0.447) (0,1) (0.707, -0.707) (-1,0) (0,1) (1,0) (0,-1) 
= (-0.894, 0.447) (0,1) (0.707, -0.707) (-1,0) (1,0) (0,-1) 
**Step 3 - 4**: Loop through
**(-0.894, 0.447)**:
A: (-0.894, 0.000)
B: (-1.342, -0.671)
overlap

**(0.0, 1.0):**
A: (0.000, 2.000)
B: (0.000, 0.500)
overlap

**(0.707, -0.707):**
A: (-0.707, 0.000)
B: (0.354, 1.061)
no overlap
-> Stop here and conclude that there is no collision


## 6.2 Collision
Step 1: Edge Vectors
Edges of A:
AB = (1, 2)
BC = (1, 0)
CA = (-2, -2)

Edges of B:
DE = (0, 1.5)
EF = (1, 0)
FG = (0, -1.5)
GD = (-1, 0)

Step 2: Normal Unit Vectors
From A: (-0.894, 0.447), (0, 1), (0.707, -0.707)
From B: (-1, 0), (0, 1), (1, 0), (0, -1)
Normal Units: (-0.894, 0.447), (0, 1), (0.707, -0.707), (-1, 0), (1, 0)

Step 3-4: Projection and Collision Testing
(-0.894, 0.447):
A: (-0.894, 0.000)
B: (-0.894, -0.224)
overlap

(0.0, 1.0):
A: (0.000, 2.000)
B: (0.000, 1.500)
overlap

(0.707, -0.707):
A: (-0.707, 0.000)
B: (-0.354, 0.707)
overlap

(-1.0, 0.0):
A: (-2.000, 0.000)
B: (-2.000, -1.000)
overlap

(1.0, 0.0):
A: (0.000, 2.000)
B: (1.000, 2.000)
overlap

Conclusion: All axes show overlap. There is a collision

