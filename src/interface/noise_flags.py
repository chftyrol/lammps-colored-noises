import argparse

def configure():
#Parser for flags

    #The ArgumentParser object will hold all the information necessary to parse\
    #the command line into Python data types.
    parser = argparse.ArgumentParser(description='Python script interface able to generate\
                                 lj+colored noise simulations',prefix_chars= '-')
    #Create flags
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

    parser.add_argument('--pot', choices=['yukawa'], default='yukawa',  \
                    help='passa il tipo di potenziale da accoppiare a lj')

    parser.add_argument('--pot_coeff', action= 'append',type=float,nargs='+',default=[2.0, 2.5 , 100.0, 2.3],  help='passa i coefficienti richiesti dal potenziale: *)per yukawa sono screening_length, global_cutoff, A (energy*distance units), cutoff(locale, di quel preciso accoppiamento)')
    
    parser.add_argument('--if_dump_atom', action='store_true')

    parser.add_argument('--dump_atom', action='store', default=10, type=int, \
                    help='passa ogni quante simulazioni salvare uno snapshot del sistema di atomi, un int che ha valore 10 di default')

    parser.add_argument('--if_dump_speed', action='store_true')

    parser.add_argument('--dump_speed', action='store', default=99, type=int, \
                    help='passa ogni quante simulazioni salvare uno snapshot delle velocità degli atomi, un int che ha valore 100 di default')
    
    return parser


