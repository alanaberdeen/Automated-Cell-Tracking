# README

(c) 2016   
Author: Alan Aberdeen   
Email: alanaberdeen (at) gmail (dot) com

## Archive
This repository is archived and not actively maintained.

## Intention   
Python implementation of the tracking methodology as presented in:  
*Padfield, Dirk, Jens Rittscher, and Badrinath Roysam. "Coupled minimum-cost flow cell tracking for high-throughput quantitative analysis." Medical image analysis 15.4 (2011): 650-668.*

### Solver Details  
This project uses the [GLPK (GNU Linear Programming Kit)](https://www.gnu.org/software/glpk/). Installation instructions can be found on the webpage. It was realtively easy to install. The `Pyomo` python package interfaces with the solver, the directory containing the `glpsol` executable must be in the list of paths defined by the `PATH` environment variable.  

Sometimes, wehn working with a Python `virtualenv` the `Pyomo` package can't locate the solver despite it's location being included in the `PATH` variable. I think this is a known issue, but coping the `glpsol` exectable to the `venv` directory fixes this - a little bit of a rubbish workaround but a workaround none the less.  

### Output details  
Currently returning tracking output as list of lists structure.  

     |Tracks                                     |
     |   --> cell ID                             |
     |       --> frame,                          |
     |           centroid,                       |
     |           area,                           |
     |           parent cell ID                  |

### Disclaimer   
This set of tools was built (and tested on) a few particular sets of data. The functions are not error free and have not been extensively tested. Application to new datasets may require some new developments. 

