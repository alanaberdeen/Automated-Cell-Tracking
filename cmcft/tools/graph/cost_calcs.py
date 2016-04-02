# cost_calcs.py
# Set of functions used to calculate costs elements between nodes

import math

__all__ = ['closest_border', 'dist_calc', 'area_diff', 'split_cost',
           'merge_cost', 'extract_num', ]


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
    # Calculate the association 'cost' for a cell resulting from a merge
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
    # Inputs: node_label    - node label (string)
    # Outputs: numbers      - set of node numbers in label
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
