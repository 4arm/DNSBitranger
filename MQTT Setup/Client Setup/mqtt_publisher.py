import paho.mqtt.client as mqtt
import json
import requests

def get_public_ip():
    try:
        return requests.get("https://ifconfig.me", timeout=5).text.strip()
    except Exception as e:
        print(f"[!] Failed to get public IP: {e}")
        return "0.0.0.0"

DEVICE_INFO = {
    "serial_number": "SN123456",
    "public_ip": get_public_ip()
}

client = mqtt.Client(client_id="dns-" + DEVICE_INFO["serial_number"])

# OPTIONAL: Use username/password if broker requires it
client.username_pw_set("mqttuser", "Muhd2003@")

try:
    client.connect("203.80.23.229", 1883, 60)
    client.publish("dns/registration", json.dumps(DEVICE_INFO), qos=1)
    print("[+] Sent device info:", DEVICE_INFO)
    client.disconnect()
except Exception as e:
    print(f"[!] MQTT publish failed: {e}")
