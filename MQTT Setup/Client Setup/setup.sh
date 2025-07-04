#!/bin/bash

echo "[*] Starting DNS Client Auto-Setup..."

# Update system and install dependencies
sudo apt update
sudo apt install python3-paho-mqtt
sudo apt install -y python3-pip curl

# Create install directory
INSTALL_DIR="/opt/dns-client"
sudo mkdir -p "$INSTALL_DIR"
sudo chown $USER:$USER "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download the publisher script
curl -O https://raw.githubusercontent.com/4arm/DNSBitranger/refs/heads/main/MQTT%20Setup/Client%20Setup/mqtt_publisher.py

# Install required Python packages system-wide
pip3 install --break-system-packages paho-mqtt requests

# Make sure the script is executable
chmod +x mqtt_publisher.py

# Set up cron job (if not already there)
cron_entry="*/0 * * * * /usr/bin/python3 $INSTALL_DIR/mqtt_publisher.py"
(crontab -l 2>/dev/null | grep -Fv "$cron_entry"; echo "$cron_entry") | crontab -

echo "[✓] DNS client setup complete. Publishes to MQTT every 5 minutes."
echo "The directory will be /opt/dns-client."
