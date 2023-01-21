import serial
import time
from crc16 import *
import struct





matricula = [7,4,2,6]
uartserial=-1


def openUart():
                uport = '/dev/serial0'
                ubaudrate = 9600
                global uartserial 
                uartserial = serial.Serial(uport, ubaudrate)
                if (uartserial.isOpen()):
                    print('Porta aberta, conexao realizada com sucesso')
                else:
                    print('Porta fechada, conexao nao realizada')
                
                    
def closeUart():
                global uartserial
                uartserial.close()
                print('Porta desconectada')

def send(comando, matricula, value, tamanho, ):
                
                    m1 = comando + bytes(matricula) + value
                    m2 = calcula_CRC(m1, tamanho).to_bytes(2, 'little')
                    msg = m1 + m2
                    global uartserial
                    uartserial.write(msg)
                    # print('Mensagem enviada: {}'.format(msg))
        

def receive():
                    time.sleep(0.2)
                    global uartserial
                    buffer = uartserial.read(9)
                    buffer_tam = len(buffer)

                    if buffer_tam == 9:
                        data = buffer[3:7]
                        crc16_recebido = buffer[7:9]
                        crc16_calculado = calcula_CRC(buffer[0:7], 7).to_bytes(2, 'little')

                        if crc16_recebido == crc16_calculado:
                            #print('Mensagem recebida: {}'.format(buffer))
                            return data
                        else:
                            #print('Mensagem recebida: {}'.format(buffer))
                            print('CRC16 invalido')
                            return None
                    else:
                        #print('Mensagem recebida: {}'.format(buffer))
                        print('Mensagem no formato incorreto, tamanho: {}'.format(buffer_tam))
                        return None

def readInternalTemperature():
                command = b'\x01\x23\xc1'

                send(command, matricula, b'', 7)
                data = receive()

                if data is not None:
                    temp=treatment_temp_int(data)
                return temp

def treatment_temp_int(bytes):
                temp = struct.unpack('f', bytes)[0]
                print('Temperatura Interna: ', temp)
                return temp

def readReferenceTemperature():
                command = b'\x01\x23\xc2'

                send(command, matricula, b'', 7)
                data = receive()

                if data is not None:
                    temp=treatment_temp_ref(data)
                return temp

def treatment_temp_ref(bytes):
                temp = struct.unpack('f', bytes)[0]
                print('Temperatura de Referencia: ', temp)
                return temp

def send_sig_control(pid):
                command = b'\x01\x23\xd1'
                if pid is not None:
                    value = (round(pid)).to_bytes(4, 'little', signed=True)
                    send(command, matricula, value, 11)
                

                
             
                    


        