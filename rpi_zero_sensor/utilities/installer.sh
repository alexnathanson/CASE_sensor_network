#!/bin/bash

# run with sudo bash (not sudo sh)

REPO_URL="https://github.com/alexnathanson/CASE_sensor_network.git"
REPO_DST="/home/case"
REPO_DIR="/home/case/CASE_sensor_network"
DATA_DIR="/home/case/data"
CONFIG="/home/case/CASE_sensor_network/rpi_zero_sensor/config.json"
CONFIG_TEMP="/home/case/CASE_sensor_network/rpi_zero_sensor/config_template.json"

# Check if destination already exists
if [ -d "$REPO_DIR" ]; then
    echo "Directory '$REPO_DIR' already exists. Skipping clone."
else
    echo "Cloning $REPO_URL into $REPO_DST..."
    git clone "$REPO_URL" "$REPO_DST"
    if [ $? -eq 0 ]; then
        echo "Repository cloned successfully."
    else
        echo "Failed to clone repository." >&2
        exit 1
    fi
fi

# Get the hostname
HOSTNAME_STR=$(hostname)

# Remove the string 'pi' from the hostname
SENSOR_NUM=${HOSTNAME_STR//pi/}
echo "Sensor #$SENSOR_NUM"


# File to modify
sudo cp "$CONFIG_TEMP" "$CONFIG"

# this checks if its a number and puts quotes on it if not (untested)
if [[ "$SENSOR_NUM" =~ ^[0-9]+$ ]]; then
    formatted_SENSOR_NUM=$sensornum
else
    formatted_SENSOR_NUM="\"$SENSOR_NUM\""
fi

# Replace the line in the file
sed -i "s/\"number\": *[0-9]\+,/\"number\": $formatted_SENSOR_NUM,/" "$CONFIG"

echo "Updated 'sensor number' to $SENSOR_NUM in $CONFIG."


# Check if destination already exists
if [ -d "$DATA_DIR" ]; then
    echo "Directory '$DATA_DIR' already exists. Skipping mkdir."
else
	mkdir "$DATA_DIR"
	echo "Created data directory"
fi

chown case:case /home/case/data

cd /home/case

# Check if destination already exists
if [ -d "/home/case/venv" ]; then
    echo "venv already exists. Skipping create venv."
    sudo chown -R root:root /home/case/venv 
else
	python -m venv venv
fi

source /home/case/venv/bin/activate

pip install -r /home/case/CASE_sensor_network/rpi_zero_sensor/requirements.txt

sudo chown -R case:case /home/case/venv 

echo "Python requirements installed"


read -p "Are you running the temperature/ humidity sensor on this device? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.py
    cp /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.service /etc/systemd/system/sht31d_logger.service

    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable sht31d_logger.service
    systemctl start sht31d_logger.service
    echo "Sensor logger service installed"

fi

read -p "Are you running the Kasa script on this device? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/kasa_logger.py
    cp /home/case/CASE_sensor_network/rpi_zero_sensor/kasa_logger.service /etc/systemd/system/kasa_logger.service

    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable kasa_logger.service
    systemctl start kasa_logger.service
    echo "Kasa logger service installed"

fi

chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/dashboard.py
cp /home/case/CASE_sensor_network/rpi_zero_sensor/dashboard.service /etc/systemd/system/dashboard.service
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable dashboard.service
systemctl start dashboard.service
echo "Dashboard service installed"


read -p "Are you running the Airtable script on this device? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/airtable_live.py
    cp /home/case/CASE_sensor_network/rpi_zero_sensor/airtable_live.service /etc/systemd/system/airtable_live.service
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable airtable_live.service
    systemctl start airtable_live.service
    echo "Airtable Live service installed"

    chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/airtable_status.py
    cp /home/case/CASE_sensor_network/rpi_zero_sensor/airtable_status.service /etc/systemd/system/airtable_status.service
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable airtable_status.service
    systemctl start airtable_status.service
    echo "Airtable Status service installed"
fi

# Line to add
CRON_JOB="0 3 * * * /sbin/reboot"

# Check if the job already exists
(crontab -l 2>/dev/null | grep -Fxq "$CRON_JOB") && {
    echo "Cron job already exists."
    exit 0
}

# Add the job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
echo "Cron job added."