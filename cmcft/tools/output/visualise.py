# visualise.py
# Set of functions to visulaise the tracking output

# import external packages
import os
from PIL import Image, ImageDraw, ImageFont


def overlay(output_data, img, save_path):

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
