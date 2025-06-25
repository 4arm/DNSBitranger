#!/bin/bash

LOG_FILE="/var/log/bind9/queries.log"
CHECKED="/var/log/bind9/nxdomain_checked.log"
BLOCKLIST="/etc/bind/quad9_blocked_domains.txt"

tail -Fn0 "$LOG_FILE" | while read -r line; do
    domain=$(echo "$line" | grep -oP '(?<=query: ).*?(?= IN)')
    [ -z "$domain" ] && continue
    grep -qx "$domain" "$CHECKED" && continue

    echo "Checking domain: $domain"

    # DNS check
    quad9_result=$(dig @"9.9.9.9" +short "$domain")
    google_result=$(dig @"8.8.8.8" +short "$domain")

    if [ -z "$quad9_result" ] && [ -z "$google_result" ]; then
        echo "✅ Confirmed NXDOMAIN: $domain"
    else
        # Check quad9.net blocklist via web
        status=$(curl -s "https://quad9.net/result/$domain" | grep -oE 'BLOCKED|UNBLOCKED')

        if [[ "$status" == "BLOCKED" ]]; then
            echo "⚠️ Domain $domain is BLOCKED by Quad9."
            # Add to local blocklist if not already present
            grep -qxF "$domain" "$BLOCKLIST" || echo "$domain" >> "$BLOCKLIST"
        else
            echo "✅ Domain $domain is NOT blocked by Quad9."
        fi
    fi

    echo "$domain" >> "$CHECKED"
done
