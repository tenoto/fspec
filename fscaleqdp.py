#!/usr/bin/env python

import os 
import sys
import math 
from optparse import OptionParser

__name__    = 'fscaleqdp.py'
__author__  = 'Teruaki Enoto'
__version__ = '1.00'
__date__    = '2015-02-28'

def scaleQDP(inqdp,outqdp,scale,norm=1.0,
	inpco='',outpco='',ylabel='New Yaxis'):
	if not os.path.exists(inqdp):
		sys.stderr.write('QDP file %s does not exist.' % inqdp)
		quit()
	if os.path.exists(outqdp):
		sys.stderr.write('Output file %s has already existed.' % outqdp)
		quit()
	f = open(outqdp, 'w')
	for line in open(inqdp):
		cols = line.split()
		if not cols[0].replace(".","").isdigit():
			if outpco != '' and cols[0].find('@') == 0:
				line = '@%s\n' % outpco
			f.write(line)
			continue
		dump = ''
		for col in cols:
			if cols.index(col) < 2:
				dump += '%s ' % col
			else:
				if col == 'NO':
					dump += '%s ' % col
				else:
					dump += '%.8e ' % (scale*float(col)/norm)
		dump += '\n'
		f.write(dump)
	f.close()

	f = open(outpco, 'w')
	if inpco != '' and outpco != '':
		for line in open(inpco):
			cols = line.split()
			if len(cols)>2:	
				if cols[0] == 'LAB' and cols[1] == 'Y':
					line = 'LAB Y %s\n' % ylabel			
				if cols[0] == 'R' and cols[1] == 'Y':
					line = 'R Y %.8e %.8e\n' % (
						scale*float(cols[2])/norm,
						scale*float(cols[3])/norm)
			f.write(line)

	f.close()

parser = OptionParser()
parser.add_option("-s","--scale",dest="scale",
	action="store",help="scaling factor",type="float",default=1.0)
parser.add_option("-n","--norm",dest="norm",
	action="store",help="normalization factor",type="float",default=1.0)
parser.add_option("-y","--ylabel",dest="ylabel",
	action="store",help="ylabel",type="string",default='New Yaxis')
(options, args) = parser.parse_args()

if len(args) != 2:
	sys.stderr.write('%> fscaleqdp.py input.qdp output.qdp \n')
	quit()
inqdp  = args[0]	
outqdp = args[1]
inbase  = os.path.basename(inqdp).replace('.qdp','')
outbase = os.path.basename(outqdp).replace('.qdp','')
print '%> fscaleqdp.py', inbase, outbase, options.scale, options.norm

inpco  = '%s.pco' % inbase
outpco = '%s.pco' % outbase

scaleQDP(inqdp,outqdp,
	scale=options.scale,norm=options.norm,
	inpco=inpco, outpco=outpco, ylabel=options.ylabel)




