import paho.mqtt.client as mqtt
import json
import mysql.connector
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    print(f"[+] Connected to broker with result code {rc}")
    client.subscribe("dns/registration", qos=1)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        serial = payload.get("serial_number")
        ip = payload.get("public_ip")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f"[+] Received from {serial} at {ip}")

        conn = mysql.connector.connect(
            host="localhost",
            user="izham",
            password="mysqlpasswd",
            database="dns_database",
            ssl_disabled=True  # ❗ Only if your Python SSL is broken
        )
        cursor = conn.cursor()
        cursor.execute("""
            REPLACE INTO device (serial_number, device_name, public_ip)
            VALUES (%s, %s, %s)
        """, (serial, f"{serial}-auto", ip))
        conn.commit()
        conn.close()
        print(f"[✓] Stored in DB at {now}")

    except Exception as e:
        print(f"[!] Error handling message: {e}")

client = mqtt.Client(client_id="dns-reg-subscriber")
client.username_pw_set("mqttuser", "mqqtpasswd")
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("localhost", 1883, 60)
    client.loop_forever()
except Exception as e:
    print(f"[!] MQTT connection failed: {e}")
