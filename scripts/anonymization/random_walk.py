import io
import random
import networkx as nx
import matplotlib.pyplot as plt



def run(file_path, k):
    # Open whatever file the user selected in the GUI
    with open(file_path) as f:
        lines = [l for l in f if not l.startswith('%') and not l.startswith('%%')]

    # Parse the MTX metadata
    _, _, num_edges = map(int, lines[0].split())

    # Convert each remaining line into a tuple (u, v)
    edges_data = [tuple(map(int, line.split())) for line in lines[1:]]

    print(f"Loaded {len(edges_data)} edges.")
    print(f"Random Walk Anonymization with walk length k={k}")

    # Create original graph
    G = nx.Graph()
    G.add_edges_from(edges_data)

    # Deterministic layout (computed on original graph for consistency)
    pos = nx.spring_layout(G, seed=42)

    # Make a copy of G for anonymization (preserve original)
    cpyG = G.copy()
    
    # Get list of edges to process (from original graph structure)
    # We iterate over original edges to ensure each edge is processed exactly once
    edges_to_process = list(G.edges())
    
    # Track statistics
    self_loops_avoided = 0
    duplicates_avoided = 0
    
    # For each edge (u, v) in original graph, perform random walk anonymization
    for u, v in edges_to_process:
        # Perform a random walk of length k starting from v
        # Walk is performed on ORIGINAL graph G to maintain proper statistics
        current = v
        
        # Random walk: start at v, take k steps
        for step in range(k):
            # Get neighbors of current node in original graph
            neighbors = list(G.neighbors(current))
            
            # If no neighbors (isolated node), cannot continue walk
            # Endpoint remains at current node
            if not neighbors:
                break
            
            # Move to random neighbor (uniform random choice)
            # This naturally preserves degree distribution: high-degree nodes
            # are visited more frequently
            current = random.choice(neighbors)
        
        # Endpoint of random walk
        endpoint = current
        
        # Remove original edge (u, v) from anonymized graph
        if cpyG.has_edge(u, v):
            cpyG.remove_edge(u, v)
        
        # Add anonymized edge (u, endpoint) with constraints:
        # 1. Avoid self-loops: u != endpoint
        # 2. Avoid duplicates: edge (u, endpoint) should not already exist
        
        # Check for self-loop
        if u == endpoint:
            # Self-loop detected: keep original edge or use a neighbor of u
            # Strategy: use a random neighbor of u (if available) instead
            u_neighbors = list(G.neighbors(u))
            if u_neighbors:
                # Exclude v to avoid recreating original edge
                candidates = [n for n in u_neighbors if n != v]
                if candidates:
                    endpoint = random.choice(candidates)
                else:
                    # If only v is available, use it (better than self-loop)
                    endpoint = v
            else:
                # u has no neighbors, cannot avoid self-loop
                # Keep original edge in this case
                cpyG.add_edge(u, v)
                self_loops_avoided += 1
                continue
        
        # Check for duplicate edge
        if cpyG.has_edge(u, endpoint):
            # Duplicate detected: try to find alternative endpoint
            # Strategy: continue walk one more step or use different neighbor
            endpoint_neighbors = list(G.neighbors(endpoint))
            if endpoint_neighbors:
                # Take one more step to avoid duplicate
                alternative_endpoint = random.choice(endpoint_neighbors)
                if alternative_endpoint != u and not cpyG.has_edge(u, alternative_endpoint):
                    endpoint = alternative_endpoint
                else:
                    # If alternative also creates duplicate/self-loop, keep original edge
                    cpyG.add_edge(u, v)
                    duplicates_avoided += 1
                    continue
            else:
                # No alternative, keep original edge
                cpyG.add_edge(u, v)
                duplicates_avoided += 1
                continue
        
        # Add the anonymized edge (u, endpoint)
        # This preserves the number of edges (one-to-one replacement)
        cpyG.add_edge(u, endpoint)
    
    # Print statistics
    print(f"Anonymization complete.")
    print(f"  Original edges: {G.number_of_edges()}")
    print(f"  Anonymized edges: {cpyG.number_of_edges()}")
    print(f"  Self-loops avoided: {self_loops_avoided}")
    print(f"  Duplicates avoided: {duplicates_avoided}")
    
    # Check connectivity
    if not nx.is_connected(cpyG):
        num_components = nx.number_connected_components(cpyG)
        print(f"  Warning: Graph has {num_components} connected components")
    else:
        print(f"  Graph remains connected")
    
    # Visualize anonymized graph
    plt.figure(figsize=(8,8))
    nx.draw(
        cpyG,
        pos,
        with_labels=True,
        node_color="lightcoral",
        node_size=600,
        edge_color="gray",
        )
    plt.title(f"Random Walk Anonymization (k={k})")
    plt.show()
