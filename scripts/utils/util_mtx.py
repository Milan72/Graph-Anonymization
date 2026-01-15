import os

def save_graph_as_mtx(G, out_path=None, comment=None, remap_to_one_based=True):
    """Save a NetworkX graph `G` to Matrix Market (.mtx) coordinate format.

        - By default (`remap_to_one_based=True`) nodes are remapped to 1..n in the
            output file to match typical MTX files. If `remap_to_one_based=False`,
            the node labels from `G.nodes()` are written verbatim (they must be
            integers to be written directly).
        - Writes a symmetric `pattern` matrix for undirected graphs (one entry per edge).

    Parameters:
    - G: networkx.Graph-like object with integer or hashable node labels.
    - out_path: destination path. If None, raises ValueError.
    - comment: optional comment string written as a `%` line.

    Returns the path written.
    """
    if out_path is None:
        raise ValueError("out_path must be provided")

    nodes = list(G.nodes())

    if remap_to_one_based:
        # Build a deterministic mapping of nodes -> 1..n
        mapping = {node: i + 1 for i, node in enumerate(nodes)}
        n = len(nodes)

        # For undirected graphs, write each edge once. Preserve the edge order from G.edges().
        edges = []
        for u, v in G.edges():
            uu = mapping[u]
            vv = mapping[v]
            edges.append((uu, vv))

        m = len(edges)
    else:
        # Use node labels as-is. They must be integers for MTX coordinate format.
        try:
            int_nodes = [int(n) for n in nodes]
        except Exception:
            raise ValueError("All node labels must be integers when remap_to_one_based=False")
        n = max(int_nodes) if int_nodes else 0

        # Write edges using original labels
        edges = []
        for u, v in G.edges():
            edges.append((int(u), int(v)))

        m = len(edges)

    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or '.', exist_ok=True)

    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('%%MatrixMarket matrix coordinate pattern symmetric\n')
        if comment:
            fh.write(f"% {comment}\n")
        if remap_to_one_based:
            fh.write(f"% node_mapping: original_label->new_label (1-based)\n")
            # optionally include mapping details
            for orig, new in mapping.items():
                fh.write(f"% {orig} -> {new}\n")
            fh.write(f"{n} {n} {m}\n")
            for u, v in edges:
                fh.write(f"{u} {v}\n")
        else:
            fh.write(f"{n} {n} {m}\n")
            for u, v in edges:
                fh.write(f"{u} {v}\n")

    return out_path
