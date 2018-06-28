import random
import os
import subprocess

generatorpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/noise/tester.x"
nlaststepx = -1
nlaststepy = -1
nlaststepz = -1
lastvaluex = 0
lastvaluey = 0
lastvaluez = 0
samplex = None
sampley = None
samplez = None

def gensample(samplesize, alpha, devstd, leak, seed, dimensionlabel):
    global samplex, sampley, samplez
    cmd = generatorpath + " -N " + str(samplesize) + " -a " + str(alpha) + " -d " + str(devstd) + " -l " + str(leak) + " -s " + str(seed)
    print("Running generator:\n" + cmd)
    proc = subprocess.Popen(cmd, shell=True, encoding='ascii', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if dimensionlabel == "fx" :
        samplex = proc.communicate()[0].splitlines()
    elif dimensionlabel == "fy" :
        sampley = proc.communicate()[0].splitlines()
    elif dimensionlabel == "fz" :
        samplez = proc.communicate()[0].splitlines()

def generatex(nstep, noisesamplesize, noisealpha, noisedevstd, noiseleak, noiseseed):
    global nlaststepx, lastvaluex
    if nlaststepx == nstep :
        return lastvaluex

    if nstep == 0 :
        print("Setting up generator for noise sample of dimension x...")
        print("Noise sample size = " + str(noisesamplesize) + "\nNoise alpha = " + str(noisealpha) + "\nNoise devstd = " + str(noisedevstd) + "\nNoise leak coeff = " + str(noiseleak) + "\nNoise seed = " + str(noiseseed))
        gensample(noisesamplesize, noisealpha, noisedevstd, noiseleak, noiseseed, "fx")

    nlaststepx = nstep
    value = float(samplex[nstep])
    lastvaluex = value
    return value

def generatey(nstep, noisesamplesize, noisealpha, noisedevstd, noiseleak, noiseseed):
    global nlaststepy, lastvaluey
    if nlaststepy == nstep :
        return lastvaluey

    if nstep == 0 :
        print("Setting up generator for noise sample of dimension y...")
        print("Noise sample size = " + str(noisesamplesize) + "\nNoise alpha = " + str(noisealpha) + "\nNoise devstd = " + str(noisedevstd) + "\nNoise leak coeff = " + str(noiseleak) + "\nNoise seed = " + str(noiseseed))
        gensample(noisesamplesize, noisealpha, noisedevstd, noiseleak, noiseseed, "fy")

    nlaststepy = nstep
    value = float(sampley[nstep])
    lastvaluey = value
    return value

def generatez(nstep, noisesamplesize, noisealpha, noisedevstd, noiseleak, noiseseed):
    global nlaststepz, lastvaluez
    if nlaststepz == nstep :
        return lastvaluez

    if nstep == 0 :
        print("Setting up generator for noise sample of dimension z...")
        print("Noise sample size = " + str(noisesamplesize) + "\nNoise alpha = " + str(noisealpha) + "\nNoise devstd = " + str(noisedevstd) + "\nNoise leak coeff = " + str(noiseleak) + "\nNoise seed = " + str(noiseseed))
        gensample(noisesamplesize, noisealpha, noisedevstd, noiseleak, noiseseed, "fz")

    nlaststepz = nstep
    value = float(samplez[nstep])
    lastvaluez = value
    return value
