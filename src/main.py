import signal  
import time  
import uart as UART 
import gpio as GPIO
from pid import *
import sensorBME280 as BME
from threading import Thread
import write_log as LOG
import time

p = None

def exit_handler(signal, frame):

   print('\nSignal ' , signal , 'recebido\nEncerrando..........')
   UART.sendSystemStateSignal(0) 
   UART.sendFunctioningStateSignal(0)
   UART.turn_off_res_vent()
   UART.close_uart()
   exit(1)

# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, exit_handler)
 

def init_all():

      UART.init_uart() 
      GPIO.initWipi() 
      BME.init_i2c() 
      global p
      p= PID()
   
    

def temps():
               int_temp = UART.readInternalTemperature()    #ler temp interna
               ref_temp = UART.readReferenceTemperature()   #ler temp de referencia
               amb_temp= BME.readAmbientTemperature()    #ler temp ambiente do sensor
               UART.send_ambient_temp(amb_temp)  #enviar temperatura ambiente


               p.pid_update_ref(ref_temp) #atualizar temp de referencia

               control_sig= (p.pid_control(int_temp)) #receber calculo do pid no sinal de controle

               UART.send_sig_control(control_sig) #enviar sinal de controle

               LOG.log_rec(int_temp,ref_temp,amb_temp) # registrar no log
               
      
               GPIO.control_res_vent(control_sig) # controlar acionamento de resistencia e ventoinha - wiringpi


if __name__ == "__main__":

                  init_all()
                 
      
                  while True:
                        command = b'\x01\x23\xc3'
                        data =   UART.send_receive(command, UART.matricula, b'', 7)
                        if (data!=None):
                              data = str(hex(data[0]))
                              print('data', data) 
                        if data == '0xa1':
                              print("Ligando forno...Por favor Aguarde...")
                              UART.sendSystemStateSignal(1)

                        elif data == '0xa2': 
                              print("Desligando forno...Por favor Aguarde..")
                              UART.sendSystemStateSignal(0)

                        elif data == '0xa3': 
                              print("Iniciando aquecimento...Por favor Aguarde...") 
                              UART.sendFunctioningStateSignal(1)
                  

                        elif data == '0xa4': 
                              UART.sendFunctioningStateSignal(0)
                              print("Cancelando processo de aquecimento...Por favor Aguarde...") 

                        elif data == '0xa5': 
                              pass
                        temps()
                        time.sleep(1)

                  
               
          


               
               
               
   

   


   


