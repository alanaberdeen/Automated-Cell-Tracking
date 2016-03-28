# edges.py
# Functions used to build edges in graph structure

# Import external packages
import math


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
    node_sets = {'l_n':[], 'r_n':[], 's_n':[], 'm_n':[]}

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


def closest_border(g, cell):

    # closest_border
    # Finds the distance from given cell to the border of the image.
    # Note that image dimensions are measured from top left hand corner.
    #
    # inputs:   cell        - label of cell in question
    #           img_shape   - image dimensions. (x, y) Tuple.
    #
    # outputs:  dist - distance to the closest border
    #

    # Data
    node_x = g.node[cell]['centroid'][0]
    node_y = g.node[cell]['centroid'][1]

    # Distances from borders
    x_dist_r = abs(g.graph['img_shape'][0] - node_x)
    y_dist_b = abs(g.graph['img_shape'][1] - node_y)

    # Closest border
    dist = min(node_x, x_dist_r, node_y, y_dist_b)

    return dist


def dist_calc(g_nodes, node1, node2):

    # dist_calc
    # Calculate the Euclidean distance between two nodes.
    #
    # Inputs:   g_nodes - nodes in graph structure with associated attributes
    #           node1   - label of node 1
    #           node2   - label of node 2
    #
    #
    # Outputs:  dist - distance value (Float)
    #

    x1, y1 = g_nodes[node1]['centroid']
    x2, y2 = g_nodes[node2]['centroid']

    x_distance = float(x2) - float(x1)
    y_distance = float(y2) - float(y1)
    distance = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance, 2))

    return distance


def area_diff(area1, area2):

    # area_diff
    # Calculate the absolute difference in area between two nodes.
    #
    # Inputs:   area1   -    area of node 1
    #           area2   -    area of node 2
    #
    # Outputs:  area_difference - distance value. Float
    #

    area_difference = math.sqrt(abs(area2 - area1))

    return area_difference


def split_cost(g_nodes, node, event):

    # split_cost
    # Calculate the association 'cost' for a cell splitting
    #
    # Inputs:   g_nodes -   nodes in graph with associated attributes
    #           node    -   cell in question
    #           event   -   label of split node
    #
    # Outputs:  cost    - association cost

    # Daughter cells
    d_cells = [('R' + str(s)) for s in extract_num(event)]

    # Centroid distance feature
    dist = [dist_calc(g_nodes, node, d) for d in d_cells]
    dist_cost = sum(dist)

    # Area difference feature
    split_area = sum(g_nodes[d]['area'] for d in d_cells)
    area_cost = area_diff(split_area, g_nodes[node]['area'])

    cost = int(dist_cost + area_cost)

    return cost


def merge_cost(g_nodes, node, event):

    # merge_cost
    # Calculate the association 'cost' for a cell resutling from a merge
    #
    # Inputs:   g_nodes -   nodes in graph with associated attributes
    #           node    -   cell in question
    #           event   -   label of merge node
    #
    # Outputs:  cost    - association cost

    # Daughter/parent cells
    p_cells = [('L' + str(s)) for s in extract_num(event)]

    # Centroid distance feature
    dist = [dist_calc(g_nodes, node, p) for p in p_cells]
    dist_cost = sum(dist)

    # Area difference feature
    merge_area = sum(g_nodes[p]['area'] for p in p_cells)
    area_cost = area_diff(merge_area, g_nodes[node]['area'])

    cost = int(dist_cost + area_cost)

    return cost


def extract_num(node_label):

    # extract_node_number
    # Extract the node numbers from the cell label as a set
    #
    # Inputs: node_label    -  node label (string)
    #
    # Outputs: numbers      - set of node numbers in label
    #
    #

    # Initialise set
    numbers = set()

    # If merge/split node then partition at ,
    partition = node_label.partition(',')

    # Add each number to set
    numbers.add(int(''.join(i for i in partition[0] if i.isdigit())))
    try:
        numbers.add(int(''.join(i for i in partition[2] if i.isdigit())))
    except ValueError:
        pass

    return numbers
