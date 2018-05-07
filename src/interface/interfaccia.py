#!/usr/local/bin/python3
#here to insert python3 interpreter path

#from __future__ import print_function
import sys #modulo che gestisce l'interazione fra variabili passate e l'interprete
import argparse

from lammps import lammps


#Parser per le flags

#The ArgumentParser object will hold all the information necessary to parse the command line into Python data types.
parser = argparse.ArgumentParser(description='Python script interface able to generate\
                                 lj+colored noise simulations',prefix_chars= '-')
#Creo le flags
parser.add_argument('--step', action='store', default=100, type=int, \
                    help='passa il numero di simulazioni, un int che ha valore 100 di default') #optional argument

parser.add_argument('--mass', action='store', default=1.0, type=float, \
                    help='passa il valore della massa delle particelle della simulazione, un float che ha valore 1.0 di default')

parser.add_argument('--xx', action='store', default=20, type=int, \
                    help='passa la lunghezza lungo x della nostra regione, un int che ha valore 20 di default')

parser.add_argument('--yy', action='store', default=20, type=int, \
                    help='passa la lunghezza lungo y della nostra regione, un int che ha valore 20 di default')

parser.add_argument('--zz', action='store', default=20, type=int,\
                    help='passa la lunghezza lungo z della nostra regione, un int che ha valore 20 di default')

parser.add_argument('--thermo', action='store', default=10, type=int, \
                    help='passa ogni quante simulazioni printare la termodinamica del mio sistema, un int che ha valore 10 di default')

#parser.add_argument('--lj', action='append', default=lj , type=int,
#help='passa ogni quante simulazioni printare la termodinamica del mio sistema, un int che ha valore 10 di default')
#['rock', 'paper', 'scissors']
parser.add_argument('pot', choices=['yukawa'],  \
                    help='passa il tipo di potenziale da accoppiare a lj')

parser.add_argument('pot_coeff', action= 'append',type=float,nargs='+', help='passa i coefficienti richiesti dal potenziale: *)per yukawa sono screening_length, global_cutoff, A (energy*distance units), cutoff(locale, di quel preciso accoppiamento)')


parser.add_argument('--if_dump_atom', action='store_true')

parser.add_argument('--dump_atom', action='store', default=10, type=int, \
                    help='passa ogni quante simulazioni salvare uno snapshot del sistema di atomi, un int che ha valore 10 di default')

parser.add_argument('--if_dump_coord', action='store_true')

parser.add_argument('--dump_coord', action='store', default=99, type=int, \
                    help='passa ogni quante simulazioni salvare uno snapshot delle coordinate degli atomi, un int che ha valore 100 di default')


args = parser.parse_args()
#NB:: per il potenziale: usare choices

print("Arguments parsed correctly.")

while True:
    n=ord(input("Continue by setting the system by lammps? [y/n]"))
    if n == 121:
        lmp = lammps()

#Genero le variabili che andranno a definirmi la mia regione
#Variables of style 'equal' store a formula which when evaluated produces a single numeric value which can be output
        lmp.command("variable    xx equal %i" % (args.xx))
        lmp.command("variable    yy equal %i" % (args.yy))
        lmp.command("variable    zz equal %i" % (args.zz))

#Decido il sistema di unità di misura della grandezze che manipolo
#For style lj, all quantities are unitless.
#Without loss of generality, LAMMPS sets the fundamental quantities mass, sigma, epsilon, and the Boltzmann constant = 1.
        lmp.command("units        lj")

#Definisco il tipo di atomi
        lmp.command("atom_style    atomic") #atom_style style args

#Genero il mio reticolo fcc con passo 0.8422
        lmp.command("lattice        fcc 0.8442")    #lattice style scale keyword values

#Genero la regione della simulazione, lammps applicherà le giuste condizioni al contorno
        lmp.command("region        scatola block 0 ${xx} 0 ${yy} 0 ${zz}")

#Creo la scatola e che atomi metterci dentro
        lmp.command("create_box    1 scatola") #create_box N-type_atoms region-ID keyword value

#Creo gli atomi nella scatola
#create_atoms command creates atoms on the lattice points inside the simulation box;For the box style, the create_atoms command fills the entire simulation box with particles on the lattice.
        lmp.command("create_atoms    1 box")

#Assegno la massa a un dato tipo di atomi
        lmp.command("mass        1 %f" % (args.mass) )

#Genero le velocità

#The create style generates an ensemble of velocities using a random number generator with the specified temperature amd the specified seed.
#If loop = geom, then each processor loops over only its atoms.
#For each atom a unique random number seed is created, based on the atom’s xyz coordinates.
#A velocity is generated using that seed.
        lmp.command("velocity    all create 1.44 87287 loop geom")

#Definisco il tipo di potenziale e cutoff
#pair_style yukawa kappa=screening_length cutoff=global_cutoff_for_Yukawa_interactions
        if args.pot == 'yukawa':
            try:
                lmp.command("pair_style hybrid/overlay lj/cut 2.5 %s %f %f " % (args.pot,args.pot_coeff[0][0],args.pot_coeff[0][1]))
#default yukawa 2.0 2.5
#Definisco i coeff dell'interazione fra i vari tipi di atomi
                lmp.command("pair_coeff * * lj/cut 1.0 1.0") #interazione 1 1 con epsilon, sigma e cutoff passati

                lmp.command("pair_coeff * * %s %f %f" % (args.pot,args.pot_coeff[0][2],args.pot_coeff[0][3]))
#default yukawa 100.0 2.3
            except IndexError:
                sys.exit("IndexError: not enough coefficients for potential definition. Stopping lammps setting..program quit")
#Come si costruisce la lista dei primi vicini
#This command sets parameters that affect the building of pairwise neighbor lists;
#All atom pairs within a neighbor cutoff distance equal to the their force cutoff plus
#the skin distance are stored in the list
#bin è la modalità di creare la lista di primi vicini
        lmp.command("neighbor    0.3 bin") #neighbor skin style


        lmp.command("neigh_modify    delay 0 every 20 check no")

#Definisco il tipo di integratore temporale
        lmp.command("fix        1 all nve") #fix <nome_del_fix> <gruppo_di_atomi> <cosa_fixiamo>

#Printa la termodinamica del sistema ogni tot passi
        lmp.command("thermo          %i" % (args.thermo))
        print("System set correctly.")
        break
    elif n == 110:
        sys.exit("Stopping lammps setting..program quit")
#SE dico allo script di farlo, salva gli snapshot della simulazione zippati (meno pesanti di quelli di default, ma leggermente più lenti ad aprirsi) ogni tot passi
if args.if_dump_atom == True:
    lmp.command("dump myDump all atom %i dump_atom.*.gz" % (args.dump_atom))

if args.if_dump_coord == True:
    lmp.command("dump myDump2 all xyz %i dump_coordinates.*" % (args.dump_coord))

while True:
    n=ord(input("Continue by running the simulation? [y/n]"))
    if n == 121:
        lmp.command("run       %i" % (args.step)) #i perche è un int
        break
    elif n == 110:
        sys.exit("Stopping the simulation..program quit")


