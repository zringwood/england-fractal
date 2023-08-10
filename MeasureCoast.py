from PIL import Image, ImageDraw
import math
import numpy as np
mask = Image.open("mask.png")

#The length of our "measuring stick", per the coastline paradox. 
radius = 30
startpoint = (353, 353)
allPoints = [startpoint]

BLACK = (0,0,0, 255)
WHITE = (255, 255, 255, 255)
ONE_DEGREE = (2*math.pi) / 360
MAX_POINTS = 2571

def rotate(point, center, delta_radians) :
    ROTATION = [[math.cos(delta_radians), -math.sin(delta_radians)], [math.sin(delta_radians), math.cos(delta_radians)]]
    point_origin = [point[0] - center[0], point[1] - center[1]]
    point_rotated = np.matmul(point_origin, ROTATION)
    return (point_rotated[0] + center[0], point_rotated[1] + center[1])
def toInteger(point):
    return (math.trunc(point[0]), math.trunc(point[1]))
savePoints = []
def isOutOfBounds(point):
    return point[0] > mask.size[0] or point[1] > mask.size[1]
currentpoint = (startpoint[0] - radius, startpoint[1])
# allPoints needs two points in the array for the loop to work properly. 
initialcolor = mask.getpixel(currentpoint) 
while mask.getpixel(toInteger(currentpoint)) == initialcolor :
    currentpoint = rotate(currentpoint, allPoints[len(allPoints)-1], ONE_DEGREE)
    savePoints.append(currentpoint)
   
allPoints.append((currentpoint)) 

while math.dist(currentpoint, startpoint) > radius :  
    currentpoint = rotate(allPoints[len(allPoints)-2], allPoints[len(allPoints)-1], ONE_DEGREE*180)
    #We're searching for the edge. Therefore, we're always looking for the OPPOSITE color of the initial point.
    initialcolor = mask.getpixel(currentpoint) 
    direction = 1 if initialcolor == BLACK else -1
    
    while isOutOfBounds(currentpoint) or mask.getpixel(toInteger(currentpoint)) == initialcolor :
        currentpoint = rotate(currentpoint, allPoints[len(allPoints)-1], ONE_DEGREE*direction)
        if not isOutOfBounds(currentpoint):
            savePoints.append(currentpoint)
        
    allPoints.append((currentpoint))
    if len(allPoints) > MAX_POINTS:
        break
    


# for i in range(len(savePoints)):
#     point = toInteger(savePoints[i])
#     mask.paste((255, 0, 0, 255), (point[0], point[1], point[0] + 1, point[1] + 1))

draw = ImageDraw.Draw(mask)
draw.polygon(allPoints, None, (255,0,0), 3)
for i in range(len(allPoints)):
    point = toInteger(allPoints[i])
    mask.paste((0, 0, 255, 255), (point[0], point[1], point[0] + 5, point[1] + 5))
mask.show()