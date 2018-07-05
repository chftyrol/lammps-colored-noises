import argparse

def configure():
# Parser for flags

    # The ArgumentParser object will hold all the information necessary to parse
    # the command line into Python data types.
    parser = argparse.ArgumentParser(description='Python script interface able to generate\
                                 lj+colored noise simulations.',prefix_chars= '-')
                                
    
    # Create flags
    parser.add_argument('--units', choices=['lj','real','metal','si','cgs','electron','micro','nano'], default='lj',  \
                        help='pass the style of units used in the simulation and for all the variables. Default value is \' lj \' ')
    
    parser.add_argument('--step_length', action='store', default=0.005, type=float, \
                        help='pass the timesteps\' length. Default value is 0.005 .')
                        
    parser.add_argument('--step_number', action='store', default=2000, type=int, \
                    help='pass the number of simulations, int with a default value of 100.')
                    
    parser.add_argument('--atom_style', choices=['angle','atomic','body','bond','charge','dipole','dpd','edpd', 'mdpd','tdpd','electron','ellipsoid','full','line','meso','molecular','peri','smd','sphere','tri','template','hybrid'], default='atomic',  \
                    help='pass the style of the atoms used in the simulation. Default value is \' atomic \'')

    parser.add_argument('--sphere_coord', action= 'append',type=float,nargs='+',default=[0, 0 , 0, 10],  help='Pass the needing for defining the spherical region in which the particles have to be created; the parameters needed are the three coordinates of the center and the radius. The default values are: 0 0 0 10')
    
    parser.add_argument('--lj_coeff', action= 'append',type=float,nargs='+',default=[2.5,0.8,1.0],  help='Pass the needing coefficients for defining the lj potential; the parameters needed are the cutoff, epsilon, sigma. The default values are: 2.5,1.0,1.0 .')
    
    parser.add_argument('--mass', action='store', default=1.0, type=float, \
                        help='pass the particles\' mass value, a float with a default value of 1.0 .')
    
    parser.add_argument('--box', action= 'append',type=float,nargs='+',default=[-100, 100 , -100, 100,-100,100],  help='Pass the needing for defining the simulation box; the parameters needed are the xlo,xhi,ylo,yhi,zlo,zhi. The default values are: -100, 100, -100, 100, -100, 100.')
    
    parser.add_argument('--skin', action='store', default=3.0, type=float, \
                        help='pass the value of the skin distance, used in defining pairwise neighbor lists.')
        
    parser.add_argument('--neigh_delay', action='store', default=0, type=int, \
                        help='pass how many steps may pass before building a new neighbour list. It has an intvalue of 0.')
                        
    parser.add_argument('--neigh_every', action='store', default=10, type=int, \
                    help='pass every how many steps must be built a new list. It has an intvalue of 10.')
                    
    parser.add_argument('--neigh_check', choices=['yes','no'], default='no',  \
                    help='If the check setting is yes, then the every and delay settings determine when a build may possibly be performed, but an actual build only occurs if some atom has moved more than half the skin distance (specified in the neighbor command) since the last build. It is a str with choices "yes" or "no", with a default value of "no".')


    parser.add_argument('--thermo', action='store', default=50, type=int, \
                        help='pass the number of steps in which the program prints the thermodynamics of the system; it is an int with a default value of 50.')

    parser.add_argument('--dump_atom', action='store', default=0, type=int, \
                    help='print in a .gz file a snapshot of the simulation every args.dump_atom steps, an int with a default value of 0.')

    parser.add_argument('--dump_speed', action='store', default=0, type=int, \
                    help='print in a file all particles\' speed components every args.dump_speed steps, an int with a default value of 0')
                    
    parser.add_argument('--dump_pos', action='store', default=0, type=int, \
                        help='print in a file all particles\' position components every args.dump_pos steps, an int with a default value of 0')
                        
    parser.add_argument('--gir', action='store', default=0, type=int, \
                    help='create a plot of the radius of gyration in function of the timesteps. The flag represents how much time elapses between an evaluation and another. ')
    
    parser.add_argument('--final_speed', action='store_true',help='stores the condition for creating a vector containing all final velocities: it is conditioned by --final_speed. (bool variable, false by default)')
    
    parser.add_argument('-s', action='store_true',help='stores the condition to mute all lammps setting printout and log.lammps storing. (bool variable, false by default)')
    
    #flags for the generator
    parser.add_argument('--noise_alpha', action='store', default=0.0, type=float, \
                        help='Set the parameter alpha needed for the generator, a float with a default value of 1.0')
                        
    parser.add_argument('--noise_stddev', action='store', default=1.0, type=float, \
                        help='Set the parameter stddev needed for the generator, a float with a default value of 1.0')
                                        
    parser.add_argument('--noise_leak', action='store', default=0.0, type=float, \
                        help='Set the parameter leak needed for the generator, a float with a default value of 0.0')
                    
    parser.add_argument('--global_seed', action='store', default=7, type=int, \
                        help='Set the parameter leak needed for the generator, a float with a default value of 7')
    
    
    print("Arguments parsed correctly.")
    
    
    return parser


