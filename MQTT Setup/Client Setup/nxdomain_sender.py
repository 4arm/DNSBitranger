import requests
import time
import re
from datetime import datetime

LOG_FILE = "/var/log/dnsmasq.log"
SERVER_URL = "http://203.80.23.229/dns/nxdomain_api.php"

def get_public_ip():
    try:
        return requests.get("https://ipv4.icanhazip.com", timeout=5).text.strip()
    except Exception as e:
        print(f"[!] Failed to get public IP: {e}")
        return "0.0.0.0"


RESOLVER_IP = get_public_ip()

query_pattern = re.compile(r"query\[\w+\] ([\w\.\-]+) from ([\d\.]+)")
reply_pattern = re.compile(r"reply ([\w\.\-]+) is NXDOMAIN")

query_cache = {}

def follow(log_file):
    with open(log_file, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

for line in follow(LOG_FILE):
    ts_str = line.split("dnsmasq")[0].strip()
    try:
        timestamp = datetime.strptime(ts_str, "%b %d %H:%M:%S")
        timestamp = timestamp.replace(year=datetime.now().year)
    except:
        timestamp = datetime.now()

    query_match = query_pattern.search(line)
    if query_match:
        domain, src_ip = query_match.groups()
        query_cache[domain] = src_ip
        continue

    reply_match = reply_pattern.search(line)
    if reply_match:
        domain = reply_match.group(1)
        source_ip = query_cache.get(domain, "unknown")

        log_entry = {
            "timestamp": timestamp.isoformat(),
            "domain": domain,
            "source_ip": source_ip,
            "resolver_ip": RESOLVER_IP,
            "serial_number": "SN123456"
        }

        try:
            requests.post(SERVER_URL, json=log_entry)
            print(f"Sent NXDOMAIN for {domain} from {source_ip} on {RESOLVER_IP}")
        except Exception as e:
            print("Error sending data:", e)
