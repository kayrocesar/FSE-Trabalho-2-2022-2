import serial
import time
from crc16 import calc_CRC
import struct





matricula = [7,4,2,6]
ser=-1


def init_uart():
                uport = '/dev/serial0'
                ubaudrate = 9600
                global ser 
                ser = serial.Serial(uport, ubaudrate)
                if (ser.isOpen()):
                    print('Porta aberta, conexao realizada com sucesso')
                else:
                    print('Porta fechada, conexao nao realizada')
                
                    
def close_uart():
                global ser
                ser.close()
                print('Porta desconectada........')

def send(comando, matricula, value, tamanho):
                
                    msg1 = comando + bytes(matricula) + value
                    msg2 = calc_CRC(msg1, tamanho).to_bytes(2, 'little')
                    msg = msg1 + msg2
                    global ser
                    ser.write(msg)
def receive():
                    time.sleep(0.2)
                    global ser
                    buffer = ser.read(9)
                    buffer_tam = len(buffer)

                    if buffer_tam == 9:
                        data = buffer[3:7]
                        crc16_received = buffer[7:9]
                        calculated_crc16 = calc_CRC(buffer[0:7], 7).to_bytes(2, 'little')

                        if crc16_received == calculated_crc16:
                            return data
                        else:
                            print('CRC16 invalido')
                            receive()
                    else:
                        print('Mensagem no formato incorreto, tamanho: {}'.format(buffer_tam))
                        receive()

def readInternalTemperature():
                command = b'\x01\x23\xc1'

                send(command, matricula, b'', 7)
                data = receive()

                if data is not None:
                    temp_Internal = struct.unpack('f', data)[0]
                    print('Temperatura Interna: ', temp_Internal)
                return temp_Internal



def readReferenceTemperature():
                command = b'\x01\x23\xc2'

                send(command, matricula, b'', 7)
                data = receive()
                if data is not None:
                    temp_Reference = struct.unpack('f', data)[0]
                    print('Temperatura de Referencia: ', temp_Reference)
                return temp_Reference

def requestUserCommand():
        command = b'\x01\x23\xc3'
        send(command, matricula, b'', 7)
        data = receive()
        #text= data.hex()
        #print(text)
        opc = int.from_bytes(data, 'little') ## convertendo para inteiro
        #print('botao', b) 
        if opc == 161: #0xa1 em decimal - liga forno
           print("Ligando forno...Por favor Aguarde...")
           sendSystemStateSignal(1)

        elif opc == 162: #0xa2 em decimal - Desliga forno
           print("Desligando forno...Por favor Aguarde..")
           sendSystemStateSignal(0)

        elif opc == 163: #0xa3 em decimal - Inicia aquecimento
           print("Iniciando aquecimento...Por favor Aguarde...") 
           sendFunctioningStateSignal(1)
 

        elif opc == 164: #0xa4 em decimal - Cancela processo
            sendFunctioningStateSignal(0)
            print("Cancelando processo de aquecimento...Por favor Aguarde...") 

        elif opc == 165: #0xa5 em decimal - Alterna temp ref e curva
           pass
        
def send_sig_control(pid):
                command = b'\x01\x23\xd1'
                if pid is not None:
                    value = (round(pid)).to_bytes(4, 'little', signed=True)
                    send(command, matricula, value, 11)
        
def send_sig_ref(temp_ref):
        command = b'\x01\x23\xd2'
        value =struct.pack('f', temp_ref)
        send(command, matricula, value, 11)
                
def sendSystemStateSignal(state):
        command = b'\x01\x23\xd3'
        if state == 1:  # on
            send(command, matricula, b'\x01', 8)
        elif state == 0: # off
            send(command, matricula, b'\x00', 8)
        
        #data = receive()

def sendFunctioningStateSignal(state):
        command = b'\x01\x23\xd5'
        if state == 1:  # on
            send(command, matricula, b'\x01', 8)
        elif state == 0: # off
            send(command, matricula, b'\x00', 8)
       # data = receive()
        
def send_ambient_temp(temp_amb):
        
        command = b'\x01\x23\xd6'
        value =struct.pack('f', temp_amb)
        send(command, matricula, value, 11)
        #data = receive()
    

        



    


       


                
             
                    


        