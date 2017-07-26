from mpu6050 import mpu6050
import RPi.GPIO as GPIO 
import time
import os
from datetime import datetime,date ,timedelta
import socket

sensor=mpu6050(0x68)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.IN)

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
     #print(acc_data)
     #print(gyro_data)
      ax=str(acc_data['x'])
      ay=str(acc_data['y'])
      az=str(acc_data['z'])
      gx=str(gyro_data['x'])
      gy=str(gyro_data['y'])
      gz=str(gyro_data['z'])
      td=str(temp_data)
      sd=str(s_data)
      Ct=time.strftime("%Y-%m-%d %H-%M-%S")
      f.write(Ct+" ")
      f.write("Ax: "+ax+" ")
      f.write("Ay: "+ay+" ")
      f.write("Az: "+az+" ")
      f.write("Gx: "+gx+" ")
      f.write("Gy: "+gy+" ")
      f.write("Gz: "+gz+" ")
      f.write("Temp: "+td+" ")
      f.write("Sd: "+sd+"\n")
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
