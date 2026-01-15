import networkx as nx
import matplotlib.pyplot as plt

def run(file_path, k):
    """
    Compute the k-core of the graph and evaluate the k-core utility metric.
    Utility = (Number of nodes in k-core / Original number of nodes)
    """

    # --- Load MTX network file ---
    with open(file_path) as f:
        lines = [l for l in f if not l.startswith('%') and not l.startswith('%%')]

    # Parse header
    _, _, num_edges = map(int, lines[0].split())

    # Convert each remaining line into an edge pair
    edges_data = [tuple(map(int, line.split())) for line in lines[1:]]

    # Build graph
    G = nx.Graph()
    G.add_edges_from(edges_data)

    max_deg = max(dict(G.degree()).values())
    print("Max degree in graph =", max_deg)


    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # --- Compute k-core ---
    try:
        kcore = nx.k_core(G, k=k)
    except nx.NetworkXError:
        print(f"Error: k={k} is too large — produces an empty graph.")
        return

    core_nodes = kcore.number_of_nodes()
    original_nodes = G.number_of_nodes()

    # Utility metric
    utility = core_nodes / original_nodes if original_nodes > 0 else 0

    print(f"K-core size (k={k}): {core_nodes} nodes")
    print(f"Utility metric U_k = {utility:.4f}")

    # --- Visualization ---
    # Layout from original graph for consistent positioning
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 8))

    # Draw original graph faded
    nx.draw(
        G,
        pos,
        node_color="#dddddd",
        edge_color="#cccccc",
        alpha=0.3,
        with_labels=False
    )

    # Draw k-core highlighted
    nx.draw(
        kcore,
        pos,
        node_color="orange",
        edge_color="red",
        node_size=600,
        with_labels=True
    )

    plt.title(f"K-Core (k={k}) — Utility={utility:.4f}")
    try:
        plt.show(block=False)
    except TypeError:
        plt.show()
