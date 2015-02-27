#!/usr/bin/env python
# 
# This script add "PHASE" column calculated from "PERIOD" column.
# The original script is aeplsphase.pl created by T.Enoto 
# created by Teruaki Enoto 2015-02-07 
# converted from perl script 

__name__    = 'faddenergy'
__author__  = 'Teruaki Enoto'
__version__ = '1.00'
__date__    = '2015 Feb. 7'

import os
import pyfits
from optparse import OptionParser
from datetime import datetime 

parser = OptionParser()
parser.add_option("-i","--inputfits",dest="inputfits",
	action="store",help="input fits file",type="string")
parser.add_option("-o","--outputfits",dest="outputfits",
	action="store",help="output fits file",type="string")
(options, args) = parser.parse_args()

if options.inputfits == None:
	print "input fits file is needed. %> -i inputfits"
	quit()
if options.outputfits == None:	
	print "output fits file is needed. %> -o outputfits"
	quit()
print "inputfits : %s " % options.inputfits
print "outputfits: %s " % options.outputfits

if not os.path.exists(options.inputfits):
	print "input file does not exists: %s" % options.inputfits
	quit()
if os.path.exists(options.outputfits):
	print "output file has already existed: %s " % options.outputfits
	quit()

"""
XIS_NAME = ['XIS', 'XI0', 'XI1', 'XI2', 'XI3', 'xis', 'xi0', 'xi1', 'xi2', 'xi3']
PIN_NAME = ['PIN', 'pin', 'HXD-PIN', 'hxd-pin']
GSO_NAME = ['GSO', 'gso', 'HXD-GSO', 'hxd-gso']
NUSTAR_NAME = ['NuSTAR', 'nustar', 'FPM', 'fpm', 'FPMA', 'fpma', 'FPMB', 'fpmb']
XIS     : E = 3.65 PI [eV]
HXD-PIN : E = 0.375 ( PI_PIN + 1.0 ) [keV]
HXD-GSO : E = 2 ( PI_SLOW + 0.5 ) [keV]
NuSTAR  : E = Channel Number * 0.04 keV + 1.6 keV
"""

hdu = pyfits.open(options.inputfits)
if hdu[0].header['TELESCOP'] in ['SUZAKU']:
	if hdu[0].header['INSTRUME'] in ['HXD']:
		if hdu[0].header['DETNAM'] in ['WELL_PIN']:
			print "Suzaku/HXD/PIN"
			slope  = 0.375 
			offset = slope * 1.000 
			pi_name = 'PI_PIN'
		elif hdu[0].header['DETNAM'] in ['WELL_GSO']:
			print "Suzaku/HXD/GSO"
			slope  = 2.000
			offset = slope * 0.500
			pi_name = 'PI_SLOW'
elif hdu[0].header['TELESCOP'] in ['NuSTAR']:
	if hdu[0].header['INSTRUME'] in ['FPMA','FPMB']:
		slope  = 0.04 
		offset = 1.60 
		pi_name = 'PI'
else:
	print "Telescop/Instrum/detnam are not recorded."
	quit()

operation = "%.4f * %s + %.4f" % (slope, pi_name, offset)
print operation
cmd  = 'fcalc infile=%s+1 ' % options.inputfits
cmd += 'outfile=%s ' % options.outputfits
cmd += 'clname=\"ENERGY\" expr=\"%s\" rowrange=\"-\"' % operation
print cmd; os.system(cmd)

out = """
HISTORY -----------------------------------------------------
HISTORY  %s version %s at %s
HISTORY -----------------------------------------------------
HISTORY   inputfits='%s'
HISTORY   outputfits='%s'
HISTORY   %s 
""" % (__name__, __version__, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
	options.inputfits, options.outputfits,
	operation)
print out
f = open('temp_header.txt','w')
f.write(out)
f.close()
cmd  = ''
for i in range(0,2):
	cmd += 'fthedit %s+%d \@temp_header.txt\n' % (options.outputfits,i)
cmd += 'rm -f temp_header.txt'
print cmd; os.system(cmd)

