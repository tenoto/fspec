#!/usr/bin/env python

import os 
import sys
import yaml

if len(sys.argv) != 3:
	sys.stderr.write('> %s param.yaml get_error.xcm\n' % sys.argv[0]) 
	quit()
param_yaml    = sys.argv[1]	
get_error_xcm = sys.argv[2]	
sys.stdout.write('parameter yaml (param_yaml): %s\n' % param_yaml)
sys.stdout.write('error xcm (get_error.xcm): %s\n' % get_error_xcm)

print "--- fpyxspec.py ---"
param = yaml.load(open(param_yaml))

os.system('rm -f fit.log')
f = open(get_error_xcm,'w')
#lines  = '@150303try/edge_all.xcm\n'
lines  = ''
lines += 'log fit.log\n'
lines += 'fit\n'
for compNumber in param:
	title = param[compNumber]["title"]
	for value in param[compNumber]:
		if value ==  'title':
			continue
		parameterNumber = param[compNumber][value]
		lines += 'err 1.0 %d\n' % int(parameterNumber)
lines += 'log none\n'		
f.write(lines)
f.close()

quit()

