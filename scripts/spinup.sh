#!/usr/bin/env bash

## Name the Linode/subdomain to be created
TOKEN="1130e72b887afd10b9961e035241c2c90c73080ad535e69c88950d22cfa23d77"
LINODE_NAMES=(
    "linode_2"
)
DOMAIN_NAME="wideshotapp.com"

## Get the domain's ID from the Linode APIv4
DOMAIN_ID="$(curl -H "Authorization: Bearer $TOKEN" \
        "https://api.linode.com/v4/domains" | jq -S | \
        grep -A 11 "$DOMAIN_NAME" | grep '"id"' | \
        awk '{print $2}' | sed 's/,//')"

## Create the Linodes
for i in "${LINODE_NAMES[@]}"; do
    curl -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -X POST -d '{
        "backups_enabled": true,
        "swap_size": 512,
        "image": "linode/debian9",
        "root_pass": "aComplexP@ssword",
        "booted": true,
        "label": "'"${i}"'",
        "type": "g6-standard-2",
        "region": "us-east",
        "group": "Linode-Group"
        }' \
        https://api.linode.com/v4/linode/instances
done

## Create the subdomain - this assumes your base domain already exists
## in the Linode DNS Manager
for i in "${LINODE_NAMES[@]}"; do
    curl -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -X POST -d '{
        "type": "A",
        "name": "'"${i}"'",
        "target" : "104.200.31.53",
        "priority": 50,
        "weight": 50,
        "port": 80,
        "service": null,
        "protocol": null,
        "ttl_sec": 604800
        }' \
        "https://api.linode.com/v4/domains/${DOMAIN_ID}/records"
done