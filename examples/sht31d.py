# based on code from https://learn.adafruit.com/adafruit-sht31-d-temperature-and-humidity-sensor-breakout/python-circuitpython

import adafruit_sht31d
import board
import time

i2c = board.I2C() # this also works
sensor = adafruit_sht31d.SHT31D(i2c)


sensor.mode = adafruit_sht31d.MODE_SINGLE

#sensor.mode = adafruit_sht31d.MODE_PERIODIC
#sensor.frequency = adafruit_sht31d.FREQUENCY_2

# convert celcius to farenheit
def cToF(c):
	return c * (9/5) + 32

# print('Humidity: {0}%'.format(sensor.relative_humidity))
# print('Temperature: {0} C'.format(sensor.temperature))
# print('Temperature: {0} F'.format(cToF(sensor.temperature)))

while True:
    print(f"\nTemperature: {sensor.temperature} C")
    print(f"\nTemperature: {cToF(sensor.temperature)} F")
    print(f"Humidity: {sensor.relative_humidity} %")
    time.sleep(10)