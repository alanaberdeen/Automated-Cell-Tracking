# b_flow
# Flow constraint vector

__all__ = ["b_flow"]


def b_flow(a_vertices):

    # b_flow
    #
    # Construct flow constraint vector
    # (vector of size |V| x 1 representing the sum of flow for each vertex.
    # 0 for all vertices expect for source and sink)
    #
    # Inputs:   g       -   current graph structure
    # Outputs:  b_flow  -   flow constraint vector.
    #

    b = []

    # Total Cells
    total_cells = sum(1 for x in a_vertices if 'L' in x or 'R' in x)

    # run through nodes and adjust flow for source/drain
    for node in a_vertices:
        if node == 'T+':
            b.append((-1)*total_cells)
        elif node == 'T-':
            b.append(total_cells)
        elif 'M' not in node and 'S' not in node:
            b.append(0)

    return b