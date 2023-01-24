import serial
import crc16 as Crc16
import ver_crc as VER_CRC
import time
import struct

def init_uart():
      uart0_file= serial.Serial ("/dev/serial0", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)    
      if uart0_file == -1:
            print("UART nao iniciada! Erro.\n")
      else:
            print("UART foi inicializada com sucesso!\n")
      return uart0_file

def req_uart(U,command):

      crc = Crc16.calc(b'\x01'+b'\x23'+command+b'\x07\x04\x02\x06',7).to_bytes(2,'little')
      msg = b'\x01'+b'\x23'+command+b'\x07\x04\x02\x06'+crc
      U.write(msg) 
      response = U.read(9) 

      if(VER_CRC.verify_crc(response, response[-2:], 9) == 'ERRO-CRC'):
            print('Calculo CRC está errado... Tentando novamente')
            req_uart(U,command)
      
      time.sleep(0.5)
      return response
      
def send(U, command, value):

      if value == 0:
            crc = Crc16.calc(b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+b'\x00',8).to_bytes(2,'little')
            msg = b'\x01'+b'\x16'+command +b'\x07\x04\x02\x06'+ b'\x00'+crc
      elif value == 1:
            crc = Crc16.calc(b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+ b'\x01',8).to_bytes(2,'little')
            msg = b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+ b'\x01'+crc

      U.write(msg) 
      response = U.read(9) 

      if(VER_CRC.verify_crc(response, response[-2:], 9) == 'ERRO-CRC'):
         print('Calculo CRC está errado... Tentando novamente')
         send(U, command, value)

def get_temperature(response):
        temp_by = response[3:7]
        temperature_ = struct.unpack('f', temp_by)
        return temperature_[0]

def send_ref_sig(U, command, reference_signal):

      
      crc = Crc16.calc(b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+reference_signal,11).to_bytes(2,'little')
      msg = b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+reference_signal+crc
      U.write(msg) 

def send_ctrl_sig(U, command, crtl_sig):
      ctrl_signal_by = crtl_sig.to_bytes(4,'little',signed=True)
      crc = Crc16.calc(b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+ctrl_signal_by,11).to_bytes(2,'little')
      msg = b'\x01'+b'\x16'+command+b'\x07\x04\x02\x06'+ctrl_signal_by+crc
      U.write(msg) 

def send_ambient_temp(U,temp_amb):
      data_temp = struct.pack('f', temp_amb)
      crc = Crc16.calc(b'\x01'+b'\x16'+b'\xD6'+b'\x07\x04\x02\x06'+data_temp,11).to_bytes(2,'little')
      msg = b'\x01'+b'\x16'+b'\xD6'+b'\x07\x04\x02\x06'+data_temp+crc
      U.write(msg) 