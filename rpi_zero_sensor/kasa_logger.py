import time
import csv
import os
import datetime
import json
from dotenv import load_dotenv
import asyncio
from kasa import Discover, Credentials
import logging
import pandas as pd
import subprocess

# ------------------ Config ------------------ #
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='/home/case/CASE_sensor_network/rpi_zero_sensor/kasa.log',format='%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)

with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
    config = json.load(f)
freq = int(config["sensor"]["frequency_seconds"])

# ------------------ Environmental Variables ------------------ #
load_dotenv()
un = os.getenv('KASA_UN')
pw = os.getenv('KASA_PW')
if not un or not pw:
    logger.error("Missing KASA_UN or KASA_PW in environment.")
    raise EnvironmentError("Missing Kasa credentials")

# discover Kasa devices and collect power data
async def discoverAll():

    #discover all available devices
    devices = await Discover.discover(
        credentials=Credentials(un, pw),
        discovery_timeout=10
        )

    dataDF = pd.DataFrame(data={
        "datetime" : [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "kasa1_W": "",
        "kasa2_W": "",
        "kasa3_W": "",
        "kasa4_W": ""})

    logging.debug(len(devices))

    for ip, device in devices.items():
        try:
            await device.update()

            # print(f'{device.alias} ({device.mac}) at {device.host}')
            energy_module = device.modules.get("Energy")
            # print(f'Power: {energy_module.current_consumption}W') #this library is really dumb - they use the word current to describe live power in Watts, NOT amperage
            # print('')

            dataDF['kasa'+device.alias[4]+'_W']=energy_module.current_consumption
            logging.debug(energy_module.current_consumption)
            await device.disconnect()
        except Exception as e:
            logging.error(e)

    return dataDF

def getUpdate()->None:
    result = subprocess.run(
            ['sudo','git','pull'],
            cwd='/home/drux/demandResponse_UX_research',
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

async def main():

    count = 0
    while True:
        # check for update once an hour
        if count % 2==0:#(60/(freq/60)) == 0:
            getUpdate()
        count = count + 1

        power_data = await discoverAll()

        logging.debug(power_data)

        # create a new file daily to save data or append if the file already exists
        fileName = '/home/case/data/kasa' + '_'+str(datetime.date.today())+'.csv'

        try:
            with open(fileName) as csvfile:
                df = pd.read_csv(fileName)
                df = pd.concat([df,power_data], ignore_index = True)
                df.to_csv(fileName, sep=',',index=False)
                logging.debug('Data appended.')
        except Exception as e:
            logging.debug(f'Failed to append CSV... trying to write new CSV. {e}')
            try:
                power_data.to_csv(fileName, sep=',',index=False)
                logging.debug('New CSV created.')
            except Exception as e:
                logging.error(f'Failed to write new CSV. {e}')

        await asyncio.sleep(freq)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Main loop crashed: {e}")
