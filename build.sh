#!/usr/bin/env bash

sudo apt-get install docker vagrant python3.7 python3.7-venv virtualbox-dkms\
linux-headers-generic -y --no-install-recommends
vagrant plugin install vagrant-vbguest vagrant-scp
source venv/bin/activate
pip3.7 install -r startpoint/requirements.txt
