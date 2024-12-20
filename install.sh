#!/bin/bash

set -e  # Exit on error

echo "Starting installation..."

# Update and install system dependencies
sudo apt-get update
sudo apt-get install -y software-properties-common sudo git wget build-essential libx11-6 libgl1-mesa-glx libxrender1 libglu1-mesa libglib2.0-0 libegl1-mesa-dev libgles2-mesa-dev libosmesa6-dev

# Add deadsnakes PPA for Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update

# Install Python 3.11 and pip
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Create a virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
pip install genesis-world gradio

# Clone the Genesis repository
git clone https://github.com/Genesis-Embodied-AI/Genesis.git
cd Genesis

# Install Genesis in editable mode
pip install -e .

echo "Installation completed successfully."
