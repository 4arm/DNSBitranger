# generate_bind_blockzones.py
import os

BLOCK_LIST = "/etc/bind/blockeddomain.txt"
ZONE_CONF = "/etc/bind/named.conf.blocked"
ZONE_DIR = "/etc/bind/blocked_zones"
REDIRECT_IP = "192.168.1.100"

os.makedirs(ZONE_DIR, exist_ok=True)

with open(BLOCK_LIST, "r") as f:
    domains = [line.strip() for line in f if line.strip()]

with open(ZONE_CONF, "w") as f:
    for domain in domains:
        zone_file = os.path.join(ZONE_DIR, f"{domain}.zone")
        f.write(f"""
zone "{domain}" {{
    type master;
    file "{zone_file}";
}};
""")
        with open(zone_file, "w") as zf:
            zf.write(f"""
$TTL 1h
@   IN  SOA ns.{domain}. admin.{domain}. (
        1       ; serial
        1h      ; refresh
        15m     ; retry
        1w      ; expire
        1h )    ; minimum

    IN  NS  ns.{domain}.
ns  IN  A   {REDIRECT_IP}
@   IN  A   {REDIRECT_IP}
*   IN  A   {REDIRECT_IP}
""")

print("Blocked zone files and config generated.")
