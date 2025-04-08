import requests
import datetime
import os
import json

# RPi Sensor Host Names
hostNames = []

for s in range(1,9):
    hostNames.append('pi' + str(s) + ".local")

print(hostNames)

# URL of the API that returns CSV data
port = 5000
endPoint = "/api/files?date="

#get yesterday's date to make API requests
def getYesterday():
    pass

async def main():

    #url = "https://example.com/api/data.csv"  # Replace with actual API URL

    # Headers or authentication (if needed)
    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN",  # Optional
        "Accept": "text/csv"
    }

    # File path to save the CSV
    output_path = r"C:\Users\YourName\Documents\output.csv"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if the request failed

        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"CSV saved to: {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
