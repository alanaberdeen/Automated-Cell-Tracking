# save.py
# Offer functions for saving the tracking output

import csv


def save_csv(output_data, save_path):

    # csv
    # save tracking output to csv file
    #
    # Inputs:   output_data - output data structure (list of lists)
    #           save_path   - dir to save csv inside
    #

    # Set save path
    save_out = save_path + '/output_data.csv'

    with open(save_out, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output_data)
