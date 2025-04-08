# Windows Installation

Backs up and visualizes data

There are 3 Python programs running on this device:
* rpi_data_collector fetches data from the RPi sensors
* kasa_logger collects data from the smart plugs
* post_data posts aggregated data to the cloud to view from outside the network

There is also a JS frontend that can visualize data from sensor on the LAN.

## Installation

### Kasa

For some reason, the Kasa library wasn't working when install with pip, so it needed to be installed from git.

`git clone https://github.com/python-kasa/python-kasa.git`
`cd python-kasa/`
`pip install .`