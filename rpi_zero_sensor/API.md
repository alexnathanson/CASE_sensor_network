# GET Request API

All RPi sensors use the same naming convention: pi + #1-8 + .local i.e. pi1.local

All APIs and dashboards are available on port 5000

* A dataviz of today's data is available at root: http://pi1.local:5000
* A list of files stored on the device (in json) is available at `api/files`: http://pi1.local:5000/api/files
* To download a specific csv file, use the `api/data` endpoint with the date argument `?date=YYYY-MM-DD`: http://pi1.local:5000/api/data?date=2025-04-6
	* To get most recent data (json), use the `api/data` endpoint with the date argument set to now `?date=now`: http://pi1.local:5000/api/data?date=now
* To check disk usage (json), use the `/api/disk` endpoint: http://pi1.local:5000/api/disk
* To check RPi health `api/health`: http://pi1.local:5000/api/health
