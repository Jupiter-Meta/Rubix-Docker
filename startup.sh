#!/bin/bash
logfilerubix="/cronlog/rubixstartup.log"
logfileBridge="/cronlog/bridgestartup.log"

#screen -dmS node2 -L -Logfile $log_file $runfile
echo "Starting Rubix" >> $logfilerubix
screen -dmS rubix /Rubix-Docker/rubix/rubixgoplatform run -p node1 -n 0 -s -port 20000 -testNet -grpcPort 10500
echo "Started Rubix" >> $logfilerubix

echo "Starting Bridge" >> $logfileBridge
screen -dmS bridge /Rubix-Docker/middleware/bridge.py
echo "Started Bridge" >> $logfileBridge
