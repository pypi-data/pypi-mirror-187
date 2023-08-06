#!/bin/bash

parent=$(dirname $(dirname $(realpath $0)))

mkdir bin

chmod +x reconfigurator/reconfigurator.py
ln -s ../reconfigurator/reconfigurator.py bin/reconfigurator
    
export_path='export PATH="$PATH:parent/../bin/"'
export_path=${export_path/parent/$parent}
echo $export_path >> ~/.bashrc
source ~/.bashrc

echo "Reconfigurator CLI added!"


