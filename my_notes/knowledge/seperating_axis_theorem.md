
In short, Seperating Axis Theorem SAD is used to detect whether there is a collision between two shapes
# Polygon
In Greek, [Polygon] contains **Poly** and gon mean many and angle, respectively. Like the name suggest, it is a shape where contains many line-segment to [form](https://en.wikipedia.org/wiki/Polygon) a closed chain. 
- Each line-segment is called an *edge*
- Each intersection point of two edge is are call *vertice*
The polygon is usually represent as a circular list of vertices 
$$P_0(x_0,x_0), P_1(x_1,y_1), P_2(x_2,y_2)...,P_{n-1}(x_{n-1},y_{n-1}) $$
where any two adjacent vertices could form an edge. Since it is circular list, $P_0,P_n$ also form an edge to close the shape.
There are two type of angle for each interseciton between 
- interior angle: the angle inside the shape
- Exterior angle: the angle outside of the shape

There could be many type of polygon. For simplicity, we could two basic type: convex and concave. 
## convex polygon
**convex**: An polygon where all the interior is below 180 degree. It there is a line intersect the polygon, it doesn't intersect its edges more than twice. This is our main focus for the SAD algorithm
## Concave Polygon
**concave**: Opposite to convex, there is at least one interior angle that is more than 180 degree. A line could intesect its shape more than twice

# Seperating axis theorem
**Seperating axis theorem**: two convex objects doens't collide if there exist a line where it could seperate two shapes.

It onyly works for the two convex shapes but fail for the concave. However, if we think concave as collection of convex and consider each convex seperately. Then it still works

I This is really efficient algorithm for detecting no collision since we don't have to check for all.
***You might wonder how many axes we might have to check if there exist collision***
Well good catch! the above theorem is kinda of general and infer that we could have to check inifite number of axis. Thankfully, we actually have a [stronger](https://math.stackexchange.com/questions/2106402/proof-of-separating-axis-theorem-for-polygons) version of this in the case of 2D.
**2D Collision Detection:** If there exist a stragiht that is parrallel to one of those shape edges and seperate two shapes, then they don't collide
This stronger version give us a hint that we only need to check for those edges.
**Okay i know how to many lines to check, but how do we actually check if a line seperate two shapes?**
well there is a bit of confusion here in the name. The theory is based on the line, but the name is on the axis which is **not** the same thing.
- seperating [line](https://www.maxthomarino.com/blog/sat-collision-detection-separating-axis-theorem-how-it-works-why-it-works-and-how-to-implement-it): Just any line in the 2D space
- seperating axis: The normal direction of the seperating line
If we think about it, it is kinda intuitive. if we are to draw a line to seperate between two shape, how do we know if it is even seperated. We look at the distance between the closest point of each shape. 
<img width="903" height="711" alt="Image" src="https://github.com/user-attachments/assets/31a64f1a-5ce6-42ee-84ed-f2707cc10007" />

as we talking about the distance, the smallest one which can be use to measure is the perpendicular line from that point to the seperating line. Yes we did mention the perpendicular line. So to automate the process, we basically project the whole shape onto the perpendicular line. do the samething for the other shape. If there is a gap between maximum and minimum of both shape, then there is a space which means we could draw a seperating line. thus that is the whole idea of seperating axis theorem
# Projection with dot product
As state above, we have to project all the shape on the seperating axis. But how can we do this?
When we talk about project, we usually mention the dot product. Dot product is define as
$$\vec{m} \cdot \vec{n} = |m|*|n|*\cos{\theta}$$

<img width="410" height="312" alt="Image" src="https://github.com/user-attachments/assets/7c73bc21-a3b3-406a-b946-bb4d1b127aa2" />

If $n$ is an unit vector where its length is 1 $|\vec{n}| = 1$, then the dot product basiclly become an projection onto that direction

<img width="450" height="383" alt="Image" src="https://github.com/user-attachments/assets/6bd2a970-2132-48bb-b70b-177884194c04" />

# General algorithm
- ***Step 1:*** Form the list of edge vectors to represent the polygon
- ***Step 2:*** for each edge, calculate the normal unit vector by using following formula
$$normal\_unit((x,y)) = \frac{(-y,x)}{\sqrt{x^2 + y^2}}$$
Repeatedly do the same thing for all edges and store them in a list. If shape A has $n_a$ edges and shape B has $n_b$ so the legnth of the list is $n_a+n_b$
- ***Step 3:*** (This step can be done along with step 2 but i seperate for understandability)
Loop through all unit vector, for each unit vector, project an entire shape on that vector by using dot product for each pair of edge and normal. Then take the maximum and minimum values of projection for each shape
- ***step 4:*** (this is done during each iteration of unit vector)Now we simply compare between maximum and minimum between shapes. we see that the possible interection is between minimum of one shape and maximum of other. So we could check 
If 
$$\max(A) < \min(B) \lor \min(A) > \max(B)$$
<img width="751" height="280" alt="Image" src="https://github.com/user-attachments/assets/d2bed94b-0c91-4d83-a8db-1abf41bf411e" />
This basically mean that if the maximum of a shape is smaller then the minimum of other, then entire shape is smaller than other shape, which result in a gap. There are two cases that could happen as show above. We only need it to be true for one case so we use *or* operator for two cases. If the statement is fall for **all** the unit vectors, then there exist a collision and we could exist the loop early. However if it is false for all unit vectors, that mean we have detect a collision


# Example of triangle and rectangle
It is better to illustate how we can apply its on paper before we even code. For simplicty, i only do bare example for the case of triangle and rectangle. It should be the same for other shapes
## No collision
Given the triangle and rectangle below, determine whether there is collision using Seperating Axis theorem
<img width="586" height="462" alt="Image" src="https://github.com/user-attachments/assets/39ba15d7-efce-46aa-85ea-ac2decabf9a5" />
Let call the triangle be A and rectangle be B.
**Step 1**: Calculate the edge vectors list for each shape
Edges of A: {(1,2), (-1,0),(-2,-2)}
Edges of B: {(1,0), (1,0.5), (1.5,0.5), (1.5,0)}
(0,0.5) (0.5,0) (0,-0.5) (-0.5,0)
**Step 2**: for each edge vector caclulate the normal unit
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
Normmal units of B: (-1,0) (0,1) (1,0) (0,-1)
Combine we have a list of normal vector
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
-> Stop here and conclude that there is no a collision


## there is collison
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

Conclusion: all axes show overlap. there is collision

