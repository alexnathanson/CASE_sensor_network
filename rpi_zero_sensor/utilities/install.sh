#!/bin/bash

#cd /home/case
REPO="https://github.com/alexnathanson/CASE_sensor_network.git"
REPO_DST="/home/case"

# Check if destination already exists
if [ -d "$DEST_DIR" ]; then
    echo "Directory '$DEST_DIR' already exists. Skipping clone."
else
    echo "Cloning $REPO_URL into $DEST_DIR..."
    git clone "$REPO_URL" "$DEST_DIR"
    if [ $? -eq 0 ]; then
        echo "Repository cloned successfully."
    else
        echo "Failed to clone repository." >&2
        exit 1
    fi
fi

DATA_DIR="/home/case/data"
# Check if destination already exists
if [ -d "$DATA_DIR" ]; then
    echo "Directory '$DATA_DIR' already exists. Skipping mkdir."
else
	mkdir "$DATA_DIR"

chown case:case /home/case/data

cd /home/case/CASE_sensor_network

# Check if destination already exists
if [ -d "venv" ]; then
    echo "venv already exists. Skipping create venv."
else
	python -m venv venv

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
echo "Dashbaord service installed"


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