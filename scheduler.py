from mpu6050 import mpu6050
import RPi.GPIO as GPIO 
import time
import os
from datetime import datetime,date ,timedelta
import socket

sensor=mpu6050(0x68)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.IN)
GPIO.setup(4,GPIO.IN)
GPIO.setup(27,GPIO.IN)

now=datetime.strftime(datetime.now(),"%H:%M:%S")
print(now)
night="23:59:00"
day="00:00:30"
def function(str):
     s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     addr='10.147.73.136'
     s.connect((addr,8001))
    # s.send("Hello")
     with open(str,'rb') as fi:
         s.sendall(fi.read())
     fi.close()
     os.remove(str)
while(1):
 now3=datetime.strftime(datetime.now(),"%H:%M:%S")
 if(day<=now3<night):
   fname=time.strftime("%Y%m%d")+".txt"
   print("Recording data-"+time.strftime("%d-%m-%Y"))
   f=open(fname,"a+")

   while(1):
      acc_data=sensor.get_accel_data()
      gyro_data=sensor.get_gyro_data()
      temp_data=sensor.get_temp()
      s_data=GPIO.input(12)
      l_data=GPIO.input(27)
      ir_data=GPIO.input(4)          
     #print(acc_data)
     #print(gyro_data)
      Ct=time.strftime("%Y-%m-%d %H-%M-%S")
      f.write(Ct+" ")
      f.write("Ax: "+str(acc_data['x'])+" ")
      f.write("Ay: "+str(acc_data['y'])+" ")
      f.write("Az: "+str(acc_data['z'])+" ")
      f.write("Gx: "+str(gyro_data['x'])+" ")
      f.write("Gy: "+str(gyro_data['y'])+" ")
      f.write("Gz: "+str(gyro_data['z'])+" ")
      f.write("Temp: "+str(temp_data)+" ")
      f.write("Sd: "+str(s_data)+" ")
      f.write("Ld: "+str(l_data)+" ")
      f.write("IRd: "+str(ir_data)+"\n")
      time.sleep(2)
      now1=datetime.strftime(datetime.now(),"%H:%M:%S")
      if(now1>=night):
         print("Recording Completed")
         function(str=fname)
         break
f.close()
GPIO.cleanup()
