import socket
import time
from datetime import datetime,date ,timedelta

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',8001))
s.listen(10)
yesterday=date.today()-timedelta(1)
yday=yesterday.strftime("%Y%m%d")

while True:
 tday=time.strftime("%Y%m%d")
 while(yday!=tday):
   print("Connecting...")
   tday=time.strftime("%Y%m%d")
   fname=time.strftime("%Y%m%d")+".txt"
   f=open(fname,'w+').close()
   (c, addr) =s.accept()
   #print(addr)
   data = []
   f=open(fname,'wb')
   print("Receiving Data..."+time.strftime("%d-%m-%Y"))
   while True:
      data = c.recv(4096)
      #print(data)
      if not data: 
           break
      f.write(data)
   f.close()
   yday=tday
   print("Data Received...")
