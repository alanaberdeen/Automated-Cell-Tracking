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

# Setup Image directories
cwd = os.getcwd()
parent = os.path.abspath(os.path.join(cwd, '../../'))

images = parent + '/test_datasets/PhC-C2DH-U373/01_GT/SEG'

# Setup save directory
save = parent + '/test_datasets/test_results'
previous_saves = glob.glob(save + '/*')
for f in previous_saves:
    os.remove(f)

# Profile
command = 'track.track(images, save_path=save, annotated=True, csv=False, prune=(0.25, 0.2), json=True)'
test_profile = cProfile.runctx(command, globals(), locals(),
                               filename='track_profile')

# TODO: pyomo interface is slowing things down. Declaration of constraints.
