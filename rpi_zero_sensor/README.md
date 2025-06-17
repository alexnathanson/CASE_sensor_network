# RPi Zero W2 Installation

There are 2 Python scripts that need to be installed as services to run automatically on the RPi Zero sensors:
* logger
* dashboard

Logger collects the data and stores it as a CSV. Dashboard makes the data available via an API.

Note that it is crucial that the host name of each Pi is unique and follows the naming convention. Also, the config file should be updated with the correct number.

## OS and Software Installation

### Pi Imager Settings

It is crucial that the host name of each Pi is unique and follows the naming convention, pi + integer. There are 8 sensors, so the range of numbers is 1-8.<br>
hostname: pi[#1-8].local

See credentials doc for username, password, and network setting to use.

### Pi Setup
`sudo apt-get update`

`sudo apt-get upgrade`

`sudo raspi-config`
* Enable I2C
* Don't overlay file system
* Localization
	* enable US.UTF-8 (optionally, removing GB will free up a little space)
	* set timezone to NY
	* set WLAN to US
* Expand filesystem

Clone repository<br>
`git clone https://github.com/alexnathanson/CASE_sensor_network.git`

Create data directory and assign ownership<br>
`mkdir /home/case/data`<br>
`sudo chown case:case /home/case/data`

Create venv in user directory<br>
`python -m venv venv`

Activate venv<br>
`source venv/bin/activate`

Set sensor number<br>
`sudo nano /home/case/CASE_sensor_network/rpi_zero_sensor/config.json`

#### Install libraries

Install from requirements.txt
`pip install -r requirements.txt`

If that fails, install manually via pip:

* SHT31-D sensor library https://github.com/adafruit/Adafruit_CircuitPython_SHT31D
	* `pip install adafruit-circuitpython-sht31d`
* `pip install pandas`


#### Automate

The following lines can be run automatically via utilities/install_automation.sh

Make script executable<br>
`chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.py`

Copy service file<br>
`sudo cp sh31d_logger.service /etc/systemd/system/sht31d_logger.service`

Reload and enable<br>
`sudo systemctl daemon-reexec`<br>
`sudo systemctl daemon-reload`<br>
`sudo systemctl enable sht31d_logger.service`<br>
`sudo systemctl start sht31d_logger.service`

Dashboard Automation:<br>
`chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.py`<br>
`sudo cp sh31d_dashboard.service /etc/systemd/system/sht31d_dashboard.service`<br>
`sudo systemctl daemon-reexec`<br>
`sudo systemctl daemon-reload`<br>
`sudo systemctl enable sht31d_dashboard.service`<br>
`sudo systemctl start sht31d_dashboard.service`

After running automation installer, check if they are running<br>
`sudo systemctl status sht31d_logger.service`
`sudo systemctl status sht31d_dashboard.service`

Set daily reboot at 3am (run manually - not installed automatically)<br>
`sudo crontab -e`<br>
Add this line at the bottom of the file `0 3 * * * /sbin/reboot`

## SHT31-D Sensor Wiring
![image](https://cdn-learn.adafruit.com/assets/assets/000/101/432/medium640/adafruit_products_SHT31_RasPi_breadboard_bb.jpg?1618427246)

## Troubleshooting

### Logs
`journalctl -u sht31d_logger.service -f`

Stop (temporary) or disable (doesn't start on boot) Service<br>
`sudo systemctl stop sht31d_logger.service`<br>
`sudo systemctl disable sht31d_logger.service`

### Disk Space

Once everything is installed, a 32GB microSD card starts at about 25% full. Check the disk status via the API.