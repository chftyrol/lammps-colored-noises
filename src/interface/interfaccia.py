#!/usr/bin/env python3

import argparse
import numpy as np

import os

import noise_flags
import lmp_config
import mute
import Giration as gir
import matplot as mat


# Import the dynamical library from the shared object
from lammps import lammps

# Parse all the flags by using the module argparse
parser = noise_flags.configure()

args = parser.parse_args()

if args.s == True:
    mute.blockPrint()

# Config the experiment using the flags
lmp = lmp_config.configure(args)

# Command for running the simulation args.step times.
lmp.command("run       %i" % (args.step_number)) # i perche è un int

# If requested print the final speeds.
if args.final_speed == True:
        speed = np.genfromtxt("final_speed.%i" % (args.step_number), delimiter=" ", skip_header=9, dtype=str)
        if args.s == True:
            os.system('clear')
            mute.enablePrint()
        print("The speed vector has been initialized correctly")

if args.dump_pos != 0:
    pos = np.genfromtxt("dump_pos.%i" % (args.dump_pos), delimiter=" ", skip_header=9, dtype=str)
    if args.s == True:
        os.system('clear')
        mute.enablePrint()
        print("The pos vector has been initialized correctly")
    os.system('clear')
    print("The pos vector has been initialized correctly")
    print(pos[0][0])

if args.gir != 0:
    X = []
    Y = []
    for n in range(0, int(args.step_number/args.gir)):
        X.insert(n,int(args.gir)*n)
        Y.insert(n,gir.compute("dump_gir.%i" % (int(args.gir)*n)))

    mat.plot(X,Y)

