import numpy as np

def calculate_temperature(delta_lambda, alpha=1.86e-4, lambda_o=1550, T_o=25):
    """Calculates the temperature from the resonant wavelength shift."""
    if not isinstance(delta_lambda, (int, float)) or delta_lambda < 0:
        raise ValueError("Invalid wavelength shift value")
    
    delta_T = delta_lambda / (lambda_o * alpha)
    return T_o + delta_T

def calculate_congestion(graph, path):
    """Calculates the total congestion for a given path."""
    if len(path) < 2:
        return 0
        
    congestion = 0
    for u, v in zip(path[:-1], path[1:]):
        if not graph.has_edge(u, v):
            raise ValueError(f"Invalid path: no edge between {u} and {v}")
        congestion += graph[u][v]['utilization']
    
    return congestion

def calculate_path_score(graph, path, wc, wt):
    """Calculates the weighted score for a given path."""
    if not (0 <= wc <= 1 and 0 <= wt <= 1 and abs(wc + wt - 1) < 1e-6):
        raise ValueError("Weights must be between 0 and 1 and sum to 1")
        
    congestion = calculate_congestion(graph, path)
    temperature = sum(graph.nodes[node]['temperature'] for node in path)
    
    # Normalize scores
    avg_congestion = np.mean([graph[u][v]['utilization'] for u, v in graph.edges])
    avg_temperature = np.mean([graph.nodes[n]['temperature'] for n in graph.nodes])
    
    normalized_congestion = congestion / (len(path) * avg_congestion)
    normalized_temperature = temperature / (len(path) * avg_temperature)
    
    return wc * normalized_congestion + wt * normalized_temperature
