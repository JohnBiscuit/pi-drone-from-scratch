#include<Wire.h>
#include<Servo.h>
const int MPU_addr = 0x68; // I2C address of the MPU-6050
double AcX, AcY, AcZ, Temp, GyroX, GyroY, GyroZ;
double AcX_prev, AcY_prev, AcZ_prev, GyroX_prev = 0, GyroY_prev, GyroZ_prev ;
double acc_pitch, acc_roll, pitch, roll;
double delta_roll, delta_pitch;
double alpha = 0.992;
double gyro_pitch, pitch_error, roll_error, error_tolerance = 90;
double gyro_roll;
int motor1_output,motor2_output;
float current_time, prev_time = 0, elapsed = 0;
float kp = 5,ki=0.02,kd = 0;
float pid_p,pid_i,pid_d;
float pid_roll,pid_pitch;
float rollError,pitchError,previous_rollError,previous_pitchError;
float target_angle = 0;
Servo motor1;
Servo motor2;
void setup() {
  pid_p,pid_i,pid_d=0;
  rollError,pitchError,previous_rollError,previous_pitchError=0;
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x19);
  Wire.write(0);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  motor1.attach(8);
  motor2.attach(9);
  Serial.begin(115200);
  motor1.writeMicroseconds(1000); 
  motor2.writeMicroseconds(1000);
}
void loop() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  current_time = millis();
  elapsed = current_time - prev_time;
  Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers
  AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  Temp = Wire.read() << 8 | Wire.read();
  GyroX = Wire.read() << 8 | Wire.read();
  GyroY = Wire.read() << 8 | Wire.read();
  GyroZ = Wire.read() << 8 | Wire.read();
  AcX = (AcX / pow(2, 15)) * 16 * 9.807;
  AcY = (AcY / pow(2, 15)) * 16 * 9.807;
  AcZ = (AcZ / pow(2, 15)) * 16 * 9.807;
  GyroX = (GyroX / pow(2, 15)) * 400;
  GyroY = (GyroY / pow(2, 15)) * 400;
  GyroZ = (GyroZ / pow(2, 15)) * 400;
  acc_pitch = (atan(AcX / AcZ) * 180 / 3.14159265359);
  acc_roll = (atan(AcY / AcZ) * 180 / 3.14159265359);
  delta_pitch = (0.5 * (0.0025 * (GyroY_prev + GyroY)) * -1);
  delta_roll = 0.5 * (0.0025 * (GyroX_prev + GyroX));
  pitch = ((delta_pitch + pitch) * alpha) + (acc_pitch * (1 - alpha)) * -1;
  roll = ((delta_roll + roll) * alpha) + (acc_roll * (1 - alpha));
  gyro_pitch = gyro_pitch + delta_pitch;
  gyro_roll = gyro_roll + delta_roll;
  Serial.print(roll);
  Serial.print("\t");
  Serial.print(pitch);


  pitch_error = gyro_pitch - pitch;
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

  //Roll PID calculations
  rollError = roll-target_angle;
  pid_p = kp*roll_error;
  pid_i = pid_i + (ki*roll_error);
  pid_d = kd*((roll_error - previous_rollError)/elapsed);
  pid_roll = pid_p + pid_i + pid_d;
  previous_rollError = roll_error;
  
  //pitch_pid
  pitch_error = pitch - target_angle;
  pid_p = kp*pitch_error;
  pid_i = pid_i + (ki*roll_error);
  pid_d = kd*((roll_error - previous_rollError)/elapsed);
  pid_pitch = pid_p + pid_i + pid_d;
  previous_pitchError = pitch_error;
  Serial.print("\t");
  Serial.print(pid_roll);
  Serial.print("\t");
  Serial.print(pid_pitch);
  motor1_output = map(pid_roll,0,2000,1100,1500);
  motor2_output = map(pid_roll,0,-2000,1100,1500);
  Serial.print("\t");
  Serial.print(motor1_output);
  Serial.print("\t");
  Serial.println(motor2_output);
  motor1.writeMicroseconds(motor1_output);
  motor2.writeMicroseconds(motor2_output);
}
