#!/bin/bash

set -e  # Exit on error

echo "Starting Genesis Simulation UI..."

# Activate the virtual environment
source venv/bin/activate

# Navigate to Genesis directory
# Launch the Gradio UI
python genesis_ui.py

echo "Genesis Simulation UI has been launched."
