# Funzioni per la gestione dei calcoli multiprocessore

import cn_math as m
import cn_data_manage as di
from multiprocessing import Pool, cpu_count

def get_data_per_iter(N=1, M=1):
	"Returns data per main loop iterarion, calculating it from samples per CPU per loop (N) and sample cardinality"

	N_CPUs = cpu_count()

	return N*M*N_CPUs


def get_main_loop_iter(filename, lines_number=1, data_per_iter=1):
	"Returns main loop iterations calculating it from data per iteration and data file lines number"

	floor = lines_number//data_per_iter

	if floor == 0:
                return None
	elif lines_number%data_per_iter == 0:
                return floor
	else:
        	return floor + 1


def multi_average(samples_list):
	"From each sublist in the input list returns the corresponding average"

	pool = Pool()
	result = pool.map(m.list_average, samples_list)
	pool.close()

	return result


def multi_std_dev(samples_list, averages_list):
        "From each sublist in the input list returns the corresponding std_dev"

        pool = Pool()
        result = [ pool.apply_async(m.list_std_dev, (samples_list[i],averages_list[i])).get()\
		 for i in range(0,len(samples_list)) ]
        pool.close()

        return result


def multi_get_alpha(samples_list):
	"Return the list of alpha parameters calculating it from a list of samples"

	pool = Pool()
	result = pool.map(m.get_alpha, samples_list)
	pool.close()

	return result

