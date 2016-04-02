# b_flow
# Flow constraint vector

__all__ = ["b_flow"]


def b_flow(a_vertices):

    # b_flow
    #
    # Construct flow constraint vector
    # (vector of size |V| x 1 representing the sum of flow for each vertex.
    # Having removed source and drain nodes. Now require:
    # L nodes = -1
    # R nodes = +1
    # A node = -|L|
    # D node = +|L|
    #
    # Inputs:   a_vertices  - order of nodes in coupled matrix
    # Outputs:  b_flow      -   flow constraint vector.
    #

    b = []

    # Total Cells
    l_cells = sum(1 for x in a_vertices if 'L' in x)
    r_cells = sum(1 for x in a_vertices if 'R' in x)

    # run through nodes and adjust flow for source/drain
    for node in a_vertices:
        if 'L' in node:
            b.append(-1)
        elif 'R' in node:
            b.append(1)
        elif 'A' in node:
            b.append(r_cells * (-1))
        elif 'D' in node:
            b.append(l_cells)
        else:
            print("Coupling matrix problems, there "
                  "remain split/merge vertices")

    return b
