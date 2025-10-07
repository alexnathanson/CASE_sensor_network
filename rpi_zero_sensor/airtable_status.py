import os
import datetime
import json
from dotenv import load_dotenv
import asyncio
import logging
import requests
from typing import Any, Dict, Optional, List
from airtable import Airtable

# ------------------ Config ------------------ #
#logging.basicConfig(level=logging.INFO)
logDT = datetime.datetime.now().strftime("%Y-%m-%d")
logging.basicConfig(filename=f'/home/case/CASE_sensor_network/rpi_zero_sensor/logs/airtable_status_{logDT}.log',format='%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

#LOG_FILENAME = "kasa_log.log"

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
#MODE = 8

FREQ_SECONDS = 60 * 60 * 6 #updates every 6 hours


async def send_get_request(url,type:str,backoff:int=1,timeout:int=1) -> Any:
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
    AT = Airtable(key,'status')

    # for n in range(8):
    #     AT.names.append(f'sensor{n+1}')


    # AT.names.append('kasa')

    # logging.debug(AT.names)

    # try:
    #     AT.IDs = await AT.getRecordID(AT.names)
    #     logging.debug(AT.IDs)
    # except Exception as e:
    #     logging.error(f'Error getting airtable IDs: {e}')

    # get record IDs
    for n in range(8):
        #AT.names.append(f'sensor{n+1}')
        AT.sensors[f'sensor{n+1}']={"id":"","data":""}

    AT.sensors['kasa']={"id":"","data":""}

    logging.debug(AT.sensors)

    AT.names = list(AT.sensors.keys())

    try:
        await AT.getRecordID(AT.names)
        logging.debug(AT.sensors)
    except Exception as e:
        logging.error(f'Error getting airtable IDs: {e}')


    while True:
        logging.debug('loop!')

        #now = []

        for n in range(8):
            url = f"http://pi{n+1}.local:5000/api/health"
            AT.sensors[AT.names[n]]['data'] = await send_get_request(url,'json')

            # if no results, wait 5 seconds and try again in a few minutes
            if AT.sensors[AT.names[n]]['data'] == {}:
                await asyncio.sleep(5)
                AT.sensors[AT.names[n]]['data'] = await send_get_request(url,'json',3)

            #now.append(health)

        url = f"http://localhost:5000/api/health"
        AT.sensors[AT.names[n]]['data'] =await send_get_request(url,'json')
        # if no results, wait 5 seconds and try again in a few minutes
        if AT.sensors[AT.names[n]]['data'] == {}:
            await asyncio.sleep(5)
            AT.sensors[AT.names[n]]['data'] = await send_get_request(url,'json',3)

        #now.append(health)

        logging.debug(AT.sensors)

        try:
            await AT.updateBatch(AT.names,AT.sensors)
        except Exception as e:
            logging.error(e)

        logging.debug(f'Sleeping for {FREQ_SECONDS/60/60} hours.')
        await asyncio.sleep(FREQ_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Main loop crashed: {e}")
