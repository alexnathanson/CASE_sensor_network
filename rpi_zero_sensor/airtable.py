import os
import datetime
import json
from dotenv import load_dotenv
import asyncio
import logging
import requests
from typing import Any, Dict, Optional, List
#from kasa import Discover, Credentials


# ------------------ Config ------------------ #
logging.basicConfig(level=logging.DEBUG)
#LOG_FILENAME = "kasa_log.log"

load_dotenv()
key = os.getenv('AIRTABLE')
if not key:
    logger.error("Missing AIRTABLE in environment.")
    raise EnvironmentError("Missing Kasa credentials")

# if true collect Kasa data
includeKasa = True
un = os.getenv('KASA_UN')
pw = os.getenv('KASA_PW')
if not un or not pw:
    logger.error("Missing KASA_UN or KASA_PW in environment.")
    raise EnvironmentError("Missing Kasa credentials")

try:
    with open("/home/case/CASE_sensor_network/rpi_zero_sensor/config.json") as f:
        config = json.load(f)

    deviceNum = config["sensor"]["number"]
except Exception as e:
    logging.error(e)

# mode: 1 = only individual data; 8 = all data
MODE = 8

FREQ_SECONDS = 60 * 60

# ------------------ Airtable Class ------------------ #
class Airtable():
    def __init__(self, key:str, name:str=''):
        self.key = key
        self.url = 'https://api.airtable.com/v0/appWyfKF1xclZ6OtH/'
        self.table = 'live'
        self.IDs = []
        self.names=[]


    async def getRecordID(self,name:List)-> List:
        IDlist = []
        for n in name:
            logging.debug(name)
            try:
                # get list of records filtered by name

                mURL = f'{self.url}{self.table}?maxRecords=3&view=Grid%20view&filterByFormula=name%3D%22{n}%22' #filter results by name column
                res = await self.send_secure_get_request(mURL)
                logging.debug(res)

                # pull the id for the first record
                recordID = res['records'][0]['id']
                IDlist.append(recordID)
                logging.debug(recordID)
            except Exception as e:
                logging.error(e)

        return IDlist

    async def updateSingle(self, name:str, recordID:str,data):
        logging.debug(name)
        try:
            # # get list of records filtered by name

            # mURL = f'{self.url}{self.table}?maxRecords=3&view=Grid%20view&filterByFormula=name%3D%22{name}%22' #filter results by name column
            # res = await self.send_secure_get_request(mURL)
            # logging.debug(res)

            # # pull the id for the first record
            # recordID = res['records'][0]['id']
            # logging.debug(recordID)

            if 'kasa' in name:
                logging.debug(f'{name}!')
                # patch record - columns not included are not changed
                pData={"records": [{
                    "id": str(recordID),
                    "fields": {
                        "name": str(f"{name}"),
                        "datetime":str(data['datetime']),
                        "power": str(data[f"{name}_W"])
                        }
                    }]}
            elif 'sensor' in name:
                logging.debug(f'{name}!')

                # patch record - columns not included are not changed
                pData={"records": [{
                    "id": str(recordID),
                    "fields": {
                        "name": str(name),
                        "datetime":str(data['datetime']),
                        "humidityP": str(data["humidityP"]),
                        "tempC": str(data["tempC"]),
                        "tempF": str(data["tempF"])
                        }
                    }]}

            logging.debug(pData)

            try:

                patch_status = 0
                while patch_status < 3:
                    # note that patch leaves unchanged data in place, while a post would delete old data in the record even if not being updated
                    r = await self.send_patch_request(f'{self.url}{self.table}',pData)
                    if r != False:
                        break
                    await asyncio.sleep(1+patch_status)
                    patch_status += 1
                logging.debug(r)
            except Exception as e:
                logging.error(f'Exception with patching Airtable: {e}')
        except Exception as e:
            logging.error(f'Exception with getting Airtable records: {e}')

    # updates up to 10 records at once
    # https://airtable.com/developers/web/api/update-multiple-records
    async def updateBatch(self, names:List, recordIDs:List,data:List):
        logging.debug(names)

        records = []
        for n in range(len(names)):
            try:
                if 'kasa' in names[n]:
                    logging.debug(f'{names[n]}!')
                    # patch record - columns not included are not changed
                    records.append({
                        "id": str(recordIDs[n]),
                        "fields": {
                            "name": str(f"{names[n]}"),
                            "datetime":str(data[n]['datetime']),
                            "power": str(data[n][f"{names[n]}_W"])
                            }
                        })
                elif 'sensor' in names[n]:
                    logging.debug(f'{names[n]}!')

                    # patch record - columns not included are not changed
                    records.append({
                        "id": str(recordIDs[n]),
                        "fields": {
                            "name": str(names[n]),
                            "datetime":str(data[n]['datetime']),
                            "humidityP": str(data[n]["humidityP"]),
                            "tempC": str(data[n]["tempC"]),
                            "tempF": str(data[n]["tempF"])
                            }
                        })
            except Exception as e:
                logging.error(f'Exception while formatting sensor data: {e}')

            pData={"records": records}

            logging.debug(pData)

            try:

                patch_status = 0
                while patch_status < 3:
                    # note that patch leaves unchanged data in place, while a post would delete old data in the record even if not being updated
                    r = await self.send_patch_request(f'{self.url}{self.table}',pData)
                    if r != False:
                        break
                    await asyncio.sleep(1+patch_status)
                    patch_status += 1
                logging.debug(r)
            except Exception as e:
                logging.error(f'Exception while patching Airtable: {e}')

    async def send_secure_get_request(self, url:str,type:str='json',timeout=2) -> Any:
        """Send GET request to the IP."""
        try:
            headers = {"Content-Type": "application/json; charset=utf-8"}

            if self.key != '':
                headers = {"Authorization": f"Bearer {self.key}"}

            response = requests.get(url, headers=headers, timeout=timeout)
            if type == 'json':
                return response.json()
            elif type == 'text':
                return (response.text, response.status_code)
            else:
                return response.status_code
        except requests.Timeout as e:
            return e
        except Exception as e:
            return e

    async def send_patch_request(self, url:str, data:Dict={},timeout=1):

        headers = {"Content-Type": "application/json; charset=utf-8"}

        if self.key != '':
            headers = {"Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {self.key}"}

        response = requests.patch(url, headers=headers, json=data)

        if response.ok:
            return response.json()
        else:
            logging.warning(f'{response.status_code}: {response.text}')
            return False

async def send_get_request(url,type:str,timeout=1) -> Any:
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
                asyncio.sleep(1)

    return res

async def main():
    AT = Airtable(key)

    # get record IDs once at start to minimize API calls
    if MODE == 1:
        AT.names = [f'sensor{deviceNum}']
    else:
        for n in range(8):
            AT.names.append(f'sensor{n+1}')

        if includeKasa:
            AT.names.append('kasa')

        logging.debug(AT.names)
    AT.IDs = await AT.getRecordID(AT.names)
    logging.info(AT.IDs)

    while True:
        now = []
        # get own data
        if MODE == 1:

            url = f"http://{localhost}:5000/api/data?date=now"
            now.append(await send_get_request(url,'json'))

            try:
                await AT.updateSingle(AT.names[0],AT.IDs[0],now[0])
            except Exception as e:
                logging.error(e)

        # get everyone elses data
        else:
            for n in range(8):
                url = f"http://pi{n+1}.local:5000/api/data?date=now"
                now.append(await send_get_request(url,'json'))

                #now.append(await getSensorData(f'pi{n+1}.local'))

            if includeKasa:
                url = f"http://kasa.local:5000/api/data?date=now"
                now.append(await send_get_request(url,'json'))

            print(now)
            # try:
            #     await AT.updateBatch(AT.names,AT.IDs,now)
            # except Exception as e:
            #     logging.error(e)

        logging.debug(f'No exceptions, sleeping for {FREQ_SECONDS/60} minutes.')
        await asyncio.sleep(FREQ_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Main loop crashed: {e}")
