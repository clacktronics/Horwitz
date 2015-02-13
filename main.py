
colors = 	{
			0:{'R':0,'G':0,'B':0},
			1:{'R':18,'G':90,'B':18},
			2:{'R':0,'G':20,'B':2},
			3:{'R':0,'G':0,'B':110},
			4:{'R':2,'G':0,'B':20},
			5:{'R':50,'G':0,'B':10},
			6:{'R':50,'G':0,'B':0},
			7:{'R':50,'G':20,'B':0},
			8:{'R':100,'G':60,'B':0}
			}

			
			
import pyb, ure
from time import sleep			
from pwm import ledpwm

RedF = 200
GreenF = 200
BlueF = 200

pinconfig = {
	0:{	'R':ledpwm('Y8',12,2,RedF),
		'G':ledpwm('Y1',8,1,GreenF),
		'B':ledpwm('Y3',10,1,BlueF)
		},
	1:{	'R':ledpwm('Y4',11,1,RedF),
		'G':ledpwm('Y6',1,1,GreenF), #inv
		'B':ledpwm('X9',4,1,BlueF)
		},
	2:{	'R':ledpwm('Y7',12,1,RedF),
		'G':ledpwm('Y2',8,2,GreenF),
		'B':ledpwm('X10',4,2,BlueF)
		},
	3:{	'R':ledpwm('P18',2,1,RedF),
		'G':ledpwm('Y12',1,3,GreenF),
		'B':ledpwm('X17',2,2,BlueF)
		},
	4:{	'R':ledpwm('X2',5,2,RedF),
		'G':ledpwm('X3',9,1,GreenF),
		'B':ledpwm('Y10',2,4,BlueF)
		},
	5:{	'R':ledpwm('X4',5,4,RedF),
		'G':ledpwm('X6',0,0,GreenF),
		'B':ledpwm('X8',14,1,BlueF)
		},
	6:{	'R':ledpwm('X7',13,1,RedF),
		'G':ledpwm('X5',0,0,GreenF),
		'B':ledpwm('Y9',2,3,BlueF)
		},
	7:{ 'R':ledpwm('X1',5,1,RedF),
		'G':ledpwm('Y11',1,2,GreenF), #inv
		'B':ledpwm('LED_YELLOW',2,1,BlueF) #inv
		}
}

def clear():
	for led in pinconfig:
		for pin in pinconfig[led]:
			pinconfig[led][pin].pwm(0)
			
def color(color,pwm):
	for led in pinconfig:
		pinconfig[led][color].pwm(pwm)
		
def rainbow(speed,repeats):
	fademap = (100,20,10,1,0,1,10,20)
	for i in range(0,repeats):
		for step in range(0,8):
			for led in range(0,8):			
				pinconfig[(led+step)%8]['R'].pwm(fademap[led])
				pinconfig[(led+step+4)%8]['G'].pwm(fademap[led])
				pinconfig[(led+step+5)%8]['B'].pwm(fademap[led])
			sleep(speed)
			
def fade(color,speed,repeats):
	for intensity in range(0,101):
		for led in pinconfig:
			pinconfig[led][color].pwm(intensity)
		sleep(speed)
	
			
			
def horwitz():
	pinconfig[1]['R'].pwm(95)
	pinconfig[2]['R'].pwm(95)
	pinconfig[2]['B'].pwm(25)
	pinconfig[3]['B'].pwm(95)
	pinconfig[4]['B'].pwm(95)
	pinconfig[4]['G'].pwm(75)
	pinconfig[5]['G'].pwm(95)
	pinconfig[6]['G'].pwm(95)
	pinconfig[6]['R'].pwm(95)
	pinconfig[7]['R'].pwm(95)
	pinconfig[7]['G'].pwm(50)
	pinconfig[8]['R'].pwm(95)
	pinconfig[8]['G'].pwm(10) 

clear()

for i in range(8):
	for color in colors[i]:
		pinconfig[i][color].pwm(colors[i][color]) 
		#print('LED',i,'is',,)

			
sequence = open('data.txt','r')

# Open the data text file, it runs through the sequence a line at a time, first it checks
# if the line is 'commented' out with a # or if its a blank line to ignore. Then it checks it
# starts with a number if yes then its a sequence step. If not its a command or title.
# It works in boolean by seeing if an object is made when a match is correct.

sequenceDivide = False
seqStep = 0





with open("data.txt") as sequence:
	for line in sequence:
		if ure.match('#',line) == None or ure.match('\n',line) == None:
		
			if ure.match('[0-9]',line) == None : 
			
				#if line != ure.match(' *speed',line) or line != ure.match(' *loop',line):
				#	if sequenceDivide == False:
				#		sequenceDivide = True
				#		repeats = 0
				#		startPoint = seqStep
				#	elif repeats == loop:
				#		sequenceDivide == False:
				#		
				#		break
				#	else:
				#		repeats = repeats + 1	
			
				speedvar = ure.match('speed *= *(\.?[0-9]*)',line)
				loopvar = ure.match('loop *= *([0-9]*)',line)
				if speedvar != None:
					delay = float(speedvar.group(1))
					print('Step Delay is', delay)
				elif loopvar != None:
					loop = int(loopvar.group(1))
					#print('This sequence will loop', loop,'times')
					
			# This is compact so hard to understand, first checks if it is not an empty newline.
			
			else:
				step = 	ure.match('([0-8]) *([0-8]) *([0-8]) *([0-8]) *([0-8]) *([0-8]) *([0-8]) *([0-8])',line)
				for led in pinconfig:
					for color in pinconfig[led]:
						pinconfig[led][color].pwm(colors[int(step.group(led+1))][color])
						#print('LED',led,'(',color,')','is',step.group(led+1) )
				seqStep = seqStep + 1
				sleep(delay)


	