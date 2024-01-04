#!/bin/sh

# Log function to print messages with script name
log() {
  script_name=$(basename "$0")
  echo "[$script_name] >>> $1"
}

# Accepts an optional argument "flask_dir"
flask_dir=${1}

# Set the BUILD_PATH to "react-build/"
BUILD_PATH="react-build/"
export BUILD_PATH

# Set the base url for api calls to be blank
REACT_APP_API_URL=""
export REACT_APP_API_URL

# Run the command "npm run build" in the current directory
log "Running \"npm run build\" script..."
npm run build

# Move files except index.html into the "static/" folder
log "Reorganizing build directory..."
find "$BUILD_PATH" -maxdepth 1 -type f -not -name "index.html" -exec mv {} "$BUILD_PATH/static/" \;

# Check if flask_dir is provided
if [ -n "$flask_dir" ]; then

  # Check if react/ directory already exist in flask_dir
  if [ -d "$flask_dir/$BUILD_PATH" ]; then
    log "Deleting existing $BUILD_PATH/ in $flask_dir..."
    rm -r "$flask_dir/$BUILD_PATH"
  fi

  # Move files into flask_dir
  log "Moving files into flask application directory..."
  mv "$BUILD_PATH" "$flask_dir"
else
  log "No flask directory provided. Script ends."
fi
