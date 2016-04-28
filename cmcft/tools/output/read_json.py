# read_json
# Function to read in JSON output

import json


def read_json(path):

    # read_json
    # read output data stored in JSON file
    #
    # Inputs:   path    - path to JSON file
    # Outputs:  output  - output python object
    #

    # open and decode
    with open(path) as data_file:
        json_read = json.load(data_file, encoding="utf-8")

    # clean unicode
    data = byteify(json_read)

    return data


def byteify(input_data):

    # byteify
    # removes unicode
    # see --> https://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python/13105359#13105359
    #

    if isinstance(input_data, dict):
        return {byteify(key): byteify(value)
                for key, value in input_data.iteritems()}
    elif isinstance(input_data, list):
        return [byteify(element) for element in input_data]
    elif isinstance(input_data, unicode):
        return input_data.encode('utf-8')
    else:
        return input_data


