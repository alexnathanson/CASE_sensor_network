import requests
import asyncio
from typing import Any, Dict, Optional, List
import json
import logging

logging.basicConfig(level=logging.INFO)

class Airtable():
    def __init__(self, key:str, name:str=''):
        self.key = key
        self.url = 'https://api.airtable.com/v0/appWyfKF1xclZ6OtH/'
        self.table = 'live'

    async def update(self, name:str, data):
        logging.debug(name)
        try:
            # get list of records filtered by name

            mURL = f'{self.url}{self.table}?maxRecords=3&view=Grid%20view&filterByFormula=name%3D%22{name}%22' #filter results by name column
            res = await self.send_secure_get_request(mURL)
            logging.debug(res)

            # pull the id for the first record
            recordID = res['records'][0]['id']
            logging.debug(recordID)

            if 'kasa' in name:
                logging.debug('kasa device!')
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
                # patch record - columns not included are not changed
                pData={"records": [{
                    "id": str(recordID),
                    "fields": {
                        "name": str(f"{name}"),
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