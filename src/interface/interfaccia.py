#!/usr/local/bin/python3
#here to insert python3 interpreter path

#from __future__ import print_function
#import sys #modulo che gestisce l'interazione fra variabili passate e l'interprete
import argparse
import noise_flags
import lmp_config

from lammps import lammps

parser = noise_flags.configure()

args = parser.parse_args()

print("Arguments parsed correctly.")

while True:
    n=ord(input("Continue by setting the system by lammps? [y/n]"))
    if n == 121:
        lmp = lmp_config.configure(args)
        print("System set correctly.")
        break
    elif n == 110:
        sys.exit("Stopping lammps setting..program quit")

#SE dico allo script di farlo, salva gli snapshot della simulazione zippati (meno pesanti di quelli di default, ma leggermente più lenti ad aprirsi per Ovito) ogni tot passi
if args.if_dump_atom == True:
    lmp.command("dump myDump all atom %i dump_atom.*.gz" % (args.dump_atom))

#idem ma solo sulle componenti delle velocità
if args.if_dump_speed == True:
    lmp.command("dump myDump2 all custom %i dump_speed.* vx vy vz" % (args.dump_speed))

while True:
    n=ord(input("Continue by running the simulation? [y/n]"))
    if n == 121:
        lmp.command("run       %i" % (args.step)) #i perche è un int
        break
    elif n == 110:
        sys.exit("Stopping the simulation..program quit")


