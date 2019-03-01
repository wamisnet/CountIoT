#!/bin/sh
sudo echo KERNEL=="ttyUSB*",  ATTRS{interface}=="MONOSTICK", SYMLINK+="ttyUSB_TWELite" >> /etc/udev/rules.d/99-local.rules