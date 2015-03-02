#!/usr/bin/env python
#
# Followings are an example to simulate the He-like triplet of 
# iron from Cen X-3 based on the Suzaku and Chandra observation.
#
# Public ASTRO-H response files for spectral simulation 
# http://astro-h.isas.jaxa.jp/researchers/sim/response.html
# 
# Simulatin Procedure is written below. 
# http://astro-h.isas.jaxa.jp/researchers/sim/sxs/sxs_sim.html
#
# Please download following files in the 'resp' directory
# 
# sxs_cxb+nxb_7ev_20110211_1Gs.pha.gz  : NXB + CXB pha file 
# ah_sxs_7ev_basefilt_20090216.rmf.gz  : SXS energy response. Energy resolution (FWHM) 7eV constant
# sxt-s_120210_ts02um_intallpxl.arf.gz : all pixel, point source, open fileter
# 
# T.Enoto 2015-03-02 
# 

import os 

respfiles = [
	'sxs_cxb+nxb_7ev_20110211_1Gs.pha.gz',
	'ah_sxs_7ev_basefilt_20090216.rmf.gz',
	'sxt-s_120210_ts02um_intallpxl.arf.gz']	
if not os.path.exists('resp'):
	print 'resp directory does not exist.'
	quit()
for resp in respfiles:
	if not os.path.exists('resp/%s' % resp):
		print "response file %s does not exists." % resp
		print "please download %s from the latest webpage." % resp
		print "(e.g.) http://astro-h.isas.jaxa.jp/researchers/sim/response.html"
		quit()

# assumed spectral xcm file is cenx3_ironlines.xcm
# the iron line is set to be consistent with Wojdowski et al., 2003 from the Chandra
# http://adsabs.harvard.edu/abs/2003ApJ...582..959W		
# and also the 2008 Suzaku observation.
# Detailed prametrization of the line width has not yet to be studied. 
# This model is only valid in the 5--8 keV range. 

cmd = 'rm -rf out; mkdir out'
os.system(cmd)

# ---------------------
# Prepare spec. model 
# ---------------------
f = open('out/cenx3_ironlines_model.xcm','w')
lines = """
statistic chi
method leven 10 0.01
abund angr
xsect bcmc
cosmo 70 0 0.73
xset delta 0.01
systematic 0
model  phabs(pegpwrlw + gaussian + gaussian + gaussian + gaussian + gaussian + gaussian + gaussian)
        7.39892          1          0          0     100000      1e+06
        1.13072          1         -3         -2          9         10
              1      -0.01       -100       -100      1e+10      1e+10
             10      -0.01       -100       -100      1e+10      1e+10
        2025.13       0.01          0          0      1e+20      1e+24
        6.39845         -1          0          0      1e+06      1e+06
          1e-05      -0.05          0          0         10         20
     0.00169569       0.01          0          0      1e+20      1e+24
        6.63659         -1          0          0      1e+06      1e+06
          1e-05         -1          0          0         10         20
        0.00014      1e-06          0          0    0.00014    0.00014
        6.66754         -1          0          0      1e+06      1e+06
          1e-05         -1          0          0         10         20
    0.000332565      1e-06          0          0      1e+20      1e+24
        6.68231         -1          0          0      1e+06      1e+06
          1e-05         -1          0          0         10         20
= 1.0*14
         6.7004         -1          0          0      1e+06      1e+06
          1e-05         -1          0          0         10         20
          4e-05         -1          0          0   0.000153   0.000153
        6.95197         -1          0          0      1e+06      1e+06
          1e-05         -1          0          0         10         20
        0.00015         -1          0          0      1e+20      1e+24
        6.97316         -1          0          0      1e+06      1e+06
          1e-05         -1          0          0         10         20
    0.000285876       0.01          0          0      1e+20      1e+24
"""
f.write(lines)
f.close()

# ---------------------
# Run fakeit simulation
# ---------------------
f = open('out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_runfake.xcm','w')
cmd  = '@out/cenx3_ironlines_model.xcm\n'
cmd += 'fakeit resp/sxs_cxb+nxb_7ev_20110211_1Gs.pha.gz\n' # spectrum
cmd += 'resp/ah_sxs_7ev_basefilt_20090216.rmf.gz\n' # response 
cmd += 'resp/sxt-s_120210_ts02um_intallpxl.arf.gz\n' # ancillary file
cmd += 'y\n' # Use counting statistics in creating fake data?
cmd += '\n'  # Input optional fake file prefix
cmd += 'out/ah_sxs_7ev_cenx3_6ks_FeHeTrip.fak\n' # Fake data file name
cmd += '6e+3\n' # Exposure time, correction norm, bkg exposure time
cmd += '\n' # fake finished.
f.write(cmd)
f.close()
cmd = 'xspec < out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_runfake.xcm'
os.system(cmd)

# ---------------------
# Grouping the spectrum
# ---------------------
cmd  = 'grppha << EOF\n'
cmd += 'out/ah_sxs_7ev_cenx3_6ks_FeHeTrip.fak\n' 
cmd += 'out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_bin.fak\n' 
cmd += 'group min 50\n'
cmd += 'exit\n'
cmd += 'EOF'
print cmd
os.system(cmd)

# ---------------------
# Prepare the QDP/PCO 
# ---------------------
f = open('out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit_Helike.pco', 'w')
lines = """
loc 0.05 0.1 1.0 0.5
time off 
lab t Cen X-3 / 6 ks simulation of the ASTRO-H SXS
lab y Counts s\u1-\d keV\u-1\d
lab rotate 
r x 6.5 6.8 
r y 0 20 
lwid 5 
lwid 5 on 1..8 
ls 1 on  4 5 6 7 8 
col 1 on 1 
col 2 on 2 
$ echo all model

col 8 on 3 
$ echo continuum 

col 13 on 5 
la 5 pos 6.63659 0 "z" li 90 1.0 col 13 ls 4 
lab 15 pos 6.511 17 "6.636 keV : z forbidden" jus left
$ echo magenta : z forbidden line

col  8 on 6 
la 6 pos 6.66754 0 "y" li 90 1.0 col 8 ls 4
lab 16 pos 6.511 15 "6.667 keV : y intercombination" jus left
$ echo orange : y intercombination 

col 10 on 7 
la 7 pos 6.68231 0 "x" li 90 1.0 col 10 ls 4
lab 17 pos 6.511 13 "6.682 keV : x intercombination" jus left
$ echo green : x : intercombination 

col 12 on 8 
la 8 pos 6.70040 0 "w" li 90 1.0 col 12 ls 4
lab 18 pos 6.511 11 "6.700 keV : w resonance" jus left
$ echo purple : w resonance line
"""
f.write(lines)
f.close()

# ---------------------
# Fit and plot results
# ---------------------
f = open('out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit.xcm','w')
cmd  = 'data 1 out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_bin.fak\n' # automatically read the resp, arf, and bkg
cmd += '@out/cenx3_ironlines_model.xcm\n'
cmd += 'setplot energy\n' # channel to energy 
cmd += 'ignore **-5.0 8.0-**\n' # concentrating to the iron lines.
cmd += '\n'
cmd += 'setplot com log x off\n' # x axis to linear
cmd += 'setplot add\n'
cmd += 'fit\n'
cmd += 'iplot d\n'
cmd += '@out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit_Helike.pco\n'
cmd += 'hard out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit_Helike.ps/cps\n'
cmd += 'we ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit_Helike\n'
cmd += 'quit\n'
cmd += 'exit\n'
f.write(cmd)
f.close()
cmd = 'xspec < out/ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit.xcm'
os.system(cmd)
os.system('mv *qdp *pco out/')

os.chdir('out')
os.system('ps2pdf ah_sxs_7ev_cenx3_6ks_FeHeTrip_fit_Helike.ps')
os.chdir('../')























