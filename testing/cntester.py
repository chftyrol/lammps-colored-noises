#!/usr/bin/python

from argparse import ArgumentParser
import cn_data_manage as di
import cn_math as m
import cn_multiprocs as mp

# Definisci il parser
parser = ArgumentParser()

# Aggiungi un argomento per specificare il nome del data file
parser.add_argument("datafile", help = "a plain text file containing some\
				samples of equal cardinality")
# Aggiungi un argomento per specificare la cardinalità dei campioni
parser.add_argument("samp_card", type=int,\
		    help = "cardinality of samples in datafile")
# Aggiungi un argomento per specificare il numero di campioni
# che ogni CPU processa in media per ogni iterazione del loop principale
parser.add_argument('samp_per_CPU', nargs='?', default=1, type=int,\
		    help = "medium number of samples per CPU\
		    per main loop iteration (default = 1)")

# Parsa la linea di comando
args = parser.parse_args()

# Assegna gli argomenti selezionati dalla linea di comando
# a delle variabili (per maggiore comodità).
data_file = args.datafile
sample_cardinality = args.samp_card
samples_per_CPU = args.samp_per_CPU

# Calcola il numero complessivo dei dati
# contando le linee del data file
data_number = di.get_lines_number(data_file)
# Calcola dinamicamente il numero di dati analizzate
# ad ogni iterazione del loop principale, basandosi
# sul numero di CPU della macchina
data_per_iter = mp.get_data_per_iter(samples_per_CPU, sample_cardinality)
# Calcola il numero di iterazioni del loop principale
main_loop_iter = mp.get_main_loop_iter(data_file, data_number, data_per_iter)

# Inizializza la lista dei valori di aspettazione e
# delle deviazioni standard
averages_list = []
std_devs_list = []


# Avvia il loop principale
for index in range(0,main_loop_iter):

	# Calcola l'inizio e la fine (intese come linee nel data file)
	# del blocco di dati da analizzare nella presente iterazione
	start = index*data_per_iter
	# Se il numero della linea iniziale più la dimensione del blocco
	# supera il numero di linee del data file, poni la fine
	# uguale a quest'ultimo
	if start + data_per_iter > data_number:
		end = data_number
	else:
		end = start + data_per_iter

	# Genera la lista organizzata dei dati, per questa iterazione:
	# una lista di liste, dove ogni sottolista corrisponde ad un
	# campione di dati differente
	samples_list = di.get_complex_data(data_file,start,end,\
	sample_cardinality)

	# Calcola la lista dei valori di aspettazione dei campioni
	# per questa iterazione
	iter_averages_list = mp.multi_average(samples_list)
	# Appendi alla lista dei valori di aspettazione tutti i valori
	# di aspettazione calcolati in questa iterazione
	averages_list.extend(iter_averages_list)

	# Calcola la lista delle deviazioni standard dei campioni
	# per questa iterazione
	iter_std_devs_list = mp.multi_std_dev(samples_list,iter_averages_list)
	# Appendi alla lista delle deviazioni standard tutti le deviazioni
	# standard calcolate in questa iterazione
	std_devs_list.extend(iter_std_devs_list)


# Calcola il valore di aspettazione del  rumore
# dalla lista dei valori di apettazione di tutti i
# campioni
noise_average = m.list_average(averages_list)
# Stampa a standard output il valore di aspettazione del
# rumore
print("Noise Expectation Value:",noise_average)
# Calcola e stampa a standard output la deviazione standard
# del valore di aspettazione del rumore
print("Noise Expectation Value Std. Deviation:", m.list_std_dev(averages_list,noise_average))

# Calcola la deviazione standard del rumore
# dalla lista delle deviaioni standard di tutti i
# campioni
noise_std_dev = m.list_average(std_devs_list)
# Stampa a standard output la deviazione standard del
# rumore
print("Noise Std. Deviation:", noise_std_dev)
# Calcola e stampa a standard output la deviazione standard
# della deviazione standard del rumore.
print("Noise Std. Deviation Std. Deviation:", m.list_std_dev(std_devs_list,noise_std_dev))

