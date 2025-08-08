# This is intended to be used only in a situation where all sensors
# are in the same exact controlled environment

# unfinished and untested!

import requests
import pandas as df
import logging
import asyncio
from io import StringIO

# update date as needed
dataDate = '2025-07-17'

async def send_get_request(url,timeout=1) -> Any:
    max_tries = 3
    for attempt in range(max_tries):
        logging.debug(f'Attempt #{attempt+1}')
        try:
            response = requests.get(f"{url}", timeout=timeout)
            response.raise_for_status()
            #res = response.text()
            res = StringIO(response.text)
            res_df = pd.read_csv(res, parse_dates=['datetime'])
            return res_df
        except Exception as e:
            logging.error(f'{e}')
            await asyncio.sleep(1)

    logging.debug('FAILED!!!')
    return None

async def main():

    names = []
    for n in range(8):
        names.append(f'sensor{n+1}')

    logging.debug(names)

    files = []

    # TO DO - DONT DO IT THIS WAY!!! - COLLECT 'now' over an hour-ish

    #1 pull the files for a specific date from all sensors
    for n in range(8):
        url = f"http://pi{n+1}.local:5000/api/data?date={dataDate}"

        files.append(await send_get_request(url))

    # convert to df

    #2 bucket them by time - Round timestamps to nearest 5 minutes or '1min', '10s', etc.
    for f in files:
        df['time_bucket'] = df['timestamp'].dt.floor('5min')  # or use dt.round()

    # Bucket into 5 minute

    #3 get average for every bucket

    #4 get average offset for each sensor

    #5 update config file

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Main loop crashed: {e}")

