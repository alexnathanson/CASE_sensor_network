# Windows Installation

Backs up and visualizes data

There are 3 Python programs running on this device:
* rpi_data_collector fetches data from the RPi sensors
* kasa_logger collects data from the smart plugs
* post_data posts aggregated data to the cloud to view from outside the network

There is also a JS frontend that can visualize data from sensor on the LAN.

## Installation

`git clone https://github.com/alexnathanson/CASE_sensor_network`

`python -m venv venv`

`venv\Scripts\activate`

Install requirements from windows_collector directory<br>
`pip install -r requirements.txt`

### Kasa

To connect the Kasa devices to the network, you need to connect to them first via the Kasa app.

Devices are named kasa1 - kasa4

If for some reason, the Kasa library wasn't working when install with pip, so it needed to be installed from git.<br>
`git clone https://github.com/python-kasa/python-kasa.git`<br>
`cd python-kasa/`<br>
`pip install .`

* Download NSSM
* Place nssm.exe in nssm folder in programs directory
* add to environment paths
* open temrinal as admin
	* `nssm install KasaLogger`
	* path is path to python.exe in venv
	* startup directory is windows_collector\
	* arg is path to kasa_logger.py
	* start service with `nssm start KasaLogger`
	* check status with task manager (might just show up as python) or `nssm status KasaLogger`
## Automation

The python scripts are run via Windows Task Scheduler

General
* Name the task
* Set to run whether user is logged in or not
Triggers
* Set to daily
Actions
* set the script tp the python.exe file in your venv
* add the script's full filepath as an argument
* start in specifies the directory it starts from
Conditions
* don't depend on the network connect...
Settings
* run task as soon as possible

