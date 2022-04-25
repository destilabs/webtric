#!/bin/bash

source venv/bin/activate
rm -f "./outputs/quotes/$(date +%Y-%m-%d).json"
python -m spider -c "./configs/quotes.yaml" -o "./outputs/quotes/$(date +%Y-%m-%d).csv"