#!/bin/bash

# Enable error handling
set -e

# Configure error handling and logging
log_file="/tmp/install.log"
exec 1> >(tee -a "$log_file")
exec 2> >(tee -a "$log_file" >&2)

# Retry function for commands
retry_command() {
    local -r cmd="${1}"
    local -r description="${2}"
    local -r max_attempts=3
    local -r wait_time=5
    
    echo "Attempting: $description"
    
    for ((attempt = 1; attempt <= max_attempts; attempt++)); do
        if eval "$cmd"; then
            echo "Success: $description"
            return 0
        fi
        
        echo "Attempt $attempt of $max_attempts failed for: $description"
        if [[ $attempt != "$max_attempts" ]]; then
            echo "Waiting $wait_time seconds before retrying..."
            sleep "$wait_time"
        fi
    done
    
    echo "Error: All attempts failed for: $description"
    return 1
}

# Create CMake toolchain file
create_toolchain_file() {
    local toolchain_file="/tmp/toolchain.cmake"
    echo "Creating CMake toolchain file at $toolchain_file"
    
    cat > "$toolchain_file" << EOF
set(CMAKE_C_COMPILER /usr/bin/gcc)
set(CMAKE_CXX_COMPILER /usr/bin/g++)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
EOF
    
    echo "$toolchain_file"
}

# Verify compiler settings
verify_compiler() {
    echo "Verifying C++ compiler settings..."
    
    # Check if g++ exists and is executable
    if ! command -v g++ >/dev/null 2>&1; then
        echo "Error: g++ compiler not found"
        return 1
    fi
    
    # Test compiler functionality
    echo "Testing compiler..."
    local test_file="/tmp/test.cpp"
    echo "int main() { return 0; }" > "$test_file"
    
    if ! g++ -o /tmp/test "$test_file"; then
        echo "Error: Compiler test failed"
        return 1
    fi
    
    # Export compiler settings
    export CC=/usr/bin/gcc
    export CXX=/usr/bin/g++
    export CFLAGS="-fPIC"
    export CXXFLAGS="-fPIC"
    
    echo "C++ compiler verification successful"
    return 0
}

echo "Starting installation..."
echo "Installation log will be written to: $log_file"

# Verify compiler before proceeding
if ! verify_compiler; then
    echo "Error: C++ compiler verification failed. Cannot proceed with installation."
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a package is installed via pip
pip_package_installed() {
    pip show "$1" >/dev/null 2>&1
}

# Function to check if an apt package is installed
apt_package_installed() {
    dpkg -l "$1" >/dev/null 2>&1
}

# Function to check CMake version
check_cmake_version() {
    if command -v cmake >/dev/null 2>&1; then
        version=$(cmake --version | head -n1 | cut -d' ' -f3)
        major=$(echo $version | cut -d'.' -f1)
        minor=$(echo $version | cut -d'.' -f2)
        if [ "$major" -gt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -ge 26 ]); then
            return 0
        fi
    fi
    return 1
}

echo "Checking and installing requirements..."

# Check and install system dependencies
SYSTEM_DEPS=(
    "software-properties-common"
    "git"
    "wget"
    "build-essential"
    "libx11-6"
    "libgl1-mesa-glx"
    "libxrender1"
    "libglu1-mesa"
    "libglib2.0-0"
    "libegl1-mesa-dev"
    "libgles2-mesa-dev"
    "libosmesa6-dev"
    "g++"
    "libboost-all-dev"
    "libeigen3-dev"
    "libode-dev"
    "libyaml-cpp-dev"
    "libssl-dev"
)

MISSING_DEPS=()
for pkg in "${SYSTEM_DEPS[@]}"; do
    if ! apt_package_installed "$pkg"; then
        MISSING_DEPS+=("$pkg")
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "Installing missing system dependencies: ${MISSING_DEPS[*]}"
    sudo apt-get update
    sudo apt-get install -y "${MISSING_DEPS[@]}"
fi

# Install CMake 3.26+ from source if needed
if ! check_cmake_version; then
    echo "Installing CMake 3.26+ from source..."
    CMAKE_VERSION="3.26.5"
    wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}.tar.gz
    tar -zxvf cmake-${CMAKE_VERSION}.tar.gz
    cd cmake-${CMAKE_VERSION}
    ./bootstrap
    make -j$(nproc)
    sudo make install
    cd ..
    rm -rf cmake-${CMAKE_VERSION} cmake-${CMAKE_VERSION}.tar.gz
    hash -r
fi

# Check and install Python 3.10
if ! command_exists python3.10; then
    echo "Installing Python 3.10..."
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get update
    sudo apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.10 -m venv venv
fi
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Check and install Python packages
PYTHON_PKGS=(
    "torch"
    "genesis-world"
)

for pkg in "${PYTHON_PKGS[@]}"; do
    if ! pip_package_installed "$pkg"; then
        echo "Installing $pkg..."
        if [ "$pkg" = "torch" ]; then
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        else
            pip install "$pkg"
        fi
    fi
done

# Install Genesis if needed
if [ ! -d "Genesis" ] || ! pip_package_installed "genesis"; then
    echo "Installing Genesis..."
    if [ -d "Genesis" ]; then
        rm -rf Genesis
    fi
    git clone https://github.com/Genesis-Embodied-AI/Genesis.git
    cd Genesis
    pip install -e .
    cd ..
fi

echo "Installing optional components..."

# 1. Motion Planning (OMPL)
if ! pip_package_installed "ompl"; then
    echo "Installing OMPL..."
    # Install OMPL dependencies
    OMPL_DEPS=(
        "libboost-filesystem-dev"
        "libboost-system-dev"
        "libboost-program-options-dev"
        "libboost-serialization-dev"
        "castxml"
        "libccd-dev"
        "libfcl-dev"
        "ninja-build"
        "python3.10-dev"
    )

    MISSING_OMPL_DEPS=()
    for pkg in "${OMPL_DEPS[@]}"; do
        if ! apt_package_installed "$pkg"; then
            MISSING_OMPL_DEPS+=("$pkg")
        fi
    done

    if [ ${#MISSING_OMPL_DEPS[@]} -ne 0 ]; then
        echo "Installing missing OMPL dependencies: ${MISSING_OMPL_DEPS[*]}"
        sudo apt-get install -y "${MISSING_OMPL_DEPS[@]}"
    fi

    # Install OMPL from source with Python bindings
    if [ ! -d "ompl" ]; then
        echo "Installing OMPL from source..."
        
        # Clone OMPL repository with retry
        retry_command "git clone https://github.com/ompl/ompl.git" "Clone OMPL repository"
        
        cd ompl
        mkdir -p build
        cd build
        
        # Create toolchain file
        local toolchain_file
        toolchain_file=$(create_toolchain_file)
        
        # Configure CMake with retry
        retry_command "cmake .. \
            -DCMAKE_TOOLCHAIN_FILE=$toolchain_file \
            -DPYTHON_EXEC=/usr/bin/python3.10 \
            -DPYTHON_INCLUDE_DIR=/usr/include/python3.10 \
            -DPYTHON_LIBRARY=/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so \
            -DOMPL_BUILD_PYBINDINGS=ON \
            -DOMPL_REGISTRATION=OFF \
            -DOMPL_BUILD_DEMOS=OFF \
            -DOMPL_BUILD_PYTESTS=OFF \
            -DOMPL_BUILD_TESTS=OFF" \
            "Configure OMPL with CMake"
        
        # Build and install with retry
        retry_command "make -j $(nproc)" "Build OMPL"
        retry_command "sudo make install" "Install OMPL"
        
        cd ../py-bindings
        
        # Install Python dependencies with retry
        retry_command "pip install pyplusplus" "Install pyplusplus"
        
        # Create a custom setup.py with correct compiler settings
        cat > setup.py << EOF
from setuptools import setup
from setuptools.command.build_ext import build_ext
import subprocess
import sys
import os

class CustomBuildExt(build_ext):
    def build_extension(self, ext):
        build_temp = os.path.abspath(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        
        cmake_args = [
            'cmake',
            os.path.dirname(os.path.abspath(__file__)),
            f'-DCMAKE_TOOLCHAIN_FILE=/tmp/toolchain.cmake',
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={os.path.abspath(self.build_lib)}',
            f'-DPYTHON_EXEC={sys.executable}',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DOMPL_BUILD_PYBINDINGS=ON',
            '-DOMPL_REGISTRATION=OFF',
            '-DOMPL_BUILD_DEMOS=OFF',
            '-DOMPL_BUILD_PYTESTS=OFF',
            '-DOMPL_BUILD_TESTS=OFF'
        ]
        
        subprocess.run(cmake_args, cwd=build_temp, check=True)
        subprocess.run(['make', '-j', str(os.cpu_count())], cwd=build_temp, check=True)

setup(
    name='ompl',
    version='1.6.0',
    cmdclass={'build_ext': CustomBuildExt},
)
EOF
        
        # Build and install Python bindings with retry
        retry_command "python3.10 setup.py build" "Build OMPL Python bindings"
        retry_command "sudo python3.10 setup.py install" "Install OMPL Python bindings"
        
        cd ../..
        echo "OMPL installation completed successfully"
    fi
fi

# 2. Surface Reconstruction Tools
if ! command_exists splashsurf; then
    echo "Installing surface reconstruction tools..."
    if ! command_exists rustc; then
        echo "Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        . "$HOME/.cargo/env"
    fi
    echo "Installing splashsurf..."
    cargo install splashsurf --force
fi

# Setup ParticleMesher if not already set up
if [ ! -d "Genesis/genesis/ext/ParticleMesher" ]; then
    echo "Setting up ParticleMesher..."
    echo "export LD_LIBRARY_PATH=${PWD}/Genesis/genesis/ext/ParticleMesher/ParticleMesherPy:$LD_LIBRARY_PATH" >> ~/.bashrc
    source ~/.bashrc
fi

# 3. Ray Tracing Renderer (LuisaRender)
if [ ! -d "Genesis/genesis/ext/LuisaRender/build" ]; then
    echo "Installing LuisaRender..."
    # Install GCC 11 if not present
    if ! command_exists gcc-11; then
        sudo apt install -y build-essential manpages-dev
        sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
        sudo apt update && sudo apt install -y gcc-11 g++-11
        sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 110
        sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110
    fi
    
    # Verify CMake version again before proceeding
    if ! check_cmake_version; then
        echo "Error: CMake 3.26+ is required but not found in PATH"
        exit 1
    fi
    
    # Install LuisaRender dependencies
    LUISA_DEPS=(
        "patchelf"
        "libvulkan-dev"
        "zlib1g-dev"
        "xorg-dev"
        "libglu1-mesa-dev"
        "libsnappy-dev"
    )
    
    MISSING_LUISA_DEPS=()
    for pkg in "${LUISA_DEPS[@]}"; do
        if ! apt_package_installed "$pkg"; then
            MISSING_LUISA_DEPS+=("$pkg")
        fi
    done
    
    if [ ${#MISSING_LUISA_DEPS[@]} -ne 0 ]; then
        echo "Installing missing LuisaRender dependencies: ${MISSING_LUISA_DEPS[*]}"
        sudo apt-get install -y "${MISSING_LUISA_DEPS[@]}"
    fi
    
    if ! pip_package_installed "pybind11"; then
        pip install "pybind11[global]"
    fi
    
    # Create toolchain file
    local toolchain_file
    toolchain_file=$(create_toolchain_file)
    
    cd Genesis
    retry_command "git submodule update --init --recursive" "Initialize LuisaRender submodules"
    cd genesis/ext/LuisaRender
    
    retry_command "cmake -S . -B build \
        -DCMAKE_TOOLCHAIN_FILE=$toolchain_file \
        -DCMAKE_BUILD_TYPE=Release \
        -DPYTHON_VERSIONS=3.10 \
        -DLUISA_COMPUTE_DOWNLOAD_NVCOMP=ON \
        -DLUISA_COMPUTE_ENABLE_GUI=OFF" \
        "Configure LuisaRender with CMake"
    
    retry_command "cmake --build build -j $(nproc)" "Build LuisaRender"
    cd ../../..
fi

echo "Installation completed successfully!"
echo "Note: You may need to restart your terminal for some changes to take effect."

# Print installation status
echo -e "\nInstallation Status:"
echo "--------------------"
echo "Core Components:"
python3.10 --version 2>/dev/null && echo "✓ Python 3.10 installed" || echo "✗ Python 3.10 not installed"
pip_package_installed "torch" && echo "✓ PyTorch installed" || echo "✗ PyTorch not installed"
pip_package_installed "genesis-world" && echo "✓ genesis-world installed" || echo "✗ genesis-world not installed"
pip_package_installed "genesis" && echo "✓ Genesis installed" || echo "✗ Genesis not installed"

echo -e "\nOptional Components:"
pip_package_installed "ompl" && echo "✓ OMPL installed" || echo "✗ OMPL not installed"
command_exists splashsurf && echo "✓ splashsurf installed" || echo "✗ splashsurf not installed"
[ -d "Genesis/genesis/ext/ParticleMesher" ] && echo "✓ ParticleMesher setup" || echo "✗ ParticleMesher not setup"
[ -d "Genesis/genesis/ext/LuisaRender/build" ] && echo "✓ LuisaRender built" || echo "✗ LuisaRender not built"
