//! Fast anomaly detection module

use std::collections::VecDeque;

/// Anomaly information
#[derive(Debug, Clone)]
pub struct Anomaly {
    pub timestamp: f64,
    pub value: f32,
    pub z_score: f32,
    pub severity: Severity,
    pub mean: f32,
    pub stdev: f32,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Severity {
    Low,
    Medium,
    High,
}

/// High-performance anomaly detector using statistical methods
pub struct AnomalyDetector {
    window: VecDeque<f32>,
    window_size: usize,
    anomalies: Vec<Anomaly>,
    
    // Running statistics for O(1) updates
    running_sum: f32,
    running_sum_sq: f32,
}

impl AnomalyDetector {
    /// Create a new anomaly detector
    pub fn new(window_size: usize) -> Self {
        Self {
            window: VecDeque::with_capacity(window_size),
            window_size,
            anomalies: Vec::new(),
            running_sum: 0.0,
            running_sum_sq: 0.0,
        }
    }
    
    /// Detect anomalies using optimized single-pass statistics
    pub fn detect(&mut self, value: f32, timestamp: f64) -> Option<Anomaly> {
        // Update running statistics
        if self.window.len() >= self.window_size {
            if let Some(old_val) = self.window.pop_front() {
                self.running_sum -= old_val;
                self.running_sum_sq -= old_val * old_val;
            }
        }
        
        self.window.push_back(value);
        self.running_sum += value;
        self.running_sum_sq += value * value;
        
        // Need at least 3 values for meaningful statistics
        if self.window.len() < 3 {
            return None;
        }
        
        let n = self.window.len() as f32;
        let mean = self.running_sum / n;
        let variance = (self.running_sum_sq / n) - (mean * mean);
        let stdev = variance.max(0.0).sqrt();
        
        // Calculate Z-score
        let z_score = if stdev > 0.0001 {
            ((value - mean) / stdev).abs()
        } else {
            0.0
        };
        
        // Detect anomaly based on Z-score
        if z_score > 2.0 {
            let severity = if z_score > 3.0 {
                Severity::High
            } else if z_score > 2.5 {
                Severity::Medium
            } else {
                Severity::Low
            };
            
            let anomaly = Anomaly {
                timestamp,
                value,
                z_score,
                severity,
                mean,
                stdev,
            };
            
            self.anomalies.push(anomaly.clone());
            Some(anomaly)
        } else {
            None
        }
    }
    
    /// Get the count of detected anomalies
    #[inline]
    pub fn anomaly_count(&self) -> usize {
        self.anomalies.len()
    }
    
    /// Get all detected anomalies
    pub fn get_anomalies(&self) -> &[Anomaly] {
        &self.anomalies
    }
    
    /// Clear the detector state
    pub fn clear(&mut self) {
        self.window.clear();
        self.anomalies.clear();
        self.running_sum = 0.0;
        self.running_sum_sq = 0.0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_anomaly_detection() {
        let mut detector = AnomalyDetector::new(10);
        
        // Normal values
        for i in 0..10 {
            detector.detect(0.5, i as f64);
        }
        
        // Anomalous value
        let anomaly = detector.detect(2.0, 10.0);
        assert!(anomaly.is_some());
        
        if let Some(a) = anomaly {
            assert!(a.z_score > 2.0);
            assert_eq!(a.value, 2.0);
        }
    }
    
    #[test]
    fn test_running_statistics() {
        let mut detector = AnomalyDetector::new(5);
        
        for i in 0..5 {
            detector.detect(i as f32, i as f64);
        }
        
        assert_eq!(detector.window.len(), 5);
        assert_eq!(detector.running_sum, 10.0); // 0+1+2+3+4
    }
}