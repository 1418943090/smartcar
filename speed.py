import time
import RPi.GPIO as GPIO
time.sleep(20)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
def ce_su():
        i=0
	while True:
           f=open('speed.txt','a')
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
              f.write(str(speed))
              f.write('\n')
              f.close()  
              print(speed)
if __name__=="__main__":
    
    ce_su()
    f.close() 
