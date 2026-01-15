import io
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
from scripts.utils.util_mtx import save_graph_as_mtx

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

    # Deterministic layout
    pos = nx.spring_layout(G, seed=42)

    # Plot graph
    plt.figure(figsize=(8, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=600,
        edge_color="gray",
    )

    try:
        plt.show(block=False)
    except TypeError:
        plt.show()
