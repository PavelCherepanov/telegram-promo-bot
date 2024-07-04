#! /bin/bash
sudo apt update
mkdir /tgPromoBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
