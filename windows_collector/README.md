# Windows Installation

This scripts is intended to run a local Windows machine to backup data from all sensors.

This is done with the rpi_data_collector.py script.

The best way to automatically run the script is with the Windows Task Scheduler.

Additionally, the local website should be running the this laptop. See <a href='https://github.com/alexnathanson/CASE_sensor_network/tree/main/local_website'>https://github.com/alexnathanson/CASE_sensor_network/tree/main/local_website</a>.

## Installation

1) Clone the repository: `git clone https://github.com/alexnathanson/CASE_sensor_network`
2) Create the virtual environment: `python -m venv venv`
3) Activate the virtual environment: `venv\Scripts\activate`
4) Navigate to the windows_collector directory and install requirements:
`pip install -r requirements.txt`
5) Schedule tasks to run via Windows Task Scheduler.

### Windows Task Scheduler
Python scripts can be run via Windows Task Scheduler

General
* Name the task
* Set to run whether user is logged in or not
Triggers
* Set to daily. Around 1am is a good time, because all the sensors will have completed their daily reboot by then.
Actions
* set the script to the python.exe file in your venv
* add the script's full filepath as an argument
* start in specifies the directory it starts from
Conditions
* don't depend on the network connect...
Settings
* run task as soon as possible

## Alternative Automation Method

You can also run the script with NSSM, but this isn't fully tested and is more meant for services not running once a day like this program.

* Download NSSM
* Place nssm.exe in nssm folder in programs directory
* add to environment paths
* open temrinal as admin
	* `nssm install rpi_data_collector`
	* path is path to python.exe in venv
	* startup directory is windows_collector\
	* arg is path to rpi_data_collector.py
	* start service with `nssm start rpi_data_collector`
	* check status with task manager (might just show up as python) or `nssm status rpi_data_collector`