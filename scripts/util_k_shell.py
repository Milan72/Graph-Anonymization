import networkx as nx
import matplotlib.pyplot as plt

def run(file_path, k):
    """
    Compute the k-shell of the graph and evaluate a k-shell utility metric.
    Utility = (Number of nodes in k-shell / Original number of nodes)
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

    # Degree info
    max_deg = max(dict(G.degree()).values())
    print("Max degree in graph =", max_deg)

    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # --- Compute k-shell ---
    try:
        kshell = nx.k_shell(G, k=k)
    except nx.NetworkXError:
        print(f"Invalid k={k} for shell decomposition.")
        return

    shell_nodes = kshell.number_of_nodes()
    original_nodes = G.number_of_nodes()

    # Utility metric
    utility = shell_nodes / original_nodes if original_nodes > 0 else 0

    print(f"K-shell size (k={k}): {shell_nodes} nodes")
    print(f"Utility metric U_kShell = {utility:.4f}")

    if shell_nodes == 0:
        print(f"No nodes lie exactly in the {k}-shell.")
        return

    # --- Visualization ---
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 8))

    # Draw original faded graph
    nx.draw(
        G, pos,
        node_color="#dddddd",
        edge_color="#cccccc",
        alpha=0.25,
        with_labels=False
    )

    # Highlight ONLY the k-shell
    nx.draw(
        kshell, pos,
        node_color="orange",
        edge_color="red",
        node_size=600,
        with_labels=True
    )

    plt.title(f"K-Shell (k={k}) — Utility={utility:.4f}")
    plt.show()
