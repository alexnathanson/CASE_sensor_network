# CASE_sensor_network

This system collects temperature, humidity, and power data.

## System Design
<p>
	<img src=/images/sensor-dataflows.jpg>
	Image: System data flows
</p>

SHT31-D Temperature and humidity sensors running on 8 identically configured Raspberry Pi Zero W2 devices. https://www.adafruit.com/product/2857

An additional Raspberry Pi Zero W2 device collects data from the 4 <a href='https://github.com/alexnathanson/CASE_sensor_network/blob/main/KASA.md'>Kasa Smart Plugs</a>.

Each sensor device:
* takes readings every 5 minutes
* stores data locally
* makes data available to other devices on the network through APIs
	* host name is pi*.local where * is a number 1-8 (the host name for the Kasa Smart Plug device is kasa.local)
	* Port 5000
	* API endpoints: /api/files,/api/location, /api/disk, /api/health, /api/data?date=now, /api/data?date=YYYY-MM-DD

A Windows laptop backs up data from each RPi daily.

The specific services each RPi runs depends on its role. All RPis should be running:
* dashboard.service
The devices running temperature/ humidity sensors should be running:
* sht31d_logger.service
The device running Kasa should run:
* kasa_logger.service
The device running Airtable (the Kasa RPi in most cases):
* airtable_live.service
* airtable_status.service

## Network

The network name is CASE_sensor_network. See credentials Google Doc for login info. All Raspberry Pi devices must be on that network. To access any device you must also be on that local network.

When on network, log in to router via a browser with http://tplinkeap.net/

## Collecting Data

 Sensor data can be retrieved in a number of ways. Each Raspberry Pi Zero device stores its own data on its SD card. The data is also copied to the Windows laptop. Live data can be retrieved remotely via the Airtable database API.

* The best way to retrieve data is programmatically via the API.
* You can also retrieve data manually from:
	* the interfaces on each sensor by clicking the file name on the download page.
	* the Windows laptop, assuming it is successfully archiving data, by navigating to the archive directory located at `C:\Users\CASE\CASE_sensor_network\windows_collector\archive`

Alternative ways to collect data:
* You can SCP files from the devices directly. On all devices, the files are located in the `/home/case/data` directory.
* You can manually copy CSV files directly from SD cards on device. This is less ideal, because it means that the sensor isn't collecting data while you are doing this.

1 complete CSV file from the 8 SHT31-D sensors should be about 23kb. The CSV files from the smart plug device are around 11kb.

## Troubleshooting

All devices can be found via ssh, ping, browser, or curl by their hostname i.e. pi1.local (http://pi1.local:5000). See <a href='https://github.com/alexnathanson/CASE_sensor_network/tree/main/rpi_zero_sensor'>rpi_zero_sensor</a> directory for additional troubleshooting

If that doesn't work, log in to wireless access point via a browser, http://tplinkeap.net/.

## To do

* Fix Airtable updating issue!!!
* Windows device
	* turn off autoupdating
	* Windows device should backfil missing files
	* install Team Viewer
* Add calibration
* Final updates for RPis
	* health start date
	* location
* update rpi readme-dashboard and api section