# Use an official Ubuntu as a parent image
# FROM python:3.9-slim

FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    supervisor \
    && rm -rf /var/lib/apt/lists/*


# Create app directory
WORKDIR /app

# COPY . /app

# Copy all applications to the container
COPY . .
COPY rubix/* /app/
COPY rubix/rubixgoplatform /app/rubix/
RUN ls -al

# Install Flask
RUN pip3 install Flask Flask-Cors requests

RUN chmod +x /app/rubix/ipfs
RUN chmod +x /app/rubix/rubixgoplatform
# RUN chmod +x /app/rubix/run.sh
# Expose ports for Rubix and Flask
EXPOSE 11500 20000 5002 4002 5050 22010 8081

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]

# CMD python3 /app/bridge.py && /app/rubix/rubixgoplatform run -p node1 -n 0 -s