import argparse

def configure():
#Parser for flags

    #The ArgumentParser object will hold all the information necessary to parse\
    #the command line into Python data types.
    parser = argparse.ArgumentParser(description='Python script interface able to generate\
                                 lj+yukawa, for now, simulations',prefix_chars= '-')
    #Create flags
    parser.add_argument('--step', action='store', default=100, type=int, \
                    help='pass the number of simulations, int with a dafeault value of 100')

    parser.add_argument('--mass', action='store', default=1.0, type=float, \
                    help='pass the particles\' mass value, a float with a default value of 1.0')

    parser.add_argument('--xx', action='store', default=20, type=int, \
                    help='pass the region length along the x-axys, an int with a default value of 20')

    parser.add_argument('--yy', action='store', default=20, type=int, \
                    help='pass the region length along the y-axys, an int with a default value of 20')

    parser.add_argument('--zz', action='store', default=20, type=int,\
                    help='pass the region length along the z-axys, an int with a default value of 20')

    parser.add_argument('--thermo', action='store', default=0, type=int, \
                    help='print the thermodynamics of the system every args.thermo steps, an int with a default value of 0.')

    parser.add_argument('--pot', choices=['yukawa'], default='yukawa',  \
                    help='pass the potential type pairing with the lj one, s str type with \'yukawa\' as default str. Moreover, the potential type must be in the choices of this flag.')

    parser.add_argument('--pot_coeff', action= 'append',type=float,nargs='+',default=[2.0, 2.5 , 100.0, 2.3],  help='Pass the needing potential coefficients: \
                        *)for \'yukawa\' are the screening_length, global_cutoff, A (energy*distance units), cutoff(local, about that precise pairing)')
    
    parser.add_argument('--if_dump_atom', action='store_true')

    parser.add_argument('--dump_atom', action='store', default=10, type=int, \
                    help='print in a .gz file a snapshot of the simulation every args.dump_atom steps, an int with a default value of 10')

    parser.add_argument('--if_dump_speed', action='store_true')

    parser.add_argument('--dump_speed', action='store', default=99, type=int, \
                    help='print in a file all particles\' speed components every args.dump_speed steps, an int with a default value of 99')
                    
    parser.add_argument('--final_speed', action='store_true',help='stores the condition for creating a file containing the velocities of all particles at the final step of integration' )
    
    parser.add_argument('--fspeed_vector', action='store_true',help='stores the condition for creating a vector containing all final velocities: it is conditioned by --final_speed')
    
    parser.add_argument('--s', action='store_true',help='stores the condition to mute all lammps setting printout and log.lammps storing')
    
    
    
    return parser


