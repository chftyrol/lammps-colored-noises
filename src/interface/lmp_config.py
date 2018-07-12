from lammps import lammps
import os

import mute


def configure(args):
    
# With the commands `from lammps import lammps` and `lmp = lammps()` together do the following:
# create an instance of LAMMPS, wrapped in a Python class by the lammps Python module, and return an instance of the Python class as lmp. It is used to make all subsequent calls to the LAMMPS library.

    lmp = lammps()
    
    if args.s == True:
        lmp.command("log none")
    # Set the unit type
    # For style lj, all quantities are unitless.
    # Without loss of generality, LAMMPS sets the fundamental 
    # quantities mass, sigma, epsilon, and the Boltzmann constant = 1.
    lmp.command("units        %s" % (args.units))

    #setting timestep length
    lmp.command("timestep %f" % (args.step_length))

    # Set variables which will define my region of simulation
    # Variables of style 'equal' store a formula which when evaluated \
    # produces a single numeric value which can be output
    
    # Define atom type
    lmp.command("atom_style    %s" % (args.atom_style)) # atom_style style args
    
    # Generate the lattice of type fcc and step 0.8442
    lmp.command("lattice        fcc 0.8442")    # lattice style scale keyword values
    
    # Generate particles' initial region
    lmp.command("region        sfera sphere %f %f %f %f" % (args.sphere_coord[0],args.sphere_coord[1],args.sphere_coord[2],args.sphere_coord[3]))

    # Generate the noise region
    lmp.command("region        sferetta sphere %f %f %f %f" % (args.sphere_coord[0],args.sphere_coord[1],args.sphere_coord[2],args.sphere_coord[3]/2))

    # Generate the simulation box
    lmp.command("region        scatola block %f %f %f %f %f %f" % (args.box[0],args.box[1],args.box[2],args.box[3],args.box[4],args.box[5]))
        
    # Create the box
    lmp.command("create_box    1 scatola") # create_box N-type_atoms region-ID keyword value
        
    # Create the atoms in the box
    # create_atoms command creates atoms on the lattice points inside the simulation
    # box. For the box style, the create_atoms command fills the entire simulation box
    # with particles on the lattice.
    lmp.command("create_atoms    1 region sfera") 
        
    # Set the adimensional mass to the atoms
    lmp.command("mass        1 %f" % (args.mass) )
    
        
    # Set speed to particles
        
    # The create style generates an ensemble of velocities using a random number
    # generator with the specified temperature and the specified seed.
    # If loop = geom, then each processor loops over only its atoms.
    # For each atom a unique random number seed is created, based on the atom’s
    # xyz coordinates.
    # A velocity is generated using that seed.
    # This is a fast loop and the velocity assigned to a particular atom will be the same, independent of how many processors are used. However, the set of generated velocities may be more correlated than if the all or local keywords are used.
    lmp.command("velocity    all create 2.0 87287 loop geom")


    # Define the interaction type and intensity
    lmp.command("pair_style lj/cut %f " % (args.lj_coeff[0]))
    lmp.command("pair_coeff * * %f %f" % (args.lj_coeff[1],args.lj_coeff[2])) #interaction 1 1

    # How to build neighbour list
    # This command sets parameters that affect the building of pairwise neighbor lists;
    # All atom pairs within a neighbor cutoff distance equal to the their force cutoff plus
    # the skin distance are stored in the list
    # bin è la modalità di creare la lista di primi vicini
    #The bin style creates the list by binning which is an operation that scales linearly with N/P, the number of atoms per processor where N = total number of atoms and P = number of processors.
    lmp.command("neighbor %f bin" % (args.skin)) # neighbor skin style
    lmp.command("neigh_modify    delay %i every %i check %s" % (args.neigh_delay,args.neigh_every,args.neigh_check))

    # Define type of temporal integration
    lmp.command("fix        fix1 all nve") # fix <fix_name> <atom_group> <what_fixed>
    
    # Define a variable equal to the current time step, to pass to the generator to avoid ambiguities.
    lmp.command("variable nstep equal step")

    # Define noise sample size variable equal to the total number of step to do (the +1 is because the steps are counted from 0)
    lmp.command('variable noisesamplesize equal "%i + 1"' % (args.step_number))

    # Define noise alpha
    lmp.command('variable noisealpha equal %f' % (args.noise_alpha))

    # Define noise stddev
    lmp.command('variable noisestddev equal %f' % (args.noise_stddev))

    # Define noise leak coeff
    lmp.command('variable noiseleak equal %f' % (args.noise_leak))

    # Define noise global seed
    lmp.command('variable noiseglobalseed equal %f' % (args.global_seed))

    # Seeding mechanism:
    # Global seed --->      1       , 2       , 3       , ...
    # xyz    seed --->      {1 2 3} , {4 5 6} , {7 8 9} , ...
    #                        ^ ^ ^     ^ ^ ^     ^ ^ ^
    #                        x y z     x y z     x y z
    # Hence, if the global seed is g, then the x seed is (g - 1)*3 + 1, the y seed is (g - 1)*3 + 2 and the z seed is (g - 1)*3 + 3,

    # Define x noise seed
    lmp.command('variable noisexseed equal "(v_noiseglobalseed - 1) * 3 + 1"')
    # Define y noise seed
    lmp.command('variable noiseyseed equal "(v_noiseglobalseed - 1) * 3 + 2"')
    # Define z noise seed
    lmp.command('variable noisezseed equal "(v_noiseglobalseed - 1) * 3 + 3"')

    # Expose noise generator python function to lammps
    # The function returns a floating point number (hence the `f`) and is contained in the specified file.
    # The return value is saved in the lammps variable `coloredkickx`
    lmp.command('python generatex input 6 v_nstep v_noisesamplesize v_noisealpha v_noisestddev v_noiseleak v_noisexseed return v_coloredkickx format iifffif file generator.py')

    # Do the same for the other two dimensions
    lmp.command('python generatey input 6 v_nstep v_noisesamplesize v_noisealpha v_noisestddev v_noiseleak v_noiseyseed return v_coloredkicky format iifffif exists')
    lmp.command('python generatez input 6 v_nstep v_noisesamplesize v_noisealpha v_noisestddev v_noiseleak v_noisezseed return v_coloredkickz format iifffif exists')

    # Define the lammps variable `coloredkickx`, which value will be specified by the return value of the function defined above.
    lmp.command("variable    coloredkickx python generatex")

    # Do the same for dimensions y and z
    lmp.command("variable    coloredkicky python generatey")
    lmp.command("variable    coloredkickz python generatez")

    # Add the fix addforce to the simulation.
    # It will add an impulsive force, whose values are specified by the variables set by the python function.
    lmp.command("fix kick all addforce v_coloredkickx v_coloredkicky v_coloredkickz region sferetta")
    
    # For debugging purposes print any needed variable from here.
    # lmp.command('fix extra all print 1 "generator.generate = ${coloredkickz}"')
        
    # Print the thermodynamics of the system every args.thermo steps.
    lmp.command("thermo          %i" % (args.thermo))

    # If passed the right flag, lammps saves determined data in external files
    if args.dump_atom != 0:
        lmp.command("dump myDump1 all atom %i dump_atom.*" % (args.dump_atom))

    # Here saves particle speed
    if args.dump_speed != 0:
        lmp.command("dump myDump2 all custom %i dump_speed.* vx vy vz" % (args.dump_speed))
    
    if args.dump_pos != 0:
        lmp.command("dump myDump3 all custom %i dump_pos.* x y z" % (args.dump_pos))
    
    if args.gir != 0:
        lmp.command("dump myDump4 all custom %i dump_gir.* x y z" % (args.gir))

    # Clear shell
    os.system('clear')
    

    # Outputs about lammps status
    print("Lammps settings summary: ")
    print("\n")
    
    print("*) The units used by simulation are: " + str(args.units) + " .")

    print("*) The length of the timesteps for this simulations is : " + str(args.step_length) + " .")

    print("*) The number of timesteps for this simulations is : " + str(args.step_number) + " .")

    print("*) The atom style chosen for the particles is: " + str(args.atom_style) + " .")

    print("*) The lattice is set to be an fcc with a step of 0.8442 length units.")

    print("*) The atoms are set in a sphere with centre of coordinates x= " + str(args.sphere_coord[0]) + ", y= " + str(args.sphere_coord[1]) + ", z= " + str(args.sphere_coord[2]) + " and a ray of " + str(args.sphere_coord[3]) + " .")

    print("*) Our simulation box has coordinates Xmin= " + str(args.box[0]) + ", Xmax= " + str(args.box[1]) + ", Ymin= " + str(args.box[4]) + ", Ymax= " + str(args.box[3]) + ", Zmin= " + str(args.box[4]) + ", Zmax= " + str(args.box[5]) + " ." )

    print("*) The particles are set to have a mass equal to " + str(args.mass) + ".")

    print("*) Velocities are set to be random initially.")

    print("*) Lj potential between particles is set with cutoff = " + str(args.lj_coeff[0]) + " ,epsilon = " + str(args.lj_coeff[1]) + ", sigma = " + str(args.lj_coeff[2]) + " .")

    print("*) The neighbor list has been built by binning and with a skin distance of " + str(args.skin) + " .")

    print("*) Our simulation box has coordinates Xmin= " + str(args.box[0]) + ", Xmax= " + str(args.box[1]) + ", Ymin= " + str(args.box[4]) + ", Ymax= " + str(args.box[3]) + ", Zmin= " + str(args.box[4]) + ", Zmax= " + str(args.box[5]) + " ." )

    print("*) It will be performed a constant NVE (Particles' number, Volume,Energy) integration to update position and velocity for atoms each timestep.")

    print("*) Lammps will print the thermodynamics of the system every " + str(args.thermo) + " steps.")

    print("*) The noise is set to have alpha =  " + str(args.noise_alpha) + " and stddev = " + str(args.noise_stddev) + " .")


    
    if args.s == False:
        print("\n")
        input("press ENTER to continue or press CTRL-C to abort")
        os.system('clear')
    
    return lmp
