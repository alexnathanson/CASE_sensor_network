# GET Request API

All RPi sensors use the same naming convention: pi + #1-8 + .local i.e. pi1.local

All APIs and dashboards are available on port 5000

* A dataviz of today's data is available at root: [go](http://pi1.local:5000){:target="_blank"}
* A list of files stored on the device is available at `api/files`: [go](http://pi1.local:5000/api/files){:target="_blank"}
* To download a specific csv file, use the `api/data` endpoint with the date argument `?date=YYYY-MM-DD`: [go](http://pi1.local:5000/api/data?date=2025-04-6){:target="_blank"}
* To check disk usage, use the `/api/disk` endpoint: [go](http://pi1.local:5000/api/disk){:target="_blank"}
