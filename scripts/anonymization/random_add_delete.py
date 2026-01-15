import io
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
from scripts.utils.util_mtx import save_graph_as_mtx

## rand add/del function

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

    ## make a copy of G (our graph above)
    cpyG = G.copy()
    edges = list(cpyG.edges())

    for _ in range(k):
        # choose a random edge from the set
        # choose another edge
        e1 = random.choice(list(edges))
        e2 = random.choice(list(edges))

        if(e1 == e2):
            continue

        a, b = e1
        c, d = e2

        ## check to make sure all nodes are distinct
        if len({a,b,c,d}) < 4:
            continue

        if(a, d) in cpyG.edges() or (d, a) in cpyG.edges():
            continue
        if(b, c) in cpyG.edges() or (c, b) in cpyG.edges():
            continue

        # swap
        cpyG.remove_edge(a,b)
        cpyG.remove_edge(c,d)
        cpyG.add_edge(a,d)
        cpyG.add_edge(b,c)

        edges = list(cpyG.edges())
    plt.figure(figsize=(8,8))
    nx.draw(
        cpyG,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=600,
        edge_color="gray",
        )
    try:
        plt.show(block=False)
    except TypeError:
        plt.show()

    # Save modified graph as .mtx next to the input file
    try:
        base = os.path.splitext(os.path.basename(file_path))[0]
        out_path = os.path.join(os.path.dirname(file_path), f"{base}_randadddel.mtx")
        save_graph_as_mtx(cpyG, out_path, comment="random_add_delete output", remap_to_one_based=False)
        print(f"Saved modified graph to: {out_path}")
        return out_path
    except Exception as e:
        print(f"Failed to save .mtx: {e}")
        return None
