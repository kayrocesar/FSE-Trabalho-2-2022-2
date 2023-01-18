import serial
import time




def openUart():
        uport = '/dev/serial0'
        ubaudrate = 9600
        userial = serial.Serial(uport, ubaudrate)

        if (userial.isOpen()):
            print('Porta aberta, conexao realizada com sucesso')
        else:
            print('Porta fechada, conexao nao realizada')
            
def desconecta():
        userial.close()
        print('Porta desconectada')