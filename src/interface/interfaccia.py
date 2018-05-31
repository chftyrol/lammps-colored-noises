#!/usr/local/bin/python3
#here to insert python3 interpreter path

import sys
import argparse
import numpy as np
import os

import noise_flags
import lmp_config
import mute
import funzione


#import the dynamical library from the shared object
from lammps import lammps

#parse all the flags by using the module argparse
parser = noise_flags.configure()

args = parser.parse_args()



if args.s == True:
    mute.blockPrint()

#config the experiment using the flags
lmp = lmp_config.configure(args)


#command for running the simulation args.step times.
lmp.command("run       %i" % (args.step_number)) #i perche è un int



if args.fspeed_vector == True:
        speed = np.genfromtxt("final_speed.%i" % (args.step), delimiter=" ", skip_header=9, dtype=str)
        if args.s == True:
            os.system('clear')
            mute.enablePrint()
        print("the vector speed has been initialized correctly")




