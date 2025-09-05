//! Integration example showing how to use the Environmental Awareness System
//! in a real-world robotics application scenario.

use std::thread;
use std::sync::{Arc, Mutex};
use std::time::Duration;
use genesis_awareness::{EnvironmentalAwarenessSystem, CycleResult};

/// Robot controller that uses environmental awareness for decision making
struct RobotController {
    awareness: Arc<Mutex<EnvironmentalAwarenessSystem>>,
    position: (f32, f32, f32),
    velocity: (f32, f32, f32),
    mode: RobotMode,
}

#[derive(Debug, Clone)]
enum RobotMode {
    Exploring,
    Navigating,
    Avoiding,
    Idle,
}

impl RobotController {
    fn new() -> Self {
        Self {
            awareness: Arc::new(Mutex::new(EnvironmentalAwarenessSystem::new())),
            position: (0.0, 0.0, 0.0),
            velocity: (0.0, 0.0, 0.0),
            mode: RobotMode::Idle,
        }
    }
    
    /// Process environmental data and update robot state
    fn process_environment(&mut self) -> CycleResult {
        let mut system = self.awareness.lock().unwrap();
        let result = system.run_cycle();
        
        // Update robot mode based on environmental awareness
        if result.anomaly_detected {
            self.mode = RobotMode::Avoiding;
            println!("⚠️  Anomaly detected! Switching to avoidance mode");
        } else if result.confidence > 0.8 {
            self.mode = RobotMode::Navigating;
        } else if result.confidence > 0.5 {
            self.mode = RobotMode::Exploring;
        } else {
            self.mode = RobotMode::Idle;
        }
        
        // Update velocity based on predictions
        if let Some(prediction) = &result.prediction {
            if prediction.trend == "increasing" {
                self.velocity.0 *= 1.1;  // Speed up
            } else {
                self.velocity.0 *= 0.9;  // Slow down
            }
        }
        
        // Update position
        self.position.0 += self.velocity.0;
        self.position.1 += self.velocity.1;
        self.position.2 += self.velocity.2;
        
        result
    }
    
    /// Get current system metrics
    fn get_metrics(&self) -> String {
        let system = self.awareness.lock().unwrap();
        let metrics = system.get_metrics();
        format!(
            "Cycles: {}, Rate: {:.0} Hz, P99: {}μs, Memory: {:.2}MB",
            metrics.cycles,
            metrics.processing_rate_hz,
            metrics.p99_processing_us,
            metrics.memory_usage_mb
        )
    }
}

/// Multi-robot swarm coordination example
fn swarm_coordination_demo() {
    println!("\n🤖 Multi-Robot Swarm Coordination Demo");
    println!("=====================================\n");
    
    const NUM_ROBOTS: usize = 5;
    let mut robots: Vec<RobotController> = Vec::new();
    
    // Initialize robot swarm
    for i in 0..NUM_ROBOTS {
        let mut robot = RobotController::new();
        robot.position = (i as f32 * 10.0, 0.0, 0.0);
        robot.velocity = (1.0, 0.0, 0.0);
        robots.push(robot);
    }
    
    // Run coordination cycles
    for cycle in 1..=20 {
        println!("Cycle {}", cycle);
        
        for (i, robot) in robots.iter_mut().enumerate() {
            let result = robot.process_environment();
            
            println!(
                "  Robot {}: Mode={:?}, Pos=({:.1}, {:.1}, {:.1}), Conf={:.2}",
                i, robot.mode, 
                robot.position.0, robot.position.1, robot.position.2,
                result.confidence
            );
        }
        
        thread::sleep(Duration::from_millis(100));
    }
    
    // Print final metrics
    println!("\n📊 Final Swarm Metrics:");
    for (i, robot) in robots.iter().enumerate() {
        println!("  Robot {}: {}", i, robot.get_metrics());
    }
}

/// Real-time monitoring demo with concurrent processing
fn realtime_monitoring_demo() {
    println!("\n📡 Real-Time Environmental Monitoring");
    println!("=====================================\n");
    
    let system = Arc::new(Mutex::new(EnvironmentalAwarenessSystem::new()));
    
    // Spawn monitoring thread
    let monitor_system = system.clone();
    let monitor_thread = thread::spawn(move || {
        for _ in 0..100 {
            let mut sys = monitor_system.lock().unwrap();
            let result = sys.run_cycle();
            
            if result.anomaly_detected {
                println!("🚨 ALERT: Anomaly detected at cycle {}", result.cycle);
            }
            
            drop(sys);  // Release lock
            thread::sleep(Duration::from_millis(10));
        }
    });
    
    // Spawn analysis thread
    let analysis_system = system.clone();
    let analysis_thread = thread::spawn(move || {
        thread::sleep(Duration::from_millis(500));  // Let some data accumulate
        
        for i in 0..10 {
            let sys = analysis_system.lock().unwrap();
            let metrics = sys.get_metrics();
            
            println!("📊 Analysis Report #{}:", i + 1);
            println!("   Processing rate: {:.0} Hz", metrics.processing_rate_hz);
            println!("   Anomalies: {}", metrics.anomalies_detected);
            println!("   Predictions: {}", metrics.predictions_made);
            
            drop(sys);
            thread::sleep(Duration::from_millis(1000));
        }
    });
    
    // Wait for threads to complete
    monitor_thread.join().unwrap();
    analysis_thread.join().unwrap();
    
    // Final report
    let sys = system.lock().unwrap();
    let final_metrics = sys.get_metrics();
    
    println!("\n📈 Monitoring Session Complete:");
    println!("   Total cycles: {}", final_metrics.cycles);
    println!("   Average latency: {:.2}μs", final_metrics.avg_processing_us);
    println!("   Memory used: {:.2}MB", final_metrics.memory_usage_mb);
}

/// Integration with external systems via callback
fn callback_integration_demo() {
    println!("\n🔗 External System Integration Demo");
    println!("===================================\n");
    
    let mut system = EnvironmentalAwarenessSystem::new();
    
    // Define callbacks for different events
    let anomaly_callback = |cycle: u32| {
        println!("📧 Sending alert email for anomaly at cycle {}", cycle);
    };
    
    let prediction_callback = |cycle: u32, trend: &str, confidence: f32| {
        println!("📊 Logging prediction: cycle={}, trend={}, conf={:.2}", 
                 cycle, trend, confidence);
    };
    
    let metrics_callback = |rate: f64, memory: f64| {
        println!("📡 Telemetry: rate={:.0} Hz, memory={:.2}MB", rate, memory);
    };
    
    // Run system with callbacks
    for _ in 0..50 {
        let result = system.run_cycle();
        
        // Trigger callbacks based on results
        if result.anomaly_detected {
            anomaly_callback(result.cycle);
        }
        
        if let Some(pred) = result.prediction {
            prediction_callback(result.cycle, &pred.trend, pred.confidence);
        }
        
        if result.cycle % 10 == 0 {
            let metrics = system.get_metrics();
            metrics_callback(metrics.processing_rate_hz, metrics.memory_usage_mb);
        }
    }
}

fn main() {
    println!("🌟 Genesis Environmental Awareness - Integration Examples");
    println!("=======================================================");
    println!("\nDemonstrating real-world integration scenarios...\n");
    
    // Run different integration demos
    swarm_coordination_demo();
    realtime_monitoring_demo();
    callback_integration_demo();
    
    println!("\n✅ All integration examples completed successfully!");
    println!("\n💡 Key Integration Points:");
    println!("  • Thread-safe access via Arc<Mutex<T>>");
    println!("  • Real-time monitoring capabilities");
    println!("  • Swarm coordination support");
    println!("  • External system callbacks");
    println!("  • Microsecond-latency processing");
    
    println!("\n🎯 Ready for production deployment!");
}