import adafruit_sht31d
import board
import time
import csv
import os
import pandas as pd
import datetime
import json
import logging
import subprocess

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='/home/case/CASE_sensor_network/rpi_zero_sensor/sht31d.log',format='%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)

with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
    config = json.load(f)

with open("/home/case/CASE_sensor_network/rpi_zero_sensor/calibration.json") as f:
    calibration = json.load(f)

deviceNum = config["sensor"]["number"]
offset = calibration['offsetC'][deviceNum]
freq = int(config["sensor"]["frequency_seconds"])

#readings = 10

i2c = board.I2C() # this also works
sensor = adafruit_sht31d.SHT31D(i2c)

sensor.mode = adafruit_sht31d.MODE_SINGLE

def getUpdate()->None:
    result = subprocess.run(
            ['sudo','git','pull'],
            cwd='/home/case/CASE_sensor_network',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    logging.debug(result)

    if not 'Already up to date' in result.stdout:
        logging.info('Pulled update... rebooting now')
        os.system('sudo reboot')
    else:
        logging.debug('Already up to date :)')

    return None

# convert celcius to farenheit
def cToF(c):
	return c * (9/5) + 32

def main():
	tempC_list = []
	humidity_list = []
	tempC_offset_list = []

	startTime = 0

	count = 0
	while True:

		# check for update once an hour
		if count % 6 == 0:
			try:
				getUpdate()
			except Exception as e:
				logging.error(f'Error updating: {e}')
		count = count + 1

		#for r in range(readings):
		tempC_list.append(sensor.temperature)
		humidity_list.append(sensor.relative_humidity)
		tempC_offset_list.append(sensor.temperature + offset)

		#collect data every 5 minutes
		if time.time() - freq > startTime:
			startTime = time.time()
			logging.debug(f'loop start: {startTime}')

			tempC = sum(tempC_list)/len(tempC_list)
			tempC_offset = sum(tempC_offset_list)/len(tempC_offset_list)
			humidity = sum(humidity_list)/len(humidity_list)

			tempC_list = []
			humidity_list = []
			tempC_offset_list = []

			tempF = cToF(tempC)

			newDF = pd.DataFrame(data={
				"datetime" : [datetime.datetime.now()],
				"tempC": tempC,
				"tempC_offset": tempC_offset,
				"tempF": tempF,
				"humidityP": humidity})

			#print(newDF)
			logging.debug(newDF)

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
				logging.error(e)
				newDF.to_csv(fileName, sep=',',index=False)

		time.sleep(10)

if __name__ == "__main__":
	main()
