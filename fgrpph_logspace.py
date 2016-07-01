#!/usr/bin/env python

import os 
import sys 
import yaml 
import numpy

# A: The channel to energy conversion is linear: E = Channel Number * 0.04 keV + 1.6 keV 
# (lower energy range of bin) Channel 0 corresponds to 1.60-1.64 keV, 
# channel 1 corresponds to 1.64-1.68 keV, etc. 
# You can also check the ebounds extension of RMF files 
# (with the 'fv' command) to confirm the relationship 
# between PI value and energy.

# NuSTAR 
# 3 keV  :   35 ch 
# 10 keV :  210 ch
# 79 keV : 1935 ch 

#pi_min = 30
#pi_max = 1900
#nbin   = 40 

if len(sys.argv) != 2:
	print "%s input.yaml" % sys.argv[0]
	print "----\n"
	print "yaml format\n"
	print "input_pha: 'nu30101035002A01_sr.pha'\n"
	print "output_pha: 'nu30101035002A01_sr_logspbin.pha'\n"
	print "binning_setups: [[35,210,70],[211,1935,30]]\n"
	quit()
input_yaml = sys.argv[1]	
param = yaml.load(open(input_yaml))

basename = os.path.splitext(param['output_pha'])[0]
shfile   = '%s.sh' % basename
f = open(shfile,'w')
dump  = '#!/bin/sh -f\n\n'
dump += 'grppha << EOF\n'
dump += '%s\n' % param['input_pha']
dump += '%s\n' % param['output_pha']
for binset in param['binning_setups']:
	pi_min, pi_max, nbin = binset
	tmp_float_pi = numpy.logspace(
		numpy.log10(pi_min-1), numpy.log10(pi_max), 
		nbin, base=10)
	for i in range(len(tmp_float_pi)-1):
		p0 = int(round(tmp_float_pi[i]))+1
		p1 = int(round(tmp_float_pi[i+1]))
		binsize = p1 - p0 + 1 
		dump += 'group %d %d %d\n' % (p0, p1, binsize)
dump += 'exit\n'
print dump 
f.write(dump)
f.close()

cmd = 'chmod +x %s' % shfile
os.system(cmd)
quit()		
