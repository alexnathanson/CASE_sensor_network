#!/bin/bash

#cd /home/case/CASE_sensor_network/rpi_zero_sensor/

chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.py

sudo cp /home/case/CASE_sensor_network/rpi_zero_sensor/sh31d_logger.service /etc/systemd/system/sht31d_logger.service

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable sht31d_logger.service
sudo systemctl start sht31d_logger.service


chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.py

sudo cp sh31d_dashboard.service /etc/systemd/system/sht31d_dashboard.service
sudo systemctl daemon-reexec sudo systemctl daemon-reload
sudo systemctl enable sht31d_dashboard.service
sudo systemctl start sht31d_dashboard.service