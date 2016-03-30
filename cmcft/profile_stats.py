# profile_stats
# Print of stats analysis
#
#

import pstats

stats = pstats.Stats('test_profile_15_00')
stats.sort_stats('tottime', 'cumtime')
stats.print_stats(10)
