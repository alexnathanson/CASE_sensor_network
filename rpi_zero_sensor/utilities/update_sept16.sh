#!/bin/bash

# DO NOT INCLUDE A REBOOT IN THIS SCRIPT!

echo "Running Sept 16th update script"

# set up kernel.panic

LINE="kernel.panic = 10"
FILE="/etc/sysctl.conf"

# Check if the line already exists
if grep -q "^$LINE" "$FILE"; then
    echo "Line already exists in $FILE"
else
    echo "$LINE" | sudo tee -a "$FILE"
    echo "Added line to $FILE"
fi

sudo sysctl -p

# install watchdog

sudo apt install watchdog

LINE_ONE="watchdog-device = /dev/watchdog"
LINE_TWO="watchdog-timeout = 15"
LINE_THREE="max-load-1 = 24"

FILE_W="/etc/watchdog.conf"

# Check if line 1 already exists
if grep -q "^$LINE_ONE" "$FILE_W"; then
    echo "Line already exists in $FILE_W"
else
    echo "$LINE_ONE" | sudo tee -a "$FILE_W"
    echo "Added line to $FILE_W"
fi

# Check if line 2 already exists
if grep -q "^$LINE_TWO" "$FILE_W"; then
    echo "Line already exists in $FILE_W"
else
    echo "$LINE_TWO" | sudo tee -a "$FILE_W"
    echo "Added line to $FILE_W"
fi

# Check if line 3 already exists
if grep -q "^$LINE_THREE" "$FILE_W"; then
    echo "Line already exists in $FILE_W"
else
    echo "$LINE_THREE" | sudo tee -a "$FILE_W"
    echo "Added line to $FILE_W"
fi

sudo systemctl enable watchdog
sudo systemctl start watchdog