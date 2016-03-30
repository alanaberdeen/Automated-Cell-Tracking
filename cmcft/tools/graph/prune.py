# prune.py
# reduce the complexity of the graph
#

import networkx


def prune(graph, alpha):

    # prune
    # Function removes the edges of the graph with the highest costs to
    # reduce the complexity of the optimisation problem
    #
    # Inputs:   graph   -   current graph structure
    #           alpha   -   fraction of lowest cost edges to retain
    #
    # Outputs:  graph   -   pruned graph structure
    #
    #

    # Useful subset lists of types of nodes
    l_n = []
    m_n = []
    for n in graph.nodes_iter():
        if 'L' in n:
            l_n.append(n)
        elif 'M' in n:
            m_n.append(n)

    ####
    # Prune move and split edges
    for n in l_n:

        # Collect edges
        move_edges = [i for i in graph.edges(n, data=True) if 'R' in i[1]]
        split_edges = [i for i in graph.edges(n, data=True) if 'S' in i[1]]

        # Find sets to be removed
        move_prune = prune_set(move_edges, alpha=alpha)
        split_prune = prune_set(split_edges, alpha=alpha)

        # Remove specified edges from graph
        remove_edges = move_prune + split_prune
        graph.remove_edges_from(remove_edges)

    ###
    # Prune merge edges
    for n in m_n:

        # Collect edges
        merge_edges = [i for i in graph.edges(n, data=True) if 'R' in i[1]]

        # Find sets to be removed
        merge_prune = prune_set(merge_edges, alpha=alpha)

        # Remove specified edges from graph
        graph.remove_edges_from(merge_prune)

    return graph


def prune_set(edges, alpha):

    # prune_set
    # Sorts the edges in order of increasing cost a returns set to be removed
    #
    # Inputs:   edges   -   list of edges
    #           alpha   -   proportion to retain
    #
    # Outputs:  remove  -   list of edges to be removed
    #

    # Sort by order of increasing cost
    edges.sort(key=lambda tup: tup[2]['weight'])

    # Retain required proportion of edges with lowest cost
    retain_index = int(round(alpha * len(edges)))
    remove_edges = edges[retain_index:]

    return remove_edges
