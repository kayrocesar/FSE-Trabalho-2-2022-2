import crc.crc16 as Crc16

def verify_crc(resp, crc_resp, size):
      crc_calc = Crc16.calc(resp, size-2).to_bytes(2,'little')
      if crc_calc == crc_resp:
            return 'Certo'
      else:
            print(f'Erro! \nCRC recebido: {crc_resp}\nCRC calculado: {crc_calc}')
            return f'ERRO-CRC'