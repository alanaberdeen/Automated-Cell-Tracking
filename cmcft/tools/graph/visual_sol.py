# graph_sol.py

# import external packages
import numpy as np
import networkx as nx


def graph_sol(a_matrix, vertices, x):

    # graph_sol
    # Function to visualise the output from the optimisation
    #
    # Input:    a_matrix    -  coupled incidence matrix
    #           vertices    - list giving the order of the vertices (rows) in
    #                         the incidence matrix
    #           x           - pyomo optimisation output
    #
    # Output:   g_sol       - graphical representation of the solution
    #

    # -----
    # Reduce the matrix to only included vertices and edges

    # extract included edges as list
    included_edges = list()
    for col in xrange(len(x)):
        included_edges.append(x[col].value)

    # remove edges not included from incidence matrix
    edges_to_remove = list()
    for j in xrange(len(included_edges)):
        if included_edges[j] == 0:
            edges_to_remove.append(j)

    a_reduced = np.delete(a_matrix, edges_to_remove, 1)

    # -----
    # construct graph of solution
    g = nx.DiGraph()

    # add nodes
    g.add_nodes_from(vertices)

    # add edges
    for col in xrange(a_reduced.shape[1]):
        start_nodes = list()
        finish_nodes = list()

        edge = (a_reduced[:, col])
        node_i = np.nonzero(edge)

        for node in node_i[0]:
            if edge[node] < 0:
                start_nodes.append(node)
            else:
                finish_nodes.append(node)

        for x in xrange(len(start_nodes)):
            g.add_edge(vertices[start_nodes[x]], vertices[finish_nodes[x]])

    return g
