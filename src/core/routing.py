from heapq import heappop, heappush
from src.core.metrics import calculate_path_score
import networkx as nx

def find_best_path(graph, source, target, wc, wt):
    """Finds the best path using a weighted metric."""
    queue = [(0, source, [])]
    visited = set()
    best_path = None
    best_score = float('inf')

    while queue:
        score, current, path = heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == target:
            path_score = calculate_path_score(graph, path, wc, wt)
            if path_score < best_score:
                best_score = path_score
                best_path = path
            continue

        for neighbor in graph.neighbors(current):
            heappush(queue, (score, neighbor, path))

    return best_path, best_score

def bidirectional_search(graph, source, target, wc, wt):
    """Performs a bidirectional search and selects the optimal path."""
    clockwise_path, clockwise_score = find_best_path(graph, source, target, wc, wt)
    counterclockwise_path, counterclockwise_score = find_best_path(graph, target, source, wc, wt)

    if clockwise_score < counterclockwise_score:
        return clockwise_path, clockwise_score
    else:
        return counterclockwise_path[::-1], counterclockwise_score

def multicast_search(graph, sources, targets, wc, wt):
    """Performs multicast search from each source to all targets."""
    paths_dict = {}
    scores_dict = {}
    
    for source in sources:
        # Calculate total scores for both directions
        clock_paths = [get_clockwise_path(graph, source, target) for target in targets]
        counter_paths = [get_counter_clockwise_path(graph, source, target) for target in targets]
        
        # Calculate combined scores for all paths in each direction
        clock_total_score = sum(calculate_path_score(graph, path, wc, wt) for path in clock_paths)
        counter_total_score = sum(calculate_path_score(graph, path, wc, wt) for path in counter_paths)
        
        # Choose direction based on total score
        if clock_total_score <= counter_total_score:
            paths_dict[source] = clock_paths
            scores_dict[source] = [calculate_path_score(graph, path, wc, wt) for path in clock_paths]
        else:
            paths_dict[source] = counter_paths
            scores_dict[source] = [calculate_path_score(graph, path, wc, wt) for path in counter_paths]
    
    return paths_dict, scores_dict

def get_clockwise_path(graph, start, end):
    path = [start]
    current = start
    while current != end:
        current = (current + 1) % len(graph)
        path.append(current)
    return path

def get_counter_clockwise_path(graph, start, end):
    path = [start]
    current = start
    while current != end:
        current = (current - 1) % len(graph)
        path.append(current)
    return path

def shortest_path_first(graph, sources, targets):
    """Implements Shortest Path First algorithm for multicast routing."""
    paths_dict = {}
    scores_dict = {}
    
    for source in sources:
        # Calculate total path lengths for both directions
        clock_paths = [get_clockwise_path(graph, source, target) for target in targets]
        counter_paths = [get_counter_clockwise_path(graph, source, target) for target in targets]
        
        # Choose direction based on total path length
        clock_total_length = sum(len(path) for path in clock_paths)
        counter_total_length = sum(len(path) for path in counter_paths)
        
        if clock_total_length <= counter_total_length:
            paths_dict[source] = clock_paths
            scores_dict[source] = [len(path) for path in clock_paths]
        else:
            paths_dict[source] = counter_paths
            scores_dict[source] = [len(path) for path in counter_paths]
    
    return paths_dict, scores_dict