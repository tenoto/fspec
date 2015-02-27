#!/usr/bin/env python
#  This code is an example of python coding using a "dictionary".

__author__  = "Teru Enoto"
__version__ = "1.0.0"
__email__   = "teruaki.enoto@nasa.gov"
__status__  = "Fixed"

Ry = 0.01360 # keV
dict_atom = {'Ne':10, 'Mg':12,'Si':14,'S':16,'Fe':26}

def getMoseleysLineEnergy(Z,n_up,n_down,eta):
	# Moseley's law
	# eta: screening by inner shell electrons
	# 	   0 (H-like), ~0.4 (He-like), and ~1 (neutral)
	return (Z-eta)**2 * Ry * (1/float(n_down)**2-1/float(n_up)**2)

print '=================================================================='
print ' Moseleys Law (this is approximation)    '
print '           (Z-eta)^2 Ry (1/n^2-1/m^2)    '
print 'unit (keV)                              '
print '------------------------------------------------------------------'
print '    Z      H-like (e)           He-like (2e)         Neutral      '
print '        2->1  3->1  Edge     2->1  3->1  Edge     2->1  3->1  Edge'
print '------------------------------------------------------------------'
for atom, Z in sorted(dict_atom.items(),key=lambda x:x[1]):
	print '%2s %d ' % (atom, Z), 
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],2,1,0),
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],3,1,0),	
	print '%.3f   ' % getMoseleysLineEnergy(dict_atom[atom],1000,1,0),		
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],2,1,0.4),
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],3,1,0.4),
	print '%.3f   ' % getMoseleysLineEnergy(dict_atom[atom],1000,1,0.4),
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],2,1,1.0),
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],3,1,1.0),
	print '%.3f' % getMoseleysLineEnergy(dict_atom[atom],1000,1,1.0)			
print '=================================================================='
