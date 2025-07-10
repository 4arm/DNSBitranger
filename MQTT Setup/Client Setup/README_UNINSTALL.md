# DNS Client Uninstallation Guide

This guide explains how to completely uninstall the DNS client setup, including all installed packages, services, cron jobs, and files.

---

## What This Does

- Stops and disables the `dnsmasq` service
- Removes installed packages: `dnsmasq`, `python3-paho-mqtt`, `python3-pip`, `curl`
- Removes installed Python packages: `paho-mqtt` and `requests`
- Deletes the installation directory `/opt/dns-client`
- Removes cron jobs running MQTT scripts

---

## Uninstallation Steps

### 1. Stop and disable `dnsmasq`

```bash
sudo systemctl stop dnsmasq
sudo systemctl disable dnsmasq
```

### 2. Remove installed packages and dependencies

```bash
sudo apt remove --purge -y dnsmasq python3-paho-mqtt python3-pip curl
sudo apt autoremove -y
```

### 3. Remove cron jobs

Edit your crontab to delete MQTT client jobs:

```bash
crontab -l > mycron.tmp
```

Open `mycron.tmp` with a text editor and delete lines:

```
*/5 * * * * /usr/bin/python3 /opt/dns-client/mqtt_publisher.py
*/5 * * * * /usr/bin/python3 /opt/dns-client/nxdomain_sender.py
```

Then update your crontab:

```bash
crontab mycron.tmp
rm mycron.tmp
```

### 4. Remove installation directory

```bash
sudo rm -rf /opt/dns-client
```

### 5. (Optional) Remove Python packages globally

```bash
sudo python3 -m pip uninstall -y paho-mqtt requests
```

---

## Automated Uninstall Script

You can create a script with the following content to automate the uninstallation process:

```bash
#!/bin/bash

sudo systemctl stop dnsmasq
sudo systemctl disable dnsmasq
sudo apt remove --purge -y dnsmasq python3-paho-mqtt python3-pip curl
sudo apt autoremove -y
sudo rm -rf /opt/dns-client

crontab -l | grep -v -F '/opt/dns-client/mqtt_publisher.py' | grep -v -F '/opt/dns-client/nxdomain_sender.py' | crontab -

sudo python3 -m pip uninstall -y paho-mqtt requests

echo "Uninstallation complete."
```

Save it as `uninstall.sh`, make it executable (`chmod +x uninstall.sh`), and run it with:

```bash
./uninstall.sh
```

---

## Notes

- Make sure you run these commands with appropriate privileges (using `sudo`).
- Removing Python packages globally affects all Python projects on the system.
- Back up any important data before uninstalling.

---

## License

MIT License or as per the original repository license at [4arm/DNSBitranger](https://github.com/4arm/DNSBitranger).
