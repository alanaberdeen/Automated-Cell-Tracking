# construct.py
# Script constructs the graph cell tracking structure

# Import external packages
import networkx as nx
import skimage.io
from skimage.measure import label, regionprops
import warnings

# Import functions
import edges
import nodes


def construct(img1_path, img2_path, w, prune):

    # graph
    # Create the graph structure representing the relationships between cells
    # in two consecutive pre-segmented images.
    #
    # Inputs:   img1_path   - path to first image
    #           img2_path   - path to following image
    #           w           - feature weights (set empirically)
    #           prune       - pruning parameters, tuple (alpha, beta)
    #                         alpha - fraction of lowest cost edges to retain
    #                         beta - fraction of lowest cost nodes to retain
    #
    # Outputs:  g           - graphical representation of potential cell
    #                         behaviour.
    #

    # reading and labelling images
    cell_stats = extract_cell_stats(img1_path, img2_path)

    # Construct graph
    # Image shape added as graph attribute so that distance to image border
    # can be found in edge weight calculations.
    g = nx.DiGraph()
    g.graph['img_shape'] = cell_stats['img_shape']

    # Add nodes
    g = nodes.build(g, cell_stats['img1'], cell_stats['img2'], prune[1])

    # add edges
    g = edges.build(g, w, prune[0])

    # return g
    return g


def extract_cell_stats(img1_path, img2_path):

    # Function reads in the images and labels the cells. The features are
    # extracted from these labelled images.
    #
    # Inputs:   img1_path - path to previous image
    #           img2_path - path to current image
    #
    # Outputs:  out -   dict containing the relevant information
    #

    # TODO: be more accommodating with image types, RGB etc
    # read image data
    img1 = skimage.io.imread(img1_path)
    img2 = skimage.io.imread(img2_path)

    # Image shape
    if img1.shape != img2.shape:
        warnings.warn('Caution: Comparing image frames of different sizes.')
    img_shape = img1.shape

    # Label pre-segmented images
    l_label, l_cell_total = label(img1, return_num=True)
    r_label, r_cell_total = label(img2, return_num=True)

    # Collect cell features is cell is of minimum size (not segmented debris)
    # TODO: clever way of setting this number
    l_cells = [cell for cell in regionprops(l_label) if cell['filled_area'] > 50]
    r_cells = [cell for cell in regionprops(r_label) if cell['filled_area'] > 50]

    # Output
    out = {'img1': l_cells, 'img2': r_cells, 'img_shape': img_shape}
    return out

