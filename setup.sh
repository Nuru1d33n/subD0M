#!/bin/bash

# This script will make the Python script executable from the command line

# Define variables
PYTHON_SCRIPT="subD0M.py"   # This is the name of your Python script
TARGET_DIR="/usr/local/bin"   # Directory to place the script (default: /usr/local/bin)
SHEBANG="#!/usr/bin/env python3"   # Shebang for the Python script

# Check if the script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT does not exist. Make sure the script is in the current directory."
    exit 1
fi

# Check if the script already has the shebang line
if ! head -n 1 "$PYTHON_SCRIPT" | grep -q "$SHEBANG"; then
    echo "Adding shebang line to $PYTHON_SCRIPT..."
    # Prepend the shebang line to the Python script
    sed -i "1s|^|$SHEBANG\n|" "$PYTHON_SCRIPT"
else
    echo "Shebang already exists in $PYTHON_SCRIPT."
fi

# Make the Python script executable
echo "Making $PYTHON_SCRIPT executable..."
chmod +x "$PYTHON_SCRIPT"

# Check if the target directory is writable
if [ ! -w "$TARGET_DIR" ]; then
    echo "Error: Cannot write to $TARGET_DIR. You may need to run this script with sudo."
    echo "Please run the script again with sudo if needed."
    exit 1
fi

# Move the script to the target directory
echo "Moving $PYTHON_SCRIPT to $TARGET_DIR..."
sudo mv "$PYTHON_SCRIPT" "$TARGET_DIR"

# Alternatively, you can create a symlink instead of moving the script
# sudo ln -s "$(pwd)/$PYTHON_SCRIPT" "$TARGET_DIR/$PYTHON_SCRIPT"

# Confirm the script is now in the PATH
echo "Verifying the script is in the PATH..."
if command -v subD0M &> /dev/null; then
    echo "Success: The script is now installed and accessible as a command-line tool."
else
    echo "Error: The script was not found in the PATH."
fi

# Provide usage instructions
echo -e "\nTo use the tool, you can now run:"
echo -e "subD0M -t <target_domain> [-f <wordlist_file>] [-o <output_file>] [--json <json_file>] [--csv <csv_file>]\n"
