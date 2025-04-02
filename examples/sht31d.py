import adafruit_sht31d
import board

i2c = board.I2C()

sensor = adafruit_sht31d.SHT31D(i2c)


sensor.mode = adafruit_sht31d.MODE_SINGLE

#sensor.mode = adafruit_sht31d.MODE_PERIODIC
#sensor.frequency = adafruit_sht31d.FREQUENCY_2


def cToF(c):
	return c * (9/5) + 32
	
print('Humidity: {0}%'.format(sensor.relative_humidity))
print('Temperature: {0}C'.format(sensor.temperature))
print('Temperature: {0}C'.format(cToF(sensor.temperature)))
