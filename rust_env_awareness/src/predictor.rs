//! Fast time series prediction module

use std::collections::VecDeque;

/// Prediction result
#[derive(Debug, Clone)]
pub struct Prediction {
    pub values: Vec<f32>,
    pub confidence: f32,
    pub trend: f32,  // Positive = increasing, negative = decreasing
}

/// High-performance linear regression predictor
pub struct Predictor {
    window: VecDeque<f32>,
    window_size: usize,
    prediction_count: usize,
}

impl Predictor {
    /// Create a new predictor
    pub fn new(window_size: usize) -> Self {
        Self {
            window: VecDeque::with_capacity(window_size),
            window_size,
            prediction_count: 0,
        }
    }
    
    /// Add an observation
    pub fn add_observation(&mut self, value: f32) {
        if self.window.len() >= self.window_size {
            self.window.pop_front();
        }
        self.window.push_back(value);
    }
    
    /// Predict future values using fast linear regression
    pub fn predict(&mut self, steps_ahead: usize) -> Option<Prediction> {
        if self.window.len() < 2 {
            return None;
        }
        
        let n = self.window.len() as f32;
        
        // Fast linear regression using closed-form solution
        // Pre-compute sums for efficiency
        let mut sum_x = 0.0;
        let mut sum_y = 0.0;
        let mut sum_xy = 0.0;
        let mut sum_xx = 0.0;
        
        for (i, &y) in self.window.iter().enumerate() {
            let x = i as f32;
            sum_x += x;
            sum_y += y;
            sum_xy += x * y;
            sum_xx += x * x;
        }
        
        // Calculate slope and intercept
        let denominator = n * sum_xx - sum_x * sum_x;
        
        if denominator.abs() < 0.0001 {
            return None;
        }
        
        let slope = (n * sum_xy - sum_x * sum_y) / denominator;
        let intercept = (sum_y - slope * sum_x) / n;
        
        // Make predictions
        let mut predictions = Vec::with_capacity(steps_ahead);
        let start_x = self.window.len() as f32;
        
        for i in 0..steps_ahead {
            let x = start_x + i as f32;
            let pred = slope * x + intercept;
            predictions.push(pred.max(0.0).min(1.0));  // Clamp to [0, 1]
        }
        
        // Calculate R-squared for confidence
        let y_mean = sum_y / n;
        let mut ss_tot = 0.0;
        let mut ss_res = 0.0;
        
        for (i, &y) in self.window.iter().enumerate() {
            let x = i as f32;
            let y_pred = slope * x + intercept;
            ss_tot += (y - y_mean) * (y - y_mean);
            ss_res += (y - y_pred) * (y - y_pred);
        }
        
        let r_squared = if ss_tot > 0.0001 {
            1.0 - (ss_res / ss_tot)
        } else {
            0.0
        };
        
        self.prediction_count += 1;
        
        Some(Prediction {
            values: predictions,
            confidence: r_squared.max(0.0).min(1.0),
            trend: slope,
        })
    }
    
    /// Get the number of predictions made
    #[inline]
    pub fn prediction_count(&self) -> usize {
        self.prediction_count
    }
    
    /// Clear the predictor state
    pub fn clear(&mut self) {
        self.window.clear();
        self.prediction_count = 0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_linear_prediction() {
        let mut predictor = Predictor::new(5);
        
        // Add linearly increasing values
        for i in 0..5 {
            predictor.add_observation(i as f32 * 0.1);
        }
        
        let prediction = predictor.predict(3).unwrap();
        
        assert_eq!(prediction.values.len(), 3);
        assert!(prediction.trend > 0.0, "Should detect increasing trend");
        assert!(prediction.confidence > 0.9, "Should have high confidence for linear data");
    }
    
    #[test]
    fn test_constant_prediction() {
        let mut predictor = Predictor::new(5);
        
        // Add constant values
        for _ in 0..5 {
            predictor.add_observation(0.5);
        }
        
        let prediction = predictor.predict(3).unwrap();
        
        assert!(prediction.trend.abs() < 0.001, "Should detect no trend");
        for &val in &prediction.values {
            assert!((val - 0.5).abs() < 0.001, "Should predict constant value");
        }
    }
}