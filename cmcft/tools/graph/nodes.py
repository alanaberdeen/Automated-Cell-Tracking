# nodes.py
# Functions to build nodes in graph structure.

# Import external packages
from itertools import combinations
from cost_calcs import *


def build(g, l_cells, r_cells, beta):

    # build
    # Initialise the required nodes for the graph structure.
    #
    # Pruning is applied. The number of split/merge nodes is limited to a
    # fraction (beta) of the R/L cells with the lowest cost, where the cost
    # of a pair of cells is defined by the distance of the cells from each
    # other normalised by their size.

    #
    # Inputs:   g       - initialised graph structure to build upon
    #           l_cells - cells and corresponding feature data first image
    #           r_cells - cells and corresponding feature data second
    #           beta    - pruning coefficient for split/merge events
    #
    # Outputs:  g_out   - graph structure with required nodes added.
    #                     nodes have required feature attributes assigned

    # --------
    # Cells in previous image
    l_nodes = {}
    l_area_sum = 0
    for cell in l_cells:
        label = 'L' + str(len(l_nodes))
        centroid = (int(cell.centroid[0]), int(cell.centroid[1]))
        l_nodes[label] = {'centroid': centroid,
                          'area': cell.filled_area}

        # keep track of l cell area sum
        l_area_sum = l_area_sum + cell.filled_area

    g.add_nodes_from(l_nodes.iteritems())

    # Cells in current image
    r_nodes = {}
    r_area_sum = 0
    for cell in r_cells:
        label = 'R' + str(len(r_nodes))
        centroid = (int(cell.centroid[0]), int(cell.centroid[1]))
        r_nodes[label] = {'centroid': centroid,
                          'area': cell.filled_area}

        # keep track of r cell area sum
        r_area_sum = r_area_sum + cell.filled_area

    g.add_nodes_from(r_nodes.iteritems())

    # --------
    # Appear
    appear_area = l_area_sum/len(r_nodes)
    g.add_node('A', area=appear_area)

    # --------
    # Disappear
    disappear_area = r_area_sum/len(l_nodes)
    g.add_node('D', area=disappear_area)

    # --------
    # Split nodes
    s_n = []
    split_into = range(len(r_nodes))
    for subset in combinations(split_into, 2):
        label = "S(" + str(subset[0]) + "," + str(subset[1]) + ")"
        cost = event_cost(g, ('R' + str(subset[0])), ('R' + str(subset[1])))
        s_n.append((label, cost))

    # sort by cost and only retain the fraction beta
    s_n.sort(key=lambda tup: tup[1])
    s_retain_index = int(round(beta * len(s_n)))
    s_nodes = [s_n[i][0] for i in xrange(s_retain_index)]

    # add nodes
    g.add_nodes_from(s_nodes)

    # --------
    # Merge Nodes
    m_n = []
    merge_from = range(len(l_nodes))
    for subset in combinations(merge_from, 2):
        label = "M" + "(" + str(subset[0]) + "," + str(subset[1]) + ")"
        cost = event_cost(g, ('L' + str(subset[0])), ('L' + str(subset[1])))
        m_n.append((label, cost))

    # sort by cost and only retain the fraction beta
    m_n.sort(key=lambda tup: tup[1])
    m_retain_index = int(round(beta * len(m_n)))
    m_nodes = [m_n[i][0] for i in xrange(m_retain_index)]

    # add nodes
    g.add_nodes_from(m_nodes)

    return g


def event_cost(g, node1, node2):

    # event_cost
    # cost of a pair of cells corresponding to split/merge event
    #
    # Inputs:   g       -   current graph structure
    #           node1   -   label of node 1
    #           node2   -   label of node 2
    #
    # Outputs:  cost    -   cost metric

    dist_cost = dist_calc(g.node, node1, node2)
    area_sum = g.node[node1]['area'] + g.node[node2]['area']

    cost = dist_cost / area_sum

    return cost
