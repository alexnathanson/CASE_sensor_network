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

`pip install -r requirements.txt`

### Kasa

For some reason, the Kasa library wasn't working when install with pip, so it needed to be installed from git.

`git clone https://github.com/python-kasa/python-kasa.git`
`cd python-kasa/`
`pip install .`

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

