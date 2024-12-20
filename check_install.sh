#!/bin/bash

echo "Checking Genesis installation components..."

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
        if [ "$major" -gt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -ge 18 ]); then
            return 0
        fi
    fi
    return 1
}

echo -e "\nChecking Core Requirements:"
echo "-------------------------"

# Check Python version
if command_exists python3.11; then
    version=$(python3.11 --version 2>&1)
    echo "✓ Python: $version"
else
    echo "✗ Python 3.11+ not found"
fi

# Check system dependencies
echo -e "\nSystem Dependencies:"
SYSTEM_DEPS=(
    "git"
    "g++"
    "libboost-all-dev"
    "libeigen3-dev"
    "libode-dev"
    "libyaml-cpp-dev"
)

for pkg in "${SYSTEM_DEPS[@]}"; do
    if apt_package_installed "$pkg"; then
        echo "✓ $pkg installed"
    else
        echo "✗ $pkg not installed"
    fi
done

# Check CMake version
echo -e "\nBuild Tools:"
if check_cmake_version; then
    version=$(cmake --version | head -n1)
    echo "✓ $version"
else
    current_version=$(cmake --version 2>/dev/null | head -n1 || echo "CMake not found")
    echo "✗ CMake 3.18+ required, found: $current_version"
fi

# Check Python packages
echo -e "\nPython Packages:"
PYTHON_PKGS=(
    "torch"
    "genesis-world"
    "genesis"
)

for pkg in "${PYTHON_PKGS[@]}"; do
    if pip_package_installed "$pkg"; then
        version=$(pip show "$pkg" | grep Version | cut -d' ' -f2)
        echo "✓ $pkg ($version)"
    else
        echo "✗ $pkg not installed"
    fi
done

echo -e "\nOptional Components:"
echo "-------------------"

# Check OMPL
if pip_package_installed "ompl"; then
    version=$(pip show ompl | grep Version | cut -d' ' -f2)
    echo "✓ OMPL ($version)"
else
    echo "✗ OMPL not installed"
fi

# Check Surface Reconstruction Tools
echo -e "\nSurface Reconstruction:"
if command_exists splashsurf; then
    version=$(splashsurf --version 2>&1 || echo "version unknown")
    echo "✓ splashsurf ($version)"
else
    echo "✗ splashsurf not installed"
fi

if [ -d "Genesis/genesis/ext/ParticleMesher" ]; then
    echo "✓ ParticleMesher setup"
else
    echo "✗ ParticleMesher not setup"
fi

# Check Ray Tracing Renderer
echo -e "\nRay Tracing Renderer:"
if [ -d "Genesis/genesis/ext/LuisaRender/build" ]; then
    echo "✓ LuisaRender built"
else
    echo "✗ LuisaRender not built"
fi

# Check GPU Support
echo -e "\nGPU Support:"
if command_exists nvidia-smi; then
    echo "✓ NVIDIA GPU detected"
    nvidia-smi --query-gpu=gpu_name,driver_version --format=csv,noheader
else
    echo "✗ No NVIDIA GPU detected"
fi

echo -e "\nNote: ✓ = installed/available, ✗ = not installed/missing"
