#!/bin/bash

# CONFIG
SERIAL_NUMBER="SN121298"
SERVER="http://203.80.23.229/dns/update_ip.php"  # Replace with your actual server address

# GET PUBLIC IP
PUBLIC_IP=$(curl -s https://api.ipify.org)

# POST TO SERVER
curl -X POST -d "serial_number=$SERIAL_NUMBER&public_ip=$PUBLIC_IP" $SERVER
