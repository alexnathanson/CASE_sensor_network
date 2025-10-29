import os
import datetime
import json
from dotenv import load_dotenv
import asyncio
import logging
#from logging.handlers import RotatingFileHandler
import requests
from typing import Any, Dict, Optional, List
from airtable import Airtable

# ------------------ Config ------------------ #
#logging.basicConfig(level=logging.DEBUG)
logDT = datetime.datetime.now().strftime("%Y-%m-%d")
logging.basicConfig(filename=f'/home/case/CASE_sensor_network/rpi_zero_sensor/logs/airtable_live_{logDT}.log',format='%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)

load_dotenv()
key = os.getenv('AIRTABLE')
if not key:
    logger.error("Missing AIRTABLE in environment.")
    raise EnvironmentError("Missing Kasa credentials")

# if true collect Kasa data
#includeKasa = True

try:
    with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
        config = json.load(f)

    deviceNum = config["sensor"]["number"]
except Exception as e:
    logging.error(e)

# mode: 1 = only individual data; 8 = all data
MODE = 8

FREQ_SECONDS = 60 * 20 #updates every half an hour

async def send_get_request(url,type:str,backoff:int=1,timeout=1) -> Any:
    """Send GET request to the IP."""

    # get own data
    max_tries = 3
    for attempt in range(max_tries):
        logging.debug(f'Attempt #{attempt+1}')
        try:
            response = requests.get(f"{url}", timeout=timeout)
            response.raise_for_status()
            if type == 'json':
                res = response.json()
            elif type == 'text':
                res = response.text
            else:
                res = response.status_code
            break
        except Exception as e:
            logging.error(f'{e}')
            if attempt == max_tries-1: # try up to 3 times
                res = {}
                logging.debug('FAILED!!!')
            else:
                logging.debug('SLEEEEEEEEEEEEEEEEEPING')
                await asyncio.sleep(1+(int(backoff)* int(attempt)))

    return res

async def main():
    AT = Airtable(key,'live')

    # get names
    for n in range(8):
        AT.sensors[f'sensor{n+1}']={"id":"","data":""}

    AT.sensors['kasa']={"id":"","data":""}

    logging.debug(AT.sensors)

    AT.names = list(AT.sensors.keys())

    while True:

        logging.debug('Starting loop!')

        # get record IDs
        try:
            await AT.getRecordID(AT.names)
            logging.debug(AT.sensors)
        except Exception as e:
            logging.error(f'Error getting airtable IDs: {e}')

        # sensor data
        for n in range(8):
            url = f"http://pi{n+1}.local:5000/api/data?date=now"
            AT.sensors[AT.names[n]]['data']= await send_get_request(url,'json')

            # if no results, wait 5 seconds and try again in a few minutes
            if AT.sensors[AT.names[n]]['data'] == {}:
                await asyncio.sleep(5)
                AT.sensors[AT.names[n]]['data'] = await send_get_request(url,'json',3)


        # kasa data
        url = f"http://kasa.local:5000/api/data?date=now"
        AT.sensors['kasa']['data']=await send_get_request(url,'json')

        # if no results, wait 5 seconds and try again in a few minutes
        if AT.sensors['kasa']['data'] == {}:
            await asyncio.sleep(5)
            AT.sensors['kasa']['data'] = await send_get_request(url,'json',3)


        logging.debug(AT.sensors)
        try:
            await AT.updateBatch(AT.names,AT.sensors)
        except Exception as e:
            logging.error(e)

        logging.debug(f'Sleeping for {FREQ_SECONDS/60} minutes.')
        await asyncio.sleep(FREQ_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Main loop crashed: {e}")
