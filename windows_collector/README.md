# Windows Installation

This set of scripts is intended to run a local Windows machine to backup data from all sensors.

This is done with the rpi_data_collector.py script.

## Installation

`git clone https://github.com/alexnathanson/CASE_sensor_network`

`python -m venv venv`

`venv\Scripts\activate`

Install requirements from windows_collector directory<br>
`pip install -r requirements.txt`

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

