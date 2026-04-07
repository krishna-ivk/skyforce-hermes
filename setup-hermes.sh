#!/bin/bash

# Setup script for Hermes Agent in Skyforce Workspace

echo "Installing Hermes Agent..."

# Install via official script
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

echo "Hermes installation attempted. Please reload your shell (source ~/.bashrc)."
echo "Then you can run: hermes setup"
