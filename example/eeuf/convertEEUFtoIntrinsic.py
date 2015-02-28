#!/usr/bin/env python

import os 
import sys 
import math

if len(sys.argv) != 5:
	sys.stderr.write('> %s in.qdp out.qdp d(kpc) norm\n' % sys.argv[0])
	sys.stderr.write('> %s sample_eeuf.qdp out.qdp 3.91 1e+44 \n' % sys.argv[0])
	quit()
sys.stdout.write('> %s %s %s %s %s \n' % (sys.argv[0],
	sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
inqdp  = sys.argv[1]
outqdp = sys.argv[2]
distance_kpc = float(sys.argv[3])
norm   = float(sys.argv[4])

# 1 pc  = 3.09e+18 cm 
# 1 kpc = 3.09e+21 cm
distance_cm = 3.09e+21 * distance_kpc			
scale = 4.0 * math.pi * distance_cm**2 
log10norm = math.log10(norm)

cmd  = '../../fscaleqdp.py '
cmd += '%s %s ' % (inqdp, outqdp)
cmd += '-s %.3e ' % scale
cmd += '-n %.5e ' % norm
cmd += '-y "\gnF\gn d\u2\d(10\u%.1f\d keV\u2\d s\u-1\d keV\u-1\d)"' % log10norm
print cmd
os.system(cmd)

