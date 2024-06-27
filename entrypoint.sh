#!/bin/bash

# Function to copy files if they don't already exist
copy_if_not_exists() {
  src=$1
  dest=$2

  # Ensure source directory exists
  if [ ! -d "$src" ]; then
    echo "Source directory $src does not exist."
    return 1
  fi

  # Ensure destination directory exists
  if [ ! -d "$dest" ]; then
    echo "Creating destination directory: $dest"
    mkdir -p "$dest"
  fi

  # Copy files if they don't exist in the destination
  for file in "$src"/*; do
    if [ -f "$file" ]; then
      basefile=$(basename "$file")
      if [ ! -f "$dest/$basefile" ]; then
        echo "Copying $file to $dest"
        cp "$file" "$dest"
      fi
    fi
  done
}


# Example: Copy application files to persistent storage if they don't exist
copy_if_not_exists "/app" "/persistent/app"


# Run the main script or application
exec /persistent/app/run.sh
