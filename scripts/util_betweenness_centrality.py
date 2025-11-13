import networkx as nx
import matplotlib.pyplot as plt

def run(file_path, k):
    """
    Compute betweenness centrality utility.
    Utility = (# nodes with betweenness >= k) / N
    """

    # --- Load MTX network file ---
    with open(file_path) as f:
        lines = [l for l in f if not l.startswith('%') and not l.startswith('%%')]

    _, _, num_edges = map(int, lines[0].split())
    edges_data = [tuple(map(int, line.split())) for line in lines[1:]]

    G = nx.Graph()
    G.add_edges_from(edges_data)

    print(f"Loaded {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # --- Betweenness centrality ---
    print("\nComputing betweenness centrality...")
    bc = nx.betweenness_centrality(G, normalized=True)

    # Print values
    for node, val in bc.items():
        print(f"Node {node}: {val:.4f}")

    avg_bc = sum(bc.values()) / len(bc)
    print(f"\nAverage Betweenness: {avg_bc:.4f}")

    # Utility metric
    surviving = sum(1 for val in bc.values() if val >= k)
    utility = surviving / len(bc)
    print(f"Utility (BC >= {k}): {utility:.4f}")

    # --- Visualization ---
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 8))
    ax = plt.gca()  # get current axes

    node_colors = [bc[n] for n in G.nodes()]

    # Draw on the axes explicitly
    nodes = nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        cmap=plt.cm.viridis,
        node_size=600,
        ax=ax
    )
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#999")
    nx.draw_networkx_labels(G, pos, ax=ax)

    # Colorbar MUST use the "nodes" object
    cbar = plt.colorbar(nodes, ax=ax)
    cbar.set_label("Betweenness")

    plt.title(f"Betweenness Centrality\nUtility (BC >= {k}) = {utility:.4f}")
    plt.axis("off")
    plt.show()
