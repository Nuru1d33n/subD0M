#!/bin/bash

# Directory for the GitHub repository
REPO_DIR="$HOME/Projects/Tools/subD0M"  
GIT_REPO_URL="https://github.com/Nuru1d33n/subD0M"

# Function to check if the directory is a git repository
function check_git_repo {
    if [ ! -d "$REPO_DIR/.git" ]; then
        echo "Error: This is not a valid Git repository."
        echo "Please make sure you are in the correct directory."
        exit 1
    fi
}

# Function to update the repository
function update_repo {
    echo "Pulling the latest updates from the repository..."
    cd "$REPO_DIR" || { echo "Directory $REPO_DIR not found!"; exit 1; }

    # Check if we are in the git repository
    check_git_repo

    # Pull the latest changes
    git fetch --all
    git reset --hard origin/main  # Resets local changes to match the remote `main` branch

    if [ $? -eq 0 ]; then
        echo "Successfully pulled the latest changes from $GIT_REPO_URL"
    else
        echo "Error: Failed to update the repository."
        exit 1
    fi
}

# Main entry point
update_repo
