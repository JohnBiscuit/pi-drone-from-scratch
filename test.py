def values(elapsed):
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


    return acc_roll,acc_pitch,wx,wy,wz
