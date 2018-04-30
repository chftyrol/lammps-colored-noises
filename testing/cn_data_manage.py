# Funzioni per il caricamento e la preparazione dei dati grezzi da file

from itertools import islice
from multiprocessing import cpu_count, Pool

def get_lines_number(filename):
	"Returns lines number of input file"

	return sum(1 for line in open(filename))


def get_complex_data(filename, start=0, end=None, step=1):
	"Returns a organized list of samples multi-processing the input file"

	if end is None:
		end = sum(1 for line in open(filename))

	data_range= [ float(x.rstrip()) for x in islice(open(filename, "r"),start,end) ]

	pool = Pool()
	result = [ [ x for x in pool.apply_async(islice, (data_range, i*step, (i+1)*step))\
		.get() ] for i in range(0,(end-start)//step) ]
	pool.close()

	return result
