//! High-performance sensor processing module

use rand::{thread_rng, Rng};
use std::f32::consts::PI;

/// Sensor data structure
#[derive(Debug, Clone)]
pub struct SensorData {
    pub visual: VisualData,
    pub lidar: LidarData,
    pub audio: AudioData,
    pub imu: ImuData,
    pub timestamp: f64,
}

#[derive(Debug, Clone)]
pub struct VisualData {
    pub objects: u8,
    pub brightness: f32,
    pub motion: f32,
}

#[derive(Debug, Clone)]
pub struct LidarData {
    pub points: u16,
    pub max_range: f32,
    pub obstacles: u8,
}

#[derive(Debug, Clone)]
pub struct AudioData {
    pub amplitude: f32,
    pub frequency: f32,
    pub event_type: u8,  // 0: quiet, 1: normal, 2: loud
}

#[derive(Debug, Clone)]
pub struct ImuData {
    pub accel_x: f32,
    pub accel_y: f32,
    pub accel_z: f32,
    pub gyro: f32,
}

impl SensorData {
    /// Generate realistic sensor data
    pub fn generate() -> Self {
        let mut rng = thread_rng();
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs_f64();
        
        Self {
            visual: VisualData {
                objects: rng.gen_range(2..=10),
                brightness: 0.5 + 0.3 * (timestamp / 5.0).sin() as f32,
                motion: rng.gen::<f32>(),
            },
            lidar: LidarData {
                points: rng.gen_range(500..=1500),
                max_range: rng.gen_range(10.0..100.0),
                obstacles: rng.gen_range(0..=5),
            },
            audio: AudioData {
                amplitude: rng.gen::<f32>(),
                frequency: rng.gen_range(20.0..20000.0),
                event_type: rng.gen_range(0..=2),
            },
            imu: ImuData {
                accel_x: rng.gen_range(-0.5..0.5),
                accel_y: rng.gen_range(-0.5..0.5),
                accel_z: 9.8 + rng.gen_range(-0.1..0.1),
                gyro: rng.gen_range(-0.1..0.1),
            },
            timestamp,
        }
    }
}

/// Processed sensor data
#[derive(Debug, Clone)]
pub struct ProcessedSensorData {
    pub features: Vec<f32>,
    pub fused_confidence: f32,
}

/// High-performance sensor processor
pub struct SensorProcessor {
    weights: [f32; 4],
}

impl SensorProcessor {
    /// Create a new sensor processor
    pub fn new() -> Self {
        Self {
            weights: [0.3, 0.3, 0.2, 0.2],  // Fusion weights
        }
    }
    
    /// Process sensor data with SIMD-friendly operations
    #[inline]
    pub fn process(&self, data: &SensorData) -> ProcessedSensorData {
        // Extract normalized features
        let features = vec![
            data.visual.objects as f32 / 10.0,
            data.lidar.points as f32 / 1500.0,
            data.audio.amplitude,
            data.imu.accel_x.abs(),
        ];
        
        // Sensor fusion using SIMD-friendly operations
        let fused_confidence = self.fuse_sensors(&features);
        
        ProcessedSensorData {
            features,
            fused_confidence,
        }
    }
    
    /// Fast sensor fusion
    #[inline(always)]
    fn fuse_sensors(&self, features: &[f32]) -> f32 {
        // Manual unrolling for known size
        if features.len() == 4 {
            features[0] * self.weights[0] +
            features[1] * self.weights[1] +
            features[2] * self.weights[2] +
            features[3] * self.weights[3]
        } else {
            // Fallback for different sizes
            features.iter()
                .zip(self.weights.iter())
                .map(|(f, w)| f * w)
                .sum()
        }
    }
    
    /// Batch process multiple sensor readings
    pub fn process_batch(&self, batch: &[SensorData]) -> Vec<ProcessedSensorData> {
        batch.iter()
            .map(|data| self.process(data))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sensor_generation() {
        let data = SensorData::generate();
        
        assert!(data.visual.objects >= 2 && data.visual.objects <= 10);
        assert!(data.lidar.points >= 500 && data.lidar.points <= 1500);
        assert!(data.audio.amplitude >= 0.0 && data.audio.amplitude <= 1.0);
    }
    
    #[test]
    fn test_sensor_processing() {
        let processor = SensorProcessor::new();
        let data = SensorData::generate();
        let processed = processor.process(&data);
        
        assert_eq!(processed.features.len(), 4);
        assert!(processed.fused_confidence >= 0.0 && processed.fused_confidence <= 1.0);
    }
}