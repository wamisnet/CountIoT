#!/bin/sh
git reset --hard
git pull
cd ..
cp -r batOrigin/ bat/
chmod 755 bat/*