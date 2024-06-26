#!/bin/bash

# Function to copy files if they don't already exist
copy_if_not_exists() {
  src=$1
  dest=$2
  if [ -d "$src" ]; then
    for file in "$src"/*; do
      if [ -f "$file" ]; then
        basefile=$(basename "$file")
        if [ ! -f "$dest/$basefile" ]; then
          echo "Copying $file to $dest"
          cp "$file" "$dest"
        fi
      fi
    done
  fi
}

# Copy application files to persistent storage if they don't exist
copy_if_not_exists /app/rubix /app/rubix

# Run the main script
exec /app/rubix/run.sh
