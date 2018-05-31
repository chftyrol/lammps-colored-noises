import random
import os
import subprocess

generatorpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/noise/tester.x"
nlaststep = -1
lastvalue = 0
samplex = []
sampley = []
samplez = []

def getsample():
    N = 101
    alpha = 1.0
    d = 1.0
    leak = 0.
    seed = 776
    cmd = generatorpath + " -N " + str(N) + " -a " + str(alpha) + " -d " + str(d) + " -l " + str(leak) + " -s " + str(seed)
    print("Running generator:\n" + cmd)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    while True :
        line = proc.stdout.readline().decode('ascii')
        if line != '' :
            samplex.append(float(line))
        else :
            break

def generate(nstep):
    global nlaststep, lastvalue
    if nlaststep == nstep :
        return lastvalue
    if nstep == 0 :
        getsample()
    nlaststep = nstep
    value = samplex[nstep]
    lastvalue = value
    return value
