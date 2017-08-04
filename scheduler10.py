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
startday=time.strftime("%Y%m%d")
stday=date.today()
night="23:59:00"
day="00:00:30"
morning="10:00:00"

def function(str):
     s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     addr='10.145.220.76'
     s.connect((addr,8001))
    # s.send("Hello")
     with open(str,'rb') as fi:
         s.sendall(fi.read())
     fi.close()
     os.remove(str)
     stday=date.today()
     startday=stday.strftime("%Y%m%d")

while(1):
 now=datetime.strftime(datetime.now(),"%H:%M:%S")	
 if(day<=now<night):
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
      f.write("Sd: "+str(s_data)+"\n")
      f.write("Ld: "+str(l_data)+" ")
      f.write("IRd: "+str(ir_data)+"\n")
      time.sleep(2)

      tday=date.today()
      now1=datetime.strftime(datetime.now(),"%H:%M:%S")
      if(now1>=morning and  tday==stday+timedelta(1)):
         fname1=startday+".txt"
    
         function(str=fname1)     
      if(now1>=night):
  	 break
         
f.close()
GPIO.cleanup()
