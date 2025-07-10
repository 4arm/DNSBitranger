#!/bin/bash

sudo systemctl stop dnsmasq
sudo systemctl disable dnsmasq
sudo apt remove --purge -y dnsmasq python3-paho-mqtt python3-pip curl ufw
sudo apt autoremove -y
sudo rm -rf /opt/dns-client

crontab -l | grep -v -F '/opt/dns-client/mqtt_publisher.py' | grep -v -F '/opt/dns-client/nxdomain_sender.py' | crontab -

sudo python3 -m pip uninstall -y paho-mqtt requests

echo "Uninstallation complete."
