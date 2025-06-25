#!/bin/bash

# CONFIG
NAMED_CONF="/etc/bind/named.conf.options"
QUERY_LOG="/var/log/bind9/queries.log"
ALERT_JSON="/var/www/html/alert.json"
ALERT_LOG="/var/log/dns_acl_alerts.log"

# Parse IPs from ACL in named.conf.options
get_acl_ips() {
    awk '/acl[[:space:]]+goodclients[[:space:]]*\{/,/\}/' "$NAMED_CONF" \
    | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' \
    | sort -u
}

# Load whitelisted IPs into array
readarray -t WHITELIST < <(get_acl_ips)

# Start monitoring query log
tail -Fn0 "$QUERY_LOG" | while read -r line; do
    SRC_IP=$(echo "$line" | grep -oP 'client [^:]+: \K[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
    
    if [ -n "$SRC_IP" ]; then
        # Check if IP is in whitelist
        if ! printf '%s\n' "${WHITELIST[@]}" | grep -qx "$SRC_IP"; then
            TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
            MSG="⚠️ Unauthorized DNS access from $SRC_IP at $TIMESTAMP"
            echo "$MSG" | tee -a "$ALERT_LOG"
            
            # Append to alert.json
            jq --arg time "$TIMESTAMP" \
               --arg device "$SRC_IP" \
               --arg type "dns" \
               --arg msg "Unauthorized DNS access attempt" \
               '. += [{"timestamp": $time, "device_name": $device, "type": $type, "message": $msg}] | . |= (.[-50:] // .)' \
               "$ALERT_JSON" > tmp_alert.json && mv tmp_alert.json "$ALERT_JSON"
        fi
    fi
done
