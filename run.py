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
        a_x, a_y, a_z, w_x, w_y, w_z = mpu6050_conv()
    except:
        continue
        print(a_x)
