前 trig 13 echo 19  后  trig 12 echo 25
GPIO.setup(13,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(12,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(19,GPIO.IN)
GPIO.setup(25,GPIO.IN)
def getdistance(trig,echo):
	GPIO.output(trig,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(trig,GPIO.LOW)
	while not GPIO.input(echo):
		pass
	t1=time.time()
	while GPIO.input(echo):
		t2=time.time()
	    return (t2-t1)*340/2


