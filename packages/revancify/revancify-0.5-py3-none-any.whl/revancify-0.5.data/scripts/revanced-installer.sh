#!/bin/bash
apt update -y
apt upgrade -y
apt install python -y
apt install wget -y
apt install ncurses-utils -y
apt install jq -y
apt install git -y
pip install wheel
pip install bs4
pip install requests
cd $HOME
git clone https://github.com/Bhai4You/Revancify
cd Revancify
bash revancify
bash main.sh