#!/bin/bash
### BEGIN INIT INFO
# Provides:          startWalk.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start program RobotWalk.py
# Description:       Start program RobotWalk.py
### END INIT INFO

python /home/pi/Documents/Python/RobotWalk.py
