# tests.py
# Collection of functions to error check the tracking output.
#
#

import json
from operator import itemgetter
import collections
import track
from tools import output

def read_json(path):

    # read_json
    # read output data stored in JSON file
    #
    # Inputs:   path    - path to JSON file
    # Outputs:  output  - output python object
    #

    with open(path) as data_file:
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


def comp_gt(gt_tracks, manual_track):

    # comp_gt compares the output of the tracking results to those of the
    # to those of the ground truth.
    #
    # inputs:   gt_tracks       -   ground truth tracks in the same format
    #           manual_track    -   man_track.txt annotated text file
    #
    #

    #
    # ----------------
    # file preparation
    #
    # read CMCF-Tracking output for ground truth tracks
    gt = read_json(gt_tracks)
    gt = byteify(gt)

    # Mark all CMCF-Tracking as unassigned
    for cell_id, data in gt.iteritems():
        data['assigned'] = False

    # read in manual_tracking text file for comparison
    with open(manual_track) as infile:
            man_track = [[int(i) for i in line.strip().split(' ')] for line in infile]

    #
    # ----------------
    # Apply checks that CMCF-Tracking matches manual tracks
    #
    # first run check for those spot on.
    for cell in man_track:

        # set default
        cell.append(' --> enter and exit frame do not match')

        # check for equivalent in CMCF-Tracking data
        for cell_id, data in gt.iteritems():

            # If haven't yet found GT track id
            if not data['assigned']:

                # frame differences
                start_diff = abs(data['frame'][0] - cell[1])
                end_diff = abs(data['frame'][-1] - cell[2])

                # check if first and last appearance match
                if start_diff == 0 and end_diff == 0:

                    # if no parent then we're good
                    if data['parent'] is not list:
                        cell[4] = True
                        data['assigned'] = cell[0]
                        break

                    # if parent then check the same
                    elif cell[3] in data['parent']:
                        cell[4] = True
                        data['assigned'] = cell[0]
                        break

                    else:
                        cell[4] = ' --> parent cell_ids do not match'
                        break

    # Second run checks if the fails were because of the stupid way the
    # man_track.txt files record appear and disappear cells.
    for cell in man_track:

        if not cell[4]:

            # check for equivalent in CMCF-Tracking data
            for cell_id, data in gt.iteritems():

                # If haven't yet found GT track id
                if not data['assigned']:

                    # frame differences
                    start_diff = abs(data['frame'][0] - cell[1])
                    end_diff = abs(data['frame'][-1] - cell[2])

                    if start_diff <= 1 and end_diff <= 1 and cell[3] == 0:
                        cell[4] = True
                        break

    for cell in man_track:
        if cell[4] is not True:
            print('manual track cell_id ' + str(cell[0]) + ' has an issue ' + cell[4])

    y = 1


def comp_man_track(cmcf_track, man_track):

    # comp_man_track
    # compares the output of CMCF-Tracking to the man_track.txt file
    #
    # inputs:   cmcf_track   -   path to output of CMCF-Tracking
    #           man_track   -   path to manual tracking txt file provided
    #

    # convert cmcf output to man_track.txt format
    cmcft = format_cmcft(cmcf_track)

    # read in man_track.txt for comparison
    man = dict()
    with open(man_track) as infile:
        for line in infile:
            data = [int(i) for i in line.strip().split(' ')]
            man[data[0]] = {'start': data[1],
                            'end': data[2],
                            'parent': data[3]}

    # loop through entries in man_text.txt
    for m_id, m_data in man.iteritems():

                # loop through tracks in cmcft
                for c_id, c_data in cmcft.iteritems():

                    # check if first and last frames the same and has parent
                    if c_data['start'] == m_data['start'] \
                            and c_data['end'] == m_data['end']:

                        # check if parent's first and last frames the same
                        if c_data['parent'] not in ('A', None) \
                                and cmcft[c_data['parent']]['start'] == man[m_data['parent']]['start'] \
                                and cmcft[c_data['parent']]['end'] == man[m_data['parent']]['end']:

                            # add equivalent data labels
                            c_data['equiv'] = m_id
                            m_data['equiv'] = c_id

                            # add parent equivalent data labels
                            cmcft[c_data['parent']]['equiv'] = m_data['parent']
                            man[m_data['parent']]['equiv'] = c_data['parent']

                            break

    y = 1


def format_cmcft(out_tracks):

    # format_cmcft
    # converts tracking output to the same format as man_track.txt
    #
    # inputs:   out_tracks  -   output of cmcft algorithm
    #
    # outputs:  cmcf_track  -   formatted python object of cmcft tracks

    # read CMCF-Tracking output
    out = read_json(out_tracks)
    out = byteify(out)

    # build list of lists with striped down data
    cmcf_track = []
    for cell_id, data in out.iteritems():

        start = data['frame'][0]
        end = data['frame'][-1]
        parent = 0

        if isinstance(data['parent'], list):
            parent = data['parent'][0]
        elif data['parent'] == 'A':
            parent = 0
            #start -= 1

        if data['termination'] == 'D' and end != 114:
            y=1
            #end += 1

        cmcf_track.append((int(cell_id), start, end, parent))

        cmcf = sorted(cmcf_track, key=itemgetter(2))
        cmcf = sorted(cmcf, key=itemgetter(1))

    return cmcf


def format_man(manual_tracks):

    # format_man
    # read and format man_track.txt
    #
    # inputs: manual_tracks     -   path to man_track.txt
    # outputs: man              -   formatted man_track python object

    man = []
    with open(manual_tracks) as infile:
        for line in infile:
            data = [int(i) for i in line.strip().split(' ')]
            man.append((data[0], data[1], data[2], data[3]))

    man = sorted(man, key=itemgetter(2))
    man = sorted(man, key=itemgetter(1))

    return man


def comp_sets(cmcft_out, man_out):

    # comp_sets
    # uses sets to compare the cmcft_out and man_out
    # this gives an indication of the accuracy of the tracking algorithm

    # import as python objects
    cmcft = format_cmcft(cmcft_out)
    man = format_man(man_out)

    # record details of total tracks
    dataset_info = {'cells': 0, 'move': 0}
    parent_set = set()
    appear_set = set()
    disappear_set = set()
    for c_track in cmcft:
        dataset_info['cells'] += 1
        dataset_info['move'] = dataset_info['move'] + (c_track[2] - c_track[1])

        if c_track[3] != 0:
            parent_set.add(c_track[3])

        if c_track[3] == 0 and c_track[1] != 0:
            appear_set.add(c_track[0])

        if c_track[2] != 75:
            disappear_set.add(c_track[0])

    disappear_set = [i for i in disappear_set if i not in parent_set]
    dataset_info['mitosis'] = len(parent_set)
    dataset_info['a/d'] = (len(disappear_set) + len(appear_set))
    dataset_info['frames'] = 76

    # create multi-sets of frame numbers
    cmcft_frames = []
    for c_track in cmcft:
        cmcft_frames.append((c_track[1], c_track[2]))

    man_frames = []
    for m_track in man:
        man_frames.append((m_track[1], m_track[2]))

    cmcft_count = collections.Counter(cmcft_frames)
    man_count = collections.Counter(man_frames)

    # check the ones that don't match up (union - intersection)
    diff = (cmcft_count | man_count) - (cmcft_count & man_count)

    y = 1

#
imgs = '/Users/alan/Code/Ox/datasets/Fluo-N2DH-SIM/06_GT/TRA'
save = '/Users/alan/Code/Ox/post_work/Fluo-N2DH-SIM/03'

gt_track = save + '/TRA_tracked.json'
txt_track = save + '/man_track.txt'

# run tracking alg
track.track(img_path=imgs, save_path=save, json=True)

# annotate tracks
save_annotate = save + '/annotated_TRA/'
output.overlay_color(gt_track, imgs, save_annotate)

# check validity
#comp_sets(gt_track, txt_track)
