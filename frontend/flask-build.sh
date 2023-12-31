#!/bin/sh
echo "Running ${0} script..."

# 1. Accepts an optional argument "flask_dir"
flask_dir=${1}

# 2. Set the BUILD_PATH to "build/"
BUILD_PATH="build/"
export BUILD_PATH

# 3. Run the command "npm run build" in the current directory
echo "Running \"npm run build\" script:"
npm run build

# 4. Create the "templates/" directory and move index.html into it, move other files into the "static/" folder
echo "Reorganizing build directory..."
mkdir -p "$BUILD_PATH/templates/"
mv "$BUILD_PATH/index.html" "$BUILD_PATH/templates/"
find "$BUILD_PATH" -maxdepth 1 -type f -not -name "index.html" -exec mv {} "$BUILD_PATH/static/" \;

# Check if flask_dir is provided
if [ -n "$flask_dir" ]; then
  # Move static/ and templates/ to flask_dir
  echo "Moving files into flask application directory..."
  mv "$BUILD_PATH/static/" "$flask_dir/"
  mv "$BUILD_PATH/templates/" "$flask_dir/"
  rmdir "$BUILD_PATH"
else
  echo "No flask directory provided. Script ends."
fi
