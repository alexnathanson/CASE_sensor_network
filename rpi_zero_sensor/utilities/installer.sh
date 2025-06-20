#!/bin/bash

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

# Replace the line in the file
sed -i "s/\"number\": *[0-9]\+,/\"number\": $SENSOR_NUM,/" "$CONFIG"

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
else
	python -m venv venv
fi

source venv/bin/activate

pip install -r /home/case/CASE_sensor_network/rpi_zero_sensor/requirements.txt
echo "Python requirements installed"

chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.py

cp /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.service /etc/systemd/system/sht31d_logger.service

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable sht31d_logger.service
systemctl start sht31d_logger.service
echo "Sensor logger service installed"


chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.py

cp /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.service /etc/systemd/system/sht31d_dashboard.service
systemctl daemon-reexec
sudo systemctl daemon-reload
systemctl enable sht31d_dashboard.service
systemctl start sht31d_dashboard.service
echo "Dashboard service installed"

chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_airtable.py

cp /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.service /etc/systemd/system/sht31d_airtable.service
systemctl daemon-reexec
sudo systemctl daemon-reload
systemctl enable sht31d_airtable.service
systemctl start sht31d_airtable.service
echo "Airtable service installed"


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