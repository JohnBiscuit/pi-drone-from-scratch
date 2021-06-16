from mpu9250 import *
import scipy.integrate as integrate
#import matplotlib.pyplot as plt
import time
import smbus

alpha = 0.98
t_prev = time.time()
gyro_x_prev = 0
gyro_z_prev = 0
gyro_y_prev = 0

time.sleep(1)

while (1):
    t_now = time.time()
    elapsed = t_now-t_prev
    try:
        acc_roll,acc_pitch,wx,wy,wz = value(elapsed)
    except:
        continue
    print(acc_roll)
