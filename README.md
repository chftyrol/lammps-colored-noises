# lammps-colored-noises
In questa repository risiede il progetto del corso di Dinamica Molecolare. L'obiettivo del progetto è triplice:

1. Scrivere delle classi aggiuntive per lammps che permettano di generare rumore colorato, al fine di produrre una dinamica stocastica.
2. Produrre uno strumento in grado di analizzare le proprietà statistiche di tali rumori.
3. Scrivere una interfaccia in Python che permetta di adoperare tali strumenti in simulazioni di vario tipo in maniera agile.

## Generazione di rumore colorato
Per la generazione di rumore colorato adoperiamo il seguente schema:

1. La classe `WhiteNoise` genera del rumore bianco gaussiano: facendo uso della classe `std::normal_distribution` del C++11 si genera del rumore bianco, con media e deviazione standard specificate dall'utente. La media di questo rumore per la maggior parte delle applicazioni dev'essere pari a 0.
2. Il rumore bianco così generato viene spedito attraverso un filtro colorato, implementato dalla classe `NoiseFilter`. Questa esegue in successione le seguenti operazioni:
   - Calcolo della funzione risposta in spazio reale.
   - Calcolo della DFT (discrete Fourier transform) della funzione risposta.
   - Calcolo della DFT del segnale di input, ossia del rumore bianco.
   - Applicazione al segnale di input della funzione risposta in spazio trasformato.
   - Calcolo della DFT inversa per ottenere il segnale in output in spazio reale.

La coordinazione tra `WhiteNoise` e `NoiseFilter` è implementata in `ColoredNoise`, che si occupa di dispensare i numeri casuali che costituiscono il rumore colorato desiderato.

Nella pratica, un utente che desidera utilizzare questo generatore deve istanziare un oggetto di tipo `ColoredNoise` fornendo:

- `samplesize`: le dimensioni del campione di rumore colorato;
- `seed`: il seed per inizializzare `WhiteNoise`;
- `stddev`: la deviazione standard del rumore bianco;
- `mean`: il valor medio del rumore bianco;
- `alpha`: parametro `double` che specifica il colore del rumore bianco. In particolare:
  + `alpha = 0.0` dà rumore bianco
  + `alpha = 1.0` dà rumore rosa
  + `alpha = 2.0` dà rumore rosso

Il calcolo della funzione risposta e in generale l'algoritmo utilizzato da `NoiseFilter` è spiegato nel dettaglio su:

- [N. J. Kasdin, "Discrete simulation of colored noise and stochastic processes and 1/f^α power law noise generation," in Proceedings of the IEEE, vol. 83, no. 5, pp. 802-827, May 1995.](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=381848&isnumber=8651)
- [N. J. Kasdin and T. Walter, "Discrete simulation of power law noise (for oscillator stability evaluation)," Proceedings of the 1992 IEEE Frequency Control Symposium, Hershey, PA, 1992, pp. 274-283.](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=270003&isnumber=6712)

## Analisi dei rumori colorati
L'analisi dei rumori colorati, generati attraverso il precedente schema, è possibile grazie alo script di Python `cntester`, presente in `/testing`.

### Dipendenze
`cntester` fa uso delle librerie di python `scipy` e `numpy` (oltre ai moduli presenti nel progetto). Inoltre si rende necessario l'utilizzo di una versione del linguaggio **>=3.0.0**.

#### Installare `scipy` e `numpy`
Le librerie menzionate si possono installare sfruttando i seguenti metodi:

##### GNU/Linux
Scipy e numpy sono librerie di python molto conosciute, molto probabilmente si possono installare attraverso il package manager della propria distribuzione.

es. (Debian based) `apt-get install python-scipy python-numpy`.

##### Windows e OSX
Si faccia uso di "Pip Installs Packages" (pip):

`pip install scipy numpy`.

### Utilizzo
`./cntester --help`.

#### Esempio:
Si può testare il funzionamento di cntester mediante il file di dati `/testing/test_data.txt.xz`.

##### Istruzioni:
1. `cd $PERCORSO_REPO_GIT/testing`
2. `xz -d test_data.txt.xz` (è necessario installare il pacchetto "XZ Utils" o simili)
3. `./cntester test_data.txt 10000 4`
