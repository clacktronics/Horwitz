import pyb, ure, os
from time import sleep
from pwm import ledpwm

#=Utility=functions=======================================================================
# These are functions that can be called in the interpreter after it loads they do useful
# Functions to test parts are working.

# Sets all LEDs to black
def clear():
  for led in pinconfig:
    for pin in pinconfig[led]:
      pinconfig[led][pin].pwm(0)

# Sets one colour for all LEDs
def color(color,pwm):
  for led in pinconfig:
    pinconfig[led][color].pwm(pwm)

# walking rainbow pattern
def rainbow(speed,repeats):
  fademap = (100,20,10,1,0,1,10,20)
  for i in range(0,repeats):
    for step in range(0,8):
      for led in range(0,8):
        pinconfig[(led+step)%8]['R'].pwm(fademap[led])
        pinconfig[(led+step+4)%8]['G'].pwm(fademap[led])
        pinconfig[(led+step+5)%8]['B'].pwm(fademap[led])
      sleep(speed)

# Fades a chosen colour up a defined number of times ( checking balance between leds )
def fade(color,speed,repeats):
  for intensity in range(0,101):
    for led in pinconfig:
      pinconfig[led][color].pwm(intensity)
    sleep(speed)

# Show horwitz colours in order on LEDs 1 to 8
def horwitz():
  for i in range(0,8):
    pinconfig[i]['R'].pwm(colors[i+1]['R']) 
    pinconfig[i]['G'].pwm(colors[i+1]['G'])  
    pinconfig[i]['B'].pwm(colors[i+1]['B'])   

#=Horwitz=Colours=========================================================================

# These are the set colours

colors = { 
0:{	'R':100, 'G':100, 'B':100 },
1:{	'R':100, 'G':98,  'B':100 },
2:{	'R':100, 'G':100, 'B':1   },
3:{	'R':100, 'G':100, 'B':90  },
4:{	'R':70,  'G':100, 'B':60  },
5:{	'R':1,   'G':100, 'B':100 },
6:{	'R':1,   'G':90,  'B':100 },
7:{	'R':1,   'G':70,  'B':100 },
8:{	'R':100, 'G':20,  'B':100 }
}

#=LED=Setup===============================================================================
#Each array of LEDs can have their own frequency bar P18 which is LED 3 Red which is fixed

RedF = 100
GreenF = 150
BlueF = 75

# This initialises all the pins by setting all the frequencies. The pwm Library makes sure
# the right commands go to the right pins. Note that most of the pins share each others 
# clocks and 'P18' has a fixed frequency so setting the frequency has no effect but has to
# be there to not break the class assignment!

pinconfig = {
0:{
  'R':ledpwm('Y8',12,2,RedF),
  'G':ledpwm('Y1',8,1,GreenF),
  'B':ledpwm('Y3',10,1,BlueF)
},
1:{
  'R':ledpwm('Y4',11,1,RedF),
  'G':ledpwm('Y6',1,1,GreenF), #inv
  'B':ledpwm('X9',4,1,BlueF)
},
2:{
  'R':ledpwm('Y7',12,1,RedF),
  'G':ledpwm('Y2',8,2,GreenF),
  'B':ledpwm('X10',4,2,BlueF)
},
3:{
  'R':ledpwm('P18',2,1,RedF),
  'G':ledpwm('Y12',1,3,GreenF),
  'B':ledpwm('X17',2,2,BlueF)
},
4:{
  'R':ledpwm('X2',5,2,RedF),
  'G':ledpwm('X3',9,1,GreenF),
  'B':ledpwm('Y10',2,4,BlueF)
},
5:{
  'R':ledpwm('X4',5,4,RedF),
  'G':ledpwm('X6',0,0,GreenF),
  'B':ledpwm('X8',14,1,BlueF)
},
6:{
  'R':ledpwm('X7',13,1,RedF),
  'G':ledpwm('X5',0,0,GreenF),
  'B':ledpwm('Y9',2,3,BlueF)
},
7:{
'R':ledpwm('X1',5,1,RedF),
'G':ledpwm('Y11',1,2,GreenF), #inv
'B':ledpwm('LED_YELLOW',2,1,BlueF) #inv
}
}

#=Main=Program============================================================================

clear()

sequences = [elem for elem in os.listdir('sequences') if elem[0] != '.']

# Open the data text file, it runs through the sequence a line at a time, first it checks
# if the line is 'commented' out with a # or if its a blank line to ignore. Then it checks
# it starts with a number if yes then its a sequence step. If not its a command or title.
# It works in boolean by seeing if an object is made when a match is correct. Below are
# the groups formed by the regular expression

#group 0 : all
#group 1 : all of the variable ( speed or loop )
#group 2 : variable bits (dont use)
#group 3 : variable name
#group 4 : 
#group 5 : variable value
#group 6 : sequence step values
#group 7 : led1
#group 8 : led2
#group 9 : led3
#group 10 : led4
#group 11 : led5
#group 12 : led6
#group 13 : led7
#group 14 : led8
#group 15 : all text

# speed set to 0 so it rushes through the file until it is changed by setting the speed in
# the file.
speed = 0

while True:
  for sequence in sequences:
    with open("sequences/%s" % sequence) as datatxtLine:

      for lineNumber,line in enumerate(datatxtLine): 
        
        # Skip blank lines
        if ure.match('#|\n',line) == None: 
          
          # Use regular expressions to compile information into variables
          lineRead = ure.match(' *(((beat)|(loop)) *= *([\.0-9]*))?( *([0-9]) *([0-9]) *([0-9]) *([0-9]) *([0-9]) *([0-9]) *([0-9]) *([0-9])*)?([- a-zA-Z0-9\(\)]*)',line)
          
          if lineRead.group(2) == 'beat':
            speed = float(lineRead.group(5))
          elif lineRead.group(2) == 'loop':
            loop = lineRead.group(5)
          elif lineRead.group(14) != None:
            for i in range(0,8):
              pinconfig[i]['R'].pwm(colors[int(lineRead.group(i+7))]['R']) 
              pinconfig[i]['G'].pwm(colors[int(lineRead.group(i+7))]['G'])  
              pinconfig[i]['B'].pwm(colors[int(lineRead.group(i+7))]['B'])
            print('%s : Line - %d' % (sequence, lineNumber))
            sleep(speed)
