# Sensor Network

All RPis should be running:
* dashboard.service

The devices running temperature/ humidity sensors should be running:
* sht31d_logger.service

The device running Kasa should run:
* kasa_logger.service

The device running Airtable (the Kasa rpi in most cases):
* airtable_live.service
* airtable_status.service

Logger collects the data and stores it as a CSV. Dashboard makes the data available via an API. Airtable updates the cloud database.

Note that it is crucial that the host name of each Pi is unique and follows the naming convention. Also, the config file should be updated with the correct number. The kasa device is named kasa and the value entered into the config file should be 'kasa'.

## Installation

See installation doc.

## Dashboards and APIs

### Local Dashboard and APIs

Within the local network (CASE_sensor_network) data from each device can be accessed via their dashboard and APIs. 
All RPi sensors use the same naming convention: pi + #1-8 + .local i.e. pi1.local. The Kasa device can be found at kasa.local.

All APIs and dashboards are available on port 5000

* A dataviz of today's data is available at root: http://pi1.local:5000
* A list of files stored on the device (in json) is available at `api/files`: http://pi1.local:5000/api/files
* To download a specific csv file, use the `api/data` endpoint with the date argument `?date=YYYY-MM-DD`: http://pi1.local:5000/api/data?date=2025-04-6
* To get most recent data (json), use the `api/data` endpoint with the date argument set to now `?date=now`: http://pi1.local:5000/api/data?date=now
* To check disk usage (json), use the `/api/disk` endpoint: http://pi1.local:5000/api/disk

### Local Network Dashboard
When on the local network, live data from all devices can be seen by running the website found in the 'local website' directory.
* https://github.com/alexnathanson/CASE_sensor_network/blob/main/local%20website/README.md

### External Dashboard

Outside of the local network, data can be check via the Airtable API.

## Airtable

Only 1 account updates the airtable. With a free account, we're limited to 1000 API calls a month (~33 calls/ day). 

When both script start, they retrieve record IDs (9 calls). Then it updates data as a batch, to minimize calls. The live script makes 1 update every 2 hours, for a total of 21 calls/day. The status script makes 1 update a day, for a total of 9 calls/ day. This requires a combined 30 API calls/ day, for ~930 calls/ month. With a paid account, the resolution can be increased if necessary.


## Troubleshooting


### Status
`sudo systemctl status sht31d_logger.service`

### Logs
`journalctl -u sht31d_logger.service -f`

Stop (temporary) or disable (doesn't start on boot) Service<br>
`sudo systemctl stop sht31d_logger.service`<br>
`sudo systemctl disable sht31d_logger.service`

### Disk Space

Once everything is installed, a 32GB microSD card starts at about 25% full. Check the disk status via the API.