# Use an official Ubuntu as a parent image
# FROM python:3.9-slim

FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


# Create app directory
WORKDIR /app

COPY bridge.py /app

# Copy Rubix application files to the container
COPY rubix /app/rubix

# Copy Flask middleware files to the container

COPY rubix/ipfs /app

# COPY kubernetes /app/kubernetes

# COPY entrypoint.sh .
# RUN chmod +x entrypoint.sh

# Install Flask
RUN pip3 install Flask Flask-Cors requests

RUN chmod +x /app/rubix/ipfs
RUN chmod +x /app/rubix/rubixgoplatform
# RUN chmod +x /app/rubix/run.sh
# Expose ports for Rubix and Flask
EXPOSE 11500 20000 5002 4002 5050 22010 8081

CMD python3 bridge.py & /app/rubix/rubixgoplatform run -p node1 -n 0 -s


# Start Rubix and Flask middleware
# CMD  /app/rubix/run.sh
# ENTRYPOINT ["./entrypoint.sh"]
