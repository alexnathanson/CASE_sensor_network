import requests
import datetime
import os
import json

# RPi Sensor Host Names
hostNames = []

for s in range(1,9):
    hostNames.append('pi' + str(s) + ".local")

hostNames.append('kasa' + str(s) + ".local")

#print(hostNames)

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

def archiveCSV(data, directory, filename):
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

def main():

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
        output_path = r"archive/"+ h.split('.')[0]
        filename = h.split('.')[0] + '_' + str(yesterday) + '.csv'
        print(output_path)
        print(filename)

        archiveCSV(response, output_path, filename)

if __name__ == "__main__":
    main()
