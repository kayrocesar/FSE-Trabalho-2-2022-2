import signal  
import time  
from uart import *
from gpio import *
from pid import *
from sensorBME280 import amb_temp

def exit_handler(signal, frame):

   print('\nSignal ' , signal , 'recebido\nEncerrando..........')
   exit(1)

# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, exit_handler)
 






if __name__ == "__main__":
     
      openUart()
      initWipi()
      p = PID()
      

      #with open("log", "a+") as f:
      # here, position is already at the end
      #f.write("stuff to append")

      while True:
               time.sleep(2)
               int_temp = readInternalTemperature()
               ref_temp = readReferenceTemperature()
               p.pid_update_ref(int_temp)
               print(p.reference)
               control_sig= (p.pid_control(int_temp))
               print(control_sig)
               send_sig_control(control_sig)


                ## pid: se negativo -> ventoinha
               if(control_sig < 0):
                  print("Iniciando acionamento da ventoinha do forno...")
                  if control_sig > -40:
                     control_sig= 40
                  else:
                     control_sig=control_sig*(-1)
                  coolDown(control_sig)
                  heatUp(0)
               
               # pid: se positivo -> resistencia
               elif(control_sig > 0):
                  print("Iniciando acionamento da resistencia do forno...")
                  heatUp(control_sig)
                  coolDown(0)
               
               
               

               #sendSystemStateSignal(1)
              # sendFunctioningStateSignal(1)
         

               #print('pid f', pid)
              # envia_sinal_controle(pid)
               #d = amb_temp()
              # print(d)

   


   


