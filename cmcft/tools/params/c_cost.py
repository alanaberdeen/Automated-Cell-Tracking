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
        v = [a_vertices[i] for i in vertex_indices[1]]

        # Get weights
        cost = 0

        # For simple edges
        if len(v) == 2:
            try:
                cost = g[v[0]][v[1]]['weight']
            except KeyError:
                cost = g[v[1]][v[0]]['weight']

        # For coupled edges
        elif len(v) == 4:

            # Find merge/split event label
            ms_node = ms_event(v, g)

            for n in v:
                try:
                    cost = cost + g.edge[n][ms_node]['weight']
                except KeyError:
                    cost = cost + g.edge[ms_node][n]['weight']

        # Append to cost vector
        c.append(cost)

    return c


def ms_event(vertices, graph):

    # ms_event
    # given 4 nodes find the split or merge vertex that they are connected to
    #
    # Inputs:   vertices    - list of 4 node labels
    #           graph       - graph structure
    # Outputs:  event_label - label of split/merge node
    #

    # initialise set
    num = []
    event = None

    # split nodes
    if 'D' in vertices:
        event = 'M'

        for n in vertices:
            if 'L' in n:
                num.append(''.join(i for i in n if i.isdigit()))

    # merge nodes
    elif 'A' in vertices:
        event = 'S'

        for n in vertices:
            if 'R' in n:
                num.append(''.join(i for i in n if i.isdigit()))

    # Combine to give event label
    event_label = (event + '(' + num[0] + ',' + num[1] + ')')

    # Check if correct way around
    if not graph.has_node(event_label):
        event_label = (event + '(' + num[1] + ',' + num[0] + ')')

    return event_label

