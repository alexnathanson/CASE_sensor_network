# GET Request API

All RPi sensors use the same naming convention: pi + #1-8 + .local i.e. pi1.local

All APIs and dashboards are available on port 5000

* A dataviz of today's data is available at root: <a href="http://pi1.local:5000" target="_blank">http://pi1.local:5000</a>
* A list of files stored on the device is available at `api/files`: <a href="http://pi1.local:5000/api/files" target="_blank">http://pi1.local:5000/api/files</a>
* To download a specific csv file, use the `api/data` endpoint with the date argument `?date=YYYY-MM-DD`: <a href="http://pi1.local:5000/api/data?date=2025-04-6" target="_blank">http://pi1.local:5000/api/data?date=2025-04-6</a>
* To check disk usage, use the `/api/disk` endpoint: <a href="http://pi1.local:5000/api/disk" target="_blank">pi1.local:5000/api/disk</a>
