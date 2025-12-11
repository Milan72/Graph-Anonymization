import io
import random
import networkx as nx
import matplotlib.pyplot as plt

## naive anonymization function

def run(file_path, k):
    # Open whatever file the user selected in the GUI
    with open(file_path) as f:
        lines = [l for l in f if not l.startswith('%') and not l.startswith('%%')]

    # Parse the MTX metadata
    _, _, num_edges = map(int, lines[0].split())

    # Convert each remaining line into a tuple (u, v)
    edges_data = [tuple(map(int, line.split())) for line in lines[1:]]

    print(f"Loaded {len(edges_data)} edges.")

    # Create graph
    G = nx.Graph()
    G.add_edges_from(edges_data)

  

    ## make a copy of G (our graph above)
    cpyG = G.copy()
    
    # Naive anonymization: simply relabel nodes with anonymous IDs
    # This removes node identities but preserves all structural properties
    mapping = {old_node: i for i, old_node in enumerate(cpyG.nodes())}
    cpyG = nx.relabel_nodes(cpyG, mapping)

    # Deterministic layout (after relabeling to match new node IDs)
    pos = nx.spring_layout(cpyG, seed=42)
    

    plt.figure(figsize=(8,8))
    nx.draw(
        cpyG,
        pos,
        with_labels=True,
        node_color="lightyellow",
        node_size=600,
        edge_color="gray",
        )
    plt.show()
