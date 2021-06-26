from vpython import *
import time
x = box(length=6,width= 3,height = 0.1,opacity=1,shininess=0.1,color=color.magenta)
pointer = arrow(pos=vector(0,0,1),axis=vector(2,0,0), shaftwidth=0.1)
pointer2 = arrow(pos=vector(0,0,1),axis=vector(0,2,0), shaftwidth=0.1,color = color.red)
pointer3 = arrow(pos=vector(0,0,1),axis=vector(0,0,2), shaftwidth=0.1)


while(1):
    time.sleep(0.0015)
    x.rotate(angle = -0.001,axis =vector(0,1,0))
    x.rotate(angle = -0.001,axis =vector(1,0,0))
    x.rotate(angle = -0.001,axis =vector(0,0,1))
