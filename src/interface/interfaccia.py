#!/usr/local/bin/python3
#here to insert python3 interpreter path

import sys
import argparse
import noise_flags
import lmp_config

#import the dynamical library from the shared object
from lammps import lammps

#parse all the flags by using the module argparse
parser = noise_flags.configure()

args = parser.parse_args()

print("Arguments parsed correctly.")

while True:
    n=ord(input("Continue by setting the system by lammps? [y/n]"))
    if n == 121:
        #config the experiment using the flags
        lmp = lmp_config.configure(args)
        print("System set correctly.")
        break
    elif n == 110:
        sys.exit("Stopping lammps setting..program quit")

#if passed the right flag, lammps saves determined data in external files
if args.if_dump_atom == True:
    lmp.command("dump myDump all atom %i dump_atom.*.gz" % (args.dump_atom))

#here saves particle speed
if args.if_dump_speed == True:
    lmp.command("dump myDump2 all custom %i dump_speed.* vx vy vz" % (args.dump_speed))


while True:
    n=ord(input("Continue by running the simulation? [y/n]"))
    if n == 121:
        #command for running the simulation args.step times.
        lmp.command("run       %i" % (args.step)) #i perche è un int
        break
    elif n == 110:
        sys.exit("Stopping the simulation..program quit")


