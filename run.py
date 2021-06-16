from mpu9250 import *
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import time

while (1):
    try:
        acc_roll = acc_roll()
        acc_pitch = acc_pitch()
        gyro_x
