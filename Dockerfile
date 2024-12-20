# Use NVIDIA CUDA base image with Ubuntu 20.04
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    sudo \
    git \
    wget \
    build-essential \
    libx11-6 \
    libgl1-mesa-glx \
    libxrender1 \
    libglu1-mesa \
    libglib2.0-0 \
    libegl1-mesa-dev \
    libgles2-mesa-dev \
    libosmesa6-dev && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user 'ci' with sudo privileges
RUN useradd -ms /bin/bash ci && \
    echo 'ci:password' | chpasswd && \
    echo 'ci ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ci

# Switch to user 'ci'
USER ci
WORKDIR /home/ci

# Set up virtual environment
RUN python3.11 -m venv venv
ENV PATH="/home/ci/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install PyTorch with CUDA support, Genesis, and Gradio
RUN pip install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install genesis-world gradio

# Clone the Genesis repository (assuming it's public)
RUN git clone https://github.com/Genesis-Embodied-AI/Genesis.git /home/ci/Genesis

# Install Genesis in editable mode
RUN pip install -e /home/ci/Genesis

# Expose port for Gradio UI
EXPOSE 7860

# Set entrypoint
CMD ["bash", "start.sh"]
