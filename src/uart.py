import serial

def init_uart():
      uart0_file= serial.Serial ("/dev/serial0", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)    
      if uart0_file == -1:
            print("UART nao iniciada! Erro.\n")
      else:
            print("UART foi inicializada com sucesso!\n")
      return uart0_file