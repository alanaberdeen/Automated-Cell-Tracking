# save.py
# Offer functions for saving the tracking output

import csv
import json


def save_csv(output_data, save_path):

    # save_csv
    # save tracking output to csv file
    #
    # Inputs:   output_data - output data structure (list of lists)
    #           save_path   - dir to save csv inside
    #

    # Set save path
    save_out = save_path + '/output_data.csv'

    with open(save_out, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output_data)


def save_json(output_data, save_path):

    # save_json
    # save tracking output to json file
    #
    # Inputs:   output_data - output data structure (list of lists)
    #           save_path   - dir to save csv inside
    #

    # Convert to sensible format for JSON
    j_out = dict()
    for i_d, cell in enumerate(output_data):
        track = dict()
        track["Cell_ID"] = i_d
        track["Frames"] = cell[0]
        track["Centroid"] = cell[1]
        track["Area"] = cell[2]
        track["Parent"] = cell[3]

        j_out["Cell_" + str(i_d)] = track

    # Set save path
    save_out = save_path + '/output_data.json'

    # Write file
    with open(save_out, 'wb') as outfile:
        json.dump(j_out, outfile)
