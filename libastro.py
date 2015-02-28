
# from libastro import * 
import math 

def getRadius(T_keV,Fx11,d_kc):
	"""
	method to calculate the emission radius from XSPEC unabsorbed X-ray flux. 
	== Input ==
	Fx11 : unabsorbed X-ray flux (10^-11 erg/s/cm2)
	d_kpc : distance to the source (kpc)
	T_keV : surface temperature (keV)
	== Output ==
	radius (km) = 0.09643 d_kpc T_keV^-2 Fx11
	== Reference values ==
	Lx = 4 pi R^2 sigma T^4
	Fx = Lx / 4 pi d^2
	stefan boltzmann sigma = 5.67e-5 erg/cm^2/K^4/s 
	...[check]...
	https://heasarc.gsfc.nasa.gov/xanadu/xspec/manual/XSmodelBbodyrad.html
	assuming 0.1 keV and 10 km radius emission region at 10 kpc 
	%> xspec
	%> dummyrsp 1e-2 1e+2 100 
	%> model bbodyrad
	%> 0.1 (T=0.1 keV)
	%> 100 (norm=100=Rkm^2/d10kpc^2)
	%> flux 1e-2 1e+2
	==> 1.0823e-13 ergs/cm^2/s

	ipython
	%> from libastro import *
	%> getRadius(0.10,0.010823,10.0)
	%> 10.031964715483204 
	this is consistent within three digits of accuracy as excpected. 
	"""
	return 0.09643 * d_kc * (1/T_keV)**2 * math.sqrt(Fx11)

