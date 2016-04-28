# track_errors.py
#
# Collection of functions to error check the tracking output.
#
#

import json


def read_json(path):

    # read_json
    # read output data stored in JSON file
    #
    # Inputs:   path    - path to JSON file
    # Outputs:  output  - output python object
    #

    with open('output_data.json') as data_file:
        data = json.load(data_file, encoding="utf-8")

    return data


def bbox(tracks):

    # bbox
    # print bounding boxes to error check as was doubling up
    #
    # Inputs: output_data - python object of track outputs
    #

    x = 0
    frame = 13
    for cell_id, data in tracks.iteritems():
        if frame in data['frame']:
            x += 1
            print('Bounding Box for cell_id ' +
                  str(cell_id) +
                  ' is ' +
                  str(data['bbox'][data['frame'].index(frame)]))

    print('Total boxes in frame is ' + str(x))


def byteify(input):

    # byteify
    # removes unicode
    # see --> https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python/13105359#13105359
    #

    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def list_parents(tracks):

    # list_parents
    # print list of cells with parents and their associated parent cell IDs
    #
    # Inputs: tracks - python object of track outputs

    for cell_id, data in tracks.iteritems():
        if data['parent']:
            print('Cell_id ' + str(cell_id) + ' has parents ' +
                  str(data['parent']))


# Running required checks
output_data = read_json('output_data.json')
output_data = byteify(output_data)
list_parents(output_data)
