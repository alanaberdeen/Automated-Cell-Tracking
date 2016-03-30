# test_track.py
# Test rig for tracking script

import track
import os
import glob
import cProfile

######################################
# Performance testing

# Input setups
cwd = os.getcwd()
parent = os.path.abspath(os.path.join(cwd, '../../'))

# --------
# Quick test path variables for comparison
# Test1
images = parent + '/test_datasets/Fluo-N2DH-SIM/01_GT/SEG_test'
# Test2
#images = parent + '/test_datasets/PhC-C2DH-U373/01_GT/SEG'

# Setup save area
save = parent + '/test_datasets/test_results'
previous_saves = glob.glob(save + '/*')
for f in previous_saves:
    os.remove(f)


# Profile
command = 'track.track_cmcf(images, save, annotated=True, csv=True)'
test_profile = cProfile.runctx(command, globals(), locals(),
                               filename='test_profile_15_00')


