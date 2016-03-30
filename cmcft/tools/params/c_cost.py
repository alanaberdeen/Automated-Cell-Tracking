# c_cost.py
# Cost vector for edges in coupled matrix

import numpy as np

__all__ = ["c_cost"]


def c_cost(g, a_coup, a_vertices):

    # TODO: think this function is slow. Check for performance increases.
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

    # For all edges in coupled matrix (iterating over transpose)
    for e in a_coup.T:

        # Get vertices connected by edge
        vertex_indices = np.nonzero(e)
        vertices = [a_vertices[i] for i in vertex_indices[1]]

        # Get weights
        weights = []

        # For simple edges
        if len(vertices) == 2:
            try:
                weights.append(g[vertices[0]][vertices[1]]['weight'])
            except KeyError:
                weights.append(g[vertices[1]][vertices[0]]['weight'])

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
        edge_cost = sum(weights)

        # Add to cost vector
        c.append(edge_cost)

    return c
