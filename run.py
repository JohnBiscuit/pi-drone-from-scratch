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
        t_now = time.time()
        elapsed = t_now-t_prev
        acc_roll = acc_roll() #calculate instantaneous g-forces from accelerometer to get roll
        acc_pitch = acc_pitch()
        gyro_x = gyro_x(elapsed) #pitch
        gyro_y = gyro_y(elapsed) #yaw
        gyro_z = gyro_z(elapsed) #roll
        print("try")
    except:
        continue
    try:
        gyro_pitch = gyro_pitch(gyro_x_prev,gyro_x,t_prev)
        gyro_roll = gyro_roll(gyro_y_prev,gyro_y,t_prev)
        gyro_yaw = gyro_yaw(gyro_z_prev,gyro_z,t_prev)

        pitch = (gyro_x*alpha)+(acc_pitch*(1-alpha))
        roll = (gyro_y*alpha)+(acc_roll*(1-alpha))
        gyro_x_prev = gyro_pitch
        gyro_y_prev = gyro_roll
        gyro_z_prev = gyro_yaw
        t_prev =t_now
        print(pitch)
    except:
        print("error")
        continue
