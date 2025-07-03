
# DNS Device Whitelist System (MQTT-Based)

This project provides a secure and scalable method for DNS devices (e.g., Raspberry Pi running BIND9) inside private networks to register themselves to a public server using MQTT. The public server then updates a MySQL database with the device's `serial_number` and `public_ip` to manage a dynamic whitelist (e.g., for BIND9 ACLs).

---

## 📦 Components

| Component         | Role                                             |
|------------------|--------------------------------------------------|
| **MQTT Broker**   | Public-facing Mosquitto server                   |
| **MQTT Publisher**| Runs on each private DNS device to send its info|
| **MQTT Subscriber**| Runs on public server, stores info in MySQL     |
| **MySQL DB**      | Stores whitelist info (serial, IP, device name) |
| **BIND9 ACL**     | Uses exported IP list to control access          |

---

## 🧪 Example Data Flow

1. DNS device fetches its public IP.
2. Publishes `serial_number` + `public_ip` to `dns/registration` topic.
3. Public server subscribes to topic, receives data.
4. Data is inserted into MySQL `device` table.
5. A cronjob or script regenerates BIND9 ACLs from this DB.

---

## 📁 File Structure

```
/etc/bind/
├── mqtt_publisher.py          # Runs on local DNS device
├── mqtt_subscriber.py         # Runs on public server
├── whitelist_export.py        # Optional: generate whitelist.acl
```

---

## 📌 Prerequisites

### Public Server:
- Ubuntu/Debian system
- Mosquitto (`sudo apt install mosquitto`)
- MySQL or MariaDB
- Python 3 + packages:
  ```bash
  pip install paho-mqtt mysql-connector-python
  ```

### DNS Client (Raspberry Pi or similar):
- Python 3 + packages:
  ```bash
  pip install paho-mqtt requests
  ```

---

## ⚙️ MQTT Publisher (Client Device)

### Location: `/etc/bind/mqtt_publisher.py`
Publishes serial number and public IP to the central MQTT server.

```bash
sudo python3 /etc/bind/mqtt_publisher.py
```

Add to `crontab` for automation:
```bash
*/5 * * * * /usr/bin/python3 /etc/bind/mqtt_publisher.py
```

---

## 🧩 MQTT Subscriber (Public Server)

### Location: `/etc/bind/mqtt_subscriber.py`

Receives device info and writes it to MySQL `device` table.

Run manually:
```bash
python3 /etc/bind/mqtt_subscriber.py
```

Or run it as a systemd service (optional).

---

## 🛠️ Database Schema

```sql
CREATE DATABASE dns_database;

USE network_management;

CREATE TABLE client (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255),
    contact VARCHAR(255)
);

CREATE TABLE device (
    device_id INT PRIMARY KEY AUTO_INCREMENT,
    serial_number VARCHAR(255) UNIQUE,
    device_name VARCHAR(255),
    public_ip VARCHAR(45),
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE device_assignment (
    client_id INT,
    device_id INT,
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);
```

---

## 🔒 Security Notes

- Secure MQTT with TLS in production.
- Use strong credentials for `mqttuser`.
- Sanitize and validate incoming data.
- Whitelist devices by serial or IP depending on your ACL strategy.

---

## 📤 Exporting to BIND9 ACL (Optional)

You can use `whitelist_export.py` to write allowed IPs to `/etc/bind/whitelist.acl`, then reload BIND9:
```bash
sudo rndc reload
```

Schedule with:
```bash
crontab -e
*/5 * * * * /usr/bin/python3 /etc/bind/whitelist_export.py && sudo rndc reload
```

---

## 📈 Example MQTT Message Format

```json
{
  "serial_number": "SN123456",
  "public_ip": "203.80.23.229"
}
```

---

## 📚 References

- [paho-mqtt Python Docs](https://pypi.org/project/paho-mqtt/)
- [Mosquitto Official Docs](https://mosquitto.org/)
- [MySQL Connector Python Docs](https://dev.mysql.com/doc/connector-python/en/)
