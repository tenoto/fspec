#!/usr/bin/env python
# convert energy (keV) value to PI 

__author__  = "Teru Enoto"
__version__ = "1.0.0"
__date__    = '2015-02-27'
__email__   = "teruaki.enoto@nasa.gov"
__status__  = "Fixed"

from optparse import OptionParser

DEBUG = False

parser = OptionParser()
#parser.add_option("-e","--energy",dest="energy",
#	action="store",help="energy (keV)",type="float")
parser.add_option("-i","--instrument",dest="instrument",
	action="store",help="instrument",type="string")
(options, args) = parser.parse_args()

#if options.energy == None:
#	print "input energy (keV): %> -e energy(keV)"
#	quit()
if len(args) != 1:
	print "%> fgetpi.py energy(keV) --instrument HXD-PIN" 
	quit()
energy = float(args[0])
if options.instrument == None:	
	print "instrument: %> -i HXD-PIN"
	quit()
if DEBUG:	
	print "energy    : %.4f (keV) " % energy
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
	pi = float(energy) * 1000.0 / 3.65 
elif options.instrument in PIN_NAME:
	pi = float(energy)	/ 0.375 - 1.0 
elif options.instrument in GSO_NAME:
	pi = float(energy) / 2.0 - 0.5 
elif options.instrument in NUSTAR_NAME:
	pi = (float(energy) - 1.6) / 0.04 

print pi 
