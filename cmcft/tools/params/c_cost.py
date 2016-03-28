# c_cost.py
# Cost vector for edges in coupled matrix

import numpy as np

__all__ = ["c_cost"]


def c_cost(g, a_coup, a_vertices):

    # c_cost
    # creates vector of costs for edges
    #
    # Inputs:   g           - graph structure
    #           a_coup      - coupled incidence matrix
    #           a_vertices  - order of rows in coupled matrix
    #
    # Outputs:  c           - list of costs for each edge in incidence matrix
    #

    # Initialise cost vector
    c = []

    # For all edges in coupled matrix
    for e in xrange(a_coup.shape[1]):

        # Get vertices connected by edge
        vertex_indices = np.nonzero(a_coup[:, e])[0]
        vertices = [a_vertices[i] for i in vertex_indices]

        # Get weights
        weights = []

        # For simple edges
        if len(vertices) == 2:
            for v in vertices:
                try:
                    connect = set(g.edge[v]).intersection(vertices).pop()
                    weights.append(g.edge[v][connect]['weight'])
                except KeyError:
                    pass

        # For coupled edges
        elif len(vertices) == 4:

            # Find merge/split node that has been coupled
            neighbours = []
            for v in vertices:
                neighbours.append(set(g.predecessors(v) + g.successors(v)))
            ms_node = set.intersection(*neighbours).pop()

            for v in vertices:
                try:
                    weights.append(g.edge[v][ms_node]['weight'])
                except KeyError:
                    weights.append(g.edge[ms_node][v]['weight'])

        # Calc costs
        edge_cost = sum(w for w in weights)

        # Add to cost vector
        c.append(edge_cost)

    return c
