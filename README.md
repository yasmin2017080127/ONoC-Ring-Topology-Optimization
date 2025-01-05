# ONoC-Ring-Topology-Optimization

This project implements an algorithm for optimizing Optical Network-on-Chip (ONoC) ring topology networks with a congestion-aware heuristic algorithm. The project includes a simulation with visualization capabilities.

## Features

- Create a ring topology with a specified number of nodes.
- Partition nodes for load balancing.
- Perform multicast search to find the best paths from multiple sources to multiple targets.
- Visualize the ring topology with temperature and congestion metrics.
- Highlight the best paths and allow interactive selection of source nodes to visualize specific paths.
- Generate summary tables of path metrics and save them to CSV files.

## Requirements

- Python 3.8+
- NetworkX
- Matplotlib
- Pandas

Install the required packages using:

```sh
pip install -r [requirements.txt](http://_vscodecontentref_/1)
```

## Usage

### Running the Simulation

You can run the simulation using the GUI or directly from the command line.

Using the GUI

1.Run the gui.py script:

```python
python -m src.gui.app
```

2.Enter the required parameters in the GUI:
    - Number of Nodes
    - Source Nodes (comma-separated)
    - Target Nodes (comma-separated)
    - Partition Size
    - Weight for Congestion (wc)
    - Weight for Temperature (wt)

3.Click "Run Simulation" to start the simulation. The results will be displayed in the console, and the visualizations will be shown in separate windows.

### Using the Command Line

1.Edit the main.py file to specify the parameters:

```python
if __name__ == "__main__":
    sources = [0, 10]  # Example sources
    targets = [50, 60]  # Example targets
    main(100, 10, 0.6, 0.4, sources, targets)
```

2.Run the main.py script:

```python
python -m src.core.main
```

## Simulation Results

The simulation generates comprehensive metrics and visualizations demonstrating the performance of both TempCon-RingCast and Shortest Path First (SPF) algorithms. Results are saved in the following locations:

### Metrics (CSV files)
- `results/metrics/`: Regular simulation results
  - `node_metrics.csv`: Per-node temperature and congestion data
  - `partition_metrics.csv`: Partition-level aggregated metrics
  - `tempcon_metrics.csv`: TempCon-RingCast path metrics
  - `spf_metrics.csv`: Shortest Path First path metrics

- `results/test/metrics/`: Test scenario results
  - `high_congestion_scenario_*.csv`: Metrics for high congestion test
  - `hotspot_scenario_*.csv`: Metrics for hotspot test

### Visualizations
- `results/plots/`: Regular simulation visualizations
- `results/test/plots/`: Test scenario visualizations

Each visualization includes:
- Ring topology with temperature-based node coloring
- Path comparisons between TempCon-RingCast (red) and SPF (blue)
- Source nodes (green) and target nodes (blue)
- Interactive features for detailed path analysis

### Performance Metrics
The simulation tracks and compares:
- Path temperature distribution
- Congestion levels
- Path lengths
- Weighted performance scores
- Partition-level metrics
- Node-level metrics

## Running Tests

To run the test scenarios:

```bash
python -m src.test.run_tests
```

This will execute both high-congestion and hotspot scenarios, generating comprehensive metrics and visualizations for analysis.

## Project Structure

ONoC-Ring-Topology-Optimization/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── topology.py
│   │   ├── routing.py
│   │   ├── main.py
|   |   └── metrics.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── visualizer.py
│   └── gui/
│       ├── __init__.py
│       └── app.py
├── results/
│   ├── metrics/
|   ├── test/
|   |   ├── metrics/
|   │   └── plots/
│   └── plots/
└── docs/
    └── latex/

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
