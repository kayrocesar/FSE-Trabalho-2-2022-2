import smbus2
import bme280


data=None
bus= None
address = 0x76
calibration_params=None

def init_i2c():
        global data, bus, calibration_params,address
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)
        

def readAmbientTemperature():
        global data, bus, calibration_params,address
        data = bme280.sample(bus, address, calibration_params)
        print("Temperatura ambiente: ",data.temperature)
        return data.temperature
