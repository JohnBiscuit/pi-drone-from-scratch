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
        ax,ay,az,wx,wy,wz= mpu6050_conv()
        acc_x = ax        #get accelerometer reading of x axis
        acc_z = az        #get accelerometer reading of x axis
        a_z = (acc_z / (2.0 ** 15.0)) * accel_sens  #convert to G's of acceleration
        a_x = (acc_x / (2.0 ** 15.0)) * accel_sens
        acc_roll = math.degrees(math.atan(a_x/a_z))
        acc_y = read_raw_bits(ACCEL_YOUT_H)
        acc_z = read_raw_bits(ACCEL_ZOUT_H)
        a_y = (acc_y / (2.0 ** 15.0)) * accel_sens
        a_z = (acc_z / (2.0 ** 15.0)) * accel_sens
        acc_pitch = math.degrees(math.atan(a_y/a_z))
        gyro_x_current = gyro_x(wx,elapsed)
        gyro_y_current = gyro_y(wy,elapsed)
        gyro_z_current = gyro_z(gyro_z,elapsed)
        gyro_pitch = gyro_pitch(gyro_x_prev,gyro_x_current,elapsed)
    except:
        continue

    print(gyro_z_current)
