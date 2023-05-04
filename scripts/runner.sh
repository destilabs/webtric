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

# Validation of third argument - config
if [ -z "$3" ]
  then
    echo "Configure what config should be used as the third argument.";
fi

OUTPUT_PATH=$1;

# Checks whether you have virtualenv installed and venv created
# If not, it will install virtualenv and create a new one
# Then it would activate the virtualenv
venv_name="venv"

if [ -d "${venv_name}" ]
then
    echo "Virtualenv exists"
    source "${venv_name}/bin/activate"
else
    echo "Virtualenv does not exist"
    echo "Creating virtualenv"
    python3.10 -m pip install virtualenv --quiet 
    python3.10 -m virtualenv -q "${venv_name}"
    source "${venv_name}/bin/activate"
    pip install -r requirements.txt
    echo "Virtualenv created"
fi

# Removes the old output folder
rm -f "${OUTPUT_PATH}/$(date +%Y-%m-%d).json"
# Executes the scraper
python3 -m spider -c $3 -o "${OUTPUT_PATH}/$(date +%Y-%m-%d).csv" -m $2

