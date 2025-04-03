import adafruit_sht31d
import board
import time
import csv
import os
import pandas as pd
import datetime
import json


with open("config.json") as f:
    config = json.load(f)

deviceNum = config["sensor"]["number"]

i2c = board.I2C() # this also works
sensor = adafruit_sht31d.SHT31D(i2c)

sensor.mode = adafruit_sht31d.MODE_SINGLE

# convert celcius to farenheit
def cToF(c):
	return c * (9/5) + 32

def main():

	while True:
		tempC = sensor.temperature
		tempF = cToF(sensor.temperature)
		humidity = sensor.relative_humidity

		# print(f"\nTemperature: {sensor.temperature:.2f} C")
		# print(f"Temperature: {cToF(sensor.temperature):.2f} F")
		# print(f"Humidity: {sensor.relative_humidity:.2f}%")
		
		newDF = pd.DataFrame(data={
			"datetime" : [datetime.datetime.now()],
			"tempC": tempC,
			"tempF": tempF,
			"humidityP": humidity})

		print(newDF)

		# create a new file daily to save data
		# or append if the file already exists
		fileName = 'data/sensor' + str(deviceNum) + '_'+str(datetime.date.today())+'.csv'

		try:
			with open(fileName) as csvfile:
				df = pd.read_csv(fileName)
				df = pd.concat([df,newDF], ignore_index = True)
				#df = df.append(newDF, ignore_index = True)
				df.to_csv(fileName, sep=',',index=False)
		except Exception as e:
			print(e)
			newDF.to_csv(fileName, sep=',',index=False)

		#collect data every 5 minutes
		time.sleep(60*5)

if __name__ == "__main__":
	main()