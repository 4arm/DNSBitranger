# DNS Client Auto-Setup

This script sets up a DNS client that publishes system data to an MQTT broker every 5 minutes using a Python script.

## Features

- Installs necessary dependencies (Python packages, curl, etc.)
- Downloads the `mqtt_publisher.py` script from the official GitHub repository
- Sets up a cron job to run the script every 5 minutes
- Creates an installation directory at `/opt/dns-client`

## Prerequisites

- Ubuntu/Debian-based system
- Internet connection
- Python 3 installed

## Installation

1. Download the setup script:

```bash
curl -O https://example.com/setup.sh  # Replace with actual URL if hosted
```

2. Make the script executable:

```bash
chmod +x setup.sh
```

3. Run the script:

```bash
./setup.sh
```

## What It Does

- Updates your system package index.
- Installs `python3-paho-mqtt`, `python3-pip`, and `curl`.
- Creates `/opt/dns-client` directory and assigns appropriate permissions.
- Downloads `mqtt_publisher.py` from the GitHub repository:
  [4arm/DNSBitranger - mqtt_publisher.py](https://github.com/4arm/DNSBitranger/blob/main/MQTT%20Setup/Client%20Setup/mqtt_publisher.py)
- Installs Python packages: `paho-mqtt` and `requests`.
- Schedules the script to run every 5 minutes via `cron`.

## Cron Job

A cron job is added to run the script every 5 minutes:

```bash
*/5 * * * * /usr/bin/python3 /opt/dns-client/mqtt_publisher.py
```

To view your current cron jobs:

```bash
crontab -l
```

## Directory Structure

- `/opt/dns-client/`
  - `mqtt_publisher.py` — The MQTT publishing script

## Notes

- If the cron job already exists, it will not be duplicated.
- The script assumes `crontab` is available and the user has sufficient permissions.

## License

MIT or as per the repository license at [4arm/DNSBitranger](https://github.com/4arm/DNSBitranger)
