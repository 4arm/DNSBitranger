#!/bin/bash

set -e

echo "[*] Starting DNS Client Auto-Setup..."

# Update system and install dependencies
sudo apt update
sudo apt install -y dnsmasq python3-paho-mqtt python3-pip curl ufw

# Check for processes using port 53 (DNS)
PIDS=$(sudo lsof -t -i :53 || true)
if [ -n "$PIDS" ]; then
  echo "[!] Found processes using port 53:"
  echo "$PIDS"
  echo "[*] Killing processes on port 53..."
  sudo kill -9 $PIDS
else
  echo "[*] No processes running on port 53."
fi

# Allow DNS port through UFW firewall
sudo ufw allow 53

# Restart and enable dnsmasq service
sudo systemctl restart dnsmasq
sudo systemctl enable dnsmasq

# Create install directory
INSTALL_DIR="/opt/dns-client"
sudo mkdir -p "$INSTALL_DIR"
sudo chown "$USER:$USER" "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download the publisher scripts
curl -O https://raw.githubusercontent.com/4arm/DNSBitranger/refs/heads/main/MQTT%20Setup/Client%20Setup/mqtt_publisher.py
curl -O https://raw.githubusercontent.com/4arm/DNSBitranger/refs/heads/main/MQTT%20Setup/Client%20Setup/nxdomain_sender.py

# Install required Python packages system-wide
python3 -m pip install --break-system-packages --upgrade pip
python3 -m pip install --break-system-packages paho-mqtt requests

# Make sure the scripts are executable
chmod +x mqtt_publisher.py nxdomain_sender.py

# Set up cron jobs (avoid duplicates)
for script in mqtt_publisher.py nxdomain_sender.py; do
  cron_entry="*/5 * * * * /usr/bin/python3 $INSTALL_DIR/$script"
  # Remove any existing line running the script and add the new one
  (crontab -l 2>/dev/null | grep -Fv "$script"; echo "$cron_entry") | crontab -
done

echo "[✓] DNS client setup complete. Publishing to MQTT every 5 minutes."
echo "Scripts installed in $INSTALL_DIR"
