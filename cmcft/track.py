# track.py
# Main script applies coupled minimum-cost flow tracking method to a
# sequence of pre-segmented images.

# Import external packages
import glob

# Import function packages
from tools import solve, output, graph, params


def track(img_path, w=110, prune=(0.5, 0.2),
          save_path=None, annotated=False, csv=False):

    # track
    # tracking function. Loops through sets of image files. For each pair,
    # graph structure is created, transformed to coupled matrix, solved and
    # output updated.
    #
    # Inputs:   img_path    -  path to directory containing image files
    #           w           -  feature weights (set empirically)
    #           prune       -  pruning parameters (alpha, beta)
    #                          alpha: fraction of edges to retain
    #                          beta: fraction split/merge vertices to retain
    #           save_path   -  path to directory for saved output
    #           annotated   -  option to save annotated images of cell tracks
    #           csv         -  option to save csv of output
    #
    #
    # Outputs:  tracks      -  Output data structure for cell tracks.
    #                          List of lists.
    #                          |Tracks                                     |
    #                          |   --> cell ID                             |
    #                          |       --> frame,                          |
    #                          |           centroid,                       |
    #                          |           area,                           |
    #                          |           parent cell ID                  |

    # List of images in directory
    img_files = glob.glob(img_path + '/*.tif')

    # Initialise output
    output_data = None

    # For pairs of image frames
    for i, img in enumerate(img_files):
        if i < (len(img_files)-1):

            # Define image paths
            l_img = img
            r_img = img_files[i+1]

            # Initialise graph
            g = graph.construct(l_img, r_img, w=w, beta=prune[1])

            # Prune graph
            g = graph.prune(g, alpha=prune[0])

            # Initialise output
            if not output_data:
                output_data = output.initialise(g.node)
                if annotated:
                    output.overlay(output_data, l_img, save_path)

            # Create the coupled incidence matrix.
            a_coup, a_vertices = params.a_matrix(g)
            b_flow = params.b_flow(a_vertices)
            c_cost = params.c_cost(g, a_coup, a_vertices)

            # Build optimisation model and solve
            x = solve.opto(a_coup, b_flow, c_cost)

            # Update output
            output_data = output.update(g, a_coup, x, output_data, a_vertices)

            # print frame number to track progress
            print('Tracked frame number: ' + str(i))

            # If required, annotate images
            if annotated:
                output.overlay(output_data, r_img, save_path)

    # If required, save output as csv
    if csv:
        output.save_csv(output_data, save_path)

    return output_data
