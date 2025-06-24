#!/bin/bash

# run with sudo bash

read -p "Restart temperature and humidity (SHT31-D) logger? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable sht31d_logger.service
    systemctl start sht31d_logger.service
    echo "Kasa logger restarted"
fi

read -p "Restart Kasa logger? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable kasa_logger.service
    systemctl start kasa_logger.service
    echo "Kasa logger restarted"
fi

read -p "Restart dashboard? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	systemctl daemon-reexec
	systemctl daemon-reload
	systemctl enable dashboard.service
	systemctl start dashboard.service
	echo "Dashboard restarted"
fi

read -p "Restart Airtable? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	systemctl daemon-reexec
	systemctl daemon-reload
	systemctl enable airtable.service
	systemctl start airtable.service
	echo "Airtable restarted"
fi