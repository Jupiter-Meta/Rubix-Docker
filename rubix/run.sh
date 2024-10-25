#!/bin/bash
cd /app/rubix/

#Start Rubix Node
./rubixgoplatform run -p node1 -n 0 -s &

# Wait for the Rubix application to start
echo "Waiting for Rubix application to start..."
sleep 30


# # Check if node1 directory exists
# if [ ! -d "./node1/.ipfs" ]; then
#   echo "node1 directory does not exist. Creating it now."
#   mkdir -p ./node1/.ipfs
# fi

# # Set IPFS_PATH environment variable for node1
# export IPFS_PATH=./node1/.ipfs/

# # Remove existing bootstraps
# ./ipfs bootstrap rm --all

# # Add new bootstrap
# ./ipfs bootstrap add /ip4/103.209.145.177/tcp/4001/p2p/12D3KooWD8Rw7Fwo4n7QdXTCjbh6fua8dTqjXBvorNz3bu7d9xMc

# # Swarm connect
# ./ipfs swarm connect /ip4/103.209.145.177/tcp/4001/p2p/12D3KooWD8Rw7Fwo4n7QdXTCjbh6fua8dTqjXBvorNz3bu7d9xMc

cd /app/middleware
python3 /app/middleware/bridge.py
