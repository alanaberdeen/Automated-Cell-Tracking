# a_matrix.py
# Construct the parameters for the linear optimisation
#

# Import external packages
import networkx as nx
import numpy as np

__all__ = ["a_matrix",
           "build_coupled_edges",
           "couple_node_sets",
           "reduce_to_coupled",
           "adjust_capacity_edges"]


def a_matrix(g):

    # couple_matrix
    # Construct coupled graph matrix from graph structure
    #
    # Inputs:   g           -   current graph structure
    #
    # Outputs:  a_coup      -   coupled incidence matrix
    #           a_vertices  -   order of vertices in coupled matrix
    #

    # order of vertices in incidence matrix
    nodelist = g.nodes()
    a_vertices = [n for n in nodelist if 'M' not in n and 'S' not in n]

    # Incidence matrix
    a_sparse = nx.incidence_matrix(g, nodelist=nodelist, oriented=True)
    a_dense = a_sparse.todense()

    # Build new coupled edges
    edges_to_add = build_coupled_edges(g, nodelist)

    # Add edges to matrix
    a_extra = np.hstack((a_dense, edges_to_add))

    # Remove split/merge vertices and previously associated edges
    a_reduce = reduce_to_coupled(a_extra, nodelist)

    # Adjust for higher capacity edges
    a_cap = adjust_capacity_edges(a_reduce, nodelist)

    a_coup = a_cap.copy()
    return a_coup, a_vertices


def build_coupled_edges(g, nodelist):

    # new_coupled_edges
    # given a graph structure returns list of new coupled edges.
    #
    # Inputs:   g           - graph structure
    #           nodelist    - order of rows in incidence matrix
    #
    # Outputs:  new_edges   - list of edges to add

    # Initialise list of new edges
    new_edges = []

    # Loop through nodes
    for node in nodelist:
        if 'M' in node or 'S' in node:

            # sets of neighbouring nodes is split/merge is in solution
            fixed_set, cycle_set = couple_node_sets(g, node)

            fixed_edge = [0] * len(nodelist)
            for f in fixed_set:
                fixed_edge[nodelist.index(f[0])] = f[1]

            for c in cycle_set:
                coupled_edge = list(fixed_edge)
                coupled_edge[nodelist.index(c[0])] = c[1]
                try:
                    new_edges.append(coupled_edge)
                except UnboundLocalError:
                    new_edges = list(coupled_edge)

    new_array = np.asarray(new_edges)
    new_array = np.transpose(new_array)

    return new_array


def couple_node_sets(g, node):

    # couple_sets
    # Find the sets of coupling neighbour nodes.
    #
    # Inputs:   g       - graph structure
    #           node    - node in question
    #
    # Outputs:  fixed_set - invariant neighbours when node is in solution
    #           cycle_set - varying neighbours when node is in solution

    s = [(n, 1) for n in g.successors(node)]
    p = [(n, -1) for n in g.predecessors(node)]

    cycle_set = None
    fixed_set = None

    if 'M' in node:
        s.remove(('D', 1))
        p.append(('D', 1))

        cycle_set = s
        fixed_set = p

    elif 'S' in node:
        p.remove(('A', -1))
        s.append(('A', -1))

        cycle_set = p
        fixed_set = s

    return fixed_set, cycle_set


def reduce_to_coupled(a_extra, nodelist):

    # reduce_to_coupled
    # Given a_matrix with new coupled edges appended. Remove the split/merge
    # vertices and their connected edges
    #
    # Inputs:   a_extra     -   a matrix with coupled edges appended
    #           nodelist    -   order of vertices in incidence matrix
    #
    # Outputs:  a_reduced   -   Incidence matrix without redundant edges

    edges_to_remove = set()
    required_vertices = []

    for row, node in enumerate(nodelist):
        required_vertices.append(row)

        if 'M' in node or 'S' in node:

            # remove from included vertices
            required_vertices.pop()

            # Find edges to remove
            row = a_extra[row, :].nonzero()[1]
            for e in row:
                edges_to_remove.add(e)

    # Therefore the included edges are the
    required_edges = list(set(range(a_extra.shape[1])) - edges_to_remove)

    # Reduce to only included vertices/edges
    a_reduced = a_extra[np.ix_(required_vertices, required_edges)]

    return a_reduced


def adjust_capacity_edges(a_dense, nodelist):

    # adjust_capacity_edges
    # Account for the larger capacity edges in the graph by appending the
    # specific edges to the matrix the required amount of times.
    #
    # Inputs:   a_dense     -   incidence matrix
    #           nodelist    -   order of rows in matrix
    #
    # Outputs:  a_cap       -   incidence matrix adjusted for edge capacity
    #

    a_cap = a_dense.copy()

    # Coupled nodes
    couple_vertices = [n for n in nodelist if 'M' not in n and 'S' not in n]

    # Total nodes
    l_nodes = sum(1 for x in couple_vertices if 'L' in x)
    r_nodes = sum(1 for x in couple_vertices if 'R' in x)

    # Edge indices connected to nodes
    source_e = np.nonzero(a_dense[couple_vertices.index('T+'), :])[1]
    a_e = np.nonzero(a_dense[couple_vertices.index('A'), :])[1]
    d_e = np.nonzero(a_dense[couple_vertices.index('D'), :])[1]
    sink_e = np.nonzero(a_dense[couple_vertices.index('T-'), :])[1]

    # Edges
    source_a = set(source_e).intersection(a_e).pop()
    a_d = set(a_e).intersection(d_e).pop()
    d_sink = set(d_e).intersection(sink_e).pop()

    # Add Edges appropriate number of times
    for x in xrange(1, r_nodes):
        a_cap = np.hstack((a_cap, a_cap[:, source_a]))

    for x in xrange(1, l_nodes):
        a_cap = np.hstack((a_cap, a_cap[:, a_d]))
        a_cap = np.hstack((a_cap, a_cap[:, d_sink]))

    return a_cap
