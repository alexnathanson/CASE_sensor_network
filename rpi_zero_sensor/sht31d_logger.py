import adafruit_sht31d
import board
import time
import csv
import os
import pandas as pd
import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)

with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
    config = json.load(f)

deviceNum = config["sensor"]["number"]
freq = int(config["sensor"]["frequency_seconds"])

readings = 10

i2c = board.I2C() # this also works
sensor = adafruit_sht31d.SHT31D(i2c)

sensor.mode = adafruit_sht31d.MODE_SINGLE

# convert celcius to farenheit
def cToF(c):
	return c * (9/5) + 32

def main():
	tempC_list = []
	humidity_list = []

	startTime = 0
	while True:

		#for r in range(readings):
		tempC_list.append(sensor.temperature)
		humidity_list.append(sensor.relative_humidity)

		#collect data every 5 minutes
		if time.time() - freq > startTime:
			startTime = time.time()
			logging.debug(startTime)

			tempC = sum(tempC_list)/len(tempC_list)
			humidity = sum(humidity_list)/len(humidity_list)

			tempC_list = []
			humidity_list = []

			tempF = cToF(tempC)

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

		time.sleep(1)

if __name__ == "__main__":
	main()
