## General test instructions for graph integrity after anonymization

# We need to make sure that graphs that are saved after anonymization are correct.
# That means feeding the anonimized graph from the anonymization scripts AND the newly saved graphs
# into a comparator (isomorphism check, and degree sequence check) to make sure thre are no
# accidental structural changes in the pipeline.

# use the following functions in the test suite

#  -- sorted(dict(G1.degree()).values()) == sorted(dict(G2.degree()).values())
# this checks degree sequence equality

#  -- nx.is_isomorphic(G1, G2)
# this checks full isomorphism

# make sure to import networkx as nx in the test file
# If you can think of any other ways to check the pipeline integrity, please add them here.



