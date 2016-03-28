# import external packages
import numpy as np


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
        out = initialise(g.node)
    else:
        out = label_previous(g.node, out)

    # Update frame number
    frame = out[0][0][-1] + 1

    # Update connections
    for row, vertex in enumerate(c_vertices):

        # Find new cells and the edge going TO that cell
        if 'R' in vertex:

            checker = len([i for i in a_sol[row] if i == 1])
            edge = a_sol[row].index(1)
            y = 1

            # Find labels for predecessors
            predecessors = [c_vertices[i] for i, v in enumerate(a_sol) if v[edge] == -1]

            # Simple cell movement
            if len(predecessors) == 1:
                previous = predecessors.pop()

                # Cell moved
                if 'L' in previous:
                    out = update_move(out, vertex, previous, g.node)

                # Cell appeared
                elif 'A' in previous:
                    out = update_appear(out, vertex, g.node, frame)

            # Cell from split/merge
            elif len(predecessors) > 1:
                out = update_split_merge(out, vertex, g.node, frame, predecessors)

    # Make all tracks up to same length by appending None
    out = update_to_frame(out, frame)

    return out


def update_move(current_out, vertex, previous, g_nodes):

    # update_move
    # Update output for simple cell movements.
    #
    # inputs:   current_out     - current output data (list of lists)
    #           vertex          - label for new cell data (string)
    #           previous        - label for previous cell data (string)
    #           g_nodes         - nodes in graph with attributes
    #
    # outputs   updated_out - updated output structure

    # find output row
    for cell in current_out:
        if cell[4] == previous:

            # Update frame number
            cell[0].append(cell[0][-1]+1)

            # Append Centroid as tuple
            cell[1].append(g_nodes[vertex]['centroid'])

            # Append Area
            cell[2].append(g_nodes[vertex]['area'])

            # Append parent ID(s)
            cell[3].append(None)

    # return output
    updated_out = current_out
    return updated_out


def update_appear(current_out, vertex, g_nodes, frame, parent_id=None):

    # update_appear
    # Update output for cell appearances
    #
    # Inputs:   current_out     - current output data (list of lists)
    #           vertex          - label for new cell data (string)
    #           g_nodes         - nodes in graph with associated attributes
    #           parent_id       - parent cell labels (if any)
    #
    # Outputs   updated_out - updated output structure

    # Initialise new cmcft with current frames and data structure
    new_cell_track = [[x for x in range(frame)],
                     [None] * frame,
                     [None] * frame,
                     [None] * frame,
                      None]

    # Add to output
    updated_out = list(current_out)
    updated_out.append(new_cell_track)

    # Update frame
    updated_out[-1][0].append(updated_out[-1][0][-1] + 1)

    # Append centroid
    updated_out[-1][1].append(g_nodes[vertex]['centroid'])

    # Append area
    updated_out[-1][2].append(g_nodes[vertex]['area'])

    # Append parent ID(s)
    updated_out[-1][3].append(parent_id)

    return updated_out


def update_split_merge(current_out, vertex, g_nodes, frame, predecessors):

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

    # Initialise parents
    parent_ids = []

    # find the cell ID (row in output array) of the parent cell
    for parent in predecessors:
        if 'L' in parent:
            for cell_id, data in enumerate(current_out):
                if data[4] == parent:
                    parent_ids.append(cell_id)

    updated_out = update_appear(current_out, vertex, g_nodes, frame, parent_ids)

    return updated_out


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

    # Remove edges not included from incidence matrix
    a_reduced = a[:, included_edges]
    a_sol = a_reduced.tolist()

    return a_sol


def initialise(g_nodes):

    # initialise_out
    # Function to initialise output format
    #
    # inputs:   g   -   current graph structure
    #
    # outputs   out -   out structure
    #

    out = []

    for vertex in g_nodes:
            if 'L' in vertex:

                # initialise cell data
                cell = [list(), list(), list(), list(), 'label']

                # Frame
                cell[0].append(0)

                # Centroid
                cell[1].append(g_nodes[vertex]['centroid'])

                # Area
                cell[2].append(g_nodes[vertex]['area'])

                # Parent ID
                cell[3].append(None)

                # Temp previous label
                cell[4] = vertex

                out.append(cell)

    return out


def update_to_frame(out, frame):

    # for each track check if data up to date
    for track in out:
        diff = frame - (len(track[0])-1)

        # if not enough data cell has disappeared, append none to lists.
        if diff > 0:
            track[0].append((track[0][-1] + 1))
            track[1].append(None)
            track[2].append(None)
            track[3].append(None)
            track[4] = None

    return out


def label_previous(g_nodes, out):

    # label_previous
    # Add labels to tracks that are L cells
    #
    # Inputs:   g_nodes     - nodes in graph
    #           out         - current out data
    #
    # Outputs   updated_out - created out structure
    #

    updated_out = list(out)

    # For each L node
    for vertex in g_nodes:
        if 'L' in vertex:

            # find track associated and label with cell name
            for track in updated_out:
                if track[1][-1] == g_nodes[vertex]['centroid']:
                    track[4] = vertex

    return updated_out
