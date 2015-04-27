from time import sleep
import pyb



class ledpwm:
	
	def __init__(self,pin,timer,channel,freq):
		
		self.freq = freq
		self.timer = timer
		self.channel = channel
		self.pin = pin
		
		if pin == 'X5' or pin == 'X6':
			self.dac = pyb.DAC(pin)
			self.buf = bytearray(100)
			self.dac.write_timed(self.buf, freq * len(self.buf), mode=pyb.DAC.CIRCULAR)
			
		elif pin == 'P18':
			self.ch = pyb.LED(4)
			
		else:
			self.pinpwm = pyb.Pin(pin)
			timerset = pyb.Timer(self.timer, freq=self.freq)
			self.ch = timerset.channel(self.channel, pyb.Timer.PWM, pin=self.pinpwm)
	
	def pwm(self,PWM):
		if self.pin == 'X5' or self.pin == 'X6':
			b = self.buf # cache buf variable for speed
			pwm = PWM * len(b) // 100
			for i in range(len(b)):
				b[i] = 255 if i < pwm else 0
		elif self.pin == 'P18':
			PWM = self.map(PWM,0,100,0,256)
			self.ch.intensity(PWM)
		else:
			if self.pin in ('Y6','Y11','Y12'):
				PWM = int(self.map(PWM,0,100,100,0))
			self.ch.pulse_width_percent(PWM)
	
	# Borrowed from Arduino
	def map(self,x, in_min, in_max, out_min, out_max):
		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
		
		
			
			
			
			
	
	
	
	






'''

timer8 = pyb.Timer(8, freq=100)
timer4 = pyb.Timer(4, freq=100)

LED =  {
1:
{
'R':timer8.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.Y2, pulse_width=0),
'G':timer8.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.Y1, pulse_width=0),
'B':timer4.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.Y3, pulse_width=0)
}
}

while True:
	for pulse in range(0,10000,5):
		timer8.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.Y2, pulse_width=pulse)
		sleep(.001)
	timer8.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.Y2, pulse_width=0)	
	for pulse in range(0,10000,5):
		timer8.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.Y1, pulse_width=pulse)
		sleep(.001)
	timer8.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.Y1, pulse_width=0)	
	for pulse in range(0,10000,5):
		timer4.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.Y3, pulse_width=pulse)
		sleep(.001)
	timer4.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.Y3, pulse_width=0)	



2:
{
'R':pyb.Pin('Y4', pyb.Pin.OUT_PP),
'G':pyb.Pin('Y6', pyb.Pin.OUT_PP),
'B':pyb.Pin( 'X9', pyb.Pin.OUT_PP)
},

3:
{
'R':pyb.Pin('Y7', pyb.Pin.OUT_PP),
'G':pyb.Pin('Y8', pyb.Pin.OUT_PP),
'B':pyb.Pin( 'X10', pyb.Pin.OUT_PP)
},

4:
{
'R':pyb.Pin('X11', pyb.Pin.OUT_PP),
'G':pyb.Pin( 'X12', pyb.Pin.OUT_PP), 
'B':pyb.Pin('X17' , pyb.Pin.OUT_PP)
},

5:
{
#'R':pyb.Pin('P19', pyb.Pin.OUT_PP),
#'G':pyb.Pin('P18', pyb.Pin.OUT_PP),
'B':pyb.Pin( 'X1', pyb.Pin.OUT_PP)
},

6:
{
'R':pyb.Pin('X2', pyb.Pin.OUT_PP),
'G':pyb.Pin('X4', pyb.Pin.OUT_PP), 
'B':pyb.Pin('X3', pyb.Pin.OUT_PP)
},

7:
{
'R':pyb.Pin('X6', pyb.Pin.OUT_PP),
'G':pyb.Pin('X8', pyb.Pin.OUT_PP), 
'B':pyb.Pin('Y9', pyb.Pin.OUT_PP) 
},

8:
{
'R':pyb.Pin('Y10', pyb.Pin.OUT_PP),
'G':pyb.Pin('Y11', pyb.Pin.OUT_PP), 
'B':pyb.Pin('Y12', pyb.Pin.OUT_PP)
}
}
			
			
'''
		


