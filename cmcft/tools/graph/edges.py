# edges.py
# Functions used to build edges in graph structure

# Import functions
from cost_calcs import *


def build(g_in):

    # build
    # Create the edges for the graph structure. Edge weights are
    # calculated and set as attributes as in the Coupled Minimum Cost
    # Flow Tracking algorithm
    #
    # Inputs:   g_in    - initialised graph node structure to be built upon
    # Outputs:  g_out   - updated graph with the correct edges added
    #

    # Set feature weights (empirically)
    w = 110

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

    # -----
    # FROM source node
    for n in node_sets['l_n']:
        g_in.add_edge('T+', n, weight=dummy_cost)

    g_in.add_edge('T+', 'A', weight=dummy_cost)

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
        for r_node in node_sets['r_n']:
            cost = w * merge_cost(g_in.node, r_node, m_node)
            g_in.add_edge(m_node, r_node, weight=cost)

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
    for r_node in node_sets['r_n']:
        # find closest border
        dist_border = closest_border(g_in, r_node)

        # Feature costs: Movement and Change in Area
        move_c = w * dist_border
        area_c = w * area_diff(g_in.node[r_node]['area'], g_in.node['A']['area'])

        cost = int(area_c + move_c)
        g_in.add_edge('A', r_node, weight=cost)

    #
    # -----
    # FROM L nodes
    for l_node in node_sets['l_n']:

        # TO R nodes
        for r_node in node_sets['r_n']:

            # Feature costs: Movement and Change in Area
            move_c = w * dist_calc(g_in.node, l_node, r_node)
            area_c = w * area_diff(g_in.node[l_node]['area'], g_in.node[r_node]['area'])

            cost = int(move_c + area_c)
            g_in.add_edge(l_node, r_node, weight=cost)

        # TO disappear
        # find closest border
        dist_border = closest_border(g_in, l_node)

        # Feature costs: Movement and Change in Area
        move_c = w * dist_border
        area_c = w * area_diff(g_in.node[l_node]['area'], g_in.node[r_node]['area'])

        cost = int(area_c + move_c)
        g_in.add_edge(l_node, 'D', weight=cost)

        # TO split edges
        for s_node in node_sets['s_n']:
            cost = w * split_cost(g_in.node, l_node, s_node)

            g_in.add_edge(l_node, s_node, weight=cost)

        # TO merge edges
        for m_node in node_sets['m_n']:
            if extract_num(m_node).intersection(extract_num(l_node)):
                g_in.add_edge(l_node, m_node, weight=dummy_cost)

    # -----
    # TO sink edges
    # from R nodes
    for r_node in node_sets['r_n']:
        g_in.add_edge(r_node, 'T-', weight=dummy_cost)

    # from disappear node
    g_in.add_edge('D', 'T-', weight=dummy_cost)

    # ------------------------------------------------------------------------
    # prepare output
    g_out = g_in

    return g_out
