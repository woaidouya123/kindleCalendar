#!/bin/sh
eips -c
nohup python3 -u /mnt/us/extensions/KindleCalendar/src/layout.py > /mnt/us/extensions/KindleCalendar/src/log.log 2>&1 &
