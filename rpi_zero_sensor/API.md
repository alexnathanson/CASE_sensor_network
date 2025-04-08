# GET Request API

All RPi sensors use the same naming convention: pi + #1-8 + .local i.e. pi1.local

All APIs and dashboards are available on port 5000

* A dataviz of today's data is available at root: http://pi1.local:5000
* A list of files stored on the device is available at `api/files`: http://pi1.local:5000/api/files
* To retrieve a specific file, use the `api/data` endpoint with the date argument `?date=YYYY-MM-DD`: http://pi1.local:5000/api/data?date=2025-04-6
* To check disk usage, use the `/api/disk` endpoint: http://pi1.local:5000/api/disk
