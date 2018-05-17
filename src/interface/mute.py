import sys, os

#Python lets you overwrite standard output (stdout) with any file object. This should work cross platform and write to the null device.

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
