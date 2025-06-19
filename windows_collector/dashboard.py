from flask import Flask, jsonify, abort
import pandas as pd
import os
import requests
import datetime
import json
import asyncio

app = Flask(__name__)


# RPi Sensor Host Names
hostNames = []

for s in range(1,9):
    hostNames.append('pi' + str(s) + ".local")


# URL of the API that returns CSV data
port = 5000
endPoint = "/api/files?date="

def fetchRPi(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.content
        return data

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
    except Exception as e:
        print(f"An error occurred: {e}")

def tempCSV(data, directory, filename):
    if not data or len(data) == 0:
        print("Received empty content. CSV file will not be saved.")
        return

    #check if directory exists
    os.makedirs(directory, exist_ok=True)

    #make full file path
    file_path = os.path.join(directory, filename)

    try:
        with open(file_path, 'wb') as f:  # use 'wb' to write bytes for CSV
            f.write(data)

        print(f"CSV file saved to: {file_path}")
    except Exception as e:
        print(e)


async def fetchLive():

    # Headers or authentication (if needed)
    headers = {
        "Authorization": "",  # Optional
        "Accept": "text/csv"
    }

    for h in hostNames:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        dst = 'http://' + h + ':5000/api/data?date=' + str(yesterday)
        #print(dst)
        response = fetchRPi(dst, headers)

        # File path to save the CSV
        output_path = r"temp"
        filename = h.split('.')[0] + '_' + str(yesterday) + '.csv'
        print(output_path)
        print(filename)

        archiveCSV(response, output_path, filename)

async def main():

    #update data every minute
    fetchLive()
    asyncio.sleep(60)

# # Define file paths and map them to endpoints
# CSV_FILES = {
#     'pi1': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi2': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi3': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi4': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi5': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi6': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi7': 'archive/pi1/pi1_2025-04-07.csv',
#     'pi8': 'archive/pi1/pi1_2025-04-07.csv'
# }

@app.route('/data/<filename>', methods=['GET'])
def get_csv_data(filename):
    filepath = CSV_FILES.get(filename)
    print(filepath)

    if not filepath or not os.path.isfile(filepath):
        abort(404, description=f"File '{filename}' not found.")

    try:
        df = pd.read_csv(filepath)
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        abort(500, description=f"Error reading file '{filename}': {e}")

@app.route('/files', methods=['GET'])
def list_files():
    return jsonify(list(CSV_FILES.keys()))

# @app.route('/live', methods=['GET'])
# def list_files():
#     return jsonify(list(CSV_FILES.keys()))

if __name__ == '__main__':
    app.run(debug=True)
    #await main()
    asyncio.run(main())
