# edges.py
# Functions used to build edges in graph structure

# Import functions
from cost_calcs import *


def build(g_in, w, alpha):

    # build
    # Create the edges for the graph structure. Edge weights are
    # calculated and set as attributes as in the Coupled Minimum Cost
    # Flow Tracking algorithm
    #
    # Inputs:   g_in    - initialised graph node structure to be built upon
    #           w       - feature weights (set empirically)
    #           alpha   - pruning parameter, fraction of lowest cost
    #                     edges to retain
    # Outputs:  g_out   - updated graph with the correct edges added
    #

    # Set edge weights from dummy nodes as no cost
    dummy_cost = 0

    # ------------------------------------------------------------------------
    # Create useful subset dicts of nodes
    node_sets = {'l_n': [], 'r_n': [], 's_n': [], 'm_n': []}

    for label in g_in.nodes():

        if 'L' in label:
            node_sets['l_n'].append(label)
        elif 'R' in label:
            node_sets['r_n'].append(label)
        elif 'S' in label:
            node_sets['s_n'].append(label)
        elif 'M' in label:
            node_sets['m_n'].append(label)

    # ------------------------------------------------------------------------
    # Running through the sets, build the edges.

    #
    # -----
    # FROM split edges
    for s_node in node_sets['s_n']:
        # TO R nodes
        for r_node in node_sets['r_n']:
            if extract_num(r_node).intersection(extract_num(s_node)):
                g_in.add_edge(s_node, r_node, weight=dummy_cost)

    #
    # -----
    # FROM merge edges
    for m_node in node_sets['m_n']:

        # TO R nodes
        merge_edges = []
        for r_node in node_sets['r_n']:
            cost = w * merge_cost(g_in.node, r_node, m_node) * 10
            merge_edges.append((m_node, r_node, cost))

        # Prune and add subset of edges to graph
        edges_to_add = prune_set(merge_edges, alpha=alpha)
        g_in.add_weighted_edges_from(edges_to_add)

        # TO disappear node
        g_in.add_edge(m_node, 'D', weight=dummy_cost)

    #
    # -----
    # FROM appear node
    # TO split nodes
    for s_node in node_sets['s_n']:
        g_in.add_edge('A', s_node, weight=dummy_cost)

    # TO disappear node
    g_in.add_edge('A', 'D', weight=dummy_cost)

    # TO R nodes
    appear_edges = []
    for r_node in node_sets['r_n']:
        # find closest border
        dist_border = closest_border(g_in, r_node)

        # Feature costs: Movement and Change in Area
        move_c = w * dist_border
        area_c = w * area_diff(g_in.node[r_node]['area'], g_in.node['A']['area'])
        cost = int(area_c + move_c) * 1

        appear_edges.append(('A', r_node, cost))

    # Prune and add subset of edges to graph
    edges_to_add = prune_set(appear_edges, alpha=alpha)
    g_in.add_weighted_edges_from(edges_to_add)

    #
    # -----
    # FROM L nodes
    disappear_edges = []
    for l_node in node_sets['l_n']:

        # TO R nodes - simple move edges
        move_edges = []
        for r_node in node_sets['r_n']:

            # Feature costs: Movement and Change in Area
            move_c = w * dist_calc(g_in.node, l_node, r_node)
            area_c = w * area_diff(g_in.node[l_node]['area'], g_in.node[r_node]['area'])
            cost = int(move_c + area_c)

            move_edges.append((l_node, r_node, cost))

        # Prune and add subset of edges to graph
        edges_to_add = prune_set(move_edges, alpha=alpha)
        g_in.add_weighted_edges_from(edges_to_add)

        # TO disappear
        # find closest border
        dist_border = closest_border(g_in, l_node)

        # Feature costs: Movement and Change in Area
        move_c = w * dist_border
        area_c = w * area_diff(g_in.node[l_node]['area'], g_in.node[r_node]['area'])
        cost = int(area_c + move_c)

        disappear_edges.append((l_node, 'D', cost))

        # TO split edges
        split_edges = []
        for s_node in node_sets['s_n']:
            cost = w * split_cost(g_in.node, l_node, s_node)
            split_edges.append((l_node, s_node, cost))

        # Prune and add subset of edges to graph
        edges_to_add = prune_set(split_edges, alpha=alpha)
        g_in.add_weighted_edges_from(edges_to_add)

        # TO merge edges
        for m_node in node_sets['m_n']:
            if extract_num(m_node).intersection(extract_num(l_node)):
                g_in.add_edge(l_node, m_node, weight=dummy_cost)

    # Prune and add subset of edges to graph
    edges_to_add = prune_set(disappear_edges, alpha=alpha)
    g_in.add_weighted_edges_from(edges_to_add)

    # ------------------------------------------------------------------------
    # prepare output
    g_out = g_in

    return g_out


def prune_set(edges, alpha):

    # prune_set
    # Sorts the edges in order of increasing cost a returns set to be added
    #
    # Inputs:   edges   -   list of edges
    #           alpha   -   proportion to retain
    #
    # Outputs:  add_edges  -   list of edges to be added
    #

    # Sort by order of increasing cost
    edges.sort(key=lambda tup: tup[2])

    # Retain required proportion of edges with lowest cost
    retain_index = int(round(alpha * len(edges)))
    add_edges = edges[:retain_index]

    return add_edges
