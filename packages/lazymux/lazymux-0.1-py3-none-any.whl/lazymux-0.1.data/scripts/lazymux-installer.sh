#!/bin/bash
apt update -y
apt upgrade -y
apt install python -y
apt install git -y
cd $HOME
git clone https://github.com/Gameye98/Lazymux
cd Lazymux
python lazymux.py