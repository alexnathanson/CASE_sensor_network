#!/bin/bash

REPO_URL="https://github.com/alexnathanson/CASE_sensor_network.git"
REPO_DST="/home/case"
REPO_DIR="/home/case/CASE_sensor_network"


# Check if destination already exists
if [ -d "$REPO_DIR" ]; then
    echo "Directory '$REPO_DIR' already exists. Pulling most recent version."

	cd /home/case/CASE_sensor_network
	git stash
    git pull origin main
else
    echo "Repository doesn't exist. Run installer"
    git clone "$REPO_URL" "$REPO_DST"
    if [ $? -eq 0 ]; then
        echo "Repository cloned successfully."
    else
        echo "Failed to clone repository." >&2
        exit 1
    fi
fi

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable sht31d_logger.service
systemctl start sht31d_logger.service
echo "logger restarted"

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable sht31d_dashboard.service
systemctl start sht31d_dashboard.service
echo "dashboard restarted"

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable sht31d_airtable.service
systemctl start sht31d_airtable.service
echo "airtable restarted"

read -p "You may need to reboot for changes to take effect. Would you like to reboot? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # do dangerous stuff
    reboot -h now
fi
