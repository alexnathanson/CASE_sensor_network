#!/bin/bash

REPO_DIR="/home/case/CASE_sensor_network"

# Check if destination already exists
if [ -d "$REPO_DIR" ]; then
    echo "Directory '$REPO_DIR' already exists. Pulling most recent version. :)"

	cd /home/caseCASE_sensor_network
	git stash
    git pull origin main

else
    echo "Repository doesn't exist. :("
fi

echo "Rebooting now"
sudo reboot -h now