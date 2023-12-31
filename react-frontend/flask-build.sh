#!/bin/sh

# Accepts an optional argument "flask_dir"
flask_dir=${1}

# Set the BUILD_PATH to "build/"
BUILD_PATH="build/"
export BUILD_PATH

# Set the base url for api calls to be blank
REACT_APP_API_URL=""
export REACT_APP_API_URL

# Run the command "npm run build" in the current directory
echo "Running \"npm run build\" script:"
npm run build

# Move files into the "static/" folder
echo "Reorganizing build directory..."
find "$BUILD_PATH" -maxdepth 1 -type f -exec mv {} "$BUILD_PATH/static/" \;

# Check if flask_dir is provided
if [ -n "$flask_dir" ]; then
  # Move static/ and templates/ to flask_dir
  echo "Moving files into flask application directory..."
  mv "$BUILD_PATH/static/" "$flask_dir/"
  rmdir "$BUILD_PATH"
else
  echo "No flask directory provided. Script ends."
fi
