
import wiringpi


FAN_PIN =  18
FAN_GPIO = 24
FAN_WiPi = 5
RESISTOR_PIN =  16
RES_GPIO =  23
RES_WiPi =  4
OUTPUT=1

def initWipi():
   wiringpi.wiringPiSetup()
   wiringpi.pinMode(FAN_WiPi, OUTPUT)
   wiringpi.pinMode(RES_WiPi, OUTPUT)

   wiringpi.softPwmCreate(FAN_WiPi,1,100)
   wiringpi.softPwmCreate(RES_WiPi,1,100)

def coolDown(control_signal):
   wiringpi.softPwmWrite (FAN_WiPi, control_signal); 
   # heatOvenUp(0)
   
def heatUp(control_signal):
   wiringpi.softPwmWrite (RES_WiPi, control_signal)
   # coolOvenDown(0);
   
