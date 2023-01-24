import time
import os
import logging
import csv



def log_rec(temp_int, temp_ref ,temp_amb,control_sig):

    content =  f'Temperatura Interna: {temp_int:.1f}°C Temperatura De Referencia: {temp_ref:.1f}°C Temperatura Ambiente: {temp_amb:.1f}°C Sinal de Controle: {control_sig}'
 

    row = [time.ctime() , content]    
    with open('logs/log.csv', 'a+') as file:
                w = csv.writer(file)
                w.writerow(row)

