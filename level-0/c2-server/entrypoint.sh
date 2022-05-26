#!/bin/bash

su -c 'python -u ./app.py > /dev/null 2>&1 &' bowser
su - koopa
