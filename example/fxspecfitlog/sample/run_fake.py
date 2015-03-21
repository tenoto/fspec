#!/usr/bin/env python

import os 

os.system('rm -f xis_1mCrabFeLine_*')

cmd  = 'xspec<<EOF\n'
cmd += '@fake_run_1mCrabFeLine_80ks.xcm\n'
cmd += 'iplot d\n'
cmd += 'we xis_1mCrabFeLine_80ks_bin\n'
cmd += 'quit\n'
cmd += '/Users/enoto/work/git/fspec/fspec/fgrppha.py xis_1mCrabFeLine_80ks.fak xis_1mCrabFeLine_80ks_bin.qdp \n' 
cmd += 'EOF\n'
print cmd
os.system(cmd)
