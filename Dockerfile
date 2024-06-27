# Use an official Ubuntu as a parent image
FROM python:3.9-slim

# Create app directory
WORKDIR /app

# COPY . /app

# Copy Rubix application files to the container
COPY rubix /app/rubix

# Copy Flask middleware files to the container
COPY middleware /app/middleware

COPY kubernetes /app/kubernetes

# COPY entrypoint.sh .
# RUN chmod +x entrypoint.sh

# Install Flask
RUN pip3 install Flask Flask-Cors requests

RUN chmod +x /app/rubix/ipfs
RUN chmod +x /app/rubix/run.sh
# Expose ports for Rubix and Flask
EXPOSE 11500 20000 5002 4002 5050 22010 8081

# CMD /app/rubix/rubixgoplatform run -p node1 -n 0 -s -testNet & python3 /app/middleware/bridge.py

# Start Rubix and Flask middleware
CMD  /app/rubix/run.sh
# ENTRYPOINT ["./entrypoint.sh"]
