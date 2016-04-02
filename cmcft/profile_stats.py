# profile_stats
# Test rig for analysing performance
#
#
# This script is 'quick and dirty' only to be used to testing and profiling.
# For use of the tracker call the track func in track.py from elsewhere.

import pstats

stats = pstats.Stats('track_profile_03')
stats.sort_stats('tottime', 'cumtime')
stats.print_stats(10)
