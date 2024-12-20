# Genesis API Reference

## Overview

Genesis is a differentiable physics engine that supports various simulation types and rendering capabilities. This comprehensive API reference documents all major components and features of the Genesis framework.

## Core Components

### Scene Management
- [Scene](core/scene.md) - Main simulation environment and control
  - Scene creation and configuration
  - Entity management
  - Simulation control
  - State management

### Physical Objects
- [Entity](core/entity.md) - Physical objects and their behaviors
  - Entity creation and properties
  - Transform operations
  - Physics interactions
  - State queries

### Visualization
- [Camera](core/camera.md) - Scene visualization and recording
  - Camera setup and control
  - Frame rendering
  - Video recording
  - Multiple viewpoints

## Physics System

### Simulation
- [Solvers](physics/solvers.md) - Physics simulation engines
  - Rigid body dynamics
  - Material Point Method (MPM)
  - Smoothed Particle Hydrodynamics (SPH)
  - Position Based Dynamics (PBD)
  - Finite Element Method (FEM)

### Physical Properties
- [Materials](physics/materials.md) - Material definitions and properties
  - Rigid materials
  - Deformable materials
  - Fluid materials
  - Granular materials

### Dynamics
- [Forces](physics/forces.md) - Forces and interactions
  - Basic forces
  - Force fields
  - Special forces
  - Time-varying forces

## Visualization System

### Rendering
- [Renderers](visualization/renderers.md) - Rendering backends
  - Rasterizer
  - RayTracer
  - Headless rendering
  - Performance optimization

### Display
- [Viewer](visualization/viewer.md) - Real-time visualization
  - Viewer configuration
  - Camera controls
  - Visual elements
  - Interactive features

### Output
- [Recording](visualization/recording.md) - Output generation
  - Video recording
  - Frame capture
  - Multi-camera recording
  - Output formats

## Utility Components

### Configuration
- [Options](utils/options.md) - System configuration
  - Simulation options
  - Visualization options
  - Physics options
  - Coupling options

### Geometry
- [Morphs](utils/morphs.md) - Shape definitions
  - Basic primitives
  - Complex geometries
  - Compound shapes
  - Mesh operations

### Helpers
- [Tools](utils/tools.md) - Utility functions
  - Math utilities
  - File handling
  - Debug tools
  - Performance tools

## Quick Links

### Documentation
- [Installation Guide](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html)
- [Getting Started](https://genesis-world.readthedocs.io/en/latest/user_guide/getting_started/index.html)
- [Examples](https://genesis-world.readthedocs.io/en/latest/user_guide/examples/index.html)

### Common Tasks
- [Basic Simulation Setup](core/scene.md#example-usage)
- [Physics Configuration](physics/solvers.md#example-configurations)
- [Visualization Setup](visualization/renderers.md#example-usage)
- [Recording Output](visualization/recording.md#basic-video-recording)

### Best Practices
- [Performance Optimization](utils/tools.md#performance-tools)
- [Debug Techniques](utils/tools.md#debug-tools)
- [Memory Management](utils/options.md#memory-usage)
- [Error Handling](utils/tools.md#common-issues-and-solutions)
