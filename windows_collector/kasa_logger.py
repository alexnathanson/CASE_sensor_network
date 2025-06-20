import time
import csv
import os
import pandas as pd
import datetime
import json
from dotenv import load_dotenv
import asyncio
from kasa import Discover, Credentials
import logging
from Airtable import Airtable

# ------------------ Config ------------------ #
logging.basicConfig(level=logging.INFO)
#LOG_FILENAME = "kasa_log.log"

# ------------------ Environmental Variables ------------------ #
load_dotenv()
un = os.getenv('KASA_UN')
pw = os.getenv('KASA_PW')
if not un or not pw:
    logger.error("Missing KASA_UN or KASA_PW in environment.")
    raise EnvironmentError("Missing Kasa credentials")

key = os.getenv('AIRTABLE')

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

            await device.disconnect()
        except Exception as e:
            logging.error(e)

    return dataDF

def archiveCSV(data):
     # File path to save the CSV
    directory = r"archive/kasa"
    filename = 'kasa_' + str(datetime.date.today()) + '.csv'
    logging.debug(directory)
    logging.debug(filename)

    if data.empty:
        logging.warning("Received empty content. CSV file will not be saved.")
        return

    #check if directory exists
    os.makedirs(directory, exist_ok=True)

    #make full file path
    file_path = os.path.join(directory, filename)
    logging.debug(file_path)

    try:
        with open(file_path) as csvfile:
            df = pd.read_csv(file_path)
            df = pd.concat([df,data], ignore_index = True)
            df.to_csv(file_path, sep=',',index=False)
            print('Data written to existing CSV.')
    except Exception as e:
        logging.info('Failed to read CSV. Trying to write new CSV')
        try:
            data.to_csv(file_path, sep=',',index=False)
            logging.info('New CSV created.')
        except Exception as e:
            logging.error(f'Failed to write new CSV. {e}')

async def main():
    AT = Airtable(key)

    while True:
        power_data = await discoverAll()

        logging.debug(power_data)

        archiveCSV(power_data)

        for n in power_data.keys():
            if n != 'datetime':
                try:
                    await AT.update(n[:5],power_data.iloc[0])
                except Exception as e:
                    logging.error(e)

        #collect data every 5 minutes
        await asyncio.sleep(60 * 5) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Main loop crashed: {e}")