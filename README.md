# CASE_sensor_network

https://www.adafruit.com/product/2857

<img src=/images/sensor-dataflows.jpg>

## System Design

Temperature and humidity sensors running on 8 identically configured Raspberry Pi Zero W 2 devices. Each device:
* takes readings every 5 minutes
* stores data locally
* makes data available to other devices on the network through APIs
	* host name is pi*.local where * is a number 1-8
	* Port 5000
	* API endpoints: /api/files, /api/disk, /api/data?date=YYYY-MM-DD

A Windows laptop
* backs up data from each RPi
* collects sensors data from AC
* post aggregated data to cloud database

<p>
The specific services each RPi runs depends on its role. All RPis should be running:
* dashboard.service
The devices running temperature/ humidity sensors should be running:
* sht31d_logger.service
The device running Kasa should runu:
* kasa_logger.service
The device running Airtable (the Kasa rpi in most cases):
* airtable_live.service
* airtable_status.service
</p>

## Network

When on network, log in to router via a browser with http://tplinkeap.net/ <Br>
See Google Doc for log info.

## Troubleshooting

To find RPi IPs, log in to WAP via browser

## To do

* plot timer series data on device dashboard
* check that file status in health is accounting for everything missing, not just from start file
* plot time series data for all devices on local network page
* switch kasa to pi zero
* test that windows device is archiving properly
* print remaining cases (~4) and resolder sensors
* finish documentationn