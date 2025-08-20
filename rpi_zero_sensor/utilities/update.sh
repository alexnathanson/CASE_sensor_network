#!/bin/bash

REPO_URL="https://github.com/alexnathanson/CASE_sensor_network.git"
REPO_DIR="/home/case/CASE_sensor_network"


# Check if destination already exists
if [ -d "$REPO_DIR" ]; then
    echo "Directory '$REPO_DIR' already exists. Pulling most recent version."

	cd /home/case/CASE_sensor_network
	sudo git stash
    sudo git pull origin main

else
    echo "Repository doesn't exist."
fi

echo "Rebooting now"
sudo reboot -h now