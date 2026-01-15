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

    # Create graph
    cpyG = G.copy()
    nodes = list(cpyG.nodes())

    for _ in range(k):

        # get all possible node pairs
        possibleEdges = set((u, v) for i, u in enumerate(nodes)
                                        for v in nodes[i+1:])

        #find existing edges
        edges = set(cpyG.edges())

        # false edges possibilities (all edges that could exist but don't)
        nonedges = list(possibleEdges - edges)

        # no more possibilities (there are no remaining possible edges that dont exist)
        if not nonedges:
            break
        # take a random edge from the list we just made
        newedge = random.choice(nonedges)

        # add this edge to the graph copy
        cpyG.add_edge(*newedge)

        # delete one edge at random
        trueEdges = list(cpyG.edges())

        # error handling if there are no more true edges (this shouldn't really happen)
        if not trueEdges:
            break

        edgeToRemove = random.choice(list(edges))
        cpyG.remove_edge(*edgeToRemove)
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
        out_path = os.path.join(os.path.dirname(file_path), f"{base}_randswitch.mtx")
        save_graph_as_mtx(cpyG, out_path, comment="random_switch output", remap_to_one_based=False)
        print(f"Saved modified graph to: {out_path}")
        return out_path
    except Exception as e:
        print(f"Failed to save .mtx: {e}")
        return None
