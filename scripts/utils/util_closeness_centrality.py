import networkx as nx
import matplotlib.pyplot as plt

def run(file_path, k):
    """
    Compute closeness centrality utility.
    Utility = (# nodes with closeness >= k) / N
    """

    # --- Load MTX network file ---
    with open(file_path) as f:
        lines = [l for l in f if not l.startswith('%') and not l.startswith('%%')]

    _, _, num_edges = map(int, lines[0].split())
    edges_data = [tuple(map(int, line.split())) for line in lines[1:]]    

    G = nx.Graph()
    G.add_edges_from(edges_data)

    print(f"Loaded {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # --- Closeness centrality ---
    print("\nComputing closeness centrality...")
    cc = nx.closeness_centrality(G)

    # Print values
    for node, val in cc.items():
        print(f"Node {node}: {val:.4f}")

    avg_cc = sum(cc.values()) / len(cc)
    print(f"\nAverage Closeness: {avg_cc:.4f}")

    # Utility metric
    surviving = sum(1 for val in cc.values() if val >= k)
    utility = surviving / len(cc)
    print(f"Utility (CC >= {k}): {utility:.4f}")

    # --- Visualization ---
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    node_colors = [cc[n] for n in G.nodes()]

    nodes = nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        cmap=plt.cm.plasma,
        node_size=600,
        ax=ax
    )
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#999")
    nx.draw_networkx_labels(G, pos, ax=ax)

    cbar = plt.colorbar(nodes, ax=ax)
    cbar.set_label("Closeness")

    plt.title(f"Closeness Centrality\nUtility (CC >= {k}) = {utility:.4f}")
    plt.axis("off")
    try:
        plt.show(block=False)
    except TypeError:
        plt.show()
