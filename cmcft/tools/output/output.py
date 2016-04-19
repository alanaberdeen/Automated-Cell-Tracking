# output
# functions to manage the output of optimiser

import collections


def update(g, a_matrix, x, out, c_vertices):

    # update_out
    # Given optimisation solution update the output data structure
    #
    # Inputs:   g           -   graph structure
    #           a_matrix    -   coupled incidence matrix
    #           x           -   solution from optimisation
    #           out         -   current output data structure
    #           c_vertices  -   order of vertices in coupled matrix
    #
    # Outputs:  update_out  -   updated output data
    #

    # Reduce incidence matrix to sol list of lists
    a_sol = reduce_a(a_matrix, x)

    # Check if first output, else associate L cells with tracks
    if not out:
        out = initialise_out(g.node)
    else:
        label_previous(g.node, out)

    # Update frame number
    out['frame'] += 1

    # Update connections
    for row, vertex in enumerate(c_vertices):

        # Find new cells and the edge going TO that cell
        if 'R' in vertex:

            edge = a_sol[row].index(1)

            # Find labels for predecessors
            predecessors = [c_vertices[i] for i, v in enumerate(a_sol) if v[edge] == -1]

            # Simple cell movement
            if len(predecessors) == 1:
                previous = predecessors.pop()

                # Cell moved
                if 'L' in previous:
                    update_cell_data(out, vertex, previous, g.node)

                # Cell appeared
                elif 'A' in previous:
                    update_appear(out, vertex, g.node)

            # Cell from split/merge
            elif len(predecessors) > 1:
                update_split_merge(out, vertex, g.node, predecessors)

    return out


def update_cell_data(out, vertex, previous, g_nodes):

    # update_cell_data
    # Update output with cell data
    #
    # inputs:   out     - current output data (list of lists)
    #           vertex          - label for new cell data (string)
    #           previous        - label for previous cell data (string)
    #           g_nodes         - nodes in graph with attributes

    # find output row
    for cell_id, data in out['tracks'].iteritems():
        if data['previous'] == previous:

            for key, value in data.iteritems():
                if key == 'frame':
                    data['frame'].append((data['frame'][-1] + 1))

                elif isinstance(data[key], list):
                    data[key].append(g_nodes[vertex][key])


def update_appear(current_out, vertex, g_nodes):

    # update_appear
    # Update output for cell appearances
    #
    # Inputs:   current_out     - current output data (list of lists)
    #           vertex          - label for new cell data (string)
    #           g_nodes         - nodes in graph with associated attributes
    #           parent_id       - parent cell labels (if any)
    #

    # Initialise data structure for new track
    new_cell_track = initialise_track(vertex, g_nodes[vertex])
    cell_id = len(current_out['tracks'])
    new_cell_track['cell_id'] = cell_id

    # Adjust frame to moment appeared
    new_cell_track['frame'] = [current_out['frame']]

    # Add to output
    current_out['tracks'][cell_id] = new_cell_track


def update_split_merge(current_out, vertex, g_nodes, predecessors):

    # update_split_merge
    # Update output data structure for split/merge event
    #
    # inputs:   current_out     - current output data (list of lists)
    #           vertex          - label for new cell data (string)
    #           g_nodes         - nodes in graph structure with attributes
    #           predecessors    - list of parent cell labels
    #
    # outputs   updated_out - updated output structure
    #

    # Add new cell track to output
    update_appear(current_out, vertex, g_nodes)

    # cell_id of new cell
    cell_id = len(current_out['tracks']) - 1

    # Record the parent cell_IDs
    parent_ids = []

    # find the cell ID of the parent cell
    for parent in predecessors:
        if 'L' in parent:
            for cell_id, data in current_out['tracks'].iteritems():
                if data['previous'] == parent:
                    parent_ids.append(data['cell_id'])

    # store as parents
    current_out['tracks'][cell_id]['parent'] = tuple(parent_ids)


def reduce_a(a, x):

    # reduce_a
    # Reduces incidence matrix to only included vertices and edges
    #
    # Inputs:   a   - dense coupled incidence matrix
    #           x   - Optimisation solution
    #
    # Outputs:  a_sol - incidence matrix with only included edges/vertices
    #                   list of lists
    #

    # Extract edges to delete from solution
    included_edges = [j for j in xrange(len(x)) if x[j].value == 1]

    if not included_edges:
        raise ValueError('Optimiser did not find a solution')

    # Remove edges not included from incidence matrix
    a_reduced = a[:, included_edges]
    a_sol = a_reduced.tolist()

    return a_sol


def initialise_out(g_nodes):

    # initialise_out
    # Function to initialise_out output format
    #
    # inputs:   g   -   current graph structure
    #
    # outputs   out -   out structure
    #

    out = dict()
    out['frame'] = 0

    tracks = collections.OrderedDict()

    for vertex, data in g_nodes.iteritems():
        if 'L' in vertex:

            # initialise_out cell data
            track = initialise_track(vertex, data)
            cell_id = len(tracks)
            track['cell_id'] = cell_id
            tracks[cell_id] = track

    out['tracks'] = tracks

    return out


def label_previous(g_nodes, out):

    # label_previous
    # Add labels to tracks that are L cells
    #
    # Inputs:   g_nodes     - nodes in graph
    #           out         - current out data
    #

    # For each L node
    for vertex in g_nodes:
        if 'L' in vertex:

            # find track associated and label with cell name
            for cell_id, data in out['tracks'].iteritems():
                if cell_id is not 'frame':
                    if data['centroid'][-1] == g_nodes[vertex]['centroid']:
                        data['previous'] = vertex


def initialise_track(vertex, data):

    # initialise_track
    # initialise track for new cell in output

    track = {'frame': [0],
             'previous': vertex,
             'parent': None}

    for key, value in data.iteritems():
        track[key] = [value]

    return track
