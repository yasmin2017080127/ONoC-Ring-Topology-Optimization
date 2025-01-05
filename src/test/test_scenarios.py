def create_test_scenario_1(graph):
    """High congestion and temperature on shortest paths."""
    # Set high temperature on shortest paths
    for node in range(len(graph)):
        if node < len(graph) // 2:
            graph.nodes[node]['temperature'] = 85.0  # High temperature
        else:
            graph.nodes[node]['temperature'] = 65.0  # Normal temperature
    
    # Set high congestion on shortest paths
    for u, v in graph.edges():
        if u < len(graph) // 2 and v < len(graph) // 2:
            graph[u][v]['utilization'] = 90.0  # High congestion
        else:
            graph[u][v]['utilization'] = 30.0  # Normal congestion
    
    return graph

def create_test_scenario_2(graph):
    """Hotspots and congestion bottlenecks."""
    # Create hotspots
    hotspots = [5, 15, 25]
    for node in graph.nodes():
        if node in hotspots:
            graph.nodes[node]['temperature'] = 90.0
            # Set high congestion around hotspots
            for neighbor in graph.neighbors(node):
                graph[node][neighbor]['utilization'] = 85.0
        else:
            graph.nodes[node]['temperature'] = 60.0
            for neighbor in graph.neighbors(node):
                graph[node][neighbor]['utilization'] = 25.0
    
    return graph
