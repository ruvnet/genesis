# Build and Test Instructions

## Prerequisites

- Rust 1.75 or later
- Cargo (comes with Rust)
- Optional: Flow Nexus for AI-assisted optimization

## Installation

### 1. Install Rust

```bash
# Install Rust via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Verify installation
rustc --version
cargo --version
```

### 2. Clone Repository

```bash
git clone https://github.com/ruvnet/genesis.git
cd genesis/rust_env_awareness
```

## Building

### Debug Build

```bash
cargo build
```

### Release Build (Optimized)

```bash
cargo build --release
```

### With Parallel Features

```bash
cargo build --release --features parallel
```

## Testing

### Run All Tests

```bash
cargo test
```

### Run Tests with Output

```bash
cargo test -- --nocapture
```

### Run Specific Test

```bash
cargo test test_performance_consistency
```

### Run Release Mode Tests (Faster)

```bash
cargo test --release
```

## Running Examples

### Benchmark Example

```bash
cargo run --release --example benchmark
```

### Integration Example

```bash
cargo run --release --example integration
```

## Benchmarking

### Install Criterion (Benchmarking Tool)

Add to `Cargo.toml`:
```toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "performance"
harness = false
```

### Create Benchmark

Create `benches/performance.rs`:
```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use genesis_awareness::EnvironmentalAwarenessSystem;

fn cycle_benchmark(c: &mut Criterion) {
    let mut system = EnvironmentalAwarenessSystem::new();
    system.warmup(100);
    
    c.bench_function("single_cycle", |b| {
        b.iter(|| {
            black_box(system.run_cycle())
        })
    });
}

criterion_group!(benches, cycle_benchmark);
criterion_main!(benches);
```

### Run Benchmarks

```bash
cargo bench
```

## Performance Profiling

### Using perf (Linux)

```bash
# Build with debug symbols
cargo build --release
 
# Profile
perf record --call-graph=dwarf ./target/release/examples/benchmark
perf report
```

### Using Instruments (macOS)

```bash
cargo build --release
instruments -t "Time Profiler" ./target/release/examples/benchmark
```

### Using Flamegraph

```bash
# Install flamegraph
cargo install flamegraph

# Generate flamegraph
cargo flamegraph --example benchmark
```

## Cross-Platform Building

### For Linux (from macOS/Windows)

```bash
# Add target
rustup target add x86_64-unknown-linux-gnu

# Build
cargo build --release --target x86_64-unknown-linux-gnu
```

### For WebAssembly

```bash
# Add target
rustup target add wasm32-unknown-unknown

# Install wasm-pack
cargo install wasm-pack

# Build
wasm-pack build --release
```

## Integration with Python

### Using PyO3

Add to `Cargo.toml`:
```toml
[dependencies]
pyo3 = { version = "0.20", features = ["extension-module"] }

[lib]
crate-type = ["cdylib", "rlib"]
```

### Build Python Module

```bash
# Install maturin
pip install maturin

# Build and install
maturin develop --release
```

### Python Usage

```python
import genesis_awareness

system = genesis_awareness.EnvironmentalAwarenessSystem()
result = system.run_cycle()
print(f"Confidence: {result.confidence}")
```

## Docker Build

### Dockerfile

```dockerfile
FROM rust:1.75 as builder

WORKDIR /app
COPY . .

RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=builder /app/target/release/genesis_awareness /usr/local/bin/

CMD ["genesis_awareness"]
```

### Build and Run

```bash
docker build -t genesis-awareness .
docker run --rm genesis-awareness
```

## CI/CD with GitHub Actions

Create `.github/workflows/rust.yml`:

```yaml
name: Rust CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions-rs/toolchain@v1
      with:
        toolchain: stable
        override: true
    - uses: actions-rs/cargo@v1
      with:
        command: test
        args: --release --all-features

  bench:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions-rs/toolchain@v1
      with:
        toolchain: stable
        override: true
    - uses: actions-rs/cargo@v1
      with:
        command: bench
```

## Flow Nexus Integration

### Install Flow Nexus

```bash
npm install -g @flow-nexus/cli
```

### Optimize with AI Swarm

```bash
# Initialize optimization swarm
npx flow-nexus swarm init --topology mesh --max-agents 8

# Run optimization workflow
npx flow-nexus workflow create \
  --name "rust-optimization" \
  --agents "optimizer,benchmarker,profiler" \
  --target "./src"

# Analyze performance
npx flow-nexus analyze --language rust --metrics performance
```

## Troubleshooting

### Issue: Compilation Errors

```bash
# Clean build cache
cargo clean

# Update dependencies
cargo update

# Check for errors
cargo check
```

### Issue: Slow Performance

```bash
# Ensure release mode
cargo build --release

# Enable CPU features
RUSTFLAGS="-C target-cpu=native" cargo build --release

# Enable LTO
# Add to Cargo.toml:
[profile.release]
lto = true
codegen-units = 1
```

### Issue: Memory Usage

```bash
# Use memory profiler
valgrind --tool=massif ./target/release/examples/benchmark
ms_print massif.out.*
```

## Performance Tips

1. **Always use release builds** for benchmarking
2. **Enable LTO** in Cargo.toml for maximum optimization
3. **Use CPU-native features** with RUSTFLAGS
4. **Profile before optimizing** to identify bottlenecks
5. **Consider parallel features** for multi-core systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `cargo test`
4. Run formatter: `cargo fmt`
5. Run linter: `cargo clippy`
6. Submit pull request

## Support

- GitHub Issues: https://github.com/ruvnet/genesis/issues
- Documentation: See README.md and API docs
- Flow Nexus: https://flow-nexus.com

---

Built with ❤️ and Rust for maximum performance!