//! Benchmark demonstration for Environmental Awareness System
//! 
//! This example shows how to run benchmarks and measure performance
//! of the optimized Rust implementation.

use std::time::Instant;
use genesis_awareness::EnvironmentalAwarenessSystem;

fn main() {
    println!("🚀 Genesis Environmental Awareness System - Performance Benchmark");
    println!("================================================================\n");
    
    // Create system with optimized capacity
    let mut system = EnvironmentalAwarenessSystem::with_capacity(100, 10000);
    
    println!("⚡ Warming up system (100 cycles)...");
    system.warmup(100);
    println!("✓ Warmup complete\n");
    
    // Benchmark different cycle counts
    let test_sizes = vec![10, 100, 1000, 10000];
    
    for size in test_sizes {
        println!("📊 Running {} cycles:", size);
        let start = Instant::now();
        
        let results = system.run_cycles(size);
        
        let duration = start.elapsed();
        let total_us = duration.as_micros();
        let avg_us = total_us as f64 / size as f64;
        let throughput = 1_000_000.0 / avg_us;
        
        // Calculate statistics
        let anomalies = results.iter().filter(|r| r.anomaly_detected).count();
        let predictions = results.iter().filter(|r| r.prediction.is_some()).count();
        
        // Get detailed metrics
        let metrics = system.get_metrics();
        
        println!("  ⏱️  Total time: {:.2}ms", total_us as f64 / 1000.0);
        println!("  📈 Average latency: {:.2}μs", avg_us);
        println!("  🔥 Throughput: {:.0} Hz", throughput);
        println!("  ⚠️  Anomalies detected: {}", anomalies);
        println!("  🔮 Predictions made: {}", predictions);
        println!("  📊 Percentiles:");
        println!("     P50: {}μs", metrics.p50_processing_us);
        println!("     P95: {}μs", metrics.p95_processing_us);
        println!("     P99: {}μs", metrics.p99_processing_us);
        println!("  💾 Memory usage: {:.2}MB", metrics.memory_usage_mb);
        println!();
        
        // Reset for next benchmark
        system.reset();
        system.warmup(50);
    }
    
    println!("🏁 Benchmark complete!");
    println!("\n📊 Final System Statistics:");
    println!("================================");
    
    // Run a final comprehensive test
    system.reset();
    system.warmup(100);
    
    let final_start = Instant::now();
    let _ = system.run_cycles(50000);
    let final_duration = final_start.elapsed();
    
    let final_metrics = system.get_metrics();
    
    println!("Total cycles: {}", final_metrics.cycles);
    println!("Runtime: {:.2}s", final_metrics.runtime_seconds);
    println!("Processing rate: {:.0} Hz", final_metrics.processing_rate_hz);
    println!("Theoretical max: {:.0} Hz", final_metrics.theoretical_max_hz);
    println!("\nLatency Distribution:");
    println!("  Min: {}μs", final_metrics.min_processing_us);
    println!("  P50: {}μs", final_metrics.p50_processing_us);
    println!("  P95: {}μs", final_metrics.p95_processing_us);
    println!("  P99: {}μs", final_metrics.p99_processing_us);
    println!("  Max: {}μs", final_metrics.max_processing_us);
    println!("\nSystem Components:");
    println!("  Spatial nodes: {}", final_metrics.spatial_nodes);
    println!("  Spatial edges: {}", final_metrics.spatial_edges);
    println!("  Anomalies: {}", final_metrics.anomalies_detected);
    println!("  Predictions: {}", final_metrics.predictions_made);
    println!("  Memory: {:.2}MB", final_metrics.memory_usage_mb);
    
    // Performance comparison with Python
    println!("\n🎯 Performance Comparison:");
    println!("================================");
    println!("Python baseline: 5.66ms per cycle (176 Hz)");
    println!("Rust optimized: {:.3}ms per cycle ({:.0} Hz)", 
        1000.0 / final_metrics.processing_rate_hz,
        final_metrics.processing_rate_hz
    );
    
    let speedup = final_metrics.processing_rate_hz / 176.0;
    println!("🚀 Speedup: {:.1}x faster than Python!", speedup);
    
    // Memory comparison
    println!("\n💾 Memory Comparison:");
    println!("Python: ~125MB");
    println!("Rust: {:.2}MB", final_metrics.memory_usage_mb);
    println!("Reduction: {:.1}%", (1.0 - final_metrics.memory_usage_mb / 125.0) * 100.0);
}