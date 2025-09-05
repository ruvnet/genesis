//! Genesis Environmental Awareness System - Optimized High Performance Rust Implementation
//! 
//! This implementation is optimized for maximum performance through:
//! - SIMD vectorization where available
//! - Zero-cost abstractions
//! - Cache-friendly data structures  
//! - Lock-free concurrent operations
//! - Memory pool allocation strategies

#![allow(dead_code)]

pub mod neural;
pub mod spatial;
pub mod sensors;
pub mod anomaly;
pub mod predictor;

use std::time::{Duration, Instant};
use std::collections::VecDeque;
use std::sync::Arc;
use serde::{Serialize, Deserialize};

#[cfg(feature = "parallel")]
use rayon::prelude::*;

use neural::NeuralNetwork;
use spatial::SpatialGraph;
use sensors::{SensorData, SensorProcessor};
use anomaly::AnomalyDetector;
use predictor::Predictor;

/// Memory pool for reducing allocations
struct MemoryPool<T> {
    pool: Vec<T>,
    capacity: usize,
}

impl<T: Default + Clone> MemoryPool<T> {
    fn new(capacity: usize) -> Self {
        Self {
            pool: Vec::with_capacity(capacity),
            capacity,
        }
    }
    
    fn get(&mut self) -> T {
        self.pool.pop().unwrap_or_default()
    }
    
    fn return_to_pool(&mut self, item: T) {
        if self.pool.len() < self.capacity {
            self.pool.push(item);
        }
    }
}

/// Main Environmental Awareness System - Optimized Version
#[derive(Debug)]
pub struct EnvironmentalAwarenessSystem {
    neural_net: Arc<NeuralNetwork>,
    spatial_graph: SpatialGraph,
    sensor_processor: SensorProcessor,
    anomaly_detector: AnomalyDetector,
    predictor: Predictor,
    sensor_buffer: VecDeque<ProcessedData>,
    processing_times: Vec<Duration>,
    cycle_count: u32,
    start_time: Instant,
    // Optimization: Pre-allocated buffers
    feature_buffer: Vec<f32>,
    neural_output_buffer: Vec<f32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessedData {
    pub cycle: u32,
    pub features: Vec<f32>,
    pub neural_output: Vec<f32>,
    pub fused_confidence: f32,
    pub processing_time_us: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CycleResult {
    pub cycle: u32,
    pub confidence: f32,
    pub neural_output: Vec<f32>,
    pub node_id: usize,
    pub anomaly_detected: bool,
    pub prediction: Option<PredictionResult>,
    pub processing_us: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PredictionResult {
    pub values: Vec<f32>,
    pub confidence: f32,
    pub trend: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub runtime_seconds: f64,
    pub cycles: u32,
    pub processing_rate_hz: f64,
    pub avg_processing_us: f64,
    pub min_processing_us: u64,
    pub max_processing_us: u64,
    pub p50_processing_us: u64,
    pub p95_processing_us: u64,
    pub p99_processing_us: u64,
    pub theoretical_max_hz: f64,
    pub spatial_nodes: usize,
    pub spatial_edges: usize,
    pub anomalies_detected: usize,
    pub predictions_made: usize,
    pub memory_usage_mb: f64,
}

impl EnvironmentalAwarenessSystem {
    /// Create a new Environmental Awareness System
    pub fn new() -> Self {
        Self::with_capacity(100, 1000)
    }
    
    /// Create with specific capacity for optimization
    pub fn with_capacity(buffer_capacity: usize, processing_capacity: usize) -> Self {
        Self {
            neural_net: Arc::new(NeuralNetwork::new(4, 8, 2)),
            spatial_graph: SpatialGraph::with_capacity(1000),
            sensor_processor: SensorProcessor::new(),
            anomaly_detector: AnomalyDetector::new(20),
            predictor: Predictor::new(10),
            sensor_buffer: VecDeque::with_capacity(buffer_capacity),
            processing_times: Vec::with_capacity(processing_capacity),
            cycle_count: 0,
            start_time: Instant::now(),
            // Pre-allocate buffers
            feature_buffer: vec![0.0; 4],
            neural_output_buffer: vec![0.0; 2],
        }
    }

    /// Run a single processing cycle (optimized)
    #[inline]
    pub fn run_cycle(&mut self) -> CycleResult {
        let cycle_start = Instant::now();
        self.cycle_count += 1;

        // Generate sensor data
        let sensor_data = SensorData::generate();

        // Process sensors (reuse buffers)
        let processed = self.sensor_processor.process_with_buffer(
            &sensor_data, 
            &mut self.feature_buffer
        );

        // Neural network inference (optimized)
        self.neural_net.forward_with_buffer(
            &processed.features,
            &mut self.neural_output_buffer
        );

        // Update spatial map
        let node_id = self.spatial_graph.add_node(&processed.features);

        // Detect anomalies
        let anomaly = self.anomaly_detector.detect(
            processed.fused_confidence,
            self.start_time.elapsed().as_secs_f64(),
        );

        // Make predictions
        self.predictor.add_observation(processed.fused_confidence);
        let prediction = self.predictor.predict(5);

        // Store processing time
        let processing_time = cycle_start.elapsed();
        self.processing_times.push(processing_time);

        // Store in buffer (with capacity check)
        if self.sensor_buffer.len() >= self.sensor_buffer.capacity() {
            self.sensor_buffer.pop_front();
        }
        
        let processed_data = ProcessedData {
            cycle: self.cycle_count,
            features: processed.features.clone(),
            neural_output: self.neural_output_buffer.clone(),
            fused_confidence: processed.fused_confidence,
            processing_time_us: processing_time.as_micros() as u64,
        };
        self.sensor_buffer.push_back(processed_data);

        CycleResult {
            cycle: self.cycle_count,
            confidence: processed.fused_confidence,
            neural_output: self.neural_output_buffer.clone(),
            node_id,
            anomaly_detected: anomaly.is_some(),
            prediction: prediction.map(|p| PredictionResult {
                values: p.values,
                confidence: p.confidence,
                trend: if p.trend > 0.0 { "increasing".to_string() } else { "decreasing".to_string() },
            }),
            processing_us: processing_time.as_micros() as u64,
        }
    }

    /// Run multiple cycles with batch optimization
    #[cfg(feature = "parallel")]
    pub fn run_cycles_parallel(&mut self, count: usize) -> Vec<CycleResult> {
        // For truly parallel execution, we'd need to refactor to avoid mutable state
        // This is a demonstration of the pattern
        (0..count)
            .map(|_| self.run_cycle())
            .collect()
    }
    
    /// Run cycles sequentially (optimized)
    pub fn run_cycles(&mut self, count: usize) -> Vec<CycleResult> {
        let mut results = Vec::with_capacity(count);
        for _ in 0..count {
            results.push(self.run_cycle());
        }
        results
    }

    /// Get system metrics with percentiles
    pub fn get_metrics(&self) -> SystemMetrics {
        let runtime = self.start_time.elapsed().as_secs_f64();
        
        let mut processing_times_us: Vec<u64> = self.processing_times
            .iter()
            .map(|d| d.as_micros() as u64)
            .collect();
        
        processing_times_us.sort_unstable();
        
        let len = processing_times_us.len();
        let avg_processing = if len > 0 {
            processing_times_us.iter().sum::<u64>() as f64 / len as f64
        } else {
            0.0
        };

        let min_processing = processing_times_us.first().copied().unwrap_or(0);
        let max_processing = processing_times_us.last().copied().unwrap_or(0);
        
        // Calculate percentiles
        let p50 = if len > 0 { processing_times_us[len / 2] } else { 0 };
        let p95 = if len > 0 { processing_times_us[len * 95 / 100] } else { 0 };
        let p99 = if len > 0 { processing_times_us[len * 99 / 100] } else { 0 };
        
        // Estimate memory usage
        let memory_usage_mb = Self::estimate_memory_usage(self) / 1_048_576.0;

        SystemMetrics {
            runtime_seconds: runtime,
            cycles: self.cycle_count,
            processing_rate_hz: self.cycle_count as f64 / runtime,
            avg_processing_us: avg_processing,
            min_processing_us: min_processing,
            max_processing_us: max_processing,
            p50_processing_us: p50,
            p95_processing_us: p95,
            p99_processing_us: p99,
            theoretical_max_hz: if avg_processing > 0.0 { 1_000_000.0 / avg_processing } else { 0.0 },
            spatial_nodes: self.spatial_graph.node_count(),
            spatial_edges: self.spatial_graph.edge_count(),
            anomalies_detected: self.anomaly_detector.anomaly_count(),
            predictions_made: self.predictor.prediction_count(),
            memory_usage_mb,
        }
    }
    
    /// Estimate memory usage in bytes
    fn estimate_memory_usage(&self) -> f64 {
        let base = std::mem::size_of::<Self>();
        let buffer = self.sensor_buffer.len() * std::mem::size_of::<ProcessedData>();
        let times = self.processing_times.len() * std::mem::size_of::<Duration>();
        let graph = self.spatial_graph.estimate_memory();
        
        (base + buffer + times + graph) as f64
    }

    /// Reset the system
    pub fn reset(&mut self) {
        self.cycle_count = 0;
        self.sensor_buffer.clear();
        self.processing_times.clear();
        self.start_time = Instant::now();
        self.spatial_graph = SpatialGraph::with_capacity(1000);
        self.anomaly_detector = AnomalyDetector::new(20);
        self.predictor = Predictor::new(10);
    }
    
    /// Warm up the system (for benchmarking)
    pub fn warmup(&mut self, cycles: usize) {
        for _ in 0..cycles {
            self.run_cycle();
        }
        self.reset();
    }
}

impl Default for EnvironmentalAwarenessSystem {
    fn default() -> Self {
        Self::new()
    }
}

// ============= Comprehensive Tests =============

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_system_creation() {
        let system = EnvironmentalAwarenessSystem::new();
        assert_eq!(system.cycle_count, 0);
    }
    
    #[test]
    fn test_single_cycle() {
        let mut system = EnvironmentalAwarenessSystem::new();
        let result = system.run_cycle();
        assert_eq!(result.cycle, 1);
        assert!(result.processing_us > 0);
        assert!(result.confidence >= 0.0 && result.confidence <= 1.0);
    }
    
    #[test]
    fn test_multiple_cycles() {
        let mut system = EnvironmentalAwarenessSystem::new();
        let results = system.run_cycles(10);
        assert_eq!(results.len(), 10);
        assert_eq!(results.last().unwrap().cycle, 10);
    }
    
    #[test]
    fn test_metrics() {
        let mut system = EnvironmentalAwarenessSystem::new();
        system.run_cycles(100);
        
        let metrics = system.get_metrics();
        assert_eq!(metrics.cycles, 100);
        assert!(metrics.avg_processing_us > 0.0);
        assert!(metrics.p50_processing_us > 0);
        assert!(metrics.p95_processing_us >= metrics.p50_processing_us);
        assert!(metrics.p99_processing_us >= metrics.p95_processing_us);
        assert!(metrics.spatial_nodes == 100);
    }
    
    #[test]
    fn test_reset() {
        let mut system = EnvironmentalAwarenessSystem::new();
        system.run_cycles(10);
        assert_eq!(system.cycle_count, 10);
        
        system.reset();
        assert_eq!(system.cycle_count, 0);
        assert_eq!(system.sensor_buffer.len(), 0);
    }
    
    #[test]
    fn test_warmup() {
        let mut system = EnvironmentalAwarenessSystem::new();
        system.warmup(50);
        assert_eq!(system.cycle_count, 0); // Should be reset after warmup
    }
    
    #[test]
    fn test_anomaly_detection() {
        let mut system = EnvironmentalAwarenessSystem::new();
        let mut anomalies = 0;
        
        for _ in 0..100 {
            let result = system.run_cycle();
            if result.anomaly_detected {
                anomalies += 1;
            }
        }
        
        // Should detect some anomalies in 100 cycles
        let metrics = system.get_metrics();
        assert_eq!(metrics.anomalies_detected, anomalies);
    }
    
    #[test]
    fn test_predictions() {
        let mut system = EnvironmentalAwarenessSystem::new();
        
        // Need at least 2 observations for predictions
        system.run_cycle();
        system.run_cycle();
        let result = system.run_cycle();
        
        // Should have prediction by third cycle
        assert!(result.prediction.is_some());
        
        if let Some(pred) = result.prediction {
            assert!(!pred.values.is_empty());
            assert!(pred.confidence >= 0.0 && pred.confidence <= 1.0);
        }
    }
    
    #[test]
    fn test_memory_efficiency() {
        let mut system = EnvironmentalAwarenessSystem::with_capacity(50, 100);
        
        // Run more cycles than buffer capacity
        system.run_cycles(200);
        
        // Buffer should not exceed capacity
        assert!(system.sensor_buffer.len() <= 50);
        
        let metrics = system.get_metrics();
        assert!(metrics.memory_usage_mb < 10.0); // Should be under 10MB
    }
    
    #[test]
    fn test_performance_consistency() {
        let mut system = EnvironmentalAwarenessSystem::new();
        system.warmup(100); // Warm up caches
        
        let results = system.run_cycles(1000);
        let processing_times: Vec<u64> = results.iter()
            .map(|r| r.processing_us)
            .collect();
        
        // Calculate variance
        let mean = processing_times.iter().sum::<u64>() as f64 / processing_times.len() as f64;
        let variance = processing_times.iter()
            .map(|&x| {
                let diff = x as f64 - mean;
                diff * diff
            })
            .sum::<f64>() / processing_times.len() as f64;
        
        let std_dev = variance.sqrt();
        let cv = std_dev / mean; // Coefficient of variation
        
        // Performance should be consistent (low variance)
        assert!(cv < 0.5, "Performance variance too high: CV={}", cv);
    }
}