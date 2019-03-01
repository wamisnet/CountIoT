#!/bin/sh
git reset --hard
git pull
cd /home/countit/CountIoT
cp -r batOrigin/* bat/
chmod 755 bat/*