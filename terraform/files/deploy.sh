#!/bin/bash
set -e
APP_DIR=${1:-$HOME}
sleep 1m
sudo apt-get install -y git
sleep 1m
git clone -b monolith https://github.com/express42/reddit.git "$APP_DIR"/reddit
cd "$APP_DIR"/reddit
bundle install
sleep 1m
sudo mv /tmp/puma.service /etc/systemd/system/puma.service
sudo systemctl start puma
sudo systemctl enable puma
