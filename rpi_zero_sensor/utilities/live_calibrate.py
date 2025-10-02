# This is intended to be used only in a situation where all sensors
# are in the same exact controlled environment

# run this for the duration of the callibration time period
# if calibrating based on historical data use a different method

import requests
import pandas as pd
import logging
import asyncio
from io import StringIO
import time

async def send_get_request(url,timeout=1):
    max_tries = 3
    for attempt in range(max_tries):
        logging.debug(f'Attempt #{attempt+1}')
        try:
            response = requests.get(f"{url}", timeout=timeout)
            response.raise_for_status()
            return response.json()
            # #res = StringIO(response.text)
            # res_df = pd.DateFrame(res.json)#read_csv(res, parse_dates=['datetime'])
            # res_df["datetime"] = pd.to_datetime(res_df["datetime"], utc=True, errors="coerce")
            # return res_df
        except Exception as e:
            logging.error(f'{e}')
            await asyncio.sleep(1)

    logging.debug('FAILED!!!')
    return None

async def main():

    names = []
    data = []
    for n in range(8):
        names.append(f'sensor{n+1}')
        data.append([])

    logging.debug(names)

    while True:
        #1 get NOW data
        now = []
        for n in range(8):
            try:
                url = f"http://pi{n+1}.local:5000/api/data?date=now"
                res = await send_get_request(url)
                tC = res['tempC']
            except:
                tC = False
            print(tC)
            now.append(tC)

            #data[n].append(res['tempC'])

        avg = sum(now)/len(now)

        offsets = []
        for n in now:
            if n:
                offsets.append(avg - n)

        print(offsets)
        time.sleep(60 * 5) #sleep for 5 minutes

        #3 average offsets

        #4 save callibration report

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Main loop crashed: {e}")

