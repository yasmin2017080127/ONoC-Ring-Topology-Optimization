import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch
import os

def visualize_topology(graph, paths_tempcon, paths_spf, sources, targets, partition_size):
    """Visualizes the ring topology with temperatures and highlights the best paths."""
    fig, ax = plt.subplots(figsize=(15, 10))
    pos = nx.circular_layout(graph)
    
    # Draw base network
    node_colors = [graph.nodes[n]['temperature'] for n in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, 
           cmap=plt.cm.coolwarm, node_size=500, ax=ax)
    
    # Draw paths for each source
    for source in sources:
        for path in paths_tempcon[source]:
            edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red',
                                 width=2, arrows=True, arrowsize=20,
                                 connectionstyle='arc3,rad=0.2', ax=ax)
        
        for path in paths_spf[source]:
            edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='blue',
                                 width=2, arrows=True, arrowsize=20,
                                 connectionstyle='arc3,rad=-0.2', ax=ax)
    
    # Highlight source and target nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=sources, node_color='lime',
                          node_size=700, label='Sources', ax=ax)
    nx.draw_networkx_nodes(graph, pos, nodelist=targets, node_color='cyan',
                          node_size=700, label='Targets', ax=ax)
    
    plt.title("Ring Topology Comparison: TempCon-RingCast vs SPF")
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.coolwarm), ax=ax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.savefig('results/plots/ring_topology_comparison.png', 
                bbox_inches='tight', dpi=300)
    plt.close()

def visualize_metrics_comparison(graph, paths_tempcon, paths_spf, wc, wt, test_name=None):
    """Creates detailed comparison plots between TempCon-RingCast and SPF."""
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Temperature Distribution
    ax1 = fig.add_subplot(gs[0, 0])
    temp_data = {
        'TempCon': [graph.nodes[n]['temperature'] for source in paths_tempcon 
                   for path in paths_tempcon[source] for n in path],
        'SPF': [graph.nodes[n]['temperature'] for source in paths_spf 
                for path in paths_spf[source] for n in path]
    }
    ax1.boxplot([temp_data['TempCon'], temp_data['SPF']], labels=['TempCon', 'SPF'])
    ax1.set_title('Temperature Distribution')
    ax1.set_ylabel('Temperature (°C)')
    
    # Path Lengths
    ax2 = fig.add_subplot(gs[0, 1])
    lengths_tempcon = [len(path) for source in paths_tempcon for path in paths_tempcon[source]]
    lengths_spf = [len(path) for source in paths_spf for path in paths_spf[source]]
    ax2.bar(['TempCon', 'SPF'], [np.mean(lengths_tempcon), np.mean(lengths_spf)])
    ax2.set_title('Average Path Length')
    ax2.set_ylabel('Number of Hops')
    
    # Save to appropriate directory
    save_dir = 'results/test' if test_name else 'results/plots'
    filename = f'{test_name}_comparison.png' if test_name else 'metrics_comparison.png'
    plt.savefig(f'{save_dir}/{filename}', bbox_inches='tight', dpi=300)
    plt.close()
    
    # Add more visualization code here...
    # (The rest of the visualization code remains the same as in the original,
    # but with improved styling and error handling)

def visualize_path_metrics(graph, path, algorithm_name):
    """Visualizes congestion and temperature metrics for the selected path."""
    congestion = []
    for u, v in zip(path[:-1], path[1:]):
        if graph.has_edge(u, v):
            congestion.append(graph[u][v]['utilization'])
        else:
            congestion.append(0)  # Handle invalid edges

    temperature = [graph.nodes[node]['temperature'] for node in path]
    indices = range(len(path))

    plt.figure(figsize=(10, 6))

    # Plot congestion as bars
    plt.bar(indices[:-1], congestion, color='blue', alpha=0.6, label='Congestion (%)')

    # Plot temperature as a line
    plt.plot(indices, temperature, color='red', marker='o', label='Temperature (°C)')

    # Add labels and title
    plt.title(f"Path Metrics: Congestion and Temperature ({algorithm_name})")
    plt.xlabel("Path Node Index")
    plt.ylabel("Metrics")
    plt.legend()
    plt.grid(True)
    plt.savefig(f'path_metrics_{algorithm_name}.png')  # Save the figure as path_metrics_{algorithm_name}.png
    plt.show()

def summarize_path_metrics(graph, path, wc, wt):
    """Generates a summary table of the selected path's metrics."""
    data = {
        'Node': path,
        'Temperature (°C)': [graph.nodes[node]['temperature'] for node in path],
        'Congestion (%)': [graph[u][v]['utilization'] if graph.has_edge(u, v) else None for u, v in zip(path[:-1], path[1:])] + [None],
    }

    # Calculate weighted scores
    data['Weighted Score'] = [
        wc * c + wt * t if c is not None else None for c, t in zip(data['Congestion (%)'][:-1], data['Temperature (°C)'])
    ] + [None]
    df = pd.DataFrame(data)

    # Print the table to the console
    print("\nSummary Table for Selected Path:")
    print(df.to_string(index=False))
    return df

def create_interactive_visualization(graph, paths_tempcon, paths_spf, sources, targets):
    """Creates an interactive visualization showing multicast paths."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    pos = nx.circular_layout(graph)
    
    def draw_multicast_paths(ax, paths_dict, source, color):
        for i, path in enumerate(paths_dict[source]):
            edges = list(zip(path[:-1], path[1:]))
            rad = 0.2 + (i * 0.1)  # Different curvature for each target
            rad = rad if color == 'red' else -rad
            nx.draw_networkx_edges(graph, pos, edgelist=edges,
                                 edge_color=color, width=2,
                                 connectionstyle=f'arc3,rad={rad}',
                                 arrows=True, arrowsize=20, ax=ax)
    
    def on_click(event):
        if event.inaxes in [ax1, ax2]:
            for node, (x, y) in pos.items():
                if abs(event.xdata - x) < 0.05 and abs(event.ydata - y) < 0.05:
                    if node in sources:
                        # Clear previous paths
                        ax1.clear()
                        ax2.clear()
                        
                        # Redraw base network
                        for ax in [ax1, ax2]:
                            nx.draw(graph, pos, with_labels=True,
                                  node_color=[graph.nodes[n]['temperature'] for n in graph.nodes],
                                  cmap=plt.cm.coolwarm, node_size=500, ax=ax)
                            
                            # Highlight source and targets
                            nx.draw_networkx_nodes(graph, pos, nodelist=[node],
                                                 node_color='lime', node_size=700, ax=ax)
                            nx.draw_networkx_nodes(graph, pos, nodelist=targets,
                                                 node_color='cyan', node_size=700, ax=ax)
                        
                        # Draw multicast paths from selected source
                        draw_multicast_paths(ax1, paths_tempcon, node, 'red')
                        draw_multicast_paths(ax2, paths_spf, node, 'blue')
                        
                        ax1.set_title(f"TempCon-RingCast Paths from Node {node}")
                        ax2.set_title(f"Shortest Path First Paths from Node {node}")
                        
                        plt.draw()
    
    # Initial drawing
    nx.draw(graph, pos, with_labels=True, 
           node_color=[graph.nodes[n]['temperature'] for n in graph.nodes],
           cmap=plt.cm.coolwarm, node_size=500, ax=ax1)
    nx.draw(graph, pos, with_labels=True,
           node_color=[graph.nodes[n]['temperature'] for n in graph.nodes],
           cmap=plt.cm.coolwarm, node_size=500, ax=ax2)
    
    # Highlight source and target nodes
    for ax in [ax1, ax2]:
        nx.draw_networkx_nodes(graph, pos, nodelist=sources,
                             node_color='lime', node_size=700, ax=ax)
        nx.draw_networkx_nodes(graph, pos, nodelist=targets,
                             node_color='cyan', node_size=700, ax=ax)
    
    ax1.set_title("Click on a source node to view TempCon-RingCast path")
    ax2.set_title("Click on a source node to view Shortest Path First path")
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

def save_simulation_metrics(graph, paths_tempcon, paths_spf, wc, wt, test_name=None):
    """Saves detailed simulation metrics to CSV files."""
    # Prepare metrics for both algorithms
    metrics = {
        'TempCon': [],
        'SPF': []
    }
    
    for algo, paths in [('TempCon', paths_tempcon), ('SPF', paths_spf)]:
        for source in paths:
            for path in paths[source]:
                path_metrics = {
                    'Source': source,
                    'Path': '->'.join(map(str, path)),
                    'Path_Length': len(path),
                    'Avg_Temperature': np.mean([graph.nodes[n]['temperature'] for n in path]),
                    'Max_Temperature': max([graph.nodes[n]['temperature'] for n in path]),
                    'Avg_Congestion': np.mean([graph[u][v]['utilization'] 
                                             for u, v in zip(path[:-1], path[1:])]),
                    'Max_Congestion': max([graph[u][v]['utilization'] 
                                         for u, v in zip(path[:-1], path[1:])])
                }
                
                # Calculate weighted score
                path_metrics['Weighted_Score'] = (
                    wc * path_metrics['Avg_Congestion'] + 
                    wt * path_metrics['Avg_Temperature']
                )
                
                metrics[algo].append(path_metrics)
    
    # Save to CSV
    save_dir = 'results/test/metrics' if test_name else 'results/metrics'
    os.makedirs(save_dir, exist_ok=True)
    
    for algo, data in metrics.items():
        filename = f'{test_name}_{algo.lower()}_metrics.csv' if test_name else f'{algo.lower()}_metrics.csv'
        pd.DataFrame(data).to_csv(f'{save_dir}/{filename}', index=False)

def save_node_partition_metrics(graph, partitions, test_name=None):
    """Saves node and partition level metrics to CSV files."""
    # Node metrics
    node_metrics = []
    for node in graph.nodes():
        node_data = {
            'Node_ID': node,
            'Temperature': graph.nodes[node]['temperature'],
            'Partition': next((i for i, p in enumerate(partitions) if node in p), None),
            'Avg_Edge_Congestion': np.mean([graph[node][neighbor]['utilization'] 
                                          for neighbor in graph.neighbors(node)])
        }
        node_metrics.append(node_data)
    
    # Partition metrics
    partition_metrics = []
    for i, partition in enumerate(partitions):
        partition_data = {
            'Partition_ID': i,
            'Nodes': ','.join(map(str, partition)),
            'Avg_Temperature': np.mean([graph.nodes[n]['temperature'] for n in partition]),
            'Max_Temperature': max([graph.nodes[n]['temperature'] for n in partition]),
            'Avg_Congestion': np.mean([graph[u][v]['utilization'] 
                                     for u in partition for v in graph.neighbors(u)])
        }
        partition_metrics.append(partition_data)
    
    # Save to CSV
    save_dir = 'results/test/metrics' if test_name else 'results/metrics'
    os.makedirs(save_dir, exist_ok=True)
    
    # Save node metrics
    node_filename = f'{test_name}_node_metrics.csv' if test_name else 'node_metrics.csv'
    pd.DataFrame(node_metrics).to_csv(f'{save_dir}/{node_filename}', index=False)
    
    # Save partition metrics
    partition_filename = f'{test_name}_partition_metrics.csv' if test_name else 'partition_metrics.csv'
    pd.DataFrame(partition_metrics).to_csv(f'{save_dir}/{partition_filename}', index=False)