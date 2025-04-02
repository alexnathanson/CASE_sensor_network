import adafruit_sht31d
import board

i2c = board.I2C()

sensor = adafruit_sht31d.SHT31D(i2c)


sensor.mode = adafruit_sht31d.MODE_SINGLE

#sensor.mode = adafruit_sht31d.MODE_PERIODIC
#sensor.frequency = adafruit_sht31d.FREQUENCY_2

print(sensor.temperature)
print(sensor.relative_humidity)
