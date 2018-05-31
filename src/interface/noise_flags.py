import argparse

def configure():
# Parser for flags

    # The ArgumentParser object will hold all the information necessary to parse
    # the command line into Python data types.
    parser = argparse.ArgumentParser(description='Python script interface able to generate\
                                 lj+yukawa, for now, simulations.',prefix_chars= '-')
                                
    
    # Create flags
    parser.add_argument('--units', choices=['lj','real','metal','si','cgs','electron','micro','nano'], default='lj',  \
                        help='pass the style of units used in the simulation and for all the variables. Default value is \' lj \' ')
    
    parser.add_argument('--step_length', action='store', default=0.005, type=float, \
                        help='pass the timesteps\' length. Default value is 0.005 .')
                        
    parser.add_argument('--step_number', action='store', default=100, type=int, \
                    help='pass the number of simulations, int with a default value of 100.')
                    
    parser.add_argument('--atom_style', choices=['angle','atomic','body','bond','charge','dipole','dpd','edpd', 'mdpd','tdpd','electron','ellipsoid','full','line','meso','molecular','peri','smd','sphere','tri','template','hybrid'], default='atomic',  \
                    help='pass the style of the atoms used in the simulation. Default value is \' atomic \'')

    parser.add_argument('--sphere_coord', action= 'append',type=float,nargs='+',default=[0, 0 , 0, 10],  help='Pass the needing for defining the spherical region in which the particles have to be created; the parameters needed are the three coordinates of the center and the radius. The default values are: 0 0 0 10')
    
    parser.add_argument('--lj_coeff', action= 'append',type=float,nargs='+',default=[2.5,1.0,1.0],  help='Pass the needing coefficients for defining the lj potential; the parameters needed are the cutoff, epsilon, sigma. The default values are: 2.5,1.0,1.0 .')
    
    parser.add_argument('--mass', action='store', default=1.0, type=float, \
                        help='pass the particles\' mass value, a float with a default value of 1.0 .')
    
    parser.add_argument('--box', action= 'append',type=float,nargs='+',default=[-100, 100 , -100, 100,-100,100],  help='Pass the needing for defining the simulation box; the parameters needed are the xlo,xhi,ylo,yhi,zlo,zhi. The default values are: -100, 100, -100, 100, -100, 100.')

    

    parser.add_argument('--xx', action='store', default=20, type=int, \
                    help='pass the region length along the x-axys, an int with a default value of 20.')

    parser.add_argument('--yy', action='store', default=20, type=int, \
                    help='pass the region length along the y-axys, an int with a default value of 20.')

    parser.add_argument('--zz', action='store', default=20, type=int,\
                    help='pass the region length along the z-axys, an int with a default value of 20.')

    parser.add_argument('--thermo', action='store', default=50, type=int, \
                        help='pass the number of steps in which the program prints the thermodynamics of the system; it is an int with a default value of 50.')

    parser.add_argument('--if_dump_atom', action='store_true',help='inserting this flag makes possible to print in a .gz file a snapshot of the system. (bool variable, false by default)')

    parser.add_argument('--dump_atom', action='store', default=10, type=int, \
                    help='print in a .gz file a snapshot of the simulation every args.dump_atom steps, an int with a default value of 10.')

    parser.add_argument('--if_dump_speed', action='store_true',help='inserting this flag makes possible to print in a dump file all speed components of all particles. (bool variable, false by default)')

    parser.add_argument('--dump_speed', action='store', default=99, type=int, \
                    help='print in a file all particles\' speed components every args.dump_speed steps, an int with a default value of 99')
                    
    parser.add_argument('--final_speed', action='store_true',help='stores the condition for creating a file containing the velocities of all particles at the final step of integration. (bool variable, false by default)' )
    
    parser.add_argument('--fspeed_vector', action='store_true',help='stores the condition for creating a vector containing all final velocities: it is conditioned by --final_speed. (bool variable, false by default)')
    
    parser.add_argument('-s', action='store_true',help='stores the condition to mute all lammps setting printout and log.lammps storing. (bool variable, false by default)')
    
    print("Arguments parsed correctly.")
    
    
    return parser


