from src.core.topology import create_ring_topology, partition_nodes
from src.core.routing import multicast_search, shortest_path_first
from src.visualization.visualizer import (visualize_topology, 
                                        visualize_metrics_comparison,
                                        create_interactive_visualization,
                                        save_simulation_metrics,
                                        save_node_partition_metrics)
from src.test.test_scenarios import create_test_scenario_1, create_test_scenario_2
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('results/simulation.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'results/metrics',
        'results/plots',
        'results/test/metrics',
        'results/test/plots',
        'docs/latex'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main(num_nodes, partition_size, wc, wt, sources, targets, test_scenario=None, test_name=None):
    """Main simulation function with improved error handling and logging."""
    setup_directories()
    logging.info("Starting simulation with parameters: "
                f"nodes={num_nodes}, partition_size={partition_size}, "
                f"wc={wc}, wt={wt}")
    
    try:
        # Create topology
        ring = create_ring_topology(num_nodes)
        logging.info("Ring topology created successfully")
        
        # Apply test scenario if provided
        if test_scenario:
            ring = test_scenario(ring)
            logging.info(f"Applied test scenario: {test_scenario.__name__}")
        
        # Partition nodes
        partitions = partition_nodes(ring, partition_size)
        logging.info(f"Network partitioned into {len(partitions)} partitions")
        
        # Run algorithms
        paths_tempcon, scores_tempcon = multicast_search(ring, sources, 
                                                       targets, wc, wt)
        paths_spf, scores_spf = shortest_path_first(ring, sources, targets)
        
        # Visualize results with test name if provided
        visualize_topology(ring, paths_tempcon, paths_spf, sources, 
                         targets, partition_size)
        visualize_metrics_comparison(ring, paths_tempcon, paths_spf, wc, wt, test_name)
        create_interactive_visualization(ring, paths_tempcon, paths_spf, sources, targets)
        
        # Save metrics to CSV
        save_simulation_metrics(ring, paths_tempcon, paths_spf, wc, wt, test_name)
        save_node_partition_metrics(ring, partitions, test_name)
        
        logging.info("Simulation completed successfully")
        
    except Exception as e:
        logging.error(f"Simulation failed: {str(e)}")
        raise

if __name__ == "__main__":
    sources = [0, 10]
    targets = [5, 15]
    main(20, 5, 0.7, 0.3, sources, targets)