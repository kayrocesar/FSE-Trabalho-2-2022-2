import signal   
import os
import time
import struct
import uart as UART 
import gpio as GPIO
import sensor_amb as BME
import write_log as LOG
import uart as UART
import ver_crc as VER_CRC
from pid import *



control_init = False



def exit_handler(signal, frame):

   print('\nSignal ' , signal , 'recebido\nEncerrando..........')
   UART.send(u,b'\xD3', 0)
   UART.send(u,b'\xD4', 0)
   UART.send(u,b'\xD5', 0)
   GPIO.turn_off_res_vent()
   UART.close_uart(u)
   exit(1)

# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, exit_handler)



def init_states_oven(u,p):

      reference_fix = False
      temp_fix = 0.0
      UART.send(u,b'\xD3', 0) #estado do sistema (Ligado = 1 / Desligado = 0)
      UART.send(u,b'\xD4', 0) #modo de controle(Dashboard = 0 / Curva/Terminal = 1) 
      UART.send(u,b'\xD5', 0) #funcionamento (Funcionando = 1 / Parado = 0)
      

      opc = -1
      while opc != 0 and opc != 1:
            os.system('clear')
            opc = int(input( 'Usar temperatura de referencia fixa? 0-Não 1-Sim  \n '))
      if opc == 1:
            temp_fix = float(input('\nValor da temperatura de referencia a ser fixada: '))
            reference_fix = True
      
      opc = -1
      while opc != 0 and opc != 1:
            os.system('clear')
            opc = int(input('Alterar valores das constantes Kp,Ki e Kd? 0-Não 1-Sim \n'))
            time.sleep(1)
            if opc == 1:
                  kp = float(input('Valor de Kp: '))
                  ki = float(input('Valor de Ki: '))
                  kd = float(input('Valor de Kd: '))
                  p.pid_config_consts(kp,ki,kd)
      return p, reference_fix, temp_fix

def init_all():
      uart_conf = UART.init_uart() 
      GPIO.initWipi() 
      BME.init_i2c() 
      p= PID()
      p, reference_fix, temp_ref_fix = init_states_oven(uart_conf,p)
      return uart_conf, p, reference_fix, temp_ref_fix


if __name__ == "__main__":

                  u, p, reference_fix, temp_ref_fix = init_all()
                  
                  while True:
                        amb_temp_data = BME.init_i2c()
                        UART.send_ambient_temp(u,amb_temp_data)
                        
                        print('Lendo comandos da dashboard')
            
                        dash = UART.req_uart(u,b'\xC3')
                        dash = str(hex(dash[3]))
                        #print(dash)
                        
                        if dash == '0xa1':
                              print('Ligando o Forno...Aguarde....')
                              UART.send(u,b'\xD3', 1)


                        elif dash == '0xa2':
                              print('Desligando o forno...Aguarde...')
                              UART.send(u,b'\xD3', 0)

                        elif dash == '0xa3':
                              print('Iniciando Aquecimento do Forno...Aguarde..')
                              control_init = True
                              UART.send(u,b'\xD5',1)

                        elif dash == '0xa4':
                              control_init = False
                              print('Cancelando funcionamento...')
                              UART.send(u,b'\xD5',0)
                              GPIO.turn_off_res_vent

                        elif dash == '0xa5':
                              print('Modo de Temperatura de Referência e Curva de Temperatura alternado...')
                              UART.send(u,b'\xD4', 1)

                       
                        if control_init == True:

                              print('Forno em funcionamento...Iniciando o controle de temperatura...')
                              amb_temp = float(amb_temp_data)
                              res = UART.req_uart(u, b'\xC1')   #solicitando temperatura interna
                              temp_int = UART.get_temperature(res) #armazenando temperatura
                             
                              if reference_fix == False:

                                    res = UART.req_uart(u, b'\xC2') #solicitando temperatura de referencia
                                    temp_ref = UART.get_temperature(res) #armazenando temperatura
                                    UART.send_ref_sig(u,b'\xD2',struct.pack('f', float(temp_ref))) #envia sinal de referencia da temperatura lida
                              else:
                                    UART.send_ref_sig(u,b'\xD2',struct.pack('f', temp_ref_fix)) #envia sinal de referencia da temperatura fixada se for o caso
                                    temp_ref=temp_ref_fix
                                    
                              p.pid_update_ref(temp_ref) #atualiza temp de referencia na funcao pid
                              ctrl_sig = int(p.pid_control(temp_int))
                              UART.send_ctrl_sig(u,b'\xD1',ctrl_sig)
                              
                              LOG.log_rec(temp_int,temp_ref,amb_temp, ctrl_sig)

                     
                              GPIO.control_res_vent(ctrl_sig) # controlar acionamento de resistencia e ventoinha - wiringpi
                              
             
                 
      
                  

                  
               
          


               
               
               
   

   


   


