#!/bin/bash
apt update -y
apt upgrade -y
apt install python -y
apt install openjdk-17-jdk -y
apt install wget -y
apt install ncurses-utils -y
apt install jq -y
apt install git -y
termux-setup-storage
cd storage
git clone https://github.com/decipher3114/Revancify
cd Revancify
bash revancify
bash main.sh
