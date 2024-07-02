#!/bin/bash
logfilerubix="/home/saishibu/cronlog/rubixstartup.log"
logfileBridge="/home/saishibu/cronlog/bridgestartup.log"

#screen -dmS node2 -L -Logfile $log_file $runfile
echo "Starting Rubix" >> $logfilerubix
screen -dmS rubix /home/saishibu/Rubix-Docker/rubix/rubixgoplatform run -p node1 -n 0 -s -port 20000 -testNet -grpcPort 10500
echo "Started Rubix" >> $logfilerubix

echo "Starting Bridge" >> $logfileBridge
screen -dmS bridge /home/saishibu/Rubix-Docker/middleware/bridge.py
echo "Started Bridge" >> $logfileBridge
