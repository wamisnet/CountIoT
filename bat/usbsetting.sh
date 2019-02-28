#!/bin/sh
sudo echo KERNEL=="ttyUSB*",  ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="ttyUSB_TWELite" >> /etc/udev/rules.d/99-local.rules