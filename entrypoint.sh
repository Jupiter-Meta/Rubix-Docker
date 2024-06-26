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

echo pwd
pwd

echo ls
ls

cd app
echo app ls
ls

# Copy application files to persistent storage if they don't exist
copy_if_not_exists /app /mnt/app

# Run the main script
exec /app/run.sh
