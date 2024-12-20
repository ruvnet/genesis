# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

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
    curl \
    build-essential \
    cmake \
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
    add-apt-repository ppa:ubuntu-toolchain-r/test && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    gcc-11 \
    g++-11 \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 110 && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user 'ci' with sudo privileges
RUN useradd -ms /bin/bash ci && \
    echo 'ci ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    mkdir -p /home/ci && \
    chown -R ci:ci /home/ci

# Switch to user 'ci'
USER ci
WORKDIR /home/ci

# Set up environment in .bashrc
RUN echo 'export PATH="/home/ci/genesis/venv/bin:$PATH"' >> ~/.bashrc && \
    echo 'export VIRTUAL_ENV="/home/ci/genesis/venv"' >> ~/.bashrc && \
    echo 'export PYTHON_VERSION=3.10' >> ~/.bashrc && \
    echo 'export PYTHON_INCLUDE_DIR=/usr/include/python3.10' >> ~/.bashrc && \
    echo 'export PYTHON_LIBRARY=/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so' >> ~/.bashrc && \
    echo 'export CC=/usr/bin/gcc-11' >> ~/.bashrc && \
    echo 'export CXX=/usr/bin/g++-11' >> ~/.bashrc && \
    echo 'export CFLAGS="-fPIC"' >> ~/.bashrc && \
    echo 'export CXXFLAGS="-fPIC"' >> ~/.bashrc

# Copy the project files
COPY --chown=ci:ci . /home/ci/genesis/
WORKDIR /home/ci/genesis

# Create and activate virtual environment
RUN python3.10 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip

# Install Rust and set up environment
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    echo 'source $HOME/.cargo/env' >> ~/.bashrc && \
    . $HOME/.cargo/env && \
    rustc --version

# Copy install script and set permissions
COPY --chown=ci:ci install.sh /home/ci/genesis/install.sh
RUN chmod +x /home/ci/genesis/install.sh

# Create debug script
RUN echo '#!/bin/bash\n\
set -x\n\
. $HOME/.cargo/env\n\
source venv/bin/activate\n\
export PATH="$HOME/.cargo/bin:$PATH"\n\
./install.sh 2>&1 | tee install.log' > debug_install.sh && \
    chmod +x debug_install.sh

# Run installation script with debugging
RUN bash -c ". $HOME/.cargo/env && source venv/bin/activate && ./debug_install.sh"

# Install additional Python packages in virtual environment
RUN bash -c "source venv/bin/activate && pip install 'pybind11[global]' gradio"

# Copy and set permissions for start script
COPY --chown=ci:ci start.sh /home/ci/genesis/start.sh
RUN chmod +x /home/ci/genesis/start.sh

# Create wrapper script for startup
RUN echo '#!/bin/bash\n\
source ~/.bashrc\n\
source venv/bin/activate\n\
export PYTHONPATH=/home/ci/genesis:$PYTHONPATH\n\
python3.10 genesis_ui.py' > run.sh && \
    chmod +x run.sh

# Expose port for Gradio UI
EXPOSE 7860

# Set entrypoint
CMD ["./run.sh"]
