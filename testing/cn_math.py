# Questo modulo contiene le funzioni matematiche utilizzate nel progetto

from math import sqrt
from argparse import ArgumentTypeError
from numpy.fft import rfft
from numpy import conjugate, multiply, real, inf
from scipy.optimize import curve_fit

def check_positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise ArgumentTypeError("%s is not a positive int value" % value)
    return ivalue


def list_average(list):
	"Returns the average of the elements of a float list"

	return  sum(list)/len(list)


def list_std_dev(list, list_average):
	"Returns the standard deviation of the elements of a list, from their average"

	return sqrt(sum([(list_average-x)**2 for x in list])/(len(list)-1))


def list_power_spectrum(list):
	"Returns the power spectrum of a list of reals"

	f = rfft(list)

	return real(multiply(f, conjugate(f)))


def noise_ps_curve_family(f, a=1, b=1, c=0):
	"Evaluates the family of curves representing the power spectrum\
	of a generic pink noise"

	return 1/((b*(f + c))**a)


def get_alpha(sample, n_rfpoints=100):
	"Return alpha parameter from noise sample"

	ps = list_power_spectrum(sample)
	n_fpoints = ""

	if n_rfpoints > len(ps) - 1:
		n_fpoints = len(ps) - 1
	else:
		n_fpoints = n_rfpoints

	f_points = [ x for x in range(1, n_fpoints) ]
	p_points = [ ps[p] for p in range(1, n_fpoints) ]
	p_bounds = ([0, 0, 0], [2 ,1 ,inf])

	return curve_fit(noise_ps_curve_family, f_points, p_points,\
		bounds=p_bounds)[0][0]
