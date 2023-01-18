import RPi.GPIO as GPIO
import signal  
import time  
from uart import *

def exit_handler(signal, frame):

   print('\nSignal ' , signal , 'recebido\nEncerrando..........')
   exit(1)

# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, exit_handler)
 






if __name__ == "__main__":
     
   openUart()
   


   


