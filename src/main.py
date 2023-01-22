import signal  
import time  
from uart import *
from gpio import *
from pid import *
from sensorBME280 import *
from threading import Thread
import time

p = None

def exit_handler(signal, frame):

   print('\nSignal ' , signal , 'recebido\nEncerrando..........')
   sendSystemStateSignal(0) 
   sendFunctioningStateSignal(0)
   turn_off_res_vent()
   close_uart()
   exit(1)

# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, exit_handler)
 

def start():

      init_uart() 
      initWipi() 
      init_i2c() 
      global p
      p= PID()
       



if __name__ == "__main__":
      start()
     
      
      #sendSystemStateSignal(1) 
      #sendFunctioningStateSignal(1)

      #with open("log", "a+") as f:
      # here, position is already at the end
      #f.write("stuff to append")

      while True:
               int_temp = readInternalTemperature()    #ler temp interna
               ref_temp = readReferenceTemperature()   #ler temp de referencia
               amb_temp=readAmbientTemperature()    #ler temp ambiente do sensor
               send_ambient_temp(amb_temp)  #enviar temperatura ambiente


               p.pid_update_ref(ref_temp) #atualizar temp de referencia

               control_sig= (p.pid_control(int_temp)) #receber calculo do pid no sinal de controle

               send_sig_control(control_sig) #enviar sinal de controle
               
      
               control_res_vent(control_sig) # controlar acionamento de resistencia e ventoinha
            
               
   

   


   


