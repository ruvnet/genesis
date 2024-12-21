# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    CC=/usr/bin/gcc \
    CXX=/usr/bin/g++ \
    CFLAGS="-fPIC" \
    CXXFLAGS="-fPIC"

# Install minimal dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    sudo \
    git \
    wget \
    build-essential \
    g++ \
    libboost-all-dev && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    # OMPL dependencies
    libboost-filesystem-dev \
    libboost-system-dev \
    libboost-program-options-dev \
    libboost-serialization-dev \
    castxml \
    libccd-dev \
    libfcl-dev \
    ninja-build && \
    rm -rf /var/lib/apt/lists/*

# Install CMake 3.26+
RUN wget https://github.com/Kitware/CMake/releases/download/v3.26.5/cmake-3.26.5.tar.gz && \
    tar -zxvf cmake-3.26.5.tar.gz && \
    cd cmake-3.26.5 && \
    ./bootstrap && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf cmake-3.26.5 cmake-3.26.5.tar.gz && \
    hash -r

# Create test user
RUN useradd -ms /bin/bash ci && \
    echo 'ci:password' | chpasswd && \
    echo 'ci ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ci && \
    mkdir -p /home/ci && \
    chown -R ci:ci /home/ci

USER ci
WORKDIR /home/ci

# Verify Python installation and set up venv
RUN echo "Python installation check:" && \
    python3.10 --version && \
    echo "Python development files:" && \
    ls -l /usr/include/python3.10/ && \
    ls -l /usr/lib/python3.10/config-3.10-x86_64-linux-gnu/ && \
    echo "Python library check:" && \
    ldconfig -p | grep libpython3.10 && \
    echo "Python config dir check:" && \
    python3.10-config --configdir && \
    echo "Creating virtual environment..." && \
    python3.10 -m venv venv && \
    echo "Virtual environment created successfully"

ENV PATH="/home/ci/venv/bin:$PATH" \
    PYTHONPATH="/usr/lib/python3.10:/usr/lib/python3.10/lib-dynload:/home/ci/venv/lib/python3.10/site-packages" \
    LD_LIBRARY_PATH="/usr/lib/python3.10/config-3.10-x86_64-linux-gnu:$LD_LIBRARY_PATH"

# Verify Python environment and libraries
RUN echo "Python path:" && \
    which python3.10 && \
    echo "Python version:" && \
    python3.10 --version && \
    echo "Pip version:" && \
    pip --version && \
    echo "Python paths:" && \
    python3.10 -c "import sys; print('\n'.join(sys.path))" && \
    echo "Library paths:" && \
    echo $LD_LIBRARY_PATH | tr ':' '\n' && \
    echo "Verifying Python library:" && \
    ls -l /usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so && \
    ldd /usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so && \
    echo "Testing Python library load:" && \
    python3.10 -c "import ctypes; ctypes.CDLL('/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so')"

# Create CMake toolchain file with Python paths (after verifying paths)
RUN echo "# Compiler settings" > toolchain.cmake && \
    echo "set(CMAKE_C_COMPILER /usr/bin/gcc)" >> toolchain.cmake && \
    echo "set(CMAKE_CXX_COMPILER /usr/bin/g++)" >> toolchain.cmake && \
    echo "set(CMAKE_CXX_STANDARD 17)" >> toolchain.cmake && \
    echo "set(CMAKE_CXX_STANDARD_REQUIRED ON)" >> toolchain.cmake && \
    echo "set(CMAKE_POSITION_INDEPENDENT_CODE ON)" >> toolchain.cmake && \
    echo "# Python settings" >> toolchain.cmake && \
    echo "set(Python_EXECUTABLE /usr/bin/python3.10)" >> toolchain.cmake && \
    echo "set(Python_INCLUDE_DIRS /usr/include/python3.10)" >> toolchain.cmake && \
    echo "set(Python_LIBRARIES /usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so)" >> toolchain.cmake

# Clone and build OMPL
RUN git clone https://github.com/ompl/ompl.git && \
    cd ompl && \
    mkdir -p build && \
    cd build && \
    echo "Current environment:" && \
    env && \
    echo "Compiler check:" && \
    which g++ && \
    g++ --version && \
    echo "CMake version:" && \
    cmake --version && \
    echo "Running CMake..." && \
    cmake .. \
        -DCMAKE_TOOLCHAIN_FILE=/home/ci/toolchain.cmake \
        -DPYTHON_EXEC=/home/ci/venv/bin/python3.10 \
        -DPYTHON_INCLUDE_DIR=/usr/include/python3.10 \
        -DPYTHON_LIBRARY=/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so \
        -DOMPL_BUILD_PYBINDINGS=ON \
        -DOMPL_REGISTRATION=OFF \
        -DOMPL_BUILD_DEMOS=OFF \
        -DOMPL_BUILD_PYTESTS=OFF \
        -DOMPL_BUILD_TESTS=OFF && \
    make -j$(nproc) && \
    sudo make install && \
    cd ../py-bindings && \
    pip install pyplusplus

# Create custom setup.py with debug output
RUN cd /home/ci/ompl/py-bindings && \
    echo "Creating setup.py..." && \
    echo 'from setuptools import setup' > setup.py && \
    echo 'from setuptools.command.build_ext import build_ext' >> setup.py && \
    echo 'import subprocess, sys, os' >> setup.py && \
    echo '' >> setup.py && \
    echo 'class CustomBuildExt(build_ext):' >> setup.py && \
    echo '    def build_extension(self, ext):' >> setup.py && \
    echo '        build_temp = os.path.abspath(self.build_temp)' >> setup.py && \
    echo '        os.makedirs(build_temp, exist_ok=True)' >> setup.py && \
    echo '' >> setup.py && \
    echo '        cmake_args = [' >> setup.py && \
    echo '            "cmake",' >> setup.py && \
    echo '            os.path.dirname(os.path.abspath(__file__)),' >> setup.py && \
    echo '            f"-DCMAKE_TOOLCHAIN_FILE=/home/ci/toolchain.cmake",' >> setup.py && \
    echo '            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={os.path.abspath(self.build_lib)}",' >> setup.py && \
    echo '            f"-DPYTHON_EXEC={sys.executable}",' >> setup.py && \
    echo '            "-DCMAKE_BUILD_TYPE=Release",' >> setup.py && \
    echo '            "-DOMPL_BUILD_PYBINDINGS=ON",' >> setup.py && \
    echo '            "-DOMPL_REGISTRATION=OFF",' >> setup.py && \
    echo '            "-DOMPL_BUILD_DEMOS=OFF",' >> setup.py && \
    echo '            "-DOMPL_BUILD_PYTESTS=OFF",' >> setup.py && \
    echo '            "-DOMPL_BUILD_TESTS=OFF"' >> setup.py && \
    echo '        ]' >> setup.py && \
    echo '' >> setup.py && \
    echo '        subprocess.run(cmake_args, cwd=build_temp, check=True)' >> setup.py && \
    echo '        subprocess.run(["make", "-j", str(os.cpu_count())], cwd=build_temp, check=True)' >> setup.py && \
    echo '' >> setup.py && \
    echo 'setup(' >> setup.py && \
    echo '    name="ompl",' >> setup.py && \
    echo '    version="1.6.0",' >> setup.py && \
    echo '    cmdclass={"build_ext": CustomBuildExt},' >> setup.py && \
    echo ')' >> setup.py && \
    echo "setup.py contents:" && \
    cat setup.py && \
    echo "Running setup.py build..." && \
    python3.10 setup.py build && \
    echo "Running setup.py install..." && \
    sudo python3.10 setup.py install

CMD ["bash"]
