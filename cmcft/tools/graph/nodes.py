# nodes.py
# Functions to build nodes in graph structure.

# Import external packages
from itertools import combinations


def build(g, l_cells, r_cells):

    # build
    # Initialise the required nodes for the graph structure
    #
    # Inputs:   g       - initialised graph structure to build upon
    #           l_cells - cells and corresponding feature data first image
    #           r_cells - cells and corresponding feature data second image
    #
    # Outputs:  g_out   - graph structure with required nodes added.
    #                     nodes have required feature attributes assigned

    # --------
    # Cells in previous image
    l_nodes = {}
    for cell in l_cells:
        label = 'L' + str(len(l_nodes))
        centroid = (int(cell.centroid[0]), int(cell.centroid[1]))
        l_nodes[label] = {'centroid': centroid,
                          'area': cell.filled_area}

    g.add_nodes_from(l_nodes.iteritems())

    # Cells in current image
    r_nodes = {}
    for cell in r_cells:
        label = 'R' + str(len(r_nodes))
        centroid = (int(cell.centroid[0]), int(cell.centroid[1]))
        r_nodes[label] = {'centroid': centroid,
                          'area': cell.filled_area}

    g.add_nodes_from(r_nodes.iteritems())

    # --------
    # Source, drain, appear and disappear nodes always exist
    fixed_n = ['T+', 'T-']
    g.add_nodes_from(fixed_n)

    # --------
    # Appear
    appear_area = sum(node[1]['area'] for node in r_nodes.iteritems())/len(r_nodes)
    g.add_node('A', area=appear_area)

    # --------
    # Disappear
    disappear_area = sum(node[1]['area'] for node in l_nodes.iteritems())/len(l_nodes)
    g.add_node('D', area=disappear_area)

    # --------
    # Split nodes
    split_into = range(len(r_nodes))
    for subset in combinations(split_into, 2):
        label = "S(" + str(subset[0]) + "," + str(subset[1]) + ")"
        g.add_node(label)

    # --------
    # Merge Nodes
    merge_from = range(len(l_nodes))
    for subset in combinations(merge_from, 2):
        label = "M" + "(" + str(subset[0]) + "," + str(subset[1]) + ")"
        g.add_node(label)

    return g




