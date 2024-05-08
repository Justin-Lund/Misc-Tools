#!/bin/bash

# Script Name: pcap-query.sh
# Author: Justin Lund
# Last Modified: 04/16/24
# Date Created: 03/14/24
# Version: 1.1
#
## Purpose: Query a folder of PCAPs using TCPDump for an IP address, or list of IPs
#
## Usage:
# ./tcpquery.sh --folder pcaps --ip 127.0.0.1
# ./tcpquery.sh --folder pcaps --input iplist.txt

# Roadmap:
# - Optimize script. This script currently searches for 1 IP at a time, which is slow to run against a large number of PCAPs

############################################################

# Initialize variables
FOLDER=""
IP_ADDRESS=""
IP_FILE=""

# Function to print usage
usage() {
    echo "Usage: $0 --folder <target folder> (--ip <IP address> | --input <file with IP addresses>)"
    exit 1
}

# Parse command line options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --folder) FOLDER="$2"; shift ;;
        --ip) IP_ADDRESS="$2"; shift ;;
        --input) IP_FILE="$2"; shift ;;
        *) usage ;;
    esac
    shift
done

# Check mandatory folder option and at least one of IP or input options
if [[ -z "$FOLDER" || ( -z "$IP_ADDRESS" && -z "$IP_FILE" ) ]]; then
    usage
fi

# Function to search for IP addresses in pcap files
search_ip() {
    local ip=$1
    for file in "$FOLDER"/*.pcap; do
        OUTPUT=$(tcpdump -nr "$file" src "$ip" or dst "$ip" 2>/dev/null)
        if [ ! -z "$OUTPUT" ]; then
            echo ""
            echo "Match found in $file for IP $ip:"
            echo "$OUTPUT" | grep --color=always "$ip"
        fi
    done
}

# Handle direct IP address
if [ ! -z "$IP_ADDRESS" ]; then
    search_ip "$IP_ADDRESS"
fi

# Handle IP list from file
if [ ! -z "$IP_FILE" ]; then
    while IFS= read -r line; do
        search_ip "$line"
    done < "$IP_FILE"
fi
