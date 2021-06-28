from mpu9250 import *
import scipy.integrate as integrate
#import matplotlib.pyplot as plt
import time
import smbus
kp = 2
ki = 0.01
kd = 1
pid_p = 0
pid_i = 0
pid_d = 0
target_angle = -6.1 #only for testing
previous_roll_error = 0

roll = 0
pitch =0
alpha = 0.99
t_prev = time.time()
delta_roll = 0
delta_pitch = 0
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
    elapsed = time.time()-t_prev
    t_now = time.time()
    t = elapsed
    #complementary filter (the whole try section,why? just because)
    try:
        acc_x,acc_y,acc_z,wx,wy,wz= mpu6050_conv() #get accelerometer reading

        acc_roll = math.degrees(math.atan(acc_x/acc_z))  #calculate roll and pitch using trigonometry
        acc_pitch = math.degrees(math.atan(acc_y/acc_z))
        
        
        gyro_x_current = gyro_x(wx,elapsed)
        gyro_y_current = gyro_y(wy,elapsed)
        gyro_z_current = gyro_z(wz,elapsed)
        alpha = elapsed = (0.1/(0.1+elapsed))
        #gyro pitch
        dt[1] = elapsed
        data = [gyro_x_prev,gyro_x_current]
        delta_pitch = integrate.trapz(dt,data)
        gyro_pitch = gyro_pitch +delta_pitch
        #gyro roll
        data = [gyro_y_prev,gyro_y_current]
        delta_roll = integrate.trapz(dt,data)
        
        #gyro_roll = roll_angle + area
        
        #gyro yaw
        data = [gyro_z_prev,gyro_z_current]
        area = integrate.trapz(dt,data)
        gyro_yaw = gyro_yaw +area
        roll = ((delta_roll + roll)*alpha)+(acc_roll*(1-alpha))
        pitch = ((delta_pitch + pitch)*alpha)+(acc_pitch*(1-alpha))
        
    except:
        continue
    #print(t)
    t_prev = time.time()
    gyro_x_prev = gyro_x_current
    gyro_y_prev = gyro_y_current
    gyro_z_prev = gyro_z_current
    
    roll_error = roll - target_angle
    pid_p = kp*roll_error
    pid_i = pid_i + (ki*roll_error)
    pid_d = kd*((roll_error - previous_roll_error)/elapsed)
    pid_roll = pid_p + pid_i + pid_d
    previous_roll_error = roll_error
    
    #print(acc_roll)
    #print("roll:",gyro_roll.round(2),"pitch:",gyro_pitch.round(2),"yaw:",gyro_yaw.round(0),"roll angle:",roll_angle.round(2))
    #print("roll:",roll.round(2),"pitch:",pitch.round(2))
    print("roll:",roll.round(2),"pid_roll:",pid_roll)
