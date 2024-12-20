# Use NVIDIA CUDA base image with Ubuntu 20.04
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

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
    libosmesa6-dev \
    g++ \
    libboost-all-dev \
    libeigen3-dev \
    libode-dev \
    libyaml-cpp-dev \
    libssl-dev \
    # OMPL dependencies
    libboost-filesystem-dev \
    libboost-system-dev \
    libboost-program-options-dev \
    libboost-serialization-dev \
    castxml \
    libccd-dev \
    libfcl-dev \
    ninja-build \
    # LuisaRender dependencies
    patchelf \
    libvulkan-dev \
    zlib1g-dev \
    xorg-dev \
    libsnappy-dev && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install CMake 3.18+ from source
RUN wget https://github.com/Kitware/CMake/releases/download/v3.18.6/cmake-3.18.6.tar.gz && \
    tar -zxvf cmake-3.18.6.tar.gz && \
    cd cmake-3.18.6 && \
    ./bootstrap && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf cmake-3.18.6 cmake-3.18.6.tar.gz && \
    hash -r

# Create a non-root user 'ci' with sudo privileges
RUN useradd -ms /bin/bash ci && \
    echo 'ci:password' | chpasswd && \
    echo 'ci ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ci && \
    mkdir -p /home/ci && \
    chown -R ci:ci /home/ci

# Copy install script and set permissions
COPY --chown=ci:ci install.sh /home/ci/install.sh
RUN chmod +x /home/ci/install.sh

# Switch to user 'ci' and run installation
USER ci
WORKDIR /home/ci

# Set up virtual environment
ENV PATH="/home/ci/venv/bin:$PATH" \
    PYTHON_VERSION=3.10 \
    PYTHON_INCLUDE_DIR=/usr/include/python3.10 \
    PYTHON_LIBRARY=/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so

RUN python3.10 -m venv venv

# Run installation script
RUN /home/ci/install.sh

# Install additional Python packages
RUN pip install "pybind11[global]" gradio

# Expose port for Gradio UI
EXPOSE 7860

# Set entrypoint
CMD ["bash", "start.sh"]
