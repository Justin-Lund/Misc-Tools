#!/bin/bash
#
# Script Name: compare-csvs.sh
# Author: Justin Lund
# Last Modified: 04/16/24
# Date Created: 07/04/24
# Version: 0.8
#
## Purpose:
# This script will compare 1 specific column from 2 separate CSV files for matches & differences.
#
## Usage:
# ./compare-csvs.sh --csv1 usernames_from_alert.csv --csv2 aduserlookup.csv
# 
## Roadmap:
# - Add parameter option to specify the output to display (CSV1, CSV2, Matches)
# - Add parameter option to save output to file
#    - Output file should be a CSV with 3 columns, 1 for each results section
# - I may re-write this in Python for easier-to-read code
#
#
########## Usage example: ##########
# This example will look to see if entries in "usernames_from_alert.csv" are also in "aduserlookup.csv"
# It will prompt you to select the column that the usernames are in
#
# ./compare-csvs.sh --csv1 usernames_from_alert.csv --csv2 aduserlookup.csv
# Columns in usernames_from_alert.csv:
# 1         UserName
# Enter number of column to compare from CSV 1: 1
#
# Columns in aduserlookup.csv:
# 1         Name
# 2         Login ID
# Enter number of column to compare from CSV 2: 2
#
# ====== Entries that are in both CSVs ======
# user1
# user2
# user3
#
# ====== Entries that are in CSV1 but not in CSV2 ======
# user4
# user5
#
# ====== Entries that are in CSV2 but not in CSV1 ======
# user6
# user7
#
##############################################


# Usage function
usage() {
    echo "Usage: $0 --csv1 file1 --csv2 file2"
    exit 1
}

# Check arguments
if [ $# -ne 4 ]; then
    usage
fi

# Parse arguments
while [ "$1" != "" ]; do
    case $1 in
        --csv1) shift
                CSV1=$1
                ;;
        --csv2) shift
                CSV2=$1
                ;;
        *)      usage
    esac
    shift
done

# Check if files exist
if [ ! -f "$CSV1" ] || [ ! -f "$CSV2" ]; then
    echo "One or both files do not exist."
    exit 1
fi

# Display columns of CSV1 and CSV2
echo "Columns in $CSV1:"
head -n 1 $CSV1 | tr ',' '\n' | nl -n ln
echo ""
read -p "Enter number of column to compare from CSV 1: " COLUMN1

echo "Columns in $CSV2:"
head -n 1 $CSV2 | tr ',' '\n' | nl -n ln
echo ""
read -p "Enter number of column to compare from CSV 2: " COLUMN2
echo ""

# Find entries that are in both CSVs
echo ""
echo "====== Entries that are in both CSVs ======"
awk -F, -v col1="$COLUMN1" -v col2="$COLUMN2" 'FNR>1 && NR==FNR{a[$col1];next} FNR>1 && ($col2 in a){print $col2}' $CSV1 $CSV2

# Find entries that are in CSV1 but not in CSV2
echo ""
echo "====== Entries that are in CSV1 but not in CSV2 ======"
awk -F, -v col1="$COLUMN1" -v col2="$COLUMN2" 'FNR>1 && NR==FNR{a[$col2];next} FNR>1 && !($col1 in a){print $col1}' $CSV2 $CSV1

# Find entries that are in CSV2 but not in CSV1
echo ""
echo "====== Entries that are in CSV2 but not in CSV1 ======"
awk -F, -v col1="$COLUMN1" -v col2="$COLUMN2" 'FNR>1 && NR==FNR{a[$col1];next} FNR>1 && !($col2 in a){print $col2}' $CSV1 $CSV2

