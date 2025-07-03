#!/bin/bash

echo "[*] Starting DNS Client Auto-Setup..."

# Update system and install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv mosquitto-clients curl

# Create a virtual environment
python3 -m venv /etc/bind/mqttenv
source /etc/bind/mqttenv/bin/activate

# Install required Python packages
pip install paho-mqtt requests

# Create /etc/bind if not exists
sudo mkdir -p /etc/bind
cd /etc/bind

# Pull mqtt_publisher.py from GitHub
curl -O https://raw.githubusercontent.com/yourname/dns-client-setup/main/mqtt_publisher.py

# Make sure it's executable
chmod +x mqtt_publisher.py

# Setup crontab to run every 5 mins
(crontab -l 2>/dev/null; echo "*/5 * * * * /etc/bind/mqttenv/bin/python /etc/bind/mqtt_publisher.py") | crontab -

echo "[✓] Setup complete. Device will publish every 5 minutes."
