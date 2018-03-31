
from bottle import route,run,static_file,template,post,redirect,request
import time
import json
import os
import RPi.GPIO as GPIO
import threading
time.sleep(300)
assets_path='/home/pi/smart_car/assets'
pin=[05,06,7,8,26,21,16,20]
GPIO.setmode(GPIO.BCM)
for x in pin:
	GPIO.setwarnings(False)
	GPIO.setup(x,GPIO.OUT)
GPIO.setup(13,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(12,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(19,GPIO.IN)
GPIO.setup(25,GPIO.IN)
GPIO.setup(4,GPIO.IN)
IN4=05
IN3=06
ENB=7
ENA=8
IN2=26
IN1=21
L=GPIO.PWM(7,100)
R=GPIO.PWM(8,100)
L.start(0)
R.start(0)
D_Z_Y=GPIO.PWM(16,50)
D_S_X=GPIO.PWM(20,50)
D_Z_Y.start(0)
D_S_X.start(0)
D_Z_Y.ChangeDutyCycle(5)
D_S_X.ChangeDutyCycle(3)
time.sleep(2)
GPIO.setup(20,GPIO.IN)
GPIO.setup(16,GPIO.IN)
status=1
up_dis=0.3
down_dis=0
forward=0
secure_dis=0.25
Lock=threading.Lock() 
def getdistance(trig,echo):
   global status
   global forward
   global secure_dis
   while True:
	GPIO.output(trig,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(trig,GPIO.LOW)
	global up_dis
        global forward
        while not GPIO.input(echo):
		pass
	t1=time.time()
	while GPIO.input(echo):
               pass
        t2=time.time()
        Lock.acquire()
	up_dis=(t2-t1)*340/2
        speed=read_speed()
        secure_dis=(speed*43.58-3.617)/100
        if(secure_dis<0):
          secure_dis=0.1
        print("secure_dis:%s"%(secure_dis))
        if(up_dis<secure_dis and forward==1):
           STOP()
        Lock.release()
        time.sleep(0.1)
t1=threading.Thread(target=getdistance,args=(13,19))
t1.setDaemon(True)
t1.start()
def read_speed():
    file=open('/home/pi/smart_car/speed.txt','r')
    lines=file.readlines()
    count=len(lines)
    print(count)
    if(count!=0):
      s=lines[-1]
      s=s.strip('\n')
      print(s)
      if(count>200):
         file=open('/home/pi/smart_car/speed.txt','w')
      file.close()
      return float(s)
    return 0
def get_speed():
    print('agag')
    speed=0
    global secure_dis
    i=0
    while True:
      while not GPIO.input(4):
         if(i==0):
            t1=time.time()
         pass
      while GPIO.input(4):
         if(i==0):
            t1=time.time()
         pass
      i=i+1
      if(i==20):
        i=0
        t2=time.time()
        speed=0.2/(t2-t1)
        print('speed:%s'%speed)
#T2=threading.Thread(target=get_speed)
#T2.start()
#t2=threading.Timer(0.01,get_speed)
#t2.start()
def D_S_X_F(i):
    GPIO.setup(20,GPIO.OUT)
    D_S_X=GPIO.PWM(20,50)
    D_S_X.start(0)
    D_S_X.ChangeDutyCycle(i)
    time.sleep(1)
    GPIO.setup(20,GPIO.IN)
def D_Z_Y_F(i):
    GPIO.setup(16,GPIO.OUT)
    D_Z_Y=GPIO.PWM(16,50)
    D_Z_Y.start(0)
    D_Z_Y.ChangeDutyCycle(i)
    time.sleep(1)
    GPIO.setup(16,GPIO.IN)
def run1(x,y):
      # L.ChangeDutyCycle(x)
      # R.ChangeDutyCycle(x)
      # time.sleep(0.2)
       global forward
       global up_dis
       global secure_dis
       if(y==1 and up_dis>secure_dis):
         forward=1
         UP(x)
       if(y==2):
         forward=2
         DOWN(x)
       if(y==3):
         forward=3
         LEFT(x)
       if(y==4):
         forward=4
         RIGHT(x)
def UP(x):
        GPIO.output(IN1,GPIO.HIGH)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.HIGH)
	GPIO.output(IN4,GPIO.LOW)
        L.ChangeDutyCycle(x)
        R.ChangeDutyCycle(x)
        global status
        status=1
def DOWN(x):
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.HIGH)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.HIGH)
        L.ChangeDutyCycle(x)
        R.ChangeDutyCycle(x)
def LEFT(x):
	GPIO.output(IN1,GPIO.HIGH)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.HIGH)
        L.ChangeDutyCycle(x)
        R.ChangeDutyCycle(x)
def RIGHT(x):
        GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.HIGH)
	GPIO.output(IN3,GPIO.HIGH)
	GPIO.output(IN4,GPIO.LOW)
        L.ChangeDutyCycle(x)
        R.ChangeDutyCycle(x)
def STOP():
        global status
        status=0
        print('stop')
        L.ChangeDutyCycle(0)
        R.ChangeDutyCycle(0)
@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
	return static_file(filename,root=assets_path)
#******************************************
@route('/duoji_move',method='POST')
def f():
  val=int(request.POST.get('val'))
  direction=request.POST.get('direction')
  print(val,direction)
  print(val)
  if(direction=='Z_Y'):
    D_Z_Y_F(val)
  if(direction=='S_X'):
    D_S_X_F(val)
#*******************************************
@route('/car_start',method='POST')
def f():
   speed=request.POST.get('speed')
   direction=request.POST.get('direction')
   print(speed)
   X=int(speed)
   Y=int(direction)
   print(X,Y)
   if(Y==0):
     STOP()
   else:
     run1(X,Y)

#*******************************************
@route('/cai.html')
def f():
 # t1=threading.Thread(target=getdistance,args=(13,19))
 # t1.setDaemon(True)
 # t1.start()
  return template('cai.html')
#************************************************
run(host='192.168.100.100',port='8090',debug=True)
