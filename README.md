# CASE_sensor_network

https://www.adafruit.com/product/2857

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

## Network

When on network, log in to router via a browser with http://tplinkeap.net/ <Br>
See Google Doc for log info.

## Troubleshooting

To find RPi IPs, log in to WAP via browser

## To do

SIMPLIFY setting up PIs with custom configs????
test - laptop to pull and archive files
remote access or posting... git?
look into Bonjour on windows to deal with host names
