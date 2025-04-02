# Installation

## OS and Software Installation

### Pi Setup
Enable I2C

Clone repository
`git clone https://github.com/alexnathanson/CASE_sensor_network.git`

Create data directory
`cd /home/case/CASE_sensor_network`<br>
`mkdir data`

Create venv
`python -m venv venv`

Activate venv
`source venv/bin/activate`

#### Install libraries

Install from requirements.txt
`pip install -r requirements.txt`

If that fails, install manually:

* SHT31-D sensor library https://github.com/adafruit/Adafruit_CircuitPython_SHT31D
	* `pip install adafruit-circuitpython-sht31d`
* `pip install pandas`

#### Automate

Make script executable
`chmod +x /home/case/CASE_sensor_network/sht31d_logger.py`


Copy service file
`sudo cp sh31d_logger.service /etc/systemd/system/sht31d_logger.service`

Reload and enable
`sudo systemctl daemon-reexec`
`sudo systemctl daemon-reload`
`sudo systemctl enable sht31d_logger.service`
`sudo systemctl start sht31d_logger.service`

Check if its running
`sudo systemctl status sht31d_logger.service`

## SHT31-D Sensor Wiring
![image](https://cdn-learn.adafruit.com/assets/assets/000/101/432/medium640/adafruit_products_SHT31_RasPi_breadboard_bb.jpg?1618427246)

## Troubleshooting

### Logs
`journalctl -u sht31d_logger.service -f`