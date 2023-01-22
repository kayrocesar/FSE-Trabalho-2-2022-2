
import wiringpi




VENT_WiPi = 5
RES_WiPi =  4
OUTPUT=1

def initWipi():
   wiringpi.wiringPiSetup()
   wiringpi.pinMode(VENT_WiPi, OUTPUT)
   wiringpi.pinMode(RES_WiPi, OUTPUT)

   wiringpi.softPwmCreate(VENT_WiPi,1,100)
   wiringpi.softPwmCreate(RES_WiPi,1,100)

def coolDown(control_signal):
   wiringpi.softPwmWrite (VENT_WiPi, int(control_signal)); 
   
   
def heatUp(control_signal):
   wiringpi.softPwmWrite (RES_WiPi, int (control_signal))
   

def control_res_vent(control_sig):
     if(control_sig < 0):
               print("Iniciando acionamento da ventoinha do forno...")
               if control_sig > -40:
                  control_sig= 40
               else:
                  control_sig=control_sig*(-1)
                  coolDown(control_sig)
                  heatUp(0)
     elif(control_sig > 0):
                  print("Iniciando acionamento da resistencia do forno...")
                  heatUp(control_sig)
                  coolDown(0)
def turn_off_res_vent():
   heatUp(0)
   coolDown(0)


  