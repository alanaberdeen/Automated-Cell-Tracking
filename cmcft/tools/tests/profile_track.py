# profile_track.py
# Test rig for analysing performance
#
#
# This script is 'quick and dirty' only to be used to testing and profiling.
# For use of the tracker call the track func in track.py from elsewhere.

import track
import os
import glob
import cProfile
from tools import output

# Setup Image directories
cwd = os.getcwd()
parent = os.path.abspath(os.path.join(cwd, '../../'))
images = parent + '/test_datasets/Fluo-N2DH-SIM/02_GT/SEG'

# Setup save directory
save = parent + '/test_datasets/test_results/json'

# Profile
command = 'track.track(images, save_path=save, csv=False, prune=(0.25, 0.2), json=True)'
test_profile = cProfile.runctx(command, globals(), locals(), filename='track_profile')
# TODO: pyomo interface is slowing things down. Declaration of constraints.

# annotate tracks
file = save + '/output_data.json'
save_annotate = parent + '/test_datasets/test_results/overlay/'
output.overlay_color(file, images, save_annotate)
