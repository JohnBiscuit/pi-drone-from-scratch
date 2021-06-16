from mpu9250 import *
import scipy.integrate as integrate
#import matplotlib.pyplot as plt
import time

alpha = 0.98
t_prev = time.time()
gyro_x_prev = 0
gyro_z_prev = 0
gyro_y_prev = 0
while (1):
    t_now = time.time()
    elapsed = t_now-t_prev
    try:

        acc_roll = acc_roll() #calculate instantaneous g-forces from accelerometer to get roll
        acc_pitch = acc_pitch()

    except:
        continue


    print(acc_roll)
