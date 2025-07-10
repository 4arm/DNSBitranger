# DNS Client Auto-Setup

This setup script installs and configures a DNS client that publishes system data to an MQTT broker every 5 minutes. It also installs and manages `dnsmasq` as a local DNS server, ensuring no port conflicts on DNS port 53.

---

## Features

- Installs required dependencies: `dnsmasq`, Python packages (`paho-mqtt`, `requests`), `curl`, `ufw`
- Checks and stops any processes using port 53 (DNS) to avoid conflicts
- Configures firewall to allow DNS traffic on port 53
- Restarts and enables the `dnsmasq` service for local DNS functionality
- Downloads MQTT publishing scripts:  
  - `mqtt_publisher.py`  
  - `nxdomain_sender.py`
- Sets up cron jobs to run both scripts every 5 minutes
- Creates installation directory at `/opt/dns-client`

---

## Prerequisites

- Ubuntu/Debian-based system
- Python 3 installed
- Internet connection
- Sudo privileges for installation and service management

---

## Installation

1. Download the setup script:

```bash
curl -O https://raw.githubusercontent.com/4arm/DNSBitranger/refs/heads/main/MQTT%20Setup/Client%20Setup/setup.sh
```

2. Make the script executable:

```bash
chmod +x setup.sh
```

3. Run the script:

```bash
./setup.sh
```

---

## What It Does

- Updates system package index
- Installs `dnsmasq`, `curl`, `python3-pip`, and `ufw`
- Detects and kills any processes running on port 53 to avoid DNS conflicts
- Opens port 53 (DNS) in the firewall via `ufw`
- Restarts and enables `dnsmasq` service
- Creates `/opt/dns-client` directory and downloads MQTT scripts there
- Installs Python packages `paho-mqtt` and `requests`
- Adds cron jobs to run `mqtt_publisher.py` and `nxdomain_sender.py` every 5 minutes

---

## Cron Jobs

The following cron jobs are created (no duplicates):

```bash
*/5 * * * * /usr/bin/python3 /opt/dns-client/mqtt_publisher.py
*/5 * * * * /usr/bin/python3 /opt/dns-client/nxdomain_sender.py
```

To view current cron jobs:

```bash
crontab -l
```

---

## Directory Structure

```
/opt/dns-client/
  ├── mqtt_publisher.py
  └── nxdomain_sender.py
```

---

## Notes

- The setup script requires sudo privileges to install packages, manage services, and modify firewall rules.
- If any process is detected running on port 53, it will be killed to ensure `dnsmasq` can bind to it.
- The MQTT scripts will run periodically via cron to publish DNS client data.
- You can modify or extend the scripts located in `/opt/dns-client/`.
- Make sure the system has internet access during setup to download dependencies and scripts.

---

## License

MIT License or as per the original repository license at [4arm/DNSBitranger](https://github.com/4arm/DNSBitranger).
