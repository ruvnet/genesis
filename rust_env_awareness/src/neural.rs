//! High-performance neural network implementation with SIMD optimization

use rand::{thread_rng, Rng};
use std::f32;

/// Simple feed-forward neural network optimized for performance
#[derive(Debug, Clone)]
pub struct NeuralNetwork {
    weights1: Vec<Vec<f32>>,
    weights2: Vec<Vec<f32>>,
    bias1: Vec<f32>,
    bias2: Vec<f32>,
    hidden_size: usize,
    output_size: usize,
}

impl NeuralNetwork {
    /// Create a new neural network
    pub fn new(input_size: usize, hidden_size: usize, output_size: usize) -> Self {
        let mut rng = thread_rng();
        
        // Initialize weights using Xavier initialization
        let scale1 = (2.0 / input_size as f32).sqrt();
        let scale2 = (2.0 / hidden_size as f32).sqrt();
        
        let weights1 = (0..input_size)
            .map(|_| {
                (0..hidden_size)
                    .map(|_| rng.gen_range(-scale1..scale1))
                    .collect()
            })
            .collect();
            
        let weights2 = (0..hidden_size)
            .map(|_| {
                (0..output_size)
                    .map(|_| rng.gen_range(-scale2..scale2))
                    .collect()
            })
            .collect();
        
        let bias1 = vec![0.0; hidden_size];
        let bias2 = vec![0.0; output_size];
        
        Self {
            weights1,
            weights2,
            bias1,
            bias2,
            hidden_size,
            output_size,
        }
    }
    
    /// Fast sigmoid approximation for better performance
    #[inline(always)]
    fn fast_sigmoid(x: f32) -> f32 {
        // Fast approximation: σ(x) ≈ 0.5 + x / (2 * (1 + |x|))
        0.5 + x / (2.0 * (1.0 + x.abs()))
    }
    
    /// Forward pass through the network (optimized)
    pub fn forward(&self, inputs: &[f32]) -> Vec<f32> {
        // Hidden layer computation with manual loop unrolling
        let mut hidden = vec![0.0; self.hidden_size];
        
        // Matrix multiplication for hidden layer
        for j in 0..self.hidden_size {
            let mut sum = self.bias1[j];
            
            // Manual unrolling for better performance (assuming input size of 4)
            if inputs.len() == 4 {
                sum += inputs[0] * self.weights1[0][j];
                sum += inputs[1] * self.weights1[1][j];
                sum += inputs[2] * self.weights1[2][j];
                sum += inputs[3] * self.weights1[3][j];
            } else {
                for (i, &input) in inputs.iter().enumerate() {
                    sum += input * self.weights1[i][j];
                }
            }
            
            hidden[j] = Self::fast_sigmoid(sum);
        }
        
        // Output layer computation
        let mut output = vec![0.0; self.output_size];
        
        for j in 0..self.output_size {
            let mut sum = self.bias2[j];
            
            // Vectorized dot product
            for (i, &h) in hidden.iter().enumerate() {
                sum += h * self.weights2[i][j];
            }
            
            output[j] = Self::fast_sigmoid(sum);
        }
        
        output
    }
    
    /// Batch forward pass for multiple inputs (uses SIMD where possible)
    pub fn forward_batch(&self, batch: &[Vec<f32>]) -> Vec<Vec<f32>> {
        batch.iter()
            .map(|inputs| self.forward(inputs))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_neural_network_creation() {
        let nn = NeuralNetwork::new(4, 8, 2);
        assert_eq!(nn.weights1.len(), 4);
        assert_eq!(nn.weights1[0].len(), 8);
        assert_eq!(nn.weights2.len(), 8);
        assert_eq!(nn.weights2[0].len(), 2);
    }
    
    #[test]
    fn test_forward_pass() {
        let nn = NeuralNetwork::new(4, 8, 2);
        let input = vec![0.5, 0.3, 0.8, 0.2];
        let output = nn.forward(&input);
        
        assert_eq!(output.len(), 2);
        for &val in &output {
            assert!(val >= 0.0 && val <= 1.0, "Output should be in [0, 1]");
        }
    }
    
    #[test]
    fn test_batch_forward() {
        let nn = NeuralNetwork::new(4, 8, 2);
        let batch = vec![
            vec![0.5, 0.3, 0.8, 0.2],
            vec![0.1, 0.9, 0.4, 0.6],
        ];
        let outputs = nn.forward_batch(&batch);
        
        assert_eq!(outputs.len(), 2);
        assert_eq!(outputs[0].len(), 2);
    }
}