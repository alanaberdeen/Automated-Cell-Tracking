# visualise.py
# Set of functions to visualise the tracking output

# import external packages
from __future__ import division
import os
from skimage import color, io
from skimage.morphology import remove_small_objects
from skimage.measure import label
from PIL import Image, ImageDraw, ImageFont
import glob
from read_json import read_json
import scipy.misc as misc


def overlay_num(output_data, img, save_path):

    # -----
    # WARNING: likely to no longer work due to change in output structure
    # -----
    #
    # Visualise
    # Overlay node labels on original images.
    #
    # Inputs:   output_data - output of cell tracks (list of list of list)
    #           img         - Paths to original images
    #           save_path   - Path to save annotated images
    #
    #
    # Outputs:  Image with unique cell IDs and associated centroids plotted
    #

    # Setup font
    font_path = os.getcwd() + '/tools/output/arial.ttf'
    num_font = ImageFont.truetype(font_path, 20, encoding="unic")

    # open image and prepare for edits
    img_current = Image.open(img).convert('L')
    draw = ImageDraw.Draw(img_current)

    # annotate cells positions
    for cell_id, data in enumerate(output_data):

        position = data[1][-1]
        label = str(cell_id)

        if position is not None:
            position = (position[1], position[0])
            draw.text(position, label, fill=15, font=num_font)

        # save output image
        save_path_post = save_path + '/annotated_' + os.path.split(img)[1]
        file_type = 'TIFF'

        img_current.save(save_path_post, format=file_type)


def overlay_color(output_data_path, img_path, save_path):

    # def color
    # overlay color mask on the cells in the image to indicate the behaviour
    #
    # Inputs:   output_data_path    - path to JSON output data
    #           img                 - path to original image files
    #           save_path           - path to directory for saving the image
    #
    #

    output_data = read_json(output_data_path)

    # colors to overlay on cell regions depending on cell behaviour
    key = {'merge':     (108/255, 113/255, 196/255),
           'split':     (42/255,  161/255, 152/255),
           'appear':    (133/255, 153/255, 000/255),
           'move':      (131/255, 148/255, 150/255),
           'bg':        (253/255, 246/255, 227/255)}

    # List of images in directory
    img_files = glob.glob(img_path + '/*.tif')

    for frame, image_path in enumerate(img_files):

        # Read in image and label cell regions
        img = io.imread(image_path)
        img_clean = remove_small_objects(label(img), min_size=50)
        labels, num = label(img_clean, return_num=True)

        # define overlay for each label
        colors_list = [None] * num
        for cell_id, track in output_data.iteritems():
            if frame in track['frame']:

                # find index of frame
                index_frame = track['frame'].index(frame)

                # default behaviour
                behaviour = 'move'

                if track['frame'][0] == frame:
                    if not track['parent']:
                        behaviour = 'move'
                    elif track['parent'] == 'A':
                        behaviour = 'appear'
                    elif len(track['parent']) > 1:
                        behaviour = 'merge'
                    else:
                        behaviour = 'split'

                # add behaviour to color list
                label_in_frame = track['label'][index_frame] - 1
                colors_list[label_in_frame] = key[behaviour]

        # overlay
        overlay = color.label2rgb(labels,
                                  image=None,
                                  colors=colors_list,
                                  bg_label=0,
                                  bg_color=key['bg'])

        # save output image
        fname = os.path.split(image_path)[1][:-4]
        ftype = '.png'
        save_path_post = save_path + fname + ftype

        # save image
        misc.toimage(overlay, cmin=0.0, cmax=1.0).save(save_path_post)
