#!/bin/bash
while true; do
    unset DEBUG
    /home/shyguy/whereami >> /var/log/whereami.log &
    /bin/sleep 10
done
