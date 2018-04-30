# Questo modulo contiene le funzioni matematiche utilizzate nel progetto

from math import sqrt
from argparse import ArgumentTypeError

def check_positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise ArgumentTypeError("%s is not a positive int value" % value)
    return ivalue


def list_average(list):
	"Returns the average of the elements of a float list"

	return  sum(list)/len(list)


def list_std_dev(list,list_average):
	"Returns the standard deviation of the elements of a list, from their average"

	return sqrt(sum([(list_average-x)**2 for x in list])/(len(list)-1))
