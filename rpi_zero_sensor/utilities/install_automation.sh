#!/bin/bash

#cd /home/case/CASE_sensor_network/rpi_zero_sensor/

pip install -r requirements.txt

chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.py

cp /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_logger.service /etc/systemd/system/sht31d_logger.service

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable sht31d_logger.service
systemctl start sht31d_logger.service


chmod +x /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.py

cp /home/case/CASE_sensor_network/rpi_zero_sensor/sht31d_dashboard.service /etc/systemd/system/sht31d_dashboard.service
systemctl daemon-reexec sudo systemctl daemon-reload
systemctl enable sht31d_dashboard.service
systemctl start sht31d_dashboard.service