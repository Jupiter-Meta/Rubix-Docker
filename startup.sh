#!/bin/bash
logfilerubix="/home/irctc/cronlog/rubixstartup.log"
logfileBridge="/home/irctc/cronlog/bridgestartup.log"

#screen -dmS node2 -L -Logfile $log_file $runfile
echo "Starting Rubix" >> $logfilerubix
screen -dmS rubix /home/irctc/Rubix-Docker/rubix/rubixgoplatform run -p node1 -n 0 -s -port 20000 -testNet -grpcPort 10500
echo "Started Rubix" >> $logfilerubix

echo "Starting Bridge" >> $logfileBridge
screen -dmS rubix /home/irctc/Rubix-Docker/middleware/bridge.py
echo "Started Bridge" >> $logfileBridge
