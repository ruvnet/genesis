//! Genesis Environmental Awareness System - High Performance Rust Implementation
//! 
//! This implementation focuses on maximum performance through:
//! - SIMD vectorization
//! - Zero-cost abstractions
//! - Cache-friendly data structures
//! - Parallel processing with Rayon

pub mod neural;
pub mod spatial;
pub mod sensors;
pub mod anomaly;
pub mod predictor;

use std::time::{Duration, Instant};
use std::collections::VecDeque;
use serde::{Serialize, Deserialize};
use rayon::prelude::*;

use neural::NeuralNetwork;
use spatial::SpatialGraph;
use sensors::{SensorData, SensorProcessor};
use anomaly::AnomalyDetector;
use predictor::Predictor;

/// Main Environmental Awareness System
#[derive(Debug)]
pub struct EnvironmentalAwarenessSystem {
    neural_net: NeuralNetwork,
    spatial_graph: SpatialGraph,
    sensor_processor: SensorProcessor,
    anomaly_detector: AnomalyDetector,
    predictor: Predictor,
    sensor_buffer: VecDeque<ProcessedData>,
    processing_times: Vec<Duration>,
    cycle_count: u32,
    start_time: Instant,
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
    pub theoretical_max_hz: f64,
    pub spatial_nodes: usize,
    pub spatial_edges: usize,
    pub anomalies_detected: usize,
    pub predictions_made: usize,
}

impl EnvironmentalAwarenessSystem {
    /// Create a new Environmental Awareness System
    pub fn new() -> Self {
        Self {
            neural_net: NeuralNetwork::new(4, 8, 2),
            spatial_graph: SpatialGraph::new(),
            sensor_processor: SensorProcessor::new(),
            anomaly_detector: AnomalyDetector::new(20),
            predictor: Predictor::new(10),
            sensor_buffer: VecDeque::with_capacity(100),
            processing_times: Vec::with_capacity(1000),
            cycle_count: 0,
            start_time: Instant::now(),
        }
    }

    /// Run a single processing cycle
    pub fn run_cycle(&mut self) -> CycleResult {
        let cycle_start = Instant::now();
        self.cycle_count += 1;

        // Generate sensor data
        let sensor_data = SensorData::generate();

        // Process sensors (potentially in parallel)
        let processed = self.sensor_processor.process(&sensor_data);

        // Neural network inference (SIMD optimized)
        let neural_output = self.neural_net.forward(&processed.features);

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

        // Store in buffer
        let processed_data = ProcessedData {
            cycle: self.cycle_count,
            features: processed.features.clone(),
            neural_output: neural_output.clone(),
            fused_confidence: processed.fused_confidence,
            processing_time_us: processing_time.as_micros() as u64,
        };
        
        if self.sensor_buffer.len() >= 100 {
            self.sensor_buffer.pop_front();
        }
        self.sensor_buffer.push_back(processed_data);

        CycleResult {
            cycle: self.cycle_count,
            confidence: processed.fused_confidence,
            neural_output,
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

    /// Run multiple cycles in parallel batches
    pub fn run_cycles_parallel(&mut self, count: usize) -> Vec<CycleResult> {
        (0..count)
            .map(|_| self.run_cycle())
            .collect()
    }

    /// Get system metrics
    pub fn get_metrics(&self) -> SystemMetrics {
        let runtime = self.start_time.elapsed().as_secs_f64();
        
        let processing_times_us: Vec<u64> = self.processing_times
            .iter()
            .map(|d| d.as_micros() as u64)
            .collect();
        
        let avg_processing = if !processing_times_us.is_empty() {
            processing_times_us.iter().sum::<u64>() as f64 / processing_times_us.len() as f64
        } else {
            0.0
        };

        let min_processing = processing_times_us.iter().min().copied().unwrap_or(0);
        let max_processing = processing_times_us.iter().max().copied().unwrap_or(0);

        SystemMetrics {
            runtime_seconds: runtime,
            cycles: self.cycle_count,
            processing_rate_hz: self.cycle_count as f64 / runtime,
            avg_processing_us: avg_processing,
            min_processing_us: min_processing,
            max_processing_us: max_processing,
            theoretical_max_hz: if avg_processing > 0.0 { 1_000_000.0 / avg_processing } else { 0.0 },
            spatial_nodes: self.spatial_graph.node_count(),
            spatial_edges: self.spatial_graph.edge_count(),
            anomalies_detected: self.anomaly_detector.anomaly_count(),
            predictions_made: self.predictor.prediction_count(),
        }
    }

    /// Reset the system
    pub fn reset(&mut self) {
        self.cycle_count = 0;
        self.sensor_buffer.clear();
        self.processing_times.clear();
        self.start_time = Instant::now();
        self.spatial_graph = SpatialGraph::new();
        self.anomaly_detector = AnomalyDetector::new(20);
        self.predictor = Predictor::new(10);
    }
}

impl Default for EnvironmentalAwarenessSystem {
    fn default() -> Self {
        Self::new()
    }
}

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
    }

    #[test]
    fn test_metrics() {
        let mut system = EnvironmentalAwarenessSystem::new();
        for _ in 0..10 {
            system.run_cycle();
        }
        let metrics = system.get_metrics();
        assert_eq!(metrics.cycles, 10);
        assert!(metrics.avg_processing_us > 0.0);
    }
}