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

images = parent + '/test_datasets/Fluo-N2DH-SIM/01_GT/SEG_test'

# Setup save directory
save = parent + '/test_datasets/test_results'
previous_saves = glob.glob(save + '/*')
for f in previous_saves:
    os.remove(f)

# Profile
command = 'track.track(images, save_path=save, annotated=False, csv=False)'
test_profile = cProfile.runctx(command, globals(), locals(),
                               filename='track_profile')
