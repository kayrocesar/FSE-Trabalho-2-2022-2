import serial
import crc16
import ver_crc as VER_CRC
import time

def init_uart():
      uart0_file= serial.Serial ("/dev/serial0", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)    
      if uart0_file == -1:
            print("UART nao iniciada! Erro.\n")
      else:
            print("UART foi inicializada com sucesso!\n")
      return uart0_file

def req_uart(U,command):

      crc = crc16.calc(b'\x01'+b'\x23'+command+b'\x07\x04\x02\x06',7).to_bytes(2,'little')
      msg = b'\x01'+b'\x23'+command+b'\x07\x04\x02\x06'+crc
      U.write(msg) 
      response = U.read(9) 

      if(VER_CRC.verify_crc(response, response[-2:], 9) == 'ERRO-CRC'):
            print('Calculo CRC está errado... Tentando novamente')
            req_uart(U,command)
      
      time.sleep(0.5)
      return response