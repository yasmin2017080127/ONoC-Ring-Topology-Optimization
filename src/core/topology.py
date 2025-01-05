import networkx as nx
import random
import numpy as np

def create_ring_topology(num_nodes):
    """Creates a ring topology with the given number of nodes."""
    ring = nx.cycle_graph(num_nodes)
    
    # Initialize with more realistic temperature distribution
    temperatures = np.random.normal(35, 5, num_nodes)  # Mean 35°C, std 5°C
    temperatures = np.clip(temperatures, 25, 50)  # Clip between 25-50°C
    
    for node in ring.nodes:
        ring.nodes[node]['temperature'] = temperatures[node]
        ring.nodes[node]['congestion'] = random.uniform(20, 60)  # More realistic congestion range
    
    # Initialize edges with realistic utilization
    for u, v in ring.edges:
        ring[u][v]['utilization'] = random.uniform(20, 60)
        ring[v][u]['utilization'] = ring[u][v]['utilization']  # Symmetric utilization
        
    return ring

def partition_nodes(graph, partition_size):
    """Partitions the nodes into groups of the given size."""
    if partition_size <= 0 or partition_size > len(graph):
        raise ValueError("Invalid partition size")
        
    nodes = list(graph.nodes)
    partitions = [nodes[i:i + partition_size] for i in range(0, len(nodes), partition_size)]
    
    # Store partition information in graph
    for i, partition in enumerate(partitions):
        for node in partition:
            graph.nodes[node]['partition'] = i
            
    return partitions
