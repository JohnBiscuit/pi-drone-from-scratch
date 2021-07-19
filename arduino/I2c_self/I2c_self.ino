#include<Wire.h>
const int MPU_addr=0x68; // I2C address of the MPU-6050
double AcX,AcY,AcZ,Temp,GyroX,GyroY,GyroZ;
double AcX_prev,AcY_prev,AcZ_prev,GyroX_prev=0,GyroY_prev,GyroZ_prev = 0;  
double acc_pitch,acc_roll,pitch,roll;
double delta_roll,delta_pitch;
double alpha = 0.992;
double gyro_pitch,pitch_error,roll_error,error_tolerance = 90;
double gyro_roll;
float current_time,prev_time = 0,elapsed = 0;
void setup(){
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x19);
  Wire.write(0);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(115200);
}
void loop(){
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  current_time = millis();
  elapsed = current_time - prev_time;
  Wire.requestFrom(MPU_addr,14,true); // request a total of 14 registers
  AcX=Wire.read()<<8|Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY=Wire.read()<<8|Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  Temp=Wire.read()<<8|Wire.read();
  GyroX=Wire.read()<<8|Wire.read();
  GyroY=Wire.read()<<8|Wire.read();
  GyroZ=Wire.read()<<8|Wire.read();
  AcX = (AcX/pow(2,15))*16*9.807;
  AcY = (AcY/pow(2,15))*16*9.807;
  AcZ = (AcZ/pow(2,15))*16*9.807;
  GyroX = (GyroX/pow(2,15))*400;
  GyroY = (GyroY/pow(2,15))*400;
  GyroZ = (GyroZ/pow(2,15))*400;
  acc_pitch = (atan(AcX/AcZ)*180/3.14159265359);
  acc_roll = (atan(AcY/AcZ)*180/3.14159265359);
  delta_pitch = (0.5*(0.0025*(GyroY_prev+GyroY))*-1);
  delta_roll = 0.5*(0.0025*(GyroX_prev+GyroX));
  pitch = ((delta_pitch+pitch)*alpha)+(acc_pitch*(1-alpha))*-1;
  roll = ((delta_roll+roll)*alpha)+(acc_roll*(1-alpha));
  gyro_pitch = gyro_pitch +delta_pitch;
  gyro_roll = gyro_roll + delta_roll;
  Serial.print(roll);
  Serial.print("\t");
  Serial.println(pitch);
  

  pitch_error = gyro_pitch-pitch;
  roll_error = gyro_roll - roll;
  /*
  if (pitch_error>error_tolerance||pitch_error<-error_tolerance){
    gyro_pitch = pitch;
    delta_pitch = 0;
    }
  if (roll_error>error_tolerance||roll_error<-error_tolerance){
    gyro_roll = roll;
    delta_roll = 0;
    }
 */
  GyroX_prev = GyroX;
  GyroY_prev = GyroY;
  GyroZ_prev = GyroZ;
  prev_time = current_time;
  //delay(1);
  
}
