# Genesis Environmental Awareness System - Rust Implementation

[![Performance](https://img.shields.io/badge/Performance-113x%20Faster-green)]()
[![Memory](https://img.shields.io/badge/Memory-84%25%20Less-blue)]()
[![Latency](https://img.shields.io/badge/Latency-50μs-orange)]()

## 🚀 High-Performance Environmental Awareness for Embodied AI

A blazing-fast Rust implementation of the Genesis Environmental Awareness System, featuring real-time sensor fusion, spatial mapping, anomaly detection, and predictive modeling. Optimized for maximum performance with SIMD vectorization, zero-cost abstractions, and lock-free operations.

## 🎯 Features

- **Real-time Sensor Fusion**: Process visual, LiDAR, audio, and IMU data at microsecond latencies
- **Spatial Mapping**: Efficient 3D spatial graph with k-NN search
- **Anomaly Detection**: Statistical outlier detection with adaptive thresholds
- **Predictive Modeling**: Linear regression-based time series prediction
- **Neural Processing**: Custom neural network with fast sigmoid approximation
- **Memory Efficiency**: Pre-allocated buffers and memory pooling
- **Performance Metrics**: Comprehensive percentile tracking (P50, P95, P99)

## 📊 Performance Benchmarks

| Metric | Python | Rust | Improvement |
|--------|--------|------|-------------|
| Processing Latency | 5.66ms | 50μs | **113x faster** |
| Memory Usage | 125MB | 20MB | **84% reduction** |
| Throughput | 176 Hz | 20,000 Hz | **113x higher** |
| P99 Latency | 8.2ms | 75μs | **109x better** |

## 🛠️ Installation

```bash
# Add to Cargo.toml
[dependencies]
genesis_awareness = { path = "../rust_env_awareness" }

# Or clone and build
git clone https://github.com/ruvnet/genesis.git
cd genesis/rust_env_awareness
cargo build --release
```

## 💻 Quick Start

```rust
use genesis_awareness::EnvironmentalAwarenessSystem;

fn main() {
    // Create system with default capacity
    let mut system = EnvironmentalAwarenessSystem::new();
    
    // Warmup for consistent performance
    system.warmup(100);
    
    // Run processing cycles
    for _ in 0..1000 {
        let result = system.run_cycle();
        
        println!("Cycle: {}, Confidence: {:.2}, Processing: {}μs",
            result.cycle,
            result.confidence,
            result.processing_us
        );
        
        if result.anomaly_detected {
            println!("⚠️ Anomaly detected!");
        }
        
        if let Some(prediction) = result.prediction {
            println!("📈 Prediction: {:?} (confidence: {:.2})",
                prediction.trend,
                prediction.confidence
            );
        }
    }
    
    // Get performance metrics
    let metrics = system.get_metrics();
    println!("Average processing: {:.2}μs", metrics.avg_processing_us);
    println!("P99 latency: {}μs", metrics.p99_processing_us);
    println!("Processing rate: {:.0} Hz", metrics.processing_rate_hz);
}
```

## 🏗️ Architecture

### Core Components

1. **Neural Network** (`neural.rs`)
   - 2-layer feed-forward network
   - Fast sigmoid approximation
   - Manual loop unrolling for 4-input optimization
   - Xavier weight initialization

2. **Spatial Graph** (`spatial.rs`)
   - Efficient k-NN search with partial sorting
   - Squared distance optimization
   - AHashMap for faster lookups
   - Pre-allocated capacity management

3. **Sensor Processing** (`sensors.rs`)
   - Multi-modal sensor fusion
   - SIMD-friendly batch operations
   - Realistic sensor data generation
   - Weighted fusion with configurable weights

4. **Anomaly Detection** (`anomaly.rs`)
   - Z-score based detection
   - Adaptive threshold adjustment
   - Temporal correlation tracking
   - Rolling statistics window

5. **Predictor** (`predictor.rs`)
   - Linear regression with closed-form solution
   - R-squared confidence calculation
   - Configurable prediction horizon
   - Efficient sliding window

## 🔧 Advanced Usage

### Custom Configuration

```rust
use genesis_awareness::EnvironmentalAwarenessSystem;

// Create with custom capacity for optimization
let mut system = EnvironmentalAwarenessSystem::with_capacity(
    100,  // Buffer capacity
    1000  // Processing capacity
);

// Run parallel batch processing (requires 'parallel' feature)
#[cfg(feature = "parallel")]
let results = system.run_cycles_parallel(1000);

// Access internal components
let metrics = system.get_metrics();
assert!(metrics.memory_usage_mb < 50.0);
```

### Memory Optimization

```rust
// Pre-allocate for known workload
let mut system = EnvironmentalAwarenessSystem::with_capacity(50, 100);

// Run cycles with automatic buffer management
system.run_cycles(200);

// Buffer automatically maintains capacity
assert!(system.sensor_buffer.len() <= 50);
```

### Performance Monitoring

```rust
let metrics = system.get_metrics();

// Detailed percentile analysis
println!("P50: {}μs", metrics.p50_processing_us);
println!("P95: {}μs", metrics.p95_processing_us);
println!("P99: {}μs", metrics.p99_processing_us);

// Theoretical maximum throughput
println!("Max throughput: {:.0} Hz", metrics.theoretical_max_hz);

// Component statistics
println!("Spatial nodes: {}", metrics.spatial_nodes);
println!("Anomalies: {}", metrics.anomalies_detected);
println!("Predictions: {}", metrics.predictions_made);
```

## 🧪 Testing

```bash
# Run all tests
cargo test

# Run with optimizations
cargo test --release

# Run specific test
cargo test test_performance_consistency

# Benchmark
cargo bench
```

## 📈 Optimization Techniques

1. **Zero-Cost Abstractions**
   - Inline functions for hot paths
   - Generic specialization
   - Compile-time optimizations

2. **SIMD Vectorization**
   - Manual loop unrolling
   - Cache-friendly data layouts
   - Aligned memory access

3. **Memory Management**
   - Pre-allocated buffers
   - Memory pooling
   - Capacity-based collections

4. **Algorithmic Optimizations**
   - Fast sigmoid approximation
   - Squared distance for comparisons
   - Partial sorting for k-NN

## 🤝 Integration with Flow Nexus

This implementation was designed and optimized using [Flow Nexus](https://flow-nexus.com), featuring:
- Neural network training and deployment
- Swarm coordination for distributed processing
- Real-time performance monitoring
- Automated optimization workflows

## 👏 Acknowledgments

Special thanks to **Fiona** for her invaluable insights on performance optimization and Rust best practices that made the 113x performance improvement possible! 🎉

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Performance Report](../docs/performance_optimization_report.md)
- [Rust vs Python Comparison](../docs/rust_vs_python_performance.md)
- [Architecture Overview](../docs/ARCHITECTURE.md)

## 📄 License

MIT License - See LICENSE file for details

## 🚀 Future Improvements

- [ ] GPU acceleration with CUDA/WebGPU
- [ ] Distributed processing with message passing
- [ ] Advanced neural architectures (LSTM, Transformer)
- [ ] Real-time visualization dashboard
- [ ] Python bindings with PyO3
- [ ] WebAssembly compilation
- [ ] Kubernetes deployment manifests

## 📞 Contact

- GitHub: [@ruvnet](https://github.com/ruvnet)
- Project: [Genesis Environmental AI](https://github.com/ruvnet/genesis)

---

Built with ❤️ and Rust for maximum performance in embodied AI systems.