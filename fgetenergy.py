#!/usr/bin/env python
# convert PI (channel) values to energy (keV)

__author__  = "Teru Enoto"
__version__ = "1.0.0"
__date__    = '2015-02-27'
__email__   = "teruaki.enoto@nasa.gov"
__status__  = "Fixed"

from optparse import OptionParser

DEBUG = False

parser = OptionParser()
parser.add_option("-i","--instrument",dest="instrument",
	action="store",help="instrument",type="string")
(options, args) = parser.parse_args()

if len(args) != 1:
	print "%> fgetenergy.py PI --instrument HXD-PIN" 
	quit()
pi = float(args[0])
if options.instrument == None:	
	print "instrument: %> -i HXD-PIN"
	quit()
if DEBUG:	
	print "pi        : %.4f (channel) " % pi
	print "instrument: %s " % options.instrument

XIS_NAME = ['XIS', 'XI0', 'XI1', 'XI2', 'XI3', 'xis', 'xi0', 'xi1', 'xi2', 'xi3']
PIN_NAME = ['PIN', 'pin', 'HXD-PIN', 'hxd-pin']
GSO_NAME = ['GSO', 'gso', 'HXD-GSO', 'hxd-gso']
NUSTAR_NAME = ['NuSTAR', 'nustar', 'FPM', 'fpm', 'FPMA', 'fpma', 'FPMB', 'fpmb']

"""
XIS     : E = 3.65 PI [eV]
HXD-PIN : E = 0.375 ( PI_PIN + 1.0 ) [keV]
HXD-GSO : E = 2 ( PI_SLOW + 0.5 ) [keV]
NuSTAR  : E = Channel Number * 0.04 keV + 1.6 keV
"""

if options.instrument in XIS_NAME:
	energy = 3.65 * pi / 1000.0 # keV
elif options.instrument in PIN_NAME:
	energy = 0.375 * ( pi + 1.0 ) # keV 
elif options.instrument in GSO_NAME:
	energy = 2.0 * (pi + 0.5) # keV
elif options.instrument in NUSTAR_NAME:
	energy = pi * 0.04 + 1.6 # keV

print energy 
