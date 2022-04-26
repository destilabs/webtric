#!/bin/bash
# Script to parse quotes site
#

# Validation of first argument - path to output folder
if [ -z "$1" ]
  then
    echo "Supply an output path as the first argument.";
fi

# Validation of second argument - type of driver to be used
# local - means you are using the local driver and chromedriver installed
# remote - means you are using the remote driver from docker hub (expecting it to be on localhost:4444)
if [ -z "$2" ]
  then
    echo "Configure what driver should be used [local, remote] as the second argument.";
fi

OUTPUT_PATH=$1;

# Checks whether you have virtualenv installed and venv created
# If not, it will install virtualenv and create a new one
# Then it would activate the virtualenv
FILE=venv/bin/activate
if test -f "$FILE"; 
then
    source venv/bin/activate
else
    python -m pip install virtualenv
    python -m virtualenv venv
    pip install -r requirements.txt
    source venv/bin/activate
fi

# Removes the old output folder
rm -f "${OUTPUT_PATH}/$(date +%Y-%m-%d).json"
# Executes the scraper
python -m spider -c "./configs/quotes.yaml" -o "${OUTPUT_PATH}/$(date +%Y-%m-%d).csv" -m $2