from lammps import lammps
import sys
import os
import mute

def configure(args):
    
#from lammps import lammps + lmp = lammps() :
#create an instance of LAMMPS, wrapped in a Python class by the lammps Python module, and return an instance of the Python class as lmp. It is used to make all subsequent calls to the LAMMPS library.

    lmp = lammps()
    
    if args.s == True:
        lmp.command("log none")
            
    #Set the unit type
    #For style lj, all quantities are unitless.
    #Without loss of generality, LAMMPS sets the fundamental \
    #quantities mass, sigma, epsilon, and the Boltzmann constant = 1.
    lmp.command("units        lj")

#ATTENZIONE:mettere il comando per modificarlo direttamente, e mettere in modo per cui se non mette nulla, usa il suo valore di default per ogni unità di misura usata.
    lmp.command("timestep 0.005")

    #Set variables which will define my region of simulation
    #Variables of style 'equal' store a formula which when evaluated \
    #produces a single numeric value which can be output
    #lmp.command("variable    xx equal %i" % (args.xx))
#lmp.command("variable    yy equal %i" % (args.yy))
#  lmp.command("variable    zz equal %i" % (args.zz))
    
    #Define atom type
    lmp.command("atom_style    atomic") #atom_style style args
    
    #Generate my lattice of type fcc and step 0.8442
    lmp.command("lattice        fcc 0.8442")    #lattice style scale keyword values
    
    #Generate my simulation box
    lmp.command("region        sfera sphere 0 0 0 10")

    lmp.command("region        scatola block -100 100 -100 100 -100 100")
        
    #Create the box
    lmp.command("create_box    1 scatola") #create_box N-type_atoms region-ID keyword value
        
    #Create the atoms in the box
    #create_atoms command creates atoms on the lattice points inside the simulation\
    #box;For the box style, the create_atoms command fills the entire simulation box\
    #with particles on the lattice.
    lmp.command("create_atoms    1 region sfera") #For the box style, the create_atoms command fills the entire simulation box with particles on the lattice.
        
    #Set the adimensional mass to the atoms
    lmp.command("mass        1 %f" % (args.mass) )
    
        
    #Set speed to particles
        
    #The create style generates an ensemble of velocities using a random number\
    #generator with the specified temperature and the specified seed.
    #If loop = geom, then each processor loops over only its atoms.
    #For each atom a unique random number seed is created, based on the atom’s\
    #xyz coordinates.
    #A velocity is generated using that seed.
    # This is a fast loop and the velocity assigned to a particular atom will be the same, independent of how many processors are used. However, the set of generated velocities may be more correlated than if the all or local keywords are used.
    
    lmp.command("velocity    all create 1.44 87287 loop geom")
    #lmp.command("velocity    all set 0 0 0")
    
    
    
        
    #Define the potential
    #pair_style yukawa kappa=screening_length cutoff=global_cutoff_for_Yukawa_interactions
    if args.pot == 'yukawa':
        try:
            lmp.command("pair_style hybrid/overlay lj/cut 2.5 %s %f %f " % (args.pot,args.pot_coeff[0],args.pot_coeff[1]))
            #default yukawa 2.0 2.5
            #Define coeff of the interaction between different type of atoms
            lmp.command("pair_coeff * * lj/cut 1.0 1.0") #interaction 1 1 with epsilon, sigma e cutoff passed
            
            lmp.command("pair_coeff * * %s %f %f" % (args.pot,args.pot_coeff[2],args.pot_coeff[3]))
        
            #default yukawa 100.0 2.3
        except IndexError:
            sys.exit("IndexError: not enough coefficients for potential definition. Stopping lammps setting..program quit")

    #How to build neighbour build
    #This command sets parameters that affect the building of pairwise neighbor lists;
    #All atom pairs within a neighbor cutoff distance equal to the their force cutoff plus
    #the skin distance are stored in the list
    #bin è la modalità di creare la lista di primi vicini
    lmp.command("neighbor    0.3 bin") #neighbor skin style
    
        
        
    lmp.command("neigh_modify    delay 0 every 20 check no")
    
        
    #Define type of temporal integration
    lmp.command("fix        1 all nve") #fix <fix_name> <atom_group> <what_fixed>
    

    
    
        
    #print the thermodynamics of the system every args.thermo steps.
    lmp.command("thermo          %i" % (args.thermo))


    #clear shell
    os.system('clear')
    

    #outputs about lammps status
    print("Lammps settings summary: ")
    print("*) The units are set to be adimensional and rescaled. LAMMPS sets the fundamental quantities mass, sigma, epsilon, and the Boltzmann constant = 1.")

    print("*) Lammps is set with a box of simulation of " + str(args.xx) + " length units along the x-axys." )
    print("*) Lammps is set with a box of simulation of " + str(args.yy) + " length units along the y-axys." )
    print("*) Lammps is set with a box of simulation of " + str(args.zz) + " length units along the z-axys." )

    print("*) The particles are set to be atoms.")

    print("*) The lattice is set to be an fcc with a step of 0.8442 length units.")

    print("*) The particles are set to have a mass equal to " + str(args.mass) + ".")

    print("*) Velocities are set to have null components by initial conditions.")

    print("*) Lj potential between particles is set with epsilon=1.0, sigma=1.0, cutoff=2.5 .")

    print("*) " + args.pot + " potential is set with coefficients: " + str(args.pot_coeff[0]) + ", " + str(args.pot_coeff[1]) + ", " + str(args.pot_coeff[2]) + ", " + str(args.pot_coeff[3]) + "." )

    print("*) The neighbor list has been built with the command: neighbor    0.3 bin")

    print("*) PRINT PER DEFINIZIONE DELLE MODIFICHE AI PRIMI VICINI")

    print("*) PRINT PER DEFINIZIONE DELL'INTEGRATORE")

    print("*) Lammps will print the thermodynamics of the system every " + str(args.thermo) + " steps.")
    
    if args.s == False:
        input("press ENTER to continue or press CTRL-C to abort")
        os.system('clear')
    
    return lmp
