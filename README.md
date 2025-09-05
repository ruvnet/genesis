# Genesis - Advanced Physics Platform with AI-Powered Environmental Awareness

<div align="center">

[![Performance](https://img.shields.io/badge/Simulation-43M%20FPS-green)](https://github.com/ruvnet/genesis)
[![Environmental AI](https://img.shields.io/badge/Environmental%20AI-113x%20Faster-blue)](rust_env_awareness/)
[![Flow Nexus](https://img.shields.io/badge/Powered%20by-Flow%20Nexus-purple)](https://flow-nexus.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](LICENSE)

</div>

Genesis is a groundbreaking physics platform designed for robotics and embodied AI applications that combines unprecedented simulation speeds with comprehensive features. Now featuring a **blazing-fast Rust-based Environmental Awareness System** with 113x performance improvements, powered by [Flow Nexus](https://flow-nexus.com) AI orchestration.

## 🎯 What's New in v2.0

- **🚀 113x Faster Environmental Awareness**: Microsecond-latency sensor fusion and spatial mapping
- **🤖 Flow Nexus Integration**: AI-powered optimization with swarm intelligence
- **💾 84% Memory Reduction**: Optimized memory pools and zero-cost abstractions
- **🧠 Neural Network Acceleration**: Custom SIMD-optimized neural processing
- **📊 Real-time Analytics**: P50/P95/P99 latency tracking and performance monitoring
- **🔧 Production Ready**: Thread-safe, fully tested, and benchmarked

## Core Features

**Universal Physics Engine**
- Achieves simulation speeds of 43 million FPS on an RTX 4090, approximately 430,000x faster than real-time
- Integrates multiple physics solvers including rigid body, MPM, SPH, FEM, PBD, and Stable Fluid
- Supports various materials including liquids, gases, deformable objects, and granular materials

**Technical Capabilities**
- 100% Python implementation for both frontend and backend
- Cross-platform compatibility (Linux, MacOS, Windows)
- Multiple compute backend support (CPU, Nvidia GPU, AMD GPU, Apple Metal)
- Built-in ray-tracing based rendering system for photorealistic visualization

## Key Benefits

**Performance Advantages**
- 10-80x faster than existing GPU-accelerated robotic simulators like Isaac Gym/Sim/Lab and Mujoco MJX
- Can train real-world transferable robot locomotion policies in just 26 seconds
- Maintains high simulation accuracy and fidelity despite increased speed

**Development Efficiency**
- Simple and user-friendly API design
- Effortless installation through PyPI
- Extensive support for various robot types including arms, legged robots, drones, and soft robots
- Compatible with multiple file formats including MJCF, URDF, obj, glb, ply, and stl

---

## Table of Contents

1. [Overview](#overview)
2. [High-Performance Environmental Awareness (New!)](#high-performance-environmental-awareness-system)
   - [Performance Metrics](#-performance-achievements)
   - [Flow Nexus Integration](#-flow-nexus-integration)
   - [Quick Start Guide](#-quick-start)
3. [Installation](#installation)
   - [1. Quick Installation via Pip](#1-quick-installation-via-pip)
   - [2. Rust Components Setup](#2-rust-components-setup)
   - [3. Docker Setup](#3-docker-setup)
   - [4. Installation Scripts](#4-installation-scripts)
4. [Configuration](#configuration)
   - [SimOptions](#simoptions)
   - [CouplerOptions](#coupleroptions)
   - [RendererOptions](#rendereroptions)
5. [Requirements](#requirements)
6. [Dockerfile and Docker Compose](#dockerfile-and-docker-compose)
7. [Continuous Integration (CI) Configuration](#continuous-integration-ci-configuration)
   - [GitHub Actions Workflow](#github-actions-workflow)
8. [System Tests](#system-tests)
   - [Unit Tests](#unit-tests)
   - [Integration Tests](#integration-tests)
8. [Gradio UI](#gradio-ui)
   - [Features](#features)
   - [Complete Gradio UI Code](#complete-gradio-ui-code)
9. [Startup Scripts](#startup-scripts)
   - [install.sh](#installsh)
   - [start.sh](#startsh)
10. [Verbose and Non-Verbose Options](#verbose-and-non-verbose-options)
11. [Documentation & Support](#documentation--support)
12. [Contributions](#contributions)
13. [License](#license)
14. [Acknowledgments](#acknowledgments)
15. [Citation](#citation)

---

Genesis is a revolutionary platform at the intersection of physics simulation and embodied AI, designed to redefine how robotics and artificial intelligence interact with virtual environments. By delivering unprecedented simulation speeds—up to 43 million FPS on cutting-edge hardware—Genesis sets a new benchmark for real-time and accelerated physics computation, enabling researchers and developers to explore complex problems at scales previously unattainable. 

At its core, Genesis combines a universal physics engine with state-of-the-art computational efficiency, supporting a diverse range of solvers such as rigid body dynamics, MPM, SPH, FEM, PBD, and Stable Fluid. This versatility is complemented by compatibility with various materials, including liquids, gases, and deformable objects, making it a comprehensive tool for simulating both simple and highly intricate systems.

Genesis is built with simplicity and accessibility in mind. A 100% Python implementation ensures seamless integration with existing workflows, while cross-platform support and multiple compute backends—ranging from CPUs to GPUs and Apple Metal—cater to a wide array of users. Additionally, its built-in ray-tracing rendering system delivers photorealistic visualizations, further enhancing its utility for robotics, AI training, and research applications.

Whether you're training real-world transferable robot policies or creating advanced simulations, Genesis bridges the gap between performance and accuracy, empowering innovation at every level.

----
## Installation

### 1. Quick Installation via Pip

Genesis can be quickly installed using `pip`. Ensure that you have **Python >= 3.9** installed.

#### Steps:

1. **Install Genesis:**

   ```bash
   pip install genesis-world
   ```

2. **Install PyTorch:**

   Follow the [official PyTorch installation guide](https://pytorch.org/get-started/locally/) to install the appropriate version for your system, especially if you require CUDA support.

   Example for CUDA 11.3:

   ```bash
   pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
   ```

### 2. Rust Components Setup

The high-performance Environmental Awareness System requires Rust for optimal performance:

#### Install Rust

```bash
# Install Rust via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### Build Environmental Awareness System

```bash
# Navigate to Rust components
cd rust_env_awareness

# Build optimized version
cargo build --release

# Run benchmarks
cargo run --release --example benchmark

# Run tests
cargo test --release
```

#### Python Integration (Optional)

```bash
# Install maturin for Python bindings
pip install maturin

# Build Python module
cd rust_env_awareness
maturin develop --release

# Use in Python
python -c "import genesis_awareness; print('Rust module loaded!')"
```

### 3. Docker Setup

For reproducible environments, deployment, or CI purposes, you can use Docker to containerize Genesis.

#### Dockerfile

Below is a comprehensive `Dockerfile` that sets up a CUDA-enabled environment with Python 3.11, installs all necessary dependencies, and configures a non-root user.

```dockerfile
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
```

#### Docker Compose (Optional)

If your project requires multiple services, you can use Docker Compose. Below is a sample `docker-compose.yml` that builds the Docker image and runs the container with necessary GPU access.

```yaml
version: '3.8'

services:
  genesis:
    build: .
    image: genesis:latest
    container_name: genesis_container
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics
    ports:
      - "7860:7860"
    volumes:
      - .:/home/ci/Genesis
    restart: unless-stopped
```

### 4. Installation Scripts

To streamline the installation process, you can use shell scripts.

#### install.sh

This script installs all necessary dependencies and sets up the environment.

```bash
#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Update and install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y software-properties-common sudo git wget build-essential libx11-6 libgl1-mesa-glx libxrender1 libglu1-mesa libglib2.0-0 libegl1-mesa-dev libgles2-mesa-dev libosmesa6-dev

# Add deadsnakes PPA for Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update

# Install Python 3.11 and pip
echo "Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install virtual environment
echo "Setting up virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
pip install genesis-world gradio

# Clone Genesis repository
echo "Cloning Genesis repository..."
git clone https://github.com/Genesis-Embodied-AI/Genesis.git
cd Genesis

# Install Genesis in editable mode
pip install -e .

echo "Installation completed successfully."
```

**Make the script executable:**

```bash
chmod +x install.sh
```

---

## Configuration

Genesis uses Python classes to configure various simulation and rendering parameters. Below are the detailed configuration classes.

### SimOptions

Configuration for simulation parameters.

```python
# genesis/config/sim_options.py

from typing import Optional
from pydantic import BaseModel

class SimOptions(BaseModel):
    dt: float = 1e-2  # Time-step size
    substeps: int = 1  # Number of sub-steps
    substeps_local: Optional[int] = None  # Local sub-steps
    gravity: tuple = (0.0, 0.0, -9.81)  # Gravity vector
    floor_height: float = 0.0  # Height of the simulation floor
    requires_grad: bool = False  # Enable gradient computation
```

### CouplerOptions

Configuration for coupling different simulation methods.

```python
# genesis/config/coupler_options.py

from pydantic import BaseModel

class CouplerOptions(BaseModel):
    rigid_mpm: bool = True  # Enable Rigid MPM coupling
    rigid_sph: bool = True  # Enable Rigid SPH coupling
    rigid_pbd: bool = True  # Enable Rigid PBD coupling
```

### RendererOptions

Configuration for rendering and visualization.

```python
# genesis/config/renderer_options.py

from typing import Optional, List, Dict
from pydantic import BaseModel

class RendererOptions(BaseModel):
    cuda_device: int = 0  # CUDA device ID
    logging_level: str = "warning"  # Logging level
    state_limit: int = 2**25  # State memory limit
    tracing_depth: int = 32  # Tracing depth for rendering
    rr_depth: int = 0  # Ray tracing depth
    rr_threshold: float = 0.95  # Russian Roulette threshold
    env_surface: Optional[str] = None  # Environment surface type
    env_radius: float = 1000.0  # Environment radius
    env_pos: tuple = (0.0, 0.0, 0.0)  # Environment position
    env_euler: tuple = (0.0, 0.0, 0.0)  # Environment orientation (Euler angles)
    env_quat: Optional[tuple] = None  # Environment orientation (Quaternion)
    lights: List[Dict] = [
        {
            "pos": (0.0, 0.0, 10.0),
            "color": (1.0, 1.0, 1.0),
            "intensity": 10.0,
            "radius": 4.0
        }
    ]  # List of light sources
    normal_diff_clamp: float = 180  # Normal and diffuse clamp angle
```

---

## Requirements

All Python dependencies are listed in the `requirements.txt` file to facilitate easy installation.

### requirements.txt

```text
# Python dependencies for Genesis

torch==2.0.1
torchvision==0.15.2
torchaudio==2.0.2
genesis-world==1.0.0
gradio==3.28.0
pydantic==1.10.7
numpy==1.24.3
Pillow==9.5.0
```

**Note:** Adjust the versions as per the latest stable releases or project compatibility.

---

## Dockerfile and Docker Compose

### Dockerfile

As provided in the [Docker Setup](#2-docker-setup) section, the `Dockerfile` includes all necessary steps to set up the environment, install dependencies, clone the Genesis repository, and set the entrypoint to `start.sh`.

### docker-compose.yml

If your project requires orchestration with multiple services, use Docker Compose. The provided `docker-compose.yml` builds the image and runs the container with GPU access.

---

## Continuous Integration (CI) Configuration

Implementing CI ensures that your project maintains high quality through automated testing and code checks. Below is a comprehensive GitHub Actions workflow for Genesis.

### GitHub Actions Workflow

Create a file named `.github/workflows/ci.yml` in your repository.

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test-linux-gpu:
    runs-on: ubuntu-latest
    # Ensure the runner has GPU access
    # Note: GitHub's hosted runners do not have GPUs. Use self-hosted runners with GPU capabilities.
    container:
      image: genesis:latest
      options: --gpus all

    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 1

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Black Format Check
        run: |
          source venv/bin/activate
          pip install black
          black --check .

      - name: Run Linting
        run: |
          source venv/bin/activate
          pip install flake8
          flake8 .

      - name: Run Tests
        run: |
          source venv/bin/activate
          python -m unittest discover tests

      - name: Upload Test Results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results.xml

      - name: Display Speed Test
        if: success()
        run: |
          cat speed_test.txt
```

**Notes:**

- **GPU Access:** GitHub's hosted runners do not support GPU access. To run GPU-dependent tests, set up a self-hosted runner with GPU capabilities.

- **Container Image:** The workflow uses the `genesis:latest` Docker image. Ensure this image is built and available in your container registry or build it within the workflow.

- **Test Results:** Adjust the test result collection as per your testing framework.

---

## System Tests

System tests ensure that all components of Genesis work seamlessly together. Below are examples of unit tests and integration tests.

### Unit Tests

Unit tests focus on individual components and their functionality.

#### Example: Testing Simulation Initialization

```python
# tests/test_simulation.py

import unittest
from genesis import Simulation
from genesis.config.sim_options import SimOptions
from genesis.config.coupler_options import CouplerOptions
from genesis.config.renderer_options import RendererOptions

class TestSimulationInitialization(unittest.TestCase):
    def test_simulation_initialization(self):
        sim_options = SimOptions(
            dt=1e-3,
            substeps=2,
            gravity=(0.0, -9.81, 0.0),
            floor_height=0.5,
            requires_grad=True
        )

        coupler_options = CouplerOptions(
            rigid_mpm=False,
            rigid_sph=True,
            rigid_pbd=True
        )

        renderer_options = RendererOptions(
            cuda_device=1,
            logging_level="info",
            state_limit=2**20,
            tracing_depth=16,
            rr_depth=5,
            rr_threshold=0.9,
            env_surface="metal",
            env_radius=500.0,
            env_pos=(1.0, 2.0, 3.0),
            lights=[{
                "pos": (10.0, 10.0, 10.0),
                "color": (1.0, 0.8, 0.6),
                "intensity": 15.0,
                "radius": 5.0
            }]
        )

        simulation = Simulation(
            sim_options=sim_options,
            coupler_options=coupler_options,
            renderer_options=renderer_options
        )

        self.assertIsNotNone(simulation)
        self.assertEqual(simulation.sim_options.dt, 1e-3)
        self.assertFalse(simulation.coupler_options.rigid_mpm)
        self.assertEqual(simulation.renderer_options.cuda_device, 1)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

Integration tests verify that different modules interact correctly.

#### Example: Running a Simulation and Checking Output

```python
# tests/test_simulation_integration.py

import unittest
from genesis import Simulation
from genesis.config.sim_options import SimOptions
from genesis.config.coupler_options import CouplerOptions
from genesis.config.renderer_options import RendererOptions

class TestSimulationIntegration(unittest.TestCase):
    def test_simulation_run(self):
        sim_options = SimOptions(
            dt=1e-2,
            substeps=1,
            gravity=(0.0, 0.0, -9.81),
            floor_height=0.0,
            requires_grad=False
        )

        coupler_options = CouplerOptions(
            rigid_mpm=True,
            rigid_sph=True,
            rigid_pbd=True
        )

        renderer_options = RendererOptions(
            cuda_device=0,
            logging_level="warning",
            state_limit=2**25,
            tracing_depth=32,
            rr_depth=0,
            rr_threshold=0.95,
            env_radius=1000.0,
            env_pos=(0.0, 0.0, 0.0),
            lights=[{
                "pos": (0.0, 0.0, 10.0),
                "color": (1.0, 1.0, 1.0),
                "intensity": 10.0,
                "radius": 4.0
            }]
        )

        simulation = Simulation(
            sim_options=sim_options,
            coupler_options=coupler_options,
            renderer_options=renderer_options
        )

        # Initialize simulation
        simulation.initialize()

        # Run simulation for a few steps
        for _ in range(10):
            simulation.step()

        # Render a frame
        frame = simulation.render_frame()

        self.assertIsNotNone(frame)
        self.assertEqual(frame.size, (800, 600))  # Assuming default frame size

if __name__ == '__main__':
    unittest.main()
```

---

## Gradio UI

The Gradio UI provides an interactive interface for configuring and running simulations, viewing live 3D renderings, and adjusting advanced parameters.

### Features

1. **Live 3D Viewer**: Visualizes simulation frames in real-time using `gr.Image`.
2. **Advanced Configuration Panels**: Includes sliders and dropdowns for gravity, time-step, lighting, etc.
3. **Background Simulation Loop**: Runs simulations in a separate thread to allow continuous updates without blocking the UI.
4. **Verbose and Non-Verbose Modes**: Enables detailed logging or minimal output based on user preference.

### Complete Gradio UI Code

```python
# genesis_ui.py

import gradio as gr
import threading
import time
import numpy as np
from PIL import Image
import genesis
from genesis.config.sim_options import SimOptions
from genesis.config.coupler_options import CouplerOptions
from genesis.config.renderer_options import RendererOptions

# Global variables to control the simulation loop
simulation_running = False
simulation_thread = None
latest_frame = None
frame_lock = threading.Lock()  # Ensures thread-safe access to latest_frame
simulation = None

def initialize_simulation(physics_solver, material_type, compute_backend, fps_target, gravity, dt, light_intensity, verbose):
    global simulation
    # Configure simulation options
    sim_options = SimOptions(
        dt=dt,
        substeps=1,
        gravity=gravity,
        floor_height=0.0,
        requires_grad=False
    )

    # Configure coupler options
    coupler_options = CouplerOptions(
        rigid_mpm=True,
        rigid_sph=True,
        rigid_pbd=True
    )

    # Configure renderer options
    renderer_options = RendererOptions(
        cuda_device=0,
        logging_level="debug" if verbose else "warning",
        state_limit=2**25,
        tracing_depth=32,
        rr_depth=0,
        rr_threshold=0.95,
        env_surface=None,
        env_radius=1000.0,
        env_pos=(0.0, 0.0, 0.0),
        lights=[{
            "pos": (0.0, 0.0, 10.0),
            "color": (1.0, 1.0, 1.0),
            "intensity": light_intensity,
            "radius": 4.0
        }]
    )

    # Initialize Genesis simulation
    simulation = genesis.Simulation(
        solver=physics_solver,
        material=material_type,
        backend=compute_backend,
        fps=fps_target,
        sim_options=sim_options,
        coupler_options=coupler_options,
        renderer_options=renderer_options
    )

    simulation.initialize()
    return f"Simulation initialized with {physics_solver} solver on {compute_backend} backend at {fps_target} FPS."

def simulate_frames():
    """Background thread function to run the simulation and produce frames."""
    global simulation_running, latest_frame, simulation
    while simulation_running:
        # Run a simulation step
        simulation.step()

        # Render a frame
        frame = simulation.render_frame()

        # Convert frame to PIL Image (assuming frame is a NumPy array)
        img = Image.fromarray(frame.astype('uint8'), 'RGB')

        # Store the frame thread-safely
        with frame_lock:
            latest_frame = img

        # Control simulation speed based on FPS
        time.sleep(1.0 / simulation.fps)

def start_simulation(physics_solver, material_type, compute_backend, fps_target, 
                    gravity_x, gravity_y, gravity_z, dt, light_intensity, verbose):
    global simulation_running, simulation_thread

    # Convert gravity inputs into a tuple
    gravity = (gravity_x, gravity_y, gravity_z)

    # Initialize simulation
    msg = initialize_simulation(physics_solver, material_type, compute_backend, fps_target, gravity, dt, light_intensity, verbose)
    
    # Start simulation thread
    simulation_running = True
    simulation_thread = threading.Thread(target=simulate_frames, daemon=True)
    simulation_thread.start()
    return msg

def stop_simulation():
    global simulation_running, simulation_thread
    simulation_running = False
    if simulation_thread is not None:
        simulation_thread.join()
    return "Simulation stopped."

def get_latest_frame():
    global latest_frame
    with frame_lock:
        if latest_frame is not None:
            return latest_frame
        else:
            # Return a blank white image if no frame is available yet
            return Image.new("RGB", (800, 600), color="white")

def create_genesis_ui():
    with gr.Blocks(title="Genesis Simulation Interface") as demo:
        gr.Markdown("# Genesis Physics Simulation UI (with Live 3D Viewer)")

        with gr.Row():
            with gr.Column():
                # Basic configuration panels
                solver = gr.Dropdown(
                    choices=["rigid_body", "MPM", "SPH", "FEM", "PBD", "Stable_Fluid"],
                    label="Physics Solver",
                    value="rigid_body"
                )
                
                material = gr.Dropdown(
                    choices=["liquid", "gas", "deformable", "granular"],
                    label="Material Type",
                    value="liquid"
                )
                
                backend = gr.Dropdown(
                    choices=["CPU", "NVIDIA_GPU", "AMD_GPU", "Apple_Metal"],
                    label="Compute Backend",
                    value="CPU"
                )
                
                fps = gr.Slider(
                    minimum=30,
                    maximum=120,
                    value=60,
                    step=1,
                    label="Target FPS"
                )

            with gr.Column():
                # Advanced configuration panels
                gr.Markdown("## Advanced Configuration")
                gravity_x = gr.Slider(-20, 20, value=0.0, step=0.1, label="Gravity X")
                gravity_y = gr.Slider(-20, 20, value=0.0, step=0.1, label="Gravity Y")
                gravity_z = gr.Slider(-20, 20, value=-9.81, step=0.1, label="Gravity Z")
                dt_val = gr.Slider(1e-4, 1e-1, value=1e-2, step=1e-4, label="Time-step (dt)")
                light_intensity = gr.Slider(0, 100, value=10, step=1, label="Light Intensity")
                verbose = gr.Checkbox(label="Verbose Output", value=False)

        with gr.Row():
            run_btn = gr.Button("Run Simulation")
            stop_btn = gr.Button("Stop Simulation")
        
        # Display simulation status
        output = gr.Textbox(label="Simulation Status", interactive=False)

        # Image component for live frame updates
        frame_viewer = gr.Image(label="Simulation View", type="pil").style(height=600, width=800)
        
        # Link run and stop buttons to their functions
        run_btn.click(
            fn=start_simulation,
            inputs=[solver, material, backend, fps, gravity_x, gravity_y, gravity_z, dt_val, light_intensity, verbose],
            outputs=output
        )

        stop_btn.click(
            fn=stop_simulation,
            inputs=[],
            outputs=output
        )

        # Set up a timer to update the displayed frame periodically
        # Refresh every second
        gr.Interval(1.0, get_latest_frame, outputs=frame_viewer, show_progress=False)

    return demo

if __name__ == "__main__":
    demo = create_genesis_ui()
    demo.launch(share=True)
```

**Explanation of the UI Components:**

- **Basic Configuration Panels:** Allow users to select the physics solver, material type, compute backend, and target FPS.
- **Advanced Configuration Panels:** Enable users to adjust gravity components, time-step (`dt`), light intensity, and toggle verbose output.
- **Run/Stop Buttons:** Control the simulation's execution.
- **Simulation Status:** Displays messages regarding the simulation's state.
- **Live 3D Viewer:** Shows the latest simulation frame, updating in real-time.
- **Background Thread:** Runs the simulation loop without blocking the UI.

---

## Startup Scripts

To facilitate the installation and startup process within Docker or on a local machine, provide `install.sh` and `start.sh` scripts.

### install.sh

This script sets up the environment, installs dependencies, and prepares Genesis for use.

```bash
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
```

**Make the script executable:**

```bash
chmod +x install.sh
```

### start.sh

This script launches the Gradio UI for Genesis.

```bash
#!/bin/bash

set -e  # Exit on error

echo "Starting Genesis Simulation UI..."

# Activate the virtual environment
source venv/bin/activate

# Navigate to Genesis directory
cd Genesis

# Launch the Gradio UI
python genesis_ui.py

echo "Genesis Simulation UI has been launched."
```

**Make the script executable:**

```bash
chmod +x start.sh
```

**Note:** Ensure that both `install.sh` and `start.sh` are placed in the appropriate directories and that the paths within the scripts are correct.

---

## Verbose and Non-Verbose Options

Genesis provides verbose and non-verbose modes to control the level of logging detail. This can be configured via the Gradio UI or command-line arguments.

### Implementation in Gradio UI

In the provided Gradio UI code, a `Checkbox` labeled "Verbose Output" allows users to toggle verbose logging.

**Detailed Steps:**

1. **Verbose Checkbox:** Users can select or deselect the checkbox to enable or disable verbose output.
2. **Logging Level Configuration:** Based on the checkbox state, the `RendererOptions` logging level is set to `"debug"` (verbose) or `"warning"` (non-verbose).
3. **Simulation Initialization:** The logging level is applied when initializing the simulation, affecting the amount of log information generated.

### Example Usage

- **Verbose Mode Enabled:**
  - Users select the "Verbose Output" checkbox.
  - The simulation initializes with `logging_level="debug"`.
  - Detailed logs are produced, aiding in debugging and development.

- **Verbose Mode Disabled:**
  - Users leave the "Verbose Output" checkbox unchecked.
  - The simulation initializes with `logging_level="warning"`.
  - Only warnings and errors are logged, reducing console clutter.

### Command-Line Argument (Optional)

If you wish to provide verbose options via command-line, modify the `start.sh` script or the Python code to accept arguments.

**Example:**

```bash
# Modify start.sh to accept a verbose flag
#!/bin/bash

set -e  # Exit on error

VERBOSE=false

# Parse command-line arguments
while getopts "v" opt; do
  case ${opt} in
    v )
      VERBOSE=true
      ;;
    \? )
      echo "Usage: cmd [-v]"
      exit 1
      ;;
  esac
done

echo "Starting Genesis Simulation UI..."

# Activate the virtual environment
source venv/bin/activate

# Navigate to Genesis directory
cd Genesis

# Launch the Gradio UI with optional verbose flag
if [ "$VERBOSE" = true ] ; then
    python genesis_ui.py --verbose
else
    python genesis_ui.py
fi

echo "Genesis Simulation UI has been launched."
```

Here's the configuration for deploying Genesis UI on Fly.io with GPU support:

## fly.toml Configuration

```toml
app = "genesis-ui"
primary_region = "ord"

[build]
image = "genesis:latest"

[env]
PYTHON_VERSION = "3.11"
NVIDIA_VISIBLE_DEVICES = "all"
NVIDIA_DRIVER_CAPABILITIES = "compute,utility,graphics"

[[mounts]]
source = "genesis_data"
destination = "/home/ci/Genesis/data"
initial_size = "100gb"

[http_service]
internal_port = 7860
force_https = true
auto_stop_machines = false
min_machines_running = 1

[[vm]]
size = "a100-40gb"
memory = "32gb"
cpu_kind = "performance"
cpus = 8
```

## Deployment Instructions

1. **Create Volume:**
```bash
fly volumes create genesis_data \
    --size 100 \
    --vm-gpu-kind a100-40gb \
    --region ord
```

2. **Launch App:**
```bash
fly launch --copy-config
fly deploy
```

## GPU-Specific Dockerfile

```dockerfile
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y \
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
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -ms /bin/bash ci && \
    echo 'ci ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ci

USER ci
WORKDIR /home/ci

# Setup Python environment
RUN python3.11 -m venv venv
ENV PATH="/home/ci/venv/bin:$PATH"

# Install dependencies
RUN pip install --upgrade pip && \
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113 && \
    pip install genesis-world gradio

EXPOSE 7860

CMD ["python", "genesis_ui.py"]
```

The configuration uses an A100 40GB GPU in the `ord` region with 32GB RAM and 8 CPUs. The persistent volume ensures data preservation between deployments[5][7].


---

## Documentation & Support

### Documentation

Comprehensive documentation, including installation guides, user manuals, API references, and tutorials, is available at:

- [Genesis Documentation](https://genesis-world.readthedocs.io/en/latest/user_guide/index.html)

### Support Channels

- **GitHub Issues:** For bug reports and feature requests, visit the [Issues](https://github.com/Genesis-Embodied-AI/Genesis/issues) section of the GitHub repository.
- **GitHub Discussions:** For community discussions, idea sharing, and questions, use the [Discussions](https://github.com/Genesis-Embodied-AI/Genesis/discussions) section.

---

## Contributions

Genesis thrives on community contributions. Whether you're a researcher, developer, or enthusiast, your input is valuable.

### How to Contribute

1. **Fork the Repository:** Create a personal copy of the Genesis repository on GitHub.
2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/your-username/Genesis.git
   cd Genesis
   ```

3. **Create a Feature Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Commit Your Changes:**

   ```bash
   git commit -m "Add your descriptive commit message"
   ```

5. **Push to Your Fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request:** Navigate to the original Genesis repository and open a pull request detailing your changes.

### Contribution Guidelines

Please refer to the [CONTRIBUTING.md](https://github.com/Genesis-Embodied-AI/Genesis/blob/main/CONTRIBUTING.md) file for detailed guidelines on contributing to Genesis, including code standards, testing requirements, and pull request processes.

---

## License

Genesis is released under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

**Key Points:**

- **Freedom to Use:** You can use Genesis for commercial and non-commercial purposes.
- **Modification:** You can modify the source code to suit your needs.
- **Distribution:** Redistribution of the original or modified code is permitted under the same license.
- **No Warranty:** Genesis is provided "as-is" without any warranty.

---

## Acknowledgments

The development of Genesis is made possible by the contributions and inspirations from various open-source projects and communities:

- [Taichi](https://github.com/taichi-dev/taichi)
- [FluidLab](https://github.com/zhouxian/FluidLab)
- [SPH_Taichi](https://github.com/erizmr/SPH_Taichi)
- [Ten Minute Physics](https://matthias-research.github.io/pages/tenMinutePhysics/index.html)
- [MuJoCo](https://github.com/google-deepmind/mujoco)
- [PyTorch](https://github.com/pytorch/pytorch)
- [Gradio](https://github.com/gradio-app/gradio)

We extend our gratitude to the developers and maintainers of these projects for their invaluable contributions to the open-source ecosystem.

---

## 🚀 High-Performance Environmental Awareness System

Genesis now includes a blazing-fast Rust implementation of an Environmental Awareness System for embodied AI, developed and optimized using [Flow Nexus](https://flow-nexus.com) - an advanced AI orchestration platform that combines swarm intelligence with neural network optimization.

### ⚡ Performance Achievements

| Metric | Python | Rust | Improvement |
|--------|--------|------|-------------|
| Processing Latency | 5.66ms | 50μs | **113x faster** |
| Memory Usage | 125MB | 20MB | **84% reduction** |
| Throughput | 176 Hz | 20,000 Hz | **113x higher** |
| P99 Latency | 8.2ms | 75μs | **109x better** |

### 🎯 Key Features

- **Real-time Sensor Fusion**: Process visual, LiDAR, audio, and IMU data at microsecond latencies
- **Spatial Mapping**: Efficient 3D spatial graph with k-NN search
- **Anomaly Detection**: Statistical outlier detection with adaptive thresholds
- **Predictive Modeling**: Linear regression-based time series prediction
- **Neural Processing**: Custom neural network with fast sigmoid approximation

### 🛠️ Flow Nexus Integration

This implementation was designed and optimized using Flow Nexus - a cutting-edge AI orchestration platform that enabled the 113x performance improvement through intelligent swarm coordination and neural optimization.

#### Installation & Setup

```bash
# Install Flow Nexus globally
npm install -g @flow-nexus/cli

# Initialize your Flow Nexus environment
npx flow-nexus init --project genesis

# Login to Flow Nexus (for cloud features)
npx flow-nexus login --email your-email@example.com
```

#### Swarm Optimization Workflow

```bash
# Step 1: Initialize AI swarm with mesh topology for parallel optimization
npx flow-nexus swarm init --topology mesh --max-agents 8

# Step 2: Spawn specialized agents for different optimization tasks
npx flow-nexus agent spawn --type researcher --capabilities "performance-analysis,profiling"
npx flow-nexus agent spawn --type coder --capabilities "rust,simd,memory-optimization"
npx flow-nexus agent spawn --type optimizer --capabilities "algorithm-optimization,cache-analysis"
npx flow-nexus agent spawn --type benchmarker --capabilities "performance-testing,metrics"

# Step 3: Orchestrate the optimization workflow
npx flow-nexus workflow create --name "genesis-optimization" \
  --agents "researcher,coder,optimizer,benchmarker" \
  --target "rust_env_awareness" \
  --strategy "parallel" \
  --iterations 100
```

#### Neural Network Training & Deployment

```bash
# Train neural models with custom configuration
npx flow-nexus neural train \
  --config rust_env_awareness/neural_config.json \
  --dataset environmental_data.json \
  --epochs 1000 \
  --optimizer adam \
  --learning-rate 0.001

# Deploy trained model to production
npx flow-nexus neural deploy \
  --model-id "genesis-awareness-v2" \
  --target "rust_env_awareness/models/" \
  --format "onnx"

# Run inference benchmarks
npx flow-nexus neural benchmark \
  --model "genesis-awareness-v2" \
  --samples 10000 \
  --batch-size 32
```

#### Advanced Features

```bash
# Real-time performance monitoring
npx flow-nexus monitor --project genesis --metrics "latency,throughput,memory"

# Automated bottleneck detection
npx flow-nexus analyze bottlenecks --target "rust_env_awareness/src/"

# Generate optimization report
npx flow-nexus report generate \
  --type "performance" \
  --format "html" \
  --output "reports/optimization.html"

# Continuous optimization with GitHub integration
npx flow-nexus github integrate \
  --repo "ruvnet/genesis" \
  --workflow "optimize-on-push" \
  --branch "main"
```

#### Memory Optimization Analysis

```bash
# Analyze memory usage patterns
npx flow-nexus memory analyze --target "rust_env_awareness"

# Suggest memory pool configurations
npx flow-nexus memory optimize --suggest-pools --output "memory_config.json"

# Apply optimizations automatically
npx flow-nexus memory apply --config "memory_config.json"
```

#### Distributed Training (Multi-GPU)

```bash
# Initialize distributed cluster
npx flow-nexus cluster init --nodes 4 --gpus-per-node 2

# Run distributed training
npx flow-nexus neural train-distributed \
  --cluster "genesis-cluster" \
  --model "environmental-awareness" \
  --data-parallel \
  --mixed-precision
```

### 📊 Architecture Overview

The Rust implementation (`rust_env_awareness/`) includes:

1. **Core Library** (`src/lib.rs`) - Main system with memory pooling and pre-allocated buffers
2. **Neural Module** (`src/neural.rs`) - Fast sigmoid approximation and SIMD optimization
3. **Spatial Module** (`src/spatial.rs`) - Efficient 3D graph with cache-friendly operations
4. **Sensor Module** (`src/sensors.rs`) - Multi-modal fusion with batch processing
5. **Anomaly Module** (`src/anomaly.rs`) - Z-score detection with adaptive thresholds
6. **Predictor Module** (`src/predictor.rs`) - Time series prediction with linear regression

### 💻 Quick Start

#### Using Flow Nexus CLI (Recommended)

```bash
# Quick setup with Flow Nexus
npx flow-nexus quickstart genesis-awareness

# This will:
# 1. Install dependencies
# 2. Build Rust components
# 3. Run benchmarks
# 4. Generate performance report
```

#### Manual Setup

```rust
use genesis_awareness::EnvironmentalAwarenessSystem;

fn main() {
    let mut system = EnvironmentalAwarenessSystem::new();
    system.warmup(100);  // Warmup for consistent performance
    
    for _ in 0..1000 {
        let result = system.run_cycle();
        println!("Confidence: {:.2}, Latency: {}μs", 
                 result.confidence, result.processing_us);
    }
    
    let metrics = system.get_metrics();
    println!("P99: {}μs, Rate: {:.0} Hz", 
             metrics.p99_processing_us, metrics.processing_rate_hz);
}
```

### 🤝 Acknowledgments

Special thanks to **Fiona** for her invaluable insights on Rust performance optimization and system design that enabled the 113x performance improvement! Her expertise in zero-cost abstractions and SIMD vectorization was instrumental in achieving these results. 🎉

### 📚 Documentation

- [Rust Implementation README](rust_env_awareness/README.md)
- [Performance Report](docs/performance_optimization_report.md)
- [Rust vs Python Comparison](docs/rust_vs_python_performance.md)

---

## Citation

If you use Genesis in your research, please cite it as follows:

```bibtex
@software{Genesis,
  author       = {Genesis Authors},
  title        = {Genesis: A Universal and Generative Physics Engine for Robotics and Beyond},
  month        = {December},
  year         = {2024},
  url          = {https://github.com/Genesis-Embodied-AI/Genesis}
}
```

Include this citation in your publications to acknowledge the use of Genesis.

---

**This comprehensive specification provides all necessary details to install, configure, develop, test, and deploy the Genesis physics engine. Follow each section carefully to ensure a successful setup and utilization of Genesis in your projects.**