from vpython import *
import time
x = box(length=6,width= 3,height = 0.1)
while(1):
    time.sleep(0.001)
    x.rotate(angle = -0.001,axis =vector(0,1,0))
