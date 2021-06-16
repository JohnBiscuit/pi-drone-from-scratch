from mpu9250 import *
import scipy.integrate as integrate
#import matplotlib.pyplot as plt
import time
import smbus
roll_angle = 0
alpha = 0.02
t_prev = time.time()
gyro_x_prev = 0
gyro_z_prev = 0
gyro_y_prev = 0
gyro_pitch = 0
gyro_roll = 0
gyro_yaw = 0
time.sleep(1)
dt = [0,0]
data = [0,0]
while (1):
    t_now = time.time()
    elapsed = t_now-t_prev
    #complementary filter (the whole try section,why? just because)
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
        alpha = elapsed = (0.05/(0.05+elapsed))
        #gyro pitch
        dt[1] = elapsed
        data[0] = gyro_x_prev
        data[1] = gyro_x_current
        area = integrate.trapz(dt,data)
        gyro_pitch = gyro_pitch +area
        #gyro roll
        dt[1] = elapsed
        data[0] = gyro_y_prev
        data[1] = gyro_y_current
        area = integrate.trapz(dt,data)
        gyro_roll = roll_angle +area
        #gyro yaw
        dt[1] = elapsed
        data[0] = gyro_y_prev
        data[1] = gyro_y_current
        area = integrate.trapz(dt,data)
        gyro_yaw = gyro_yaw +area
        roll_angle = (gyro_roll*alpha)+(acc_roll*(1-alpha))

    except:
        continue
    print(time.time-t_prev)
    t_prev = t_now
    gyro_x_prev = gyro_x_current
    gyro_y_prev = gyro_y_current
    gyro_z_prev = gyro_z_current

    #print("roll:",gyro_roll.round(0),"pitch:",gyro_pitch.round(0),"yaw:",gyro_yaw.round(0),"acc_roll:",acc_roll.,"roll angle:",roll_angle.round(2))
