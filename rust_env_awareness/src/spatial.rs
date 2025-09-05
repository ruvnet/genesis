//! High-performance spatial graph implementation

use std::collections::HashMap;
use ahash::AHashMap;  // Faster hash map

/// Spatial position in 3D space
#[derive(Debug, Clone, Copy)]
pub struct Position {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Position {
    /// Calculate Euclidean distance (optimized)
    #[inline(always)]
    pub fn distance_to(&self, other: &Position) -> f32 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
    
    /// Squared distance (faster when actual distance not needed)
    #[inline(always)]
    pub fn distance_squared_to(&self, other: &Position) -> f32 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        dx * dx + dy * dy + dz * dz
    }
}

/// Spatial graph node
#[derive(Debug, Clone)]
pub struct Node {
    pub id: usize,
    pub position: Position,
    pub features: Vec<f32>,
}

/// High-performance spatial graph
#[derive(Debug)]
pub struct SpatialGraph {
    nodes: Vec<Node>,
    edges: AHashMap<usize, Vec<(usize, f32)>>,  // Using faster hash map
    next_id: usize,
}

impl SpatialGraph {
    /// Create a new spatial graph
    pub fn new() -> Self {
        Self {
            nodes: Vec::with_capacity(1000),  // Pre-allocate for performance
            edges: AHashMap::with_capacity(1000),
            next_id: 0,
        }
    }
    
    /// Add a node to the graph
    pub fn add_node(&mut self, features: &[f32]) -> usize {
        // Calculate position from features
        let position = Position {
            x: features.get(0).copied().unwrap_or(0.0) * 100.0,
            y: features.get(1).copied().unwrap_or(0.0) * 100.0,
            z: features.get(2).copied().unwrap_or(0.0) * 10.0,
        };
        
        let node = Node {
            id: self.next_id,
            position,
            features: features.to_vec(),
        };
        
        let node_id = node.id;
        
        // Connect to nearby nodes (optimized with squared distance)
        const THRESHOLD_SQUARED: f32 = 2500.0;  // 50^2
        
        let mut connections = Vec::new();
        for existing_node in &self.nodes {
            let dist_sq = position.distance_squared_to(&existing_node.position);
            
            if dist_sq < THRESHOLD_SQUARED {
                let distance = dist_sq.sqrt();
                connections.push((existing_node.id, distance));
                
                // Add reverse edge
                self.edges.entry(existing_node.id)
                    .or_insert_with(Vec::new)
                    .push((node_id, distance));
            }
        }
        
        if !connections.is_empty() {
            self.edges.insert(node_id, connections);
        }
        
        self.nodes.push(node);
        self.next_id += 1;
        
        node_id
    }
    
    /// Get the number of nodes
    #[inline]
    pub fn node_count(&self) -> usize {
        self.nodes.len()
    }
    
    /// Get the number of edges
    pub fn edge_count(&self) -> usize {
        self.edges.values()
            .map(|connections| connections.len())
            .sum::<usize>() / 2  // Divide by 2 for undirected graph
    }
    
    /// Get average degree
    pub fn average_degree(&self) -> f32 {
        if self.nodes.is_empty() {
            0.0
        } else {
            (self.edge_count() * 2) as f32 / self.nodes.len() as f32
        }
    }
    
    /// Find k nearest neighbors (optimized)
    pub fn k_nearest_neighbors(&self, position: &Position, k: usize) -> Vec<(usize, f32)> {
        let mut distances: Vec<(usize, f32)> = self.nodes
            .iter()
            .map(|node| (node.id, position.distance_squared_to(&node.position)))
            .collect();
        
        // Use partial sort for better performance when k << n
        if k < distances.len() {
            distances.select_nth_unstable_by(k, |a, b| {
                a.1.partial_cmp(&b.1).unwrap()
            });
            distances.truncate(k);
        }
        
        // Convert squared distances to actual distances
        distances.iter_mut()
            .for_each(|(_, dist)| *dist = dist.sqrt());
        
        distances.sort_unstable_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
        distances
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_position_distance() {
        let pos1 = Position { x: 0.0, y: 0.0, z: 0.0 };
        let pos2 = Position { x: 3.0, y: 4.0, z: 0.0 };
        
        assert_eq!(pos1.distance_to(&pos2), 5.0);
        assert_eq!(pos1.distance_squared_to(&pos2), 25.0);
    }
    
    #[test]
    fn test_spatial_graph() {
        let mut graph = SpatialGraph::new();
        
        let id1 = graph.add_node(&[0.1, 0.2, 0.3, 0.4]);
        let id2 = graph.add_node(&[0.15, 0.25, 0.35, 0.45]);
        
        assert_eq!(graph.node_count(), 2);
        assert_eq!(id1, 0);
        assert_eq!(id2, 1);
    }
    
    #[test]
    fn test_k_nearest_neighbors() {
        let mut graph = SpatialGraph::new();
        
        // Add several nodes
        for i in 0..10 {
            let features = vec![i as f32 * 0.1, 0.5, 0.5, 0.5];
            graph.add_node(&features);
        }
        
        let query_pos = Position { x: 50.0, y: 50.0, z: 5.0 };
        let neighbors = graph.k_nearest_neighbors(&query_pos, 3);
        
        assert_eq!(neighbors.len(), 3);
    }
}